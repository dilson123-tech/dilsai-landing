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
    calls = []

    def fake(image_jpeg, settings_, topic, level, ocr_hint):
        calls.append({"jpeg": image_jpeg, "topic": topic, "level": level, "ocr": ocr_hint})
        return "Passo 1: leitura do enunciado."

    monkeypatch.setattr(main_module, "generate_image_study_answer", fake)
    monkeypatch.setattr(main_module, "_ocr_hint_for_vision", lambda image: "")
    return calls


def test_image_prompt_has_required_instructions():
    prompt = build_image_question_prompt()

    assert "Leia a questão na imagem." in prompt
    assert "Se conseguir identificar o enunciado e alternativas, explique passo a passo." in prompt
    assert "diga claramente para tirar outra foto mais perto" in prompt
    assert "Com base no que consegui ler..." in prompt
    assert "A alternativa mais provável é..." in prompt
    assert "nunca responda que não encontrou material" in prompt
    assert "Não invente texto que não está visível." in prompt
    assert "Se for questão de múltipla escolha, indique a alternativa provável e explique." in prompt
    assert "Não incentive cola" in prompt


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
    assert body["response"] == "Passo 1: leitura do enunciado."
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
