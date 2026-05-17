# Handoff Prompt — Fase 1: Fundación Mobile Logix-AI
# Sprint: 001-mobile-foundation

---

## Instrucciones para el Builder

Lee los siguientes archivos antes de escribir cualquier línea de código:

1. `AGENTS.md`
2. `CLAUDE.md`
3. `planning/STATE.md`
4. `planning/DECISIONS.md`
5. `planning/DOMAIN.md`
6. `planning/RISKS.md`
7. `planning/sprints/001-mobile-foundation/requirements.md`
8. `planning/sprints/001-mobile-foundation/blueprint.md`
9. `planning/sprints/001-mobile-foundation/acceptance.md`

Antes de implementar, resume en un mensaje:
- Qué entiendes que debe lograr esta fase
- Qué archivos vas a crear o modificar
- Qué asumir en caso de ambigüedad y por qué
- Cualquier bloqueador o pregunta antes de arrancar

No escribas código de producción hasta que el Architect apruebe tu resumen.

---

## Contexto del proyecto

**Proyecto:** Logix-AI
**Módulo:** Mobile — app para repartidores (DRIVER) y vendedores (OPERATOR)
**Stack mobile:** React Native + Expo + NativeWind + TypeScript
**Backend:** FastAPI + PostgreSQL/Supabase + JWT (existente o en construcción paralela)
**Plataformas objetivo:** iOS + Android (Expo EAS builds)
**Metodología:** Axon-AI Architect / Builder — el handoff es una carpeta, no una conversación

---

## Decisiones ya tomadas — no renegociar

Estas decisiones viven en `planning/DECISIONS.md`.
El Builder no debe cuestionarlas ni proponer alternativas salvo que haya un bloqueo técnico real.

| Decisión | Valor |
|---|---|
| Framework mobile | React Native + Expo SDK 52 |
| Routing | Expo Router v4 (file-based) |
| Estilos | NativeWind v4 (Tailwind classes en RN) |
| Estado global | Zustand v4 |
| Server state | TanStack Query v5 |
| HTTP client | Axios (mismo que frontend web) |
| Validaciones | Zod (mismas schemas que frontend web) |
| Formularios | React Hook Form |
| Auth storage | Expo SecureStore (nunca AsyncStorage para JWT) |
| Builds | Expo EAS (iOS + Android) |
| Plataformas | iOS y Android |

---

## Objetivo de la Fase 1

Construir la fundación de la app mobile de Logix-AI:

- Proyecto Expo configurado, tipado, con NativeWind funcionando
- Navegación base con separación de stacks: auth y app
- Pantalla de login funcional conectada al endpoint real del backend
- JWT almacenado de forma segura en SecureStore
- Tabs diferenciados por rol: DRIVER vs OPERATOR
- Pantalla Home con estado de sesión del usuario
- Logout limpio
- Estructura de carpetas lista para escalar en fases siguientes
- Sin secretos en código — todo por variables de entorno

---

## Alcance congelado — Fase 1

### Incluye

- Scaffolding completo del proyecto mobile con Expo + NativeWind
- Stack de navegación: (auth) y (app) usando Expo Router
- Pantalla: Login con validación Zod + React Hook Form
- Pantalla: Home con datos básicos del usuario (nombre, rol)
- Pantalla: Perfil placeholder
- Lógica de auth: login → guardar JWT en SecureStore → redirigir a app
- Lógica de logout: limpiar SecureStore → redirigir a login
- Token refresh: interceptor Axios que detecta 401 y limpia sesión
- Tab navigation diferenciada por rol (DRIVER y OPERATOR ven tabs distintos)
- Variables de entorno configuradas (API_URL en .env)
- `.env.example` documentado
- `README.md` del módulo mobile con instrucciones de setup
- Estructura de carpetas según este handoff

### Excluye explícitamente

- Módulo de reportes (Fase 2)
- Cámara y GPS (Fase 2)
- Offline Queue y Sync Engine (Fase 3)
- Push notifications (Fase 5)
- Firma digital (Fase 4)
- Cualquier pantalla de CRUD de datos de negocio
- Dashboard con KPIs o métricas
- Onboarding o tour de bienvenida

---

## Estructura de carpetas a crear

El Builder debe crear exactamente esta estructura dentro de `mobile/`.
No agregar carpetas no listadas. No omitir carpetas listadas.

```text
mobile/
├── app/
│   ├── (auth)/
│   │   ├── _layout.tsx          ← Stack navigator para auth
│   │   └── login.tsx            ← Pantalla de login
│   ├── (app)/
│   │   ├── _layout.tsx          ← Tab navigator principal (por rol)
│   │   ├── index.tsx            ← Home screen
│   │   └── profile.tsx          ← Perfil placeholder
│   ├── _layout.tsx              ← Root layout con AuthProvider
│   └── +not-found.tsx           ← 404 screen
│
├── src/
│   ├── api/
│   │   ├── client.ts            ← Instancia Axios con interceptores JWT
│   │   └── auth.api.ts          ← Funciones: login, logout, refreshToken
│   │
│   ├── stores/
│   │   └── auth.store.ts        ← Zustand store: user, token, isAuthenticated
│   │
│   ├── hooks/
│   │   ├── useAuth.ts           ← Hook que expone auth store + acciones
│   │   └── useProtectedRoute.ts ← Redirige si no hay sesión activa
│   │
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.tsx       ← Botón base reutilizable con variantes
│   │   │   ├── Input.tsx        ← Input base con label, error, helper
│   │   │   └── LoadingSpinner.tsx
│   │   └── layout/
│   │       └── SafeScreen.tsx   ← Wrapper con SafeAreaView + KeyboardAvoid
│   │
│   ├── types/
│   │   ├── auth.types.ts        ← User, AuthState, LoginRequest, LoginResponse
│   │   └── api.types.ts         ← ApiResponse<T>, ApiError
│   │
│   ├── schemas/
│   │   └── auth.schemas.ts      ← Zod: loginSchema, validation messages
│   │
│   ├── constants/
│   │   ├── roles.ts             ← ROLES enum: ADMIN, SUPERVISOR, OPERATOR, DRIVER, CLIENT, VIEWER
│   │   └── routes.ts            ← Constantes de rutas
│   │
│   └── utils/
│       ├── token.ts             ← getToken, setToken, clearToken (SecureStore wrappers)
│       └── errors.ts            ← Normalizar errores de API
│
├── assets/
│   ├── icon.png
│   ├── splash.png
│   └── adaptive-icon.png
│
├── .env                         ← NO commitear — en .gitignore
├── .env.example                 ← Commitear con valores placeholder
├── app.json                     ← Configuración Expo
├── eas.json                     ← Configuración EAS builds
├── tailwind.config.js           ← NativeWind config
├── babel.config.js              ← Con NativeWind preset
├── tsconfig.json                ← Strict mode ON
├── package.json
└── README.md                    ← Setup, comandos, variables de entorno
```

---

## Contrato de API — Fase 1

El Builder debe implementar la app mobile contra estos contratos.
Si el backend aún no existe, el Builder debe mockear las respuestas localmente
y dejar los contratos documentados para que el backend los implemente.

### POST /api/v1/auth/login

**Request:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response 200:**
```json
{
  "access_token": "string (JWT)",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "string",
    "full_name": "string",
    "role": "DRIVER | OPERATOR | SUPERVISOR | ADMIN",
    "is_active": true
  }
}
```

**Response 401:**
```json
{
  "detail": "Credenciales incorrectas"
}
```

### GET /api/v1/auth/me

**Headers:** `Authorization: Bearer <token>`

**Response 200:**
```json
{
  "id": "uuid",
  "email": "string",
  "full_name": "string",
  "role": "string",
  "is_active": true
}
```

**Response 401:**
```json
{
  "detail": "Token inválido o expirado"
}
```

---

## Implementación requerida — archivo por archivo

### `mobile/app/_layout.tsx` — Root Layout

```typescript
// Root layout de la aplicación.
// Responsabilidades:
// - Inicializar AuthProvider / Zustand hydration
// - Leer JWT de SecureStore al arrancar
// - Determinar si el usuario está autenticado
// - Redirigir a (auth) o (app) según estado
// - Manejar estado de carga inicial (splash screen extendido)
```

Comportamiento esperado:
1. App arranca → muestra splash/loading
2. Lee SecureStore → si hay token, llama GET /auth/me para validar
3. Token válido → navega a `/(app)/`
4. Sin token o token inválido → navega a `/(auth)/login`
5. Error de red → navega a `/(auth)/login` con mensaje

### `mobile/app/(auth)/login.tsx` — Login screen

```typescript
// Pantalla de login.
// Form: email + password
// Validación: Zod via React Hook Form
// Submit: POST /api/v1/auth/login
// Éxito: guardar token en SecureStore, guardar user en Zustand, navegar a /(app)/
// Error 401: mostrar "Email o contraseña incorrectos"
// Error red: mostrar "Sin conexión. Verifica tu internet."
// Loading state: deshabilitar botón y mostrar spinner
// Teclado: evitar que tape los inputs (KeyboardAvoidingView)
```

UX requerida:
- Input email: `keyboardType="email-address"`, `autoCapitalize="none"`, `autoComplete="email"`
- Input password: `secureTextEntry`, toggle para mostrar/ocultar
- Botón "Iniciar sesión" deshabilitado mientras carga
- Mensajes de error inline bajo cada campo (validación) y toast/banner para errores de API
- Sin link de "Olvidé mi contraseña" en Fase 1 (fuera de alcance)

### `mobile/app/(app)/_layout.tsx` — Tab Navigator

```typescript
// Tab navigator principal.
// Tabs diferenciadas por rol:
//
// DRIVER ve:
//   - Inicio (index)
//   - Mis reportes (placeholder Fase 2)
//   - Perfil
//
// OPERATOR ve:
//   - Inicio (index)
//   - Mis reportes (placeholder Fase 2)
//   - Mis clientes (placeholder Fase 5)
//   - Perfil
//
// SUPERVISOR / ADMIN ven:
//   - Inicio (index)
//   - Perfil
//   (acceso web preferido para roles de supervisión)
//
// Leer el rol desde el Zustand auth store.
// No hardcodear tabs — construirlas dinámicamente desde el rol.
```

### `mobile/src/api/client.ts` — Axios Instance

```typescript
// Instancia Axios configurada.
// Base URL: desde variable de entorno EXPO_PUBLIC_API_URL
// Timeout: 15000ms
// Headers default: Content-Type: application/json
//
// Interceptor de request:
//   - Lee JWT de SecureStore
//   - Si existe, agrega header: Authorization: Bearer <token>
//
// Interceptor de response:
//   - Si 401: llama clearToken(), resetea Zustand auth store, navega a login
//   - Si error de red: lanza error tipado con mensaje amigable
//   - Otros errores: normaliza y relanza
//
// IMPORTANTE: el interceptor de response NO puede hacer refresh token en Fase 1.
// En Fase 1, un 401 = sesión terminada. Refresh token es Fase 2+.
```

### `mobile/src/stores/auth.store.ts` — Zustand Store

```typescript
// Estado global de autenticación.
//
// State:
//   user: User | null
//   token: string | null
//   isAuthenticated: boolean
//   isLoading: boolean
//
// Actions:
//   login(token: string, user: User): void
//     - Guarda token en SecureStore
//     - Actualiza estado en memoria
//
//   logout(): void
//     - Limpia SecureStore
//     - Resetea estado a valores iniciales
//
//   setLoading(loading: boolean): void
//
//   hydrate(): Promise<void>
//     - Lee token de SecureStore
//     - Si existe, llama GET /auth/me
//     - Si válido: popula user y marca isAuthenticated = true
//     - Si inválido: limpia todo
//
// NOTA: persist de zustand NO se usa aquí porque SecureStore
// maneja la persistencia del token de forma segura.
```

### `mobile/src/utils/token.ts` — SecureStore Wrappers

```typescript
// Wrappers tipados sobre expo-secure-store.
// Todas las operaciones son async.
//
// export const TOKEN_KEY = 'logix_ai_jwt'
//
// export async function getToken(): Promise<string | null>
// export async function setToken(token: string): Promise<void>
// export async function clearToken(): Promise<void>
//
// Si SecureStore falla (dispositivo sin biometría configurada en algunos casos):
// - Loguear el error
// - Nunca fallar silenciosamente
// - Propagar el error para que el caller decida
```

### `mobile/src/types/auth.types.ts` — TypeScript Types

```typescript
export type UserRole = 'ADMIN' | 'SUPERVISOR' | 'OPERATOR' | 'DRIVER' | 'CLIENT' | 'VIEWER'

export interface User {
  id: string
  email: string
  full_name: string
  role: UserRole
  is_active: boolean
}

export interface LoginRequest {
  email: string
  password: string
}

export interface LoginResponse {
  access_token: string
  token_type: 'bearer'
  user: User
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean
}
```

### `mobile/src/schemas/auth.schemas.ts` — Zod Validations

```typescript
import { z } from 'zod'

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, 'El email es requerido')
    .email('Ingresa un email válido'),
  password: z
    .string()
    .min(1, 'La contraseña es requerida')
    .min(6, 'La contraseña debe tener al menos 6 caracteres'),
})

export type LoginFormValues = z.infer<typeof loginSchema>
```

---

## Configuración de proyecto

### `package.json` — Dependencias exactas

```json
{
  "name": "logix-ai-mobile",
  "version": "1.0.0",
  "main": "expo-router/entry",
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "build:android": "eas build --platform android",
    "build:ios": "eas build --platform ios",
    "type-check": "tsc --noEmit",
    "lint": "eslint . --ext .ts,.tsx"
  },
  "dependencies": {
    "expo": "~52.0.0",
    "expo-router": "^4.0.0",
    "expo-status-bar": "~2.0.0",
    "expo-secure-store": "~14.0.0",
    "expo-splash-screen": "~0.29.0",
    "react": "18.3.1",
    "react-native": "0.76.5",
    "nativewind": "^4.1.0",
    "tailwindcss": "^3.4.0",
    "zustand": "^4.5.0",
    "@tanstack/react-query": "^5.59.0",
    "axios": "^1.7.0",
    "react-hook-form": "^7.54.0",
    "@hookform/resolvers": "^3.9.0",
    "zod": "^3.23.0",
    "@react-native-async-storage/async-storage": "^2.1.0"
  },
  "devDependencies": {
    "@babel/core": "^7.25.0",
    "@types/react": "~18.3.0",
    "typescript": "^5.3.0"
  }
}
```

### `app.json` — Configuración Expo

```json
{
  "expo": {
    "name": "Logix AI",
    "slug": "logix-ai-mobile",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "scheme": "logixai",
    "userInterfaceStyle": "light",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "ios": {
      "supportsTablet": false,
      "bundleIdentifier": "com.logixai.mobile",
      "infoPlist": {
        "NSCameraUsageDescription": "Logix AI necesita acceso a la cámara para capturar evidencia fotográfica en los reportes.",
        "NSLocationWhenInUseUsageDescription": "Logix AI necesita tu ubicación para registrarla automáticamente en los reportes de campo.",
        "NSLocationAlwaysAndWhenInUseUsageDescription": "Logix AI necesita tu ubicación para registrarla en reportes de campo."
      }
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.logixai.mobile",
      "permissions": [
        "CAMERA",
        "ACCESS_FINE_LOCATION",
        "ACCESS_COARSE_LOCATION"
      ]
    },
    "plugins": [
      "expo-router",
      "expo-secure-store",
      [
        "expo-camera",
        {
          "cameraPermission": "Logix AI necesita acceso a la cámara para capturar evidencia fotográfica."
        }
      ],
      [
        "expo-location",
        {
          "locationAlwaysAndWhenInUsePermission": "Logix AI registra tu ubicación en los reportes de campo."
        }
      ]
    ],
    "experiments": {
      "typedRoutes": true
    }
  }
}
```

> **Nota:** Los permisos de cámara y GPS se declaran aquí para tenerlos listos en Fase 2.
> No se implementan en Fase 1 pero la declaración debe existir desde el inicio para evitar re-builds.

### `eas.json` — EAS Build Config

```json
{
  "cli": {
    "version": ">= 12.0.0"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "env": {
        "EXPO_PUBLIC_API_URL": "http://localhost:8000"
      }
    },
    "preview": {
      "distribution": "internal",
      "env": {
        "EXPO_PUBLIC_API_URL": "https://staging-api.logixai.com"
      }
    },
    "production": {
      "env": {
        "EXPO_PUBLIC_API_URL": "https://api.logixai.com"
      }
    }
  },
  "submit": {
    "production": {}
  }
}
```

### `tailwind.config.js` — NativeWind Config

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/**/*.{js,jsx,ts,tsx}',
    './src/**/*.{js,jsx,ts,tsx}',
  ],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        primary: {
          50:  '#f0f7ff',
          100: '#e0effe',
          500: '#2563eb',
          600: '#1d4ed8',
          700: '#1e40af',
        },
        driver: {
          500: '#0891b2',
          600: '#0e7490',
        },
        operator: {
          500: '#7c3aed',
          600: '#6d28d9',
        },
        success: '#16a34a',
        warning: '#d97706',
        danger:  '#dc2626',
      },
    },
  },
  plugins: [],
}
```

### `babel.config.js`

```javascript
module.exports = function (api) {
  api.cache(true)
  return {
    presets: [
      ['babel-preset-expo', { jsxImportSource: 'nativewind' }],
      'nativewind/babel',
    ],
  }
}
```

### `tsconfig.json`

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": [
    "**/*.ts",
    "**/*.tsx",
    ".expo/types/**/*.d.ts",
    "expo-env.d.ts"
  ]
}
```

### `.env.example`

```bash
# Logix AI Mobile — Variables de entorno
# Copiar a .env y completar con valores reales
# NUNCA commitear .env al repositorio

# URL base del backend FastAPI
# Desarrollo local: http://localhost:8000
# Staging: https://staging-api.logixai.com
# Producción: https://api.logixai.com
EXPO_PUBLIC_API_URL=http://localhost:8000
```

---

## Auth Flow completo — diagrama de estados

```text
┌─────────────────────────────────────────────────────────────┐
│                        APP START                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
              store.hydrate() ejecuta:
              - Lee SecureStore → ¿token?
                           │
               ┌───────────┴───────────┐
               │ NO                    │ SÍ
               ▼                       ▼
        navigate(/(auth)/login)   GET /auth/me
                                       │
                          ┌────────────┴────────────┐
                          │ 200 OK                  │ 401 / Error
                          ▼                         ▼
                 populate user in store        clearToken()
                 navigate(/(app)/)             navigate(/(auth)/login)
                           │
              ┌────────────┴────────────┐
              │ role === DRIVER         │ role === OPERATOR
              ▼                         ▼
    Tabs: Inicio, Reportes, Perfil    Tabs: Inicio, Reportes, Clientes, Perfil


FLUJO LOGIN:
User ingresa email + password
     │
     ▼
Zod validation
     │
  ┌──┴──┐
  │FAIL │ → Mostrar errores inline bajo cada campo
  └─────┘
     │ PASS
     ▼
POST /api/v1/auth/login
     │
  ┌──┴──┐
  │401  │ → Banner: "Email o contraseña incorrectos"
  │Net  │ → Banner: "Sin conexión. Verifica tu internet."
  └─────┘
     │ 200
     ▼
setToken(access_token) en SecureStore
store.login(token, user) en Zustand
navigate(/(app)/)


FLUJO LOGOUT:
User presiona "Cerrar sesión"
     │
     ▼
clearToken() de SecureStore
store.logout() en Zustand
navigate(/(auth)/login)


FLUJO 401 EN CUALQUIER REQUEST:
Axios interceptor detecta 401
     │
     ▼
clearToken()
store.logout()
navigate(/(auth)/login)
// Esto cubre tokens expirados sin necesidad de refresh en Fase 1
```

---

## Seguridad — reglas no negociables

El Builder debe verificar cada punto antes de marcar la fase como completa:

- [ ] JWT almacenado EXCLUSIVAMENTE en `expo-secure-store` — nunca en AsyncStorage, nunca en memoria como variable global no protegida, nunca en logs
- [ ] `EXPO_PUBLIC_API_URL` viene de variable de entorno — nunca hardcodeada
- [ ] `.env` en `.gitignore` — verificar antes del primer commit
- [ ] Ningún `console.log` imprime tokens, passwords o datos de usuario
- [ ] El interceptor Axios no imprime el header Authorization en logs de desarrollo
- [ ] `tsconfig.json` con `"strict": true`

---

## Observabilidad — Fase 1

Observabilidad básica que debe existir desde el inicio:

```typescript
// En src/utils/logger.ts
// Logger mínimo que diferencia ambientes

const isDev = __DEV__

export const logger = {
  info: (msg: string, data?: unknown) => {
    if (isDev) console.info(`[INFO] ${msg}`, data ?? '')
  },
  warn: (msg: string, data?: unknown) => {
    if (isDev) console.warn(`[WARN] ${msg}`, data ?? '')
  },
  error: (msg: string, err?: unknown) => {
    // En producción: aquí iría Sentry / Datadog
    console.error(`[ERROR] ${msg}`, err ?? '')
  },
}
```

Puntos donde se debe loguear (sin datos sensibles):

- App start + resultado de hydrate (authenticated: true/false)
- Login attempt + resultado (success / error code) — nunca el password
- Logout
- 401 interceptado
- Error de red

---

## Criterios de aceptación — Fase 1

La fase está completa ÚNICAMENTE cuando todos estos criterios son verificables:

### Funcionales

- [ ] El proyecto levanta con `npx expo start` sin errores
- [ ] En un simulador iOS y en un simulador/dispositivo Android
- [ ] La pantalla de login se muestra al abrir la app sin sesión activa
- [ ] El formulario valida email (formato) y password (mínimo 6 chars) antes de enviar
- [ ] Los errores de validación aparecen inline bajo cada campo
- [ ] Con credenciales inválidas, aparece mensaje de error claro (no el stack trace)
- [ ] Con credenciales válidas, el usuario navega a Home
- [ ] Home muestra nombre completo y rol del usuario autenticado
- [ ] Las tabs son distintas para DRIVER y para OPERATOR
- [ ] Logout limpia la sesión y regresa a login
- [ ] Al reiniciar la app con sesión activa, no pide login nuevamente
- [ ] Al reiniciar la app con token expirado, redirige a login

### Técnicos

- [ ] TypeScript sin errores (`npx tsc --noEmit` pasa limpio)
- [ ] JWT en SecureStore — verificable inspeccionando el código, nunca en AsyncStorage
- [ ] `.env` ignorado por git — `.env.example` commiteado con valores placeholder
- [ ] Axios interceptor maneja 401 → logout → redirect sin crash
- [ ] Estructura de carpetas exactamente como especificado en este handoff
- [ ] NativeWind funcionando — clases Tailwind renderizan correctamente en iOS y Android
- [ ] Sin secretos en código fuente — API URL viene de `EXPO_PUBLIC_API_URL`
- [ ] `app.json` con permisos de cámara, GPS declarados (para Fase 2)

### Documentación

- [ ] `mobile/README.md` con instrucciones de setup claras (requisitos, comandos, variables de entorno)
- [ ] `.env.example` documentado con comentarios por variable
- [ ] `planning/STATE.md` actualizado reflejando Fase 1 completada
- [ ] `planning/DECISIONS.md` con decisiones tomadas durante la implementación

---

## Validación — cómo probar esta fase

```bash
# 1. Instalar dependencias
cd mobile && npm install

# 2. Copiar variables de entorno
cp .env.example .env
# Editar .env con la URL real del backend

# 3. Levantar app
npx expo start

# 4. Probar en simulador iOS
npx expo start --ios

# 5. Probar en simulador Android
npx expo start --android

# 6. Verificar TypeScript
npx tsc --noEmit

# 7. Prueba manual — checklist
# a) Abrir app → pantalla login
# b) Enviar form vacío → errores inline
# c) Email inválido → error inline
# d) Password corta → error inline
# e) Credenciales incorrectas → mensaje de error
# f) Credenciales correctas → Home con nombre y rol
# g) Tabs correctas según rol (DRIVER vs OPERATOR)
# h) Cerrar sesión → regresa a login
# i) Reabrir app → auto-login (si token válido)
# j) Inspeccionar código → JWT no en AsyncStorage ni en logs
```

---

## Riesgos conocidos — Fase 1

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Backend no disponible durante desarrollo mobile | Alto | Medio | Crear mock de respuestas en `src/api/mocks/` para dev local |
| NativeWind v4 config rota en Expo SDK 52 | Medio | Alto | Verificar en docs oficiales NativeWind antes de arrancar; usar versión exacta del package.json |
| SecureStore no disponible en simulador iOS sin biometría | Bajo | Bajo | Funciona sin biometría; solo requiere passcode del simulador |
| Permisos de cámara/GPS rechazados en iOS | N/A Fase 1 | N/A | Se maneja en Fase 2 |
| Token expirado sin refresh → UX degradada | Bajo | Bajo | Aceptable en Fase 1; refresh token es Fase 2+ |

---

## Mock del backend — si el API no está lista

Si el backend FastAPI aún no tiene el endpoint `/api/v1/auth/login`,
el Builder debe crear un mock local para no bloquear el desarrollo mobile.

```typescript
// src/api/mocks/auth.mock.ts
// SOLO para desarrollo — eliminar antes de conectar al backend real

export const MOCK_USERS = {
  driver: {
    access_token: 'mock_jwt_driver_token',
    token_type: 'bearer' as const,
    user: {
      id: 'mock-driver-id',
      email: 'driver@logixai.com',
      full_name: 'Carlos Repartidor',
      role: 'DRIVER' as const,
      is_active: true,
    },
  },
  operator: {
    access_token: 'mock_jwt_operator_token',
    token_type: 'bearer' as const,
    user: {
      id: 'mock-operator-id',
      email: 'operator@logixai.com',
      full_name: 'María Vendedora',
      role: 'OPERATOR' as const,
      is_active: true,
    },
  },
}

// Credenciales mock para testing:
// driver@logixai.com / driver123 → responde como DRIVER
// operator@logixai.com / operator123 → responde como OPERATOR
// cualquier otro → responde 401
```

El Builder debe documentar en `planning/QUESTIONS.md` si el backend
necesita sincronización de contratos de API con el equipo backend.

---

## Commit sugerido al completar la fase

```bash
git add .
git commit -m "feat(mobile): fase 1 — fundación expo + auth flow completo

- Scaffolding React Native + Expo SDK 52 + NativeWind v4
- Expo Router con stacks (auth) y (app)
- Login screen con validación Zod + React Hook Form
- JWT en SecureStore — nunca AsyncStorage
- Zustand auth store con hydrate al arranque
- Axios client con interceptor 401 → logout
- Tab navigation diferenciada por rol DRIVER/OPERATOR
- Home screen con datos de sesión
- Variables de entorno documentadas
- TypeScript strict mode sin errores
- README con instrucciones de setup

Fase 1 completada. Siguiente: módulo de reportes (Fase 2)."
```

---

## Qué sigue — Fase 2

Una vez que la Fase 1 pase todos los criterios de aceptación,
el Architect preparará el handoff de Fase 2: Módulo de Reportes Core.

La Fase 2 incluirá:
- Formularios dinámicos por tipo de reporte (DRIVER: entrega, incidencia / OPERATOR: visita, venta)
- Captura de foto con expo-camera y compresión automática
- GPS capturado en el momento del reporte
- Lista de reportes propios del usuario
- Estados de reporte: borrador → enviado → aprobado
- Endpoints del backend: POST /api/v1/reports, GET /api/v1/reports

La Fase 2 NO comienza hasta que Fase 1 tenga todos sus criterios cumplidos.

---

*Generado por Axon-AI Architect Layer — Logix-AI Mobile Sprint 001*
*Fecha: 2026-05-17*
*Metodología: Architect / Builder — el handoff es una carpeta, no una conversación*
