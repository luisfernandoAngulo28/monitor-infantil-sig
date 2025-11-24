# 🗺️ Integración de Google Maps

## Paso 1: Obtener API Key de Google Cloud

1. Ve a: https://console.cloud.google.com/

2. Crea un nuevo proyecto o selecciona uno existente
   - Nombre: `Monitor Infantil Maps`

3. Habilita las APIs necesarias:
   - **Maps SDK for Android**
   - **Maps SDK for iOS** (opcional)
   - **Geocoding API** (opcional)

4. Ve a **APIs & Services** > **Credentials**

5. Clic en **+ CREATE CREDENTIALS** > **API Key**

6. Copia la API Key generada

7. (Recomendado) Restringe la API Key:
   - Clic en la API Key recién creada
   - **Application restrictions**: Android apps
   - **API restrictions**: Selecciona las APIs habilitadas

---

## Paso 2: Configurar en Flutter

### Android

Editar `android/app/src/main/AndroidManifest.xml`:

```xml
<application>
    <!-- Agregar dentro de <application> -->
    <meta-data
        android:name="com.google.android.geo.API_KEY"
        android:value="TU_API_KEY_AQUI"/>
</application>
```

### iOS (Opcional)

Editar `ios/Runner/AppDelegate.swift`:

```swift
import GoogleMaps

GMSServices.provideAPIKey("TU_API_KEY_AQUI")
```

---

## Paso 3: Instalar Dependencia

```bash
flutter pub add google_maps_flutter
```

---

## Paso 4: Ya está implementado!

El código ya está listo en:
- `lib/screens/mapa_screen.dart`

Solo necesitas reemplazar `flutter_map` por `google_maps_flutter`.

---

## 🔐 Seguridad de la API Key

**IMPORTANTE:** No subas la API Key a repositorios públicos.

Opción 1: Usar variables de entorno
Opción 2: Crear archivo `local.properties` (gitignore)
Opción 3: Usar Firebase Remote Config

---

¿Ya tienes una API Key de Google Maps o necesitas ayuda para crearla?
