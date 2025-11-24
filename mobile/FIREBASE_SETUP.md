# 🔥 Configuración de Firebase - Monitor Infantil

## 📋 Pasos de Configuración

### 1. Crear Proyecto en Firebase Console

1. Ir a https://console.firebase.google.com/
2. Clic en "Crear un proyecto"
3. Nombre del proyecto: `proyectosig` (o el nombre que elegiste)
4. Continuar y seguir los pasos

### 2. Agregar App Android

1. En el dashboard del proyecto, clic en el ícono de Android
2. Nombre del paquete: `com.example.monitor_infantil_app`
3. Apodo de la app (opcional): `Monitor Infantil Android`
4. SHA-1 (opcional por ahora, se puede agregar después)
5. Descargar `google-services.json`
6. Colocar el archivo en: `android/app/google-services.json`

### 3. Configurar Android

#### Archivo `android/build.gradle`:
```gradle
buildscript {
    dependencies {
        // Agregar esta línea
        classpath 'com.google.gms:google-services:4.4.0'
    }
}
```

#### Archivo `android/app/build.gradle`:
```gradle
// Al final del archivo, agregar:
apply plugin: 'com.google.gms.google-services'

// En dependencies, verificar que esté:
dependencies {
    implementation platform('com.google.firebase:firebase-bom:32.7.0')
    implementation 'com.google.firebase:firebase-messaging'
}
```

#### Archivo `android/app/src/main/AndroidManifest.xml`:
```xml
<manifest ...>
    <application ...>
        <!-- Agregar esto dentro de <application> -->
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_channel_id"
            android:value="alertas_channel" />
        
        <meta-data
            android:name="com.google.firebase.messaging.default_notification_icon"
            android:resource="@mipmap/ic_launcher" />
    </application>
</manifest>
```

### 4. Actualizar main.dart

Ya está preparado el código. Solo falta inicializar Firebase.

### 5. Activar Cloud Messaging en Firebase

1. En Firebase Console, ir a "Cloud Messaging"
2. Activar la API de Cloud Messaging

---

## 📱 Uso en la App

El servicio Firebase ya está implementado en `lib/services/firebase_service.dart`

### Funcionalidades:
- ✅ Solicitud de permisos de notificaciones
- ✅ Obtención automática del token FCM
- ✅ Envío del token al backend Django
- ✅ Notificaciones en primer plano
- ✅ Notificaciones en segundo plano
- ✅ Manejo de clics en notificaciones

---

## 🔧 Comandos Útiles

### Obtener SHA-1 para Firebase (opcional)
```bash
cd android
./gradlew signingReport
```

### Verificar configuración
```bash
flutter clean
flutter pub get
flutter run
```

---

## 🧪 Probar Notificaciones

### Desde Firebase Console:
1. Ir a "Cloud Messaging" → "Enviar tu primer mensaje"
2. Título: "Prueba"
3. Texto: "Notificación de prueba"
4. Enviar mensaje de prueba
5. Pegar el token FCM que aparece en los logs

### Desde el Backend Django:
El backend ya está configurado para enviar notificaciones cuando un niño sale del área.

---

## 📄 Archivos Importantes

- `google-services.json` → `android/app/`
- `firebase_service.dart` → `lib/services/`
- `main.dart` → Inicialización de Firebase

---

## 🐛 Solución de Problemas

### Error: "google-services.json not found"
- Verificar que el archivo esté en `android/app/google-services.json`

### Error: "Failed to get FIS auth token"
- Verificar conexión a internet
- Verificar que el proyecto de Firebase esté activo

### No recibo notificaciones
1. Verificar permisos en el dispositivo
2. Verificar que el token se haya enviado al backend
3. Ver logs: `flutter logs`
