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
    private static final String TAG = "DilsAICamera";
    private static final int OCR_MAX_IMAGE_SIDE = 800;
    private static final int OCR_JPEG_QUALITY = 85;
    private static final String STATE_CAMERA_CAPTURE_PATH = "dilsai_camera_capture_path";

    // Sobrevivem à recriação da Activity (mesmo processo) enquanto o OCR roda em background.
    private static WeakReference<MainActivity> currentInstance = new WeakReference<>(null);
    private static String pendingCameraResultJson;

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
    }

    private boolean isTrustedDilsAIPage() {
        String currentUrl = webView == null ? null : webView.getUrl();
        return currentUrl != null && currentUrl.startsWith("https://dilson123-tech.github.io/dilsai-landing/");
    }

    private void launchNativeCameraForOcr() {
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

    private void uploadCapturedImageToBackend(final File file) {
        sendCameraStatusToWeb("Executando OCR na foto...", "info");

        new Thread(new Runnable() {
            @Override
            public void run() {
                HttpURLConnection connection = null;

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

                    int statusCode = connection.getResponseCode();
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

                    sendCameraResultToWeb(payload);
                } catch (Exception error) {
                    Log.e(TAG, "OCR upload failed", error);
                    sendCameraStatusToWeb("Não consegui processar a foto. Tente novamente ou use Enviar material.", "error");
                } finally {
                    if (connection != null) {
                        connection.disconnect();
                    }
                }
            }
        }).start();
    }

    // Reduz a foto da câmera (maior lado <= 800 px, JPEG 85) para o upload de OCR não estourar o timeout.
    // O backend também limita a imagem a 800 px (IMAGE_OCR_MAX_SIDE), então enviar maior só aumentaria o upload.
    private byte[] prepareImageForOcr(File file) throws IOException {
        Bitmap bitmap = null;

        try {
            BitmapFactory.Options bounds = new BitmapFactory.Options();
            bounds.inJustDecodeBounds = true;
            BitmapFactory.decodeFile(file.getAbsolutePath(), bounds);

            if (bounds.outWidth <= 0 || bounds.outHeight <= 0) {
                throw new IOException("Invalid image bounds");
            }

            int sampleSize = 1;
            while (Math.max(bounds.outWidth, bounds.outHeight) / (sampleSize * 2) >= OCR_MAX_IMAGE_SIDE) {
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
            if (longestSide > OCR_MAX_IMAGE_SIDE) {
                float scale = (float) OCR_MAX_IMAGE_SIDE / longestSide;
                int width = Math.max(1, Math.round(bitmap.getWidth() * scale));
                int height = Math.max(1, Math.round(bitmap.getHeight() * scale));
                bitmap = replaceBitmap(bitmap, Bitmap.createScaledBitmap(bitmap, width, height, true));
            }

            ByteArrayOutputStream output = new ByteArrayOutputStream();
            if (!bitmap.compress(Bitmap.CompressFormat.JPEG, OCR_JPEG_QUALITY, output)) {
                throw new IOException("Could not compress image");
            }

            Log.d(TAG, "OCR image original=" + bounds.outWidth + "x" + bounds.outHeight
                    + " (" + file.length() + " bytes)"
                    + " processed=" + bitmap.getWidth() + "x" + bitmap.getHeight()
                    + " (" + output.size() + " bytes)"
                    + " inSampleSize=" + sampleSize);

            return output.toByteArray();
        } catch (Exception | OutOfMemoryError error) {
            Log.e(TAG, "OCR image preparation failed, sending original file", error);
            return readAllBytes(file);
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
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
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
                uploadCapturedImageToBackend(capturedFile);
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
                // Foto da câmera: OCR nativo; o input file do WebView recebe cancelamento.
                filePathCallback.onReceiveValue(null);
                filePathCallback = null;
                clearCameraCapture();
                uploadCapturedImageToBackend(capturedFile);
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
