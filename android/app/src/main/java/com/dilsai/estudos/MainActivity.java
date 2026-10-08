package com.dilsai.estudos;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.media.ExifInterface;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.util.Base64;
import android.util.Log;
import android.webkit.JavascriptInterface;
import android.webkit.ValueCallback;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;

import androidx.core.content.FileProvider;

import org.json.JSONObject;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.InputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.SocketTimeoutException;
import java.net.URL;
import java.lang.ref.WeakReference;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends Activity {
    private static final int FILE_CHOOSER_REQUEST_CODE = 1001;
    private static final int ANDROID_CAMERA_REQUEST_CODE = 1002;
    private static final String MATERIAL_EXTRACT_URL = "https://dilsai-api.onrender.com/api/v1/materials/extract-text";
    private static final String MATERIAL_SOLVE_IMAGE_URL = "https://dilsai-api.onrender.com/api/v1/materials/solve-image";
    private static final String TAG = "DilsAICamera";
    private static final String SOLVE_TAG = "DilsAIImageSolve";
    private static final int OCR_MAX_IMAGE_SIDE = 800;
    private static final int OCR_JPEG_QUALITY = 85;
    private static final int PREVIEW_MAX_IMAGE_SIDE = 1280;
    private static final int PREVIEW_JPEG_QUALITY = 80;
    // "Resolver pela foto": a IA de visão precisa de mais detalhe que o OCR. 1280 px já entrega a
    // resolução final usada pela OpenAI (lado menor 768 px) com upload mais rápido que 1600 px.
    private static final int SOLVE_MAX_IMAGE_SIDE = 1280;
    private static final int SOLVE_JPEG_QUALITY = 82;
    private static final String STATE_CAMERA_CAPTURE_PATH = "dilsai_camera_capture_path";
    private static final String STATE_PENDING_PHOTO_PATH = "dilsai_pending_photo_path";
    private static final String OCR_RETRY_MESSAGE = "Não consegui ler esta foto agora. Tente tirar outra foto mais perto ou tente novamente.";

    // Sobrevivem à recriação da Activity (mesmo processo) enquanto o OCR roda em background.
    private static WeakReference<MainActivity> currentInstance = new WeakReference<>(null);
    private static String pendingCameraResultJson;
    private static String pendingPhotoAnswerJson;
    // Foto capturada aguardando o aluno confirmar o OCR (arquivo original fica no cache até lá).
    private static volatile String pendingPhotoPath;
    private static volatile String pendingCameraPreviewJson;
    private static volatile boolean ocrUploadInProgress;

    private WebView webView;
    private boolean webPageReady;
    private ValueCallback<Uri[]> filePathCallback;
    private Uri cameraCaptureUri;
    private File cameraCaptureFile;
    private String cameraCapturePath;

    @SuppressLint({"SetJavaScriptEnabled", "AddJavascriptInterface"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        currentInstance = new WeakReference<>(this);

        if (savedInstanceState != null) {
            cameraCapturePath = savedInstanceState.getString(STATE_CAMERA_CAPTURE_PATH);
            cameraCaptureFile = cameraCapturePath == null ? null : new File(cameraCapturePath);

            if (pendingPhotoPath == null) {
                pendingPhotoPath = savedInstanceState.getString(STATE_PENDING_PHOTO_PATH);
            }
        }

        // Processo recriado com foto pendente: refaz a prévia a partir do arquivo em cache.
        if (pendingPhotoPath != null && pendingCameraPreviewJson == null) {
            File pendingFile = new File(pendingPhotoPath);
            if (isUsableCapture(pendingFile)) {
                buildCameraPreview(pendingFile);
            } else {
                pendingPhotoPath = null;
            }
        }

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);

        webView.addJavascriptInterface(new AndroidCameraBridge(), "DilsAIAndroidCamera");
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                webPageReady = false;
                super.onPageStarted(view, url, favicon);
            }

            @Override
            public void onPageFinished(WebView view, String url) {
                super.onPageFinished(view, url);
                webPageReady = true;
                deliverPendingCameraResult();
                deliverPendingPhotoAnswer();
                deliverPendingCameraPreview();
            }
        });
        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public boolean onShowFileChooser(
                    WebView webView,
                    ValueCallback<Uri[]> filePathCallback,
                    FileChooserParams fileChooserParams
            ) {
                if (MainActivity.this.filePathCallback != null) {
                    MainActivity.this.filePathCallback.onReceiveValue(null);
                }

                MainActivity.this.filePathCallback = filePathCallback;
                clearCameraCapture();

                Intent intent = null;

                if (shouldLaunchCameraDirectly(fileChooserParams)) {
                    intent = createCameraCaptureIntent();
                }

                if (intent == null) {
                    try {
                        intent = fileChooserParams.createIntent();
                    } catch (Exception error) {
                        MainActivity.this.filePathCallback = null;
                        return false;
                    }
                }

                try {
                    startActivityForResult(intent, FILE_CHOOSER_REQUEST_CODE);
                } catch (ActivityNotFoundException error) {
                    MainActivity.this.filePathCallback = null;
                    clearCameraCapture();
                    return false;
                }

                return true;
            }
        });

        if (savedInstanceState == null || webView.restoreState(savedInstanceState) == null) {
            webView.loadUrl(getString(R.string.dilsai_url));
        }
    }

    private class AndroidCameraBridge {
        @JavascriptInterface
        public void openCamera() {
            Log.d(TAG, "JS bridge openCamera");
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if (!isTrustedDilsAIPage()) {
                        sendCameraStatusToWeb("Câmera bloqueada fora da página oficial do DilsAI.", "error");
                        return;
                    }

                    launchNativeCameraForOcr();
                }
            });
        }

        @JavascriptInterface
        public void confirmPhotoOcr() {
            Log.d(TAG, "JS bridge confirmPhotoOcr");
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if (!isTrustedDilsAIPage()) {
                        sendCameraStatusToWeb("Câmera bloqueada fora da página oficial do DilsAI.", "error");
                        return;
                    }

                    startPendingPhotoOcr();
                }
            });
        }

        @JavascriptInterface
        public void solvePhotoQuestion() {
            Log.d(SOLVE_TAG, "JS bridge solvePhotoQuestion");
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if (!isTrustedDilsAIPage()) {
                        sendCameraStatusToWeb("Câmera bloqueada fora da página oficial do DilsAI.", "error");
                        return;
                    }

                    startPendingPhotoSolve();
                }
            });
        }

        @JavascriptInterface
        public void cancelPhoto() {
            Log.d(TAG, "JS bridge cancelPhoto");
            runOnUiThread(new Runnable() {
                @Override
                public void run() {
                    if (!isTrustedDilsAIPage()) return;
                    if (ocrUploadInProgress) return;

                    discardPendingPhoto();
                }
            });
        }
    }

    private boolean isTrustedDilsAIPage() {
        String currentUrl = webView == null ? null : webView.getUrl();
        return currentUrl != null && currentUrl.startsWith("https://dilson123-tech.github.io/dilsai-landing/");
    }

    private void launchNativeCameraForOcr() {
        if (ocrUploadInProgress) {
            sendCameraStatusToWeb("Aguarde: ainda estou lendo a foto anterior.", "info");
            return;
        }

        discardPendingPhoto();
        clearCameraCapture();

        Intent intent = createCameraCaptureIntent();
        if (intent == null) {
            sendCameraStatusToWeb("Não consegui abrir a câmera neste aparelho.", "error");
            return;
        }

        try {
            startActivityForResult(intent, ANDROID_CAMERA_REQUEST_CODE);
        } catch (ActivityNotFoundException error) {
            clearCameraCapture();
            sendCameraStatusToWeb("Não encontrei aplicativo de câmera neste aparelho.", "error");
        }
    }

    private boolean shouldLaunchCameraDirectly(WebChromeClient.FileChooserParams params) {
        if (params == null) {
            return false;
        }

        String[] acceptTypes = params.getAcceptTypes();
        if (acceptTypes == null || acceptTypes.length == 0) {
            return params.isCaptureEnabled();
        }

        boolean foundImageType = false;
        boolean foundNonImageType = false;

        for (String acceptType : acceptTypes) {
            String value = String.valueOf(acceptType == null ? "" : acceptType).trim().toLowerCase(Locale.ROOT);

            if (value.isEmpty()) {
                continue;
            }

            if (
                    value.startsWith("image/") ||
                    value.equals(".png") ||
                    value.equals(".jpg") ||
                    value.equals(".jpeg") ||
                    value.equals(".webp")
            ) {
                foundImageType = true;
            } else {
                foundNonImageType = true;
            }
        }

        if (params.isCaptureEnabled() && !foundNonImageType) {
            return true;
        }

        return foundImageType && !foundNonImageType;
    }

    private Intent createCameraCaptureIntent() {
        Intent cameraIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        try {
            File photoFile = createCameraImageFile();
            Uri photoUri = FileProvider.getUriForFile(
                    this,
                    getPackageName() + ".fileprovider",
                    photoFile
            );

            cameraCaptureFile = photoFile;
            cameraCapturePath = photoFile.getAbsolutePath();
            cameraCaptureUri = photoUri;

            cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
            cameraIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            cameraIntent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
            cameraIntent.setClipData(ClipData.newUri(getContentResolver(), "DilsAI capture", photoUri));

            return cameraIntent;
        } catch (IOException error) {
            Log.e(TAG, "Could not create camera image file", error);
            clearCameraCapture();
            return null;
        }
    }

    private File createCameraImageFile() throws IOException {
        String timestamp = new SimpleDateFormat("yyyyMMdd_HHmmss", Locale.ROOT).format(new Date());
        File baseDir = getExternalCacheDir();

        if (baseDir == null) {
            baseDir = getCacheDir();
        }

        File storageDir = new File(baseDir, "Pictures");
        if (!storageDir.exists() && !storageDir.mkdirs()) {
            throw new IOException("Could not create camera image directory");
        }

        return File.createTempFile("dilsai_capture_" + timestamp + "_", ".jpg", storageDir);
    }

    // Foto revisada pelo aluno: só agora vai para o OCR. Fica pendente até o OCR devolver texto.
    private void showCapturedPhotoForReview(File file) {
        discardPendingPhoto();
        pendingPhotoPath = file.getAbsolutePath();
        sendCameraStatusToWeb("Preparando prévia da foto...", "info");
        buildCameraPreview(file);
    }

    private void buildCameraPreview(final File file) {
        final String photoPath = file.getAbsolutePath();

        new Thread(new Runnable() {
            @Override
            public void run() {
                JSONObject payload = new JSONObject();

                try {
                    payload.put("file_name", file.getName());
                    payload.put("original_size", file.length());

                    try {
                        EncodedImage preview = encodeScaledJpeg(file, PREVIEW_MAX_IMAGE_SIDE, PREVIEW_JPEG_QUALITY);
                        payload.put("data_url", "data:image/jpeg;base64," + Base64.encodeToString(preview.bytes, Base64.NO_WRAP));
                        payload.put("width", preview.width);
                        payload.put("height", preview.height);
                        payload.put("original_width", preview.originalWidth);
                        payload.put("original_height", preview.originalHeight);
                        Log.d(TAG, "Camera preview ready bytes=" + preview.bytes.length
                                + " size=" + preview.width + "x" + preview.height);
                    } catch (Exception | OutOfMemoryError error) {
                        // Sem imagem a página ainda mostra os botões para ler ou tirar outra foto.
                        Log.e(TAG, "Camera preview failed", error);
                        payload.put("data_url", "");
                    }
                } catch (Exception error) {
                    Log.e(TAG, "Camera preview payload failed", error);
                    return;
                }

                final String json = payload.toString();
                MainActivity target = currentInstance.get();
                final MainActivity activity = target == null ? MainActivity.this : target;

                activity.runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        // O aluno pode ter cancelado ou tirado outra foto enquanto a prévia era gerada.
                        if (!photoPath.equals(pendingPhotoPath)) return;

                        pendingCameraPreviewJson = json;
                        activity.deliverPendingCameraPreview();
                    }
                });
            }
        }).start();
    }

    private void deliverPendingCameraPreview() {
        final String json = pendingCameraPreviewJson;
        if (json == null || webView == null || !webPageReady) return;

        String script = "(function(){"
                + "if (typeof window.dilsaiShowAndroidCameraPreview === 'function') {"
                + "window.dilsaiShowAndroidCameraPreview(" + json + ");"
                + "return 'preview';"
                + "}"
                + "if (typeof window.dilsaiSetMaterialFromAndroidCamera === 'function') return 'legacy';"
                + "return 'none';"
                + "})();";

        webView.evaluateJavascript(script, new ValueCallback<String>() {
            @Override
            public void onReceiveValue(String value) {
                Log.d(TAG, "Camera preview delivery=" + value);

                // Página antiga (sem tela de prévia): mantém o fluxo anterior e lê a foto direto.
                if ("\"legacy\"".equals(value) && json.equals(pendingCameraPreviewJson)) {
                    startPendingPhotoOcr();
                }
            }
        });
    }

    private void startPendingPhotoOcr() {
        if (ocrUploadInProgress) {
            sendCameraStatusToWeb("Já estou lendo esta foto. Aguarde...", "info");
            return;
        }

        String photoPath = pendingPhotoPath;
        File file = photoPath == null ? null : new File(photoPath);

        if (!isUsableCapture(file)) {
            discardPendingPhoto();
            sendCameraStatusToWeb("Não encontrei a foto. Toque em Tirar outra foto.", "error");
            return;
        }

        uploadCapturedImageToBackend(file);
    }

    private void startPendingPhotoSolve() {
        // Mesmo bloqueio do OCR: um envio por vez para a mesma foto.
        if (ocrUploadInProgress) {
            sendCameraStatusToWeb("Já estou analisando esta foto. Aguarde...", "info");
            return;
        }

        String photoPath = pendingPhotoPath;
        File file = photoPath == null ? null : new File(photoPath);

        if (!isUsableCapture(file)) {
            discardPendingPhoto();
            sendCameraStatusToWeb("Não encontrei a foto. Toque em Tirar outra foto.", "error");
            return;
        }

        uploadPhotoForSolve(file);
    }

    private void uploadPhotoForSolve(final File file) {
        ocrUploadInProgress = true;
        sendCameraStatusToWeb("Analisando a foto...", "info");

        new Thread(new Runnable() {
            @Override
            public void run() {
                HttpURLConnection connection = null;
                int statusCode = -1;
                String errorDetail = "";

                try {
                    byte[] bytes = prepareImageForSolve(file);
                    Log.d(SOLVE_TAG, "Solve upload start bytes=" + bytes.length
                            + " original=" + file.length());

                    connection = (HttpURLConnection) new URL(MATERIAL_SOLVE_IMAGE_URL).openConnection();
                    connection.setRequestMethod("POST");
                    connection.setConnectTimeout(30000);
                    // Render pode estar acordando + chamada de visão: dá folga maior que o OCR.
                    connection.setReadTimeout(150000);
                    connection.setDoOutput(true);
                    connection.setFixedLengthStreamingMode(bytes.length);
                    connection.setRequestProperty("Content-Type", "image/jpeg");
                    connection.setRequestProperty("X-File-Name", URLEncoder.encode(file.getName(), StandardCharsets.UTF_8.name()));

                    try (OutputStream output = connection.getOutputStream()) {
                        output.write(bytes);
                    }

                    statusCode = connection.getResponseCode();
                    Log.d(SOLVE_TAG, "Solve backend status=" + statusCode);
                    InputStream responseStream = statusCode >= 200 && statusCode < 300
                            ? connection.getInputStream()
                            : connection.getErrorStream();
                    String responseBody = readStream(responseStream);

                    if (statusCode < 200 || statusCode >= 300) {
                        errorDetail = extractErrorDetail(responseBody);
                        throw new IOException("HTTP " + statusCode);
                    }

                    JSONObject response = new JSONObject(responseBody);
                    String answer = response.optString("answer", response.optString("response", ""));
                    if (answer.trim().isEmpty()) {
                        throw new IOException("Empty answer");
                    }

                    String confidence = response.optString("confidence", "media");
                    final boolean needsBetterPhoto = response.optBoolean("needs_better_photo", false);
                    Log.d(SOLVE_TAG, "Solve confidence=" + confidence + " needsBetterPhoto=" + needsBetterPhoto);

                    JSONObject payload = new JSONObject();
                    payload.put("ok", true);
                    payload.put("answer", answer);
                    payload.put("notice", response.optString("notice", ""));
                    payload.put("warning", response.isNull("warning") ? "" : response.optString("warning", ""));
                    payload.put("confidence", confidence);
                    payload.put("can_answer", response.optBoolean("can_answer", true));
                    payload.put("needs_better_photo", needsBetterPhoto);
                    payload.put("file_name", file.getName());
                    payload.put("file_size", bytes.length);

                    // Resposta confiável: a foto original já pode sair do cache.
                    // Leitura insegura: a foto continua pendente para o aluno tentar de novo.
                    final String photoPath = file.getAbsolutePath();
                    runOnMainThread(new Runnable() {
                        @Override
                        public void run() {
                            if (!needsBetterPhoto && photoPath.equals(pendingPhotoPath)) {
                                discardPendingPhoto();
                            }
                        }
                    });

                    sendPhotoAnswerToWeb(payload);
                } catch (Exception | OutOfMemoryError error) {
                    // A foto continua pendente: o aluno pode tentar de novo ou usar "Ler texto desta foto".
                    Log.e(SOLVE_TAG, "Solve upload failed status=" + statusCode, error);
                    String message;
                    if (!errorDetail.isEmpty()) {
                        message = errorDetail;
                    } else if (error instanceof Exception && isTemporaryOcrFailure((Exception) error, statusCode)) {
                        message = "Não consegui analisar a foto agora. Tente novamente ou use Ler texto desta foto.";
                    } else {
                        message = "Não consegui processar a foto. Tente novamente ou tire outra foto.";
                    }
                    sendCameraStatusToWeb(message, "error");
                } finally {
                    ocrUploadInProgress = false;
                    if (connection != null) {
                        connection.disconnect();
                    }
                }
            }
        }).start();
    }

    private String extractErrorDetail(String responseBody) {
        try {
            Object detail = new JSONObject(responseBody).opt("detail");
            return detail instanceof String ? ((String) detail).trim() : "";
        } catch (Exception ignored) {
            return "";
        }
    }

    // Versão mais legível que a do OCR (800 px): letras pequenas e fórmulas precisam de detalhe para a IA.
    private byte[] prepareImageForSolve(File file) throws IOException {
        try {
            return encodeScaledJpeg(file, SOLVE_MAX_IMAGE_SIDE, SOLVE_JPEG_QUALITY).bytes;
        } catch (OutOfMemoryError error) {
            Log.e(SOLVE_TAG, "Solve image at " + SOLVE_MAX_IMAGE_SIDE + "px failed, falling back to preview size", error);
            return encodeScaledJpeg(file, PREVIEW_MAX_IMAGE_SIDE, PREVIEW_JPEG_QUALITY).bytes;
        }
    }

    private void sendPhotoAnswerToWeb(final JSONObject payload) {
        // Mesmo esquema do OCR: guarda até a página confirmar o recebimento.
        pendingPhotoAnswerJson = payload.toString();

        MainActivity target = currentInstance.get();
        final MainActivity activity = target == null ? this : target;
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                activity.deliverPendingPhotoAnswer();
            }
        });
    }

    private void deliverPendingPhotoAnswer() {
        final String json = pendingPhotoAnswerJson;
        if (json == null || webView == null || !webPageReady) return;

        String script = "(function(){"
                + "if (typeof window.dilsaiSetAndroidPhotoAnswer !== 'function') return false;"
                + "window.dilsaiSetAndroidPhotoAnswer(" + json + ");"
                + "return true;"
                + "})();";

        webView.evaluateJavascript(script, new ValueCallback<String>() {
            @Override
            public void onReceiveValue(String value) {
                boolean delivered = "true".equals(value);
                Log.d(SOLVE_TAG, "Photo answer delivered=" + delivered);

                if (delivered && json.equals(pendingPhotoAnswerJson)) {
                    pendingPhotoAnswerJson = null;
                }
            }
        });
    }

    private void discardPendingPhoto() {
        String photoPath = pendingPhotoPath;
        pendingPhotoPath = null;
        pendingCameraPreviewJson = null;

        if (photoPath != null && !new File(photoPath).delete()) {
            Log.d(TAG, "Pending photo already removed path=" + photoPath);
        }
    }

    private void uploadCapturedImageToBackend(final File file) {
        ocrUploadInProgress = true;
        sendCameraStatusToWeb("Lendo texto da foto...", "info");

        new Thread(new Runnable() {
            @Override
            public void run() {
                HttpURLConnection connection = null;
                int statusCode = -1;

                try {
                    Log.d(TAG, "OCR upload start path=" + file.getAbsolutePath()
                            + " exists=" + file.exists()
                            + " length=" + file.length());

                    byte[] bytes = prepareImageForOcr(file);
                    Log.d(TAG, "OCR prepared image bytes=" + bytes.length);

                    URL url = new URL(MATERIAL_EXTRACT_URL);

                    connection = (HttpURLConnection) url.openConnection();
                    connection.setRequestMethod("POST");
                    connection.setConnectTimeout(30000);
                    connection.setReadTimeout(120000);
                    connection.setDoOutput(true);
                    connection.setFixedLengthStreamingMode(bytes.length);
                    connection.setRequestProperty("Content-Type", "image/jpeg");
                    connection.setRequestProperty("X-File-Name", URLEncoder.encode(file.getName(), StandardCharsets.UTF_8.name()));

                    Log.d(TAG, "OCR before getOutputStream");
                    try (OutputStream output = connection.getOutputStream()) {
                        output.write(bytes);
                    }
                    Log.d(TAG, "OCR after write bytes=" + bytes.length);

                    statusCode = connection.getResponseCode();
                    Log.d(TAG, "OCR backend status=" + statusCode);
                    InputStream responseStream = statusCode >= 200 && statusCode < 300
                            ? connection.getInputStream()
                            : connection.getErrorStream();

                    String responseBody = readStream(responseStream);

                    if (statusCode < 200 || statusCode >= 300) {
                        throw new IOException("HTTP " + statusCode);
                    }

                    JSONObject response = new JSONObject(responseBody);
                    String text = response.optString("text", "");
                    JSONObject payload = new JSONObject();

                    payload.put("file_name", file.getName());
                    payload.put("file_size", bytes.length);
                    payload.put("text", text);
                    payload.put("char_count", response.optInt("char_count", text.length()));
                    payload.put("warning", response.optString("warning", ""));

                    if (!text.trim().isEmpty()) {
                        // OCR confirmado com texto: a foto original já pode sair do cache.
                        final String photoPath = file.getAbsolutePath();
                        runOnMainThread(new Runnable() {
                            @Override
                            public void run() {
                                if (photoPath.equals(pendingPhotoPath)) {
                                    discardPendingPhoto();
                                }
                            }
                        });
                    }

                    sendCameraResultToWeb(payload);
                } catch (Exception error) {
                    Log.e(TAG, "OCR upload failed status=" + statusCode, error);
                    sendCameraStatusToWeb(
                            isTemporaryOcrFailure(error, statusCode)
                                    ? OCR_RETRY_MESSAGE
                                    : "Não consegui processar a foto. Tente novamente ou use Enviar material.",
                            "error"
                    );
                } finally {
                    ocrUploadInProgress = false;
                    if (connection != null) {
                        connection.disconnect();
                    }
                }
            }
        }).start();
    }

    // 5xx do Render (502/503/504), timeout ou queda de rede: vale tentar de novo ou tirar foto mais perto.
    private boolean isTemporaryOcrFailure(Exception error, int statusCode) {
        if (statusCode >= 500) return true;
        if (error instanceof SocketTimeoutException) return true;
        return statusCode == -1 && error instanceof IOException;
    }

    private void runOnMainThread(Runnable action) {
        MainActivity target = currentInstance.get();
        (target == null ? this : target).runOnUiThread(action);
    }

    private static class EncodedImage {
        byte[] bytes;
        int width;
        int height;
        int originalWidth;
        int originalHeight;
    }

    // Reduz a foto da câmera (maior lado <= 800 px, JPEG 85) para o upload de OCR não estourar o timeout.
    // O backend também limita a imagem a 800 px (IMAGE_OCR_MAX_SIDE), então enviar maior só aumentaria o upload.
    private byte[] prepareImageForOcr(File file) throws IOException {
        try {
            return encodeScaledJpeg(file, OCR_MAX_IMAGE_SIDE, OCR_JPEG_QUALITY).bytes;
        } catch (Exception | OutOfMemoryError error) {
            Log.e(TAG, "OCR image preparation failed, sending original file", error);
            return readAllBytes(file);
        }
    }

    private EncodedImage encodeScaledJpeg(File file, int maxSide, int quality) throws IOException {
        Bitmap bitmap = null;

        try {
            BitmapFactory.Options bounds = new BitmapFactory.Options();
            bounds.inJustDecodeBounds = true;
            BitmapFactory.decodeFile(file.getAbsolutePath(), bounds);

            if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
                throw new IOException("Invalid image bounds");
            }

            int sampleSize = 1;
            while (Math.max(bounds.outWidth, bounds.outHeight) / (sampleSize * 2) >= maxSide) {
                sampleSize *= 2;
            }

            BitmapFactory.Options decodeOptions = new BitmapFactory.Options();
            decodeOptions.inSampleSize = sampleSize;
            bitmap = BitmapFactory.decodeFile(file.getAbsolutePath(), decodeOptions);

            if (bitmap == null) {
                throw new IOException("Could not decode image");
            }

            bitmap = replaceBitmap(bitmap, rotateBitmapFromExif(file, bitmap));

            int longestSide = Math.max(bitmap.getWidth(), bitmap.getHeight());
            if (longestSide > maxSide) {
                float scale = (float) maxSide / longestSide;
                int width = Math.max(1, Math.round(bitmap.getWidth() * scale));
                int height = Math.max(1, Math.round(bitmap.getHeight() * scale));
                bitmap = replaceBitmap(bitmap, Bitmap.createScaledBitmap(bitmap, width, height, true));
            }

            ByteArrayOutputStream output = new ByteArrayOutputStream();
            if (!bitmap.compress(Bitmap.CompressFormat.JPEG, quality, output)) {
                throw new IOException("Could not compress image");
            }

            Log.d(TAG, "Camera image original=" + bounds.outWidth + "x" + bounds.outHeight
                    + " (" + file.length() + " bytes)"
                    + " processed=" + bitmap.getWidth() + "x" + bitmap.getHeight()
                    + " (" + output.size() + " bytes)"
                    + " inSampleSize=" + sampleSize);

            EncodedImage result = new EncodedImage();
            result.bytes = output.toByteArray();
            result.width = bitmap.getWidth();
            result.height = bitmap.getHeight();
            result.originalWidth = bounds.outWidth;
            result.originalHeight = bounds.outHeight;
            return result;
        } finally {
            if (bitmap != null) {
                bitmap.recycle();
            }
        }
    }

    private Bitmap rotateBitmapFromExif(File file, Bitmap bitmap) {
        int degrees;

        try {
            ExifInterface exif = new ExifInterface(file.getAbsolutePath());
            int orientation = exif.getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);

            switch (orientation) {
                case ExifInterface.ORIENTATION_ROTATE_90:
                    degrees = 90;
                    break;
                case ExifInterface.ORIENTATION_ROTATE_180:
                    degrees = 180;
                    break;
                case ExifInterface.ORIENTATION_ROTATE_270:
                    degrees = 270;
                    break;
                default:
                    return bitmap;
            }
        } catch (IOException error) {
            Log.e(TAG, "Could not read EXIF orientation", error);
            return bitmap;
        }

        Matrix matrix = new Matrix();
        matrix.postRotate(degrees);
        return Bitmap.createBitmap(bitmap, 0, 0, bitmap.getWidth(), bitmap.getHeight(), matrix, true);
    }

    private Bitmap replaceBitmap(Bitmap current, Bitmap next) {
        if (next != current) {
            current.recycle();
        }
        return next;
    }

    private byte[] readAllBytes(File file) throws IOException {
        try (
                FileInputStream input = new FileInputStream(file);
                ByteArrayOutputStream output = new ByteArrayOutputStream()
        ) {
            byte[] buffer = new byte[8192];
            int count;

            while ((count = input.read(buffer)) != -1) {
                output.write(buffer, 0, count);
            }

            return output.toByteArray();
        }
    }

    private String readStream(InputStream stream) throws IOException {
        if (stream == null) {
            return "";
        }

        try (InputStream input = stream; ByteArrayOutputStream output = new ByteArrayOutputStream()) {
            byte[] buffer = new byte[8192];
            int count;

            while ((count = input.read(buffer)) != -1) {
                output.write(buffer, 0, count);
            }

            return new String(output.toByteArray(), StandardCharsets.UTF_8);
        }
    }

    private void sendCameraStatusToWeb(final String message, final String type) {
        MainActivity target = currentInstance.get();
        final MainActivity activity = target == null ? this : target;

        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                WebView webView = activity.webView;
                if (webView == null) return;

                String script = "window.dilsaiSetAndroidCameraStatus && window.dilsaiSetAndroidCameraStatus("
                        + JSONObject.quote(message)
                        + ", "
                        + JSONObject.quote(type)
                        + ");";

                webView.evaluateJavascript(script, null);
            }
        });
    }

    private void sendCameraResultToWeb(final JSONObject payload) {
        // Guarda o resultado até a página confirmar que recebeu (a Activity/WebView pode ter sido recriada).
        pendingCameraResultJson = payload.toString();

        MainActivity target = currentInstance.get();
        if (target == null) target = this;

        final MainActivity activity = target;
        activity.runOnUiThread(new Runnable() {
            @Override
            public void run() {
                activity.deliverPendingCameraResult();
            }
        });
    }

    private void deliverPendingCameraResult() {
        final String json = pendingCameraResultJson;
        if (json == null || webView == null || !webPageReady) return;

        String script = "(function(){"
                + "if (typeof window.dilsaiSetMaterialFromAndroidCamera !== 'function') return false;"
                + "window.dilsaiSetMaterialFromAndroidCamera(" + json + ");"
                + "return true;"
                + "})();";

        webView.evaluateJavascript(script, new ValueCallback<String>() {
            @Override
            public void onReceiveValue(String value) {
                boolean delivered = "true".equals(value);
                Log.d(TAG, "Camera OCR result delivered=" + delivered);

                // Se a página ainda não tinha a função, o próximo onPageFinished tenta de novo.
                if (delivered && json.equals(pendingCameraResultJson)) {
                    pendingCameraResultJson = null;
                }
            }
        });
    }

    private File getCurrentCameraCaptureFile() {
        if (cameraCaptureFile != null) return cameraCaptureFile;
        if (cameraCapturePath != null) return new File(cameraCapturePath);
        return null;
    }

    private void clearCameraCapture() {
        cameraCaptureUri = null;
        cameraCaptureFile = null;
        cameraCapturePath = null;
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == ANDROID_CAMERA_REQUEST_CODE) {
            File capturedFile = getCurrentCameraCaptureFile();
            logCameraResult(requestCode, resultCode, capturedFile);

            if (resultCode == RESULT_OK && isUsableCapture(capturedFile)) {
                showCapturedPhotoForReview(capturedFile);
            } else if (resultCode == RESULT_OK) {
                sendCameraStatusToWeb("A foto não foi salva pela câmera. Tente novamente.", "error");
            } else {
                sendCameraStatusToWeb("Captura cancelada.", "info");
            }

            clearCameraCapture();
            return;
        }

        if (requestCode == FILE_CHOOSER_REQUEST_CODE) {
            if (filePathCallback == null) {
                super.onActivityResult(requestCode, resultCode, data);
                return;
            }

            File capturedFile = getCurrentCameraCaptureFile();
            if (capturedFile != null) {
                logCameraResult(requestCode, resultCode, capturedFile);
            }

            if (resultCode == RESULT_OK && isUsableCapture(capturedFile)) {
                // Foto da câmera: prévia + OCR nativo; o input file do WebView recebe cancelamento.
                filePathCallback.onReceiveValue(null);
                filePathCallback = null;
                clearCameraCapture();
                showCapturedPhotoForReview(capturedFile);
                return;
            }

            Uri[] results = null;

            if (resultCode == RESULT_OK && capturedFile == null) {
                results = WebChromeClient.FileChooserParams.parseResult(resultCode, data);
            }

            filePathCallback.onReceiveValue(results);
            filePathCallback = null;
            clearCameraCapture();
            return;
        }

        super.onActivityResult(requestCode, resultCode, data);
    }

    private boolean isUsableCapture(File file) {
        return file != null && file.exists() && file.length() > 0;
    }

    private void logCameraResult(int requestCode, int resultCode, File file) {
        Log.d(TAG, "onActivityResult requestCode=" + requestCode
                + " resultCode=" + resultCode
                + " exists=" + (file != null && file.exists())
                + " size=" + (file == null ? 0 : file.length()));
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        webView.saveState(outState);
        outState.putString(STATE_CAMERA_CAPTURE_PATH, cameraCapturePath);
        outState.putString(STATE_PENDING_PHOTO_PATH, pendingPhotoPath);
        super.onSaveInstanceState(outState);
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) {
            webView.goBack();
            return;
        }

        super.onBackPressed();
    }
}
