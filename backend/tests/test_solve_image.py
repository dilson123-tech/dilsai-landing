from io import BytesIO

import pytest
from fastapi.testclient import TestClient
from PIL import Image

import app.main as main_module
from app.main import app, rate_limiter, settings
from app.services.llm import ImageAnswerUnavailable, generate_image_study_answer
from app.services.prompts import build_image_question_prompt


def _image_bytes(size=(400, 300), fmt="JPEG", exif_orientation=None) -> bytes:
    image = Image.new("RGB", size, "white")
    buffer = BytesIO()
    kwargs = {}
    if exif_orientation is not None:
        exif = Image.Exif()
        exif[0x0112] = exif_orientation
        kwargs["exif"] = exif
    image.save(buffer, format=fmt, **kwargs)
    return buffer.getvalue()


@pytest.fixture
def client():
    old_enabled = settings.rate_limit_enabled
    settings.rate_limit_enabled = False
    rate_limiter.reset()
    try:
        yield TestClient(app)
    finally:
        settings.rate_limit_enabled = old_enabled
        rate_limiter.reset()


@pytest.fixture
def fake_llm(monkeypatch):
    class Calls(list):
        # Resposta devolvida pela IA falsa; testes podem trocar fake_llm.answer[0].
        answer = ["O que consegui ler: 2 + 2.\nConfiança: alta — tudo legível.\nPasso 1: leitura do enunciado."]

    calls = Calls()

    def fake(image_jpeg, settings_, topic, level, ocr_hint):
        calls.append({"jpeg": image_jpeg, "topic": topic, "level": level, "ocr": ocr_hint})
        return calls.answer[0]

    monkeypatch.setattr(main_module, "generate_image_study_answer", fake)
    monkeypatch.setattr(main_module, "_ocr_hint_for_vision", lambda image: "")
    return calls


def test_image_prompt_has_required_instructions():
    prompt = build_image_question_prompt()

    assert "Leia a questão na imagem" in prompt
    assert "Não invente texto que não está visível." in prompt
    assert "Com base no que consegui ler..." in prompt
    assert "A alternativa mais provável é..." in prompt
    assert "nunca responda que não encontrou material" in prompt
    assert "Não incentive cola" in prompt


def test_image_prompt_requires_confidence_level():
    prompt = build_image_question_prompt()

    assert "Classifique a confiança da leitura" in prompt
    for level in ("Confiança: alta", "Confiança: média", "Confiança: baixa"):
        assert level in prompt
    assert "Na dúvida entre dois níveis, escolha o mais baixo." in prompt


def test_image_prompt_forbids_final_answer_with_low_confidence():
    prompt = build_image_question_prompt()

    assert 'Confiança baixa: NÃO escreva "Resposta final", NÃO escolha nem marque alternativa.' in prompt
    assert "Não consegui ler a questão com segurança." in prompt
    assert "Confiança média" in prompt and "com ressalva forte" in prompt


def test_image_prompt_requires_listing_what_was_read():
    prompt = build_image_question_prompt()

    assert "O que consegui ler:" in prompt
    assert "se alguma alternativa ou dado estiver ilegível, diga isso aqui" in prompt


def test_image_prompt_asks_new_photo_when_alternatives_or_data_unreadable():
    prompt = build_image_question_prompt()

    assert "alguma alternativa ilegível ou faltando, ou algum dado essencial ilegível" in prompt
    assert "Se não conseguir ler todas as alternativas, a confiança é baixa" in prompt
    assert "peça para tirar outra foto mais perto, com boa luz e a questão inteira no enquadramento" in prompt
    assert "digitar o enunciado e as alternativas" in prompt


def test_image_prompt_forces_low_confidence_when_photo_is_cut():
    prompt = build_image_question_prompt()

    assert 'faltar qualquer alternativa ou dado essencial, declare obrigatoriamente "Confiança: baixa"' in prompt
    assert "Confiança: média — SOMENTE quando a questão está inteira na foto" in prompt


@pytest.mark.parametrize(
    "answer,expected",
    [
        ("O que consegui ler: ...\nConfiança: alta — tudo legível.", "alta"),
        ("**Confiança:** média, a alternativa C está borrada.", "media"),
        ("Confiança: **Baixa**\nNão consegui ler a questão com segurança.", "baixa"),
        ("Confiança - media", "media"),
        ("Sem a linha de confiança.", None),
    ],
)
def test_image_answer_confidence_parser(answer, expected):
    assert main_module._image_answer_confidence(answer) == expected


@pytest.mark.parametrize(
    "answer,confidence,can_answer,needs_better_photo",
    [
        ("Confiança: alta — legível.\nResposta final: B.", "alta", True, False),
        ("Confiança: média — alternativa D duvidosa.\nA alternativa mais provável é B.", "media", True, False),
        ("Confiança: baixa — alternativas cortadas.\nNão consegui ler a questão com segurança.", "baixa", False, True),
    ],
)
def test_solve_image_returns_confidence_fields(client, fake_llm, answer, confidence, can_answer, needs_better_photo):
    fake_llm.answer[0] = answer
    response = client.post(
        "/api/v1/materials/solve-image", content=_image_bytes(), headers={"Content-Type": "image/jpeg"}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["confidence"] == confidence
    assert body["can_answer"] is can_answer
    assert body["needs_better_photo"] is needs_better_photo
    assert body["notice"] == main_module.IMAGE_CONFIDENCE_NOTICES[confidence]
    # Com confiança baixa o texto da IA é trocado pela versão segura, sem resposta final.
    expected = main_module._safe_low_confidence_answer(answer) if confidence == "baixa" else answer
    assert body["answer"] == expected


def test_solve_image_without_confidence_line_defaults_to_medium(client, fake_llm):
    fake_llm.answer[0] = "Resposta final: B."
    response = client.post(
        "/api/v1/materials/solve-image", content=_image_bytes(), headers={"Content-Type": "image/jpeg"}
    )

    body = response.json()
    assert body["confidence"] == "media"
    assert body["can_answer"] is True
    assert body["needs_better_photo"] is False
    assert body["answer"].endswith(main_module.IMAGE_CONFIDENCE_MISSING_LINE)
    assert "Confiança: média" in body["answer"]


def test_solve_image_rejects_empty_body(client, fake_llm):
    response = client.post(
        "/api/v1/materials/solve-image", content=b"", headers={"Content-Type": "image/jpeg"}
    )
    assert response.status_code == 400
    assert fake_llm == []


def test_solve_image_rejects_unsupported_type(client, fake_llm):
    response = client.post(
        "/api/v1/materials/solve-image",
        content=b"GIF89a....",
        headers={"Content-Type": "image/gif"},
    )
    assert response.status_code == 415


def test_solve_image_rejects_too_large(client, fake_llm):
    response = client.post(
        "/api/v1/materials/solve-image",
        content=b"\xff" * (main_module.IMAGE_UPLOAD_MAX_BYTES + 1),
        headers={"Content-Type": "image/jpeg"},
    )
    assert response.status_code == 413


def test_solve_image_rejects_invalid_image(client, fake_llm):
    response = client.post(
        "/api/v1/materials/solve-image",
        content=b"isto nao e uma imagem",
        headers={"Content-Type": "image/jpeg"},
    )
    assert response.status_code == 400
    assert fake_llm == []


@pytest.mark.parametrize("fmt,content_type", [("JPEG", "image/jpeg"), ("PNG", "image/png"), ("WEBP", "image/webp")])
def test_solve_image_success_returns_answer(client, fake_llm, fmt, content_type):
    response = client.post(
        "/api/v1/materials/solve-image",
        content=_image_bytes(fmt=fmt),
        headers={"Content-Type": content_type, "x-study-topic": "matematica_logica"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["ok"] is True
    assert body["status"] == "success"
    assert body["response"].endswith("Passo 1: leitura do enunciado.")
    assert body["confidence"] == "alta"
    assert body["answer"] == body["response"]
    assert body["notice"]
    # OCR de apoio vazio não vira aviso de erro quando a visão respondeu.
    assert body["warning"] is None
    assert body["ocr_weak"] is True
    assert body["topic"] == "matematica_logica"
    assert body["image_processed_size"] == [400, 300]
    assert fake_llm[0]["jpeg"].startswith(b"\xff\xd8")


def test_solve_image_fixes_exif_orientation_and_limits_size(client, fake_llm):
    # Orientação 6 = girar 90°: a imagem 4000x3000 deve virar retrato.
    response = client.post(
        "/api/v1/materials/solve-image",
        content=_image_bytes(size=(4000, 3000), exif_orientation=6),
        headers={"Content-Type": "image/jpeg"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["image_original_size"] == [3000, 4000]
    assert max(body["image_processed_size"]) == main_module.IMAGE_VISION_MAX_SIDE
    assert body["image_processed_size"][1] > body["image_processed_size"][0]
    assert body["image_bytes"] <= main_module.IMAGE_VISION_MAX_ENCODED_BYTES


def test_solve_image_returns_503_when_vision_unavailable(client, monkeypatch):
    def unavailable(*args, **kwargs):
        raise ImageAnswerUnavailable("missing_api_key")

    monkeypatch.setattr(main_module, "generate_image_study_answer", unavailable)
    monkeypatch.setattr(main_module, "_ocr_hint_for_vision", lambda image: "")

    response = client.post(
        "/api/v1/materials/solve-image",
        content=_image_bytes(),
        headers={"Content-Type": "image/jpeg"},
    )
    assert response.status_code == 503
    assert "indisponível" in response.json()["detail"]


def test_generate_image_answer_without_api_key_raises():
    from app.config import Settings

    with pytest.raises(ImageAnswerUnavailable) as info:
        generate_image_study_answer(_image_bytes(), Settings(openai_api_key=""))
    assert info.value.reason == "missing_api_key"


def test_generate_image_answer_sends_vision_payload(monkeypatch):
    import openai

    from app.config import Settings

    captured = {}

    class FakeCompletions:
        def create(self, **kwargs):
            captured.update(kwargs)

            class Msg:
                content = "Explicação passo a passo."

            class Choice:
                message = Msg()

            class Resp:
                choices = [Choice()]

            return Resp()

    class FakeClient:
        def __init__(self, **kwargs):
            self.chat = type("Chat", (), {"completions": FakeCompletions()})()

    monkeypatch.setattr(openai, "OpenAI", FakeClient)

    answer = generate_image_study_answer(
        _image_bytes(), Settings(openai_api_key="sk-test", llm_vision_model=""), ocr_hint="2 + 2 = ?"
    )

    assert answer == "Explicação passo a passo."
    assert captured["model"] == "gpt-4o-mini"
    user_content = captured["messages"][1]["content"]
    assert user_content[0]["type"] == "text"
    assert "2 + 2 = ?" in user_content[0]["text"]
    assert user_content[1]["image_url"]["url"].startswith("data:image/jpeg;base64,")
    assert user_content[1]["image_url"]["detail"] == "high"


def test_solve_image_uses_materials_rate_limit_bucket():
    assert main_module._expensive_route_limit("/api/v1/materials/solve-image")[0] == "materials"


def _solve(client):
    response = client.post(
        "/api/v1/materials/solve-image", content=_image_bytes(), headers={"Content-Type": "image/jpeg"}
    )
    assert response.status_code == 200
    return response.json()


def test_solve_image_cut_question_forces_low_confidence(client, fake_llm):
    fake_llm.answer[0] = (
        "O que consegui ler: a questão está cortada; o restante do enunciado não aparece.\n"
        "Confiança: média — falta parte do texto.\n"
        "Não é possível determinar a alternativa correta."
    )
    body = _solve(client)

    assert body["confidence"] == "baixa"
    assert body["can_answer"] is False
    assert body["needs_better_photo"] is True
    assert body["notice"] == main_module.IMAGE_CONFIDENCE_NOTICES["baixa"]


def test_solve_image_normal_high_confidence_stays_high(client, fake_llm):
    fake_llm.answer[0] = "O que consegui ler: 2 + 3; A) 4 B) 5 C) 6.\nConfiança: alta — tudo legível.\nResposta final: B) 5."
    body = _solve(client)

    assert body["confidence"] == "alta"
    assert body["can_answer"] is True
    assert body["needs_better_photo"] is False


@pytest.mark.parametrize(
    "answer,confidence",
    [
        ("Resposta final: B.", "media"),
        ("A questão parece incompleta, não consigo determinar a alternativa.", "baixa"),
        ("Nao e possivel determinar sem uma nova foto.", "baixa"),
    ],
)
def test_solve_image_fallback_without_confidence_line(client, fake_llm, answer, confidence):
    fake_llm.answer[0] = answer
    body = _solve(client)

    assert body["confidence"] == confidence
    assert body["can_answer"] is (confidence != "baixa")
    assert body["needs_better_photo"] is (confidence == "baixa")


@pytest.mark.parametrize(
    "text",
    [
        "Confiança: alta. Pacote recortado não conta.",
        "Confiança: alta. O handshake completo tem 3 etapas.",
    ],
)
def test_incomplete_signals_ignore_unrelated_words(text):
    assert main_module._image_answer_is_incomplete(text) is False


@pytest.mark.parametrize(
    "raw,fixed",
    [
        ("A questão pedepara somar.", "A questão pede para somar."),
        ("O restanteda questão sumiu.", "O restante da questão sumiu."),
        ("Isso vai ajudara determinar.", "Isso vai ajudar a determinar."),
        ("Banco dedados.", "Banco de dados."),
        ("Leia aper pergunta.", "Leia a pergunta."),
        ("Envie a questãocompleta.", "Envie a questão completa."),
        ("Erro comum a evitar:Não somar errado.", "Erro comum a evitar: Não somar errado."),
        ("Às 10:30, veja https://dilsai.app.", "Às 10:30, veja https://dilsai.app."),
    ],
)
def test_fix_glued_words(raw, fixed):
    assert main_module._fix_glued_words(raw) == fixed


def test_solve_image_returns_cleaned_answer(client, fake_llm):
    fake_llm.answer[0] = "Confiança: alta — legível.\nA questão pedepara somar.\nErro comum a evitar:Não trocar o sinal."
    body = _solve(client)

    assert "pede para somar" in body["answer"]
    assert "evitar: Não trocar" in body["answer"]


@pytest.mark.parametrize(
    "answer",
    [
        "O que consegui ler: A) Camada Física B) Camada de Enlace de Dados.\nConfiança: alta — legível.\n"
        "A resposta correta seria a Camada de Rede, que não está listada nas alternativas.",
        "Confiança: alta — legível.\nNenhuma das alternativas é correta, B é a mais próxima do contexto.",
        "As alternativas são: A) Camada Física B) Camada de Enlace de Dados.\nConfiança: alta — legível.\n"
        "Resposta final: B) Camada de Enlace de Dados.",
    ],
)
def test_solve_image_missing_visible_options_forces_low(client, fake_llm, answer):
    fake_llm.answer[0] = answer
    body = _solve(client)

    assert body["confidence"] == "baixa"
    assert body["can_answer"] is False
    assert body["needs_better_photo"] is True


def test_solve_image_all_five_options_high_stays_high(client, fake_llm):
    fake_llm.answer[0] = (
        "As alternativas são: A) Física B) Enlace C) Rede D) Transporte E) Aplicação.\n"
        "Confiança: alta — tudo legível.\nResposta final: C) Rede."
    )
    body = _solve(client)

    assert body["confidence"] == "alta"
    assert body["can_answer"] is True
    assert body["needs_better_photo"] is False


def test_solve_image_low_confidence_redacts_final_answer(client, fake_llm):
    fake_llm.answer[0] = (
        "O que consegui ler: Qual camada roteia pacotes? A) Camada Física B) Camada de Enlace de Dados.\n"
        "Confiança: alta — tudo legível.\n"
        "Resolução passo a passo: a Camada de Rede não está listada nas alternativas.\n"
        "Resposta final: a alternativa correta é a mais próxima do contexto, B."
    )
    body = _solve(client)

    assert body["confidence"] == "baixa"
    assert body["can_answer"] is False
    assert body["needs_better_photo"] is True
    assert body["notice"] == main_module.IMAGE_CONFIDENCE_NOTICES["baixa"]
    for text in (body["answer"], body["response"]):
        assert "Confiança: alta" not in text
        assert "Resposta final" not in text
        assert "alternativa correta" not in text
        assert "mais próxima" not in text
        assert "Confiança: baixa" in text
        assert "Não vou marcar resposta final" in text
    assert "Qual camada roteia pacotes?" in body["answer"]


def test_safe_low_confidence_answer_without_read_section():
    safe = main_module._safe_low_confidence_answer("Confiança: alta.\nResposta final: B.")

    assert safe.startswith("O que consegui ler: não consegui confirmar a questão completa com segurança.")
    assert "Resposta final" not in safe
    assert "Confiança: alta" not in safe


def test_solve_image_high_confidence_keeps_final_answer(client, fake_llm):
    fake_llm.answer[0] = (
        "As alternativas são: A) Física B) Enlace C) Rede D) Transporte E) Aplicação.\n"
        "Confiança: alta — tudo legível.\nResposta final: C) Rede."
    )
    body = _solve(client)

    assert body["confidence"] == "alta"
    assert "Resposta final: C) Rede." in body["answer"]
