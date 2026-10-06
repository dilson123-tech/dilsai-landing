plugins {
    id("com.android.application")
}

android {
    namespace = "com.dilsai.estudos"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.dilsai.estudos"
        minSdk = 23
        targetSdk = 36
        versionCode = 1
        versionName = "0.1.0-android-shell"
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}
