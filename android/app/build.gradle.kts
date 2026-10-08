import java.util.Properties

plugins {
    id("com.android.application")
}

val releaseSigningPropertiesFile =
    file("${System.getProperty("user.home")}/.dilsai-estudos-signing/release.properties")

val releaseSigningProperties = Properties()

if (releaseSigningPropertiesFile.exists()) {
    releaseSigningPropertiesFile.inputStream().use { input ->
        releaseSigningProperties.load(input)
    }
}

android {
    namespace = "com.dilsai.estudos"
    compileSdk = 36

    defaultConfig {
        applicationId = "com.dilsai.estudos"
        minSdk = 24
        targetSdk = 36
        versionCode = 10
        versionName = "0.4.2-image-answer-confidence"
    }

    signingConfigs {
        create("release") {
            if (releaseSigningPropertiesFile.exists()) {
                storeFile = file(releaseSigningProperties.getProperty("storeFile"))
                storePassword = releaseSigningProperties.getProperty("storePassword")
                keyAlias = releaseSigningProperties.getProperty("keyAlias")
                keyPassword = releaseSigningProperties.getProperty("keyPassword")
            }
        }
    }

    buildTypes {
        release {
            if (releaseSigningPropertiesFile.exists()) {
                signingConfig = signingConfigs.getByName("release")
            }
            isMinifyEnabled = false
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro"
            )
        }
    }
}

tasks.matching {
    it.name == "preReleaseBuild"
}.configureEach {
    doFirst {
        require(releaseSigningPropertiesFile.exists()) {
            "Release requires ~/.dilsai-estudos-signing/release.properties"
        }

        val releaseStoreFile = releaseSigningProperties.getProperty("storeFile")
        require(!releaseStoreFile.isNullOrBlank() && file(releaseStoreFile).exists()) {
            "Release keystore not found. Check storeFile in ~/.dilsai-estudos-signing/release.properties"
        }
    }
}

dependencies {
    implementation("androidx.core:core:1.13.1")
}
