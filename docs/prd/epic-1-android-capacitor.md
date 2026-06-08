# Epic 1: Android Nativo — Capacitor

## Metadata

| Campo | Valor |
|-------|-------|
| Epic ID | 1 |
| Status | In Progress |
| Criado em | 2026-06-08 |
| Criado por | River (@sm) |
| Fonte | Avaliação arquitetural — @architect (Aria) |
| Decisão técnica | Capacitor (wrapping zero-rewrite) |

---

## Objetivo

Empacotar o PWA Etograma em um app Android nativo instalável via APK (sideloading), sem publicação na Play Store, usando Capacitor como bridge nativa.

## Contexto Arquitetural

**Decisão documentada por @architect:**
- App atual: single HTML file (`etograma.html`, 2.524 linhas), IndexedDB, offline-first, sem backend
- Abordagem: Capacitor wrapping — zero reescrita de código
- Target inicial: Android (iOS em epic futuro)
- Distribuição: APK sideloading / ADB (sem loja)

**APIs nativas em uso:**
- `navigator.vibrate` — funciona em Capacitor WebView
- `navigator.mediaDevices.getUserMedia` — requer permissão `RECORD_AUDIO`
- `navigator.storage.persist()` — suportado
- `indexedDB` — suportado nativamente

**Gap crítico identificado:** Exportação de CSV via `blob:` URL não funciona no contexto nativo — requer `@capacitor/filesystem` + `@capacitor/share`.

---

## Acceptance Criteria do Epic

1. O Etograma pode ser instalado em um dispositivo Android via APK sem precisar da Play Store
2. O app funciona 100% offline no Android após instalação
3. IndexedDB persiste dados entre sessões normalmente
4. Vibração (`navigator.vibrate`) funciona no dispositivo
5. Exportação de CSV funciona no Android (via share nativo)
6. Permissão de microfone é solicitada corretamente (se usado)
7. O APK pode ser gerado pelo comando `npx cap build android`

---

## Stories

| Story | Título | Status |
|-------|--------|--------|
| 1.1 | Scaffolding Capacitor | Draft |
| 1.2 | Adaptar exportação CSV para Android | Draft |
| 1.3 | Configurar permissões e recursos nativos Android | Draft |
| 1.4 | Build APK e validação em dispositivo real | InProgress |
| 1.5 | Backup CSV automático integrado ao ciclo de vida do projeto | Draft |

---

## Dependências e Pré-requisitos

- Node.js 18+ instalado
- Android Studio instalado (para build final)
- JDK 17+ configurado
- ADB disponível no PATH (para instalação via cabo)

---

## Out of Scope

- Publicação na Google Play Store
- Implementação iOS (Epic futuro)
- Push notifications
- Integrações de backend / SaaS (Epic 2+ do PRD)
