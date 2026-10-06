package com.dilsai.estudos;

import android.annotation.SuppressLint;
import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
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
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

public class MainActivity extends Activity {
    private static final int FILE_CHOOSER_REQUEST_CODE = 1001;
    private static final int ANDROID_CAMERA_REQUEST_CODE = 1002;
    private static final String MATERIAL_EXTRACT_URL = "https://dilsai-api.onrender.com/api/v1/materials/extract-text";

    private WebView webView;
    private ValueCallback<Uri[]> filePathCallback;
    private Uri cameraCaptureUri;
    private File cameraCaptureFile;

    @SuppressLint({"SetJavaScriptEnabled", "AddJavascriptInterface"})
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        webView = new WebView(this);
        setContentView(webView);

        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setLoadWithOverviewMode(true);
        settings.setUseWideViewPort(true);

        webView.addJavascriptInterface(new AndroidCameraBridge(), "DilsAIAndroidCamera");
        webView.setWebViewClient(new WebViewClient());
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
                MainActivity.this.cameraCaptureUri = null;
                MainActivity.this.cameraCaptureFile = null;

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
                    MainActivity.this.cameraCaptureUri = null;
                    MainActivity.this.cameraCaptureFile = null;
                    return false;
                }

                return true;
            }
        });

        if (savedInstanceState == null) {
            webView.loadUrl(getString(R.string.dilsai_url));
        } else {
            webView.restoreState(savedInstanceState);
        }
    }

    private class AndroidCameraBridge {
        @JavascriptInterface
        public void openCamera() {
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
        cameraCaptureUri = null;
        cameraCaptureFile = null;

        Intent intent = createCameraCaptureIntent();
        if (intent == null) {
            sendCameraStatusToWeb("Não consegui abrir a câmera neste aparelho.", "error");
            return;
        }

        try {
            startActivityForResult(intent, ANDROID_CAMERA_REQUEST_CODE);
        } catch (ActivityNotFoundException error) {
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
            cameraCaptureUri = photoUri;

            cameraIntent.putExtra(MediaStore.EXTRA_OUTPUT, photoUri);
            cameraIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            cameraIntent.addFlags(Intent.FLAG_GRANT_WRITE_URI_PERMISSION);
            cameraIntent.setClipData(ClipData.newUri(getContentResolver(), "DilsAI capture", photoUri));

            return cameraIntent;
        } catch (IOException error) {
            cameraCaptureFile = null;
            cameraCaptureUri = null;
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
                    byte[] bytes = readAllBytes(file);
                    URL url = new URL(MATERIAL_EXTRACT_URL);

                    connection = (HttpURLConnection) url.openConnection();
                    connection.setRequestMethod("POST");
                    connection.setConnectTimeout(30000);
                    connection.setReadTimeout(60000);
                    connection.setDoOutput(true);
                    connection.setRequestProperty("Content-Type", "image/jpeg");
                    connection.setRequestProperty("X-File-Name", URLEncoder.encode(file.getName(), StandardCharsets.UTF_8.name()));

                    try (OutputStream output = connection.getOutputStream()) {
                        output.write(bytes);
                    }

                    int statusCode = connection.getResponseCode();
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
                    sendCameraStatusToWeb("Não consegui processar a foto. Tente novamente ou use Enviar material.", "error");
                } finally {
                    if (connection != null) {
                        connection.disconnect();
                    }
                }
            }
        }).start();
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
        runOnUiThread(new Runnable() {
            @Override
            public void run() {
                if (webView == null) return;

                String script = "window.dilsaiSetMaterialFromAndroidCamera && window.dilsaiSetMaterialFromAndroidCamera("
                        + payload.toString()
                        + ");";

                webView.evaluateJavascript(script, null);
            }
        });
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == ANDROID_CAMERA_REQUEST_CODE) {
            if (resultCode == RESULT_OK && cameraCaptureFile != null && cameraCaptureFile.exists()) {
                uploadCapturedImageToBackend(cameraCaptureFile);
            } else {
                sendCameraStatusToWeb("Captura cancelada.", "info");
            }

            cameraCaptureUri = null;
            cameraCaptureFile = null;
            return;
        }

        if (requestCode == FILE_CHOOSER_REQUEST_CODE) {
            if (filePathCallback == null) {
                super.onActivityResult(requestCode, resultCode, data);
                return;
            }

            Uri[] results = null;

            if (resultCode == RESULT_OK) {
                if (cameraCaptureUri != null) {
                    results = new Uri[]{cameraCaptureUri};
                } else {
                    results = WebChromeClient.FileChooserParams.parseResult(resultCode, data);
                }
            }

            filePathCallback.onReceiveValue(results);
            filePathCallback = null;
            cameraCaptureUri = null;
            cameraCaptureFile = null;
            return;
        }

        super.onActivityResult(requestCode, resultCode, data);
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        webView.saveState(outState);
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
