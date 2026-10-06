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
        versionCode = 2
        versionName = "0.3.2-android-identity"
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
