# Project Introvert — Technical Architecture

**Document 2 of 10 — Engineering Blueprint**
**Version:** 1.0
**Depends on:** Document 1 (PRD)
**Governs:** All backend, mobile, AI, and infrastructure implementation

---

## 0. How to Use This Document

This is the binding engineering blueprint. Any AI coding assistant or engineer implementing Project Introvert should treat the module boundaries, data model, and security requirements here as non-negotiable defaults. Deviations (e.g., swapping a database, changing an auth flow) should be a deliberate, documented decision — not a silent implementation choice.

---

## 1. System Architecture Overview

Project Introvert is built as a **modular monolith at launch, decomposable into microservices as scale demands** — this avoids premature distributed-systems complexity while keeping clean module boundaries that map directly onto future services.

```
                          ┌─────────────────────────┐
                          │      Client Apps        │
                          │  (iOS / Android / Web)  │
                          └────────────┬────────────┘
                                       │ HTTPS / WSS
                          ┌────────────▼────────────┐
                          │       API Gateway        │
                          │ (Auth, rate limit, WAF)  │
                          └────────────┬────────────┘
              ┌────────────────────────┼────────────────────────┐
              │                        │                        │
     ┌────────▼────────┐   ┌──────────▼─────────┐   ┌──────────▼─────────┐
     │ Core App Service │   │  Realtime Service   │   │   AI Service       │
     │ (modular monolith)│   │ (chat, presence,   │   │ (matching, mod,    │
     │ Identity/Community│   │  notifications)     │   │  assistant, search)│
     │ Events/Marketplace│   └──────────┬─────────┘   └──────────┬─────────┘
     └────────┬─────────┘              │                        │
              │              ┌─────────▼─────────┐   ┌──────────▼─────────┐
              │              │  Message Broker    │   │ Vector / Search DB │
              │              │  (Kafka/Redis Streams)│ │ (pgvector/Elastic)│
              │              └───────────────────┘   └────────────────────┘
     ┌────────▼─────────────────────────────────────────────────────┐
     │                     Primary Data Layer                       │
     │  PostgreSQL (primary) · Redis (cache/session) · S3 (media)    │
     └────────────────────────────────────────────────────────────────┘
```

### Guiding Principles
- **Modular monolith first.** Clear module boundaries (identity, community, messaging, marketplace, AI) as separate deployable services *later*, not day one.
- **Stateless application layer** — all session state in Redis, not in-process, so instances scale horizontally.
- **Event-driven where it matters** — notifications, recommendation recalculation, and moderation triggers flow through an event bus, not synchronous chains.
- **Security by default, not as an add-on** — see Section 10.

---

## 2. Technology Stack (with Justification)

| Layer | Choice | Why |
|---|---|---|
| Backend language/framework | Node.js (NestJS) or Go | Strong async I/O for realtime workloads; NestJS gives structured modules mapping to this doc; Go if extreme throughput needed |
| Primary database | PostgreSQL | Relational integrity for identity/community/marketplace data; mature, supports JSONB for flexible fields, pgvector for AI embeddings |
| Cache/session | Redis | Sub-millisecond session/lookup; also backs pub/sub for realtime presence |
| Search | Elasticsearch or PostgreSQL full-text + pgvector | Full-text + semantic search over communities, profiles, listings |
| Object storage | S3-compatible (AWS S3 / Cloudflare R2) | Media (images, avatars, attachments) |
| Realtime | WebSockets (Socket.IO) behind a dedicated Realtime Service | Chat, presence, live notifications |
| Message broker | Kafka (or Redis Streams for smaller scale) | Decouples event producers/consumers (e.g., "user joined community" → recommendation recalculation) |
| Mobile | React Native or Flutter | Single codebase for iOS/Android; native modules for GPS/BLE where needed |
| AI/LLM | Anthropic Claude API for assistant + moderation reasoning; embeddings model for matching/search | Managed API avoids owning model infra; embeddings power semantic matching |
| Infra | Kubernetes on AWS/GCP | Standard, portable, supports autoscaling and multi-region later |
| CI/CD | GitHub Actions → container registry → Kubernetes | Standard, auditable pipeline |

---

## 3. Database Schema (Core Entities)

> Full column-level detail lives in Document 5 (Database Design). This section defines the core entity relationships.

**Users** (`id, email, phone, password_hash, mfa_secret, created_at, status, verified_at`)
**Profiles** (`user_id FK, display_name, bio, interests[], skills[], profile_type[personal|professional|business]`)
**Locations** (`user_id FK, geo_point, precision_level[exact|area|off], updated_at`) — stored separately from Profiles for privacy-scoping and easy purge
**Communities** (`id, owner_id FK, name, type, join_policy, geo_center, geo_radius, created_at`)
**Community_Members** (`community_id FK, user_id FK, role[member|moderator|owner], joined_at`)
**Messages** (`id, conversation_id FK, sender_id FK, body_encrypted, sent_at`)
**Conversations** (`id, type[dm|group|community], participant_ids[]`)
**Events** (`id, community_id FK nullable, creator_id FK, title, geo_point, start_at, end_at`)
**Event_RSVPs** (`event_id FK, user_id FK, status`)
**Listings** (`id, creator_id FK, type[gig|service|offer], title, description, price, geo_point, status`)
**Reviews** (`subject_id FK, reviewer_id FK, context[gig|event|community], rating, body`)
**Reports** (`id, reporter_id FK, target_type, target_id, reason, status, reviewed_by, reviewed_at`)
**Businesses** (`id, owner_user_id FK, legal_name, verification_status, verification_docs_ref`)

### Entity Relationship Summary
```
Users 1─1 Profiles
Users 1─1 Locations
Users 1─* Community_Members *─1 Communities
Users 1─* Listings
Users 1─* Reviews (as reviewer and as subject)
Communities 1─* Events
Events 1─* Event_RSVPs
Users 1─* Reports (as reporter); Reports point to any target_type
```

Normalization target: 3NF for transactional tables; denormalized read-models (materialized views) for feed/discovery queries to keep read latency low.

---

## 4. Authentication & Authorization Flow

### 4.1 Authentication
1. Email/phone + password, or OAuth (Google/Apple), creates a `Users` record.
2. Password hashed with **Argon2id** (never bcrypt-only, never plaintext).
3. On login, issue a short-lived **JWT access token** (15 min) + a long-lived **rotating refresh token** stored as an httpOnly, secure, SameSite cookie (web) or secure keychain (mobile).
4. **Multi-factor authentication (MFA)** optional at signup, **required** for business accounts and platform admins.
5. Refresh token rotation: every refresh issues a new refresh token and invalidates the old one; reuse of an invalidated token triggers session-wide revocation (detects token theft).

### 4.2 Authorization
- **Role-Based Access Control (RBAC)** at the platform level (Member, Business, Admin).
- **Scoped RBAC within communities** (Member, Moderator, Owner) — checked per-resource, not globally cached, to avoid stale-permission bugs.
- All authorization checks happen **server-side only**; client-provided role claims are never trusted directly — the server re-verifies against the database (or a short-TTL cache) on every sensitive action.

---

## 5. API Design Principles

- REST for CRUD-style resources; WebSocket channels for realtime (chat, presence, live notifications).
- Every endpoint versioned (`/api/v1/...`).
- Full request/response contracts, error codes, and auth requirements documented in Document 6 (API Documentation), Swagger/OpenAPI-ready.
- Idempotency keys required on all state-mutating marketplace/payment endpoints to prevent double-processing on retry.
- Rate limiting enforced at the API Gateway (see Section 10.4).

---

## 6. Backend Modules (maps to PRD Module Breakdown)

| Module | Responsibility |
|---|---|
| Identity Service | Auth, sessions, MFA, profile CRUD |
| Location Service | Geo-indexing, proximity queries, precision/privacy enforcement |
| Community Service | Community CRUD, membership, roles, feeds |
| Messaging Service | DMs, group chat, community chat, delivery/read receipts |
| Events Service | Event CRUD, RSVPs, reminders |
| Marketplace Service | Listings, transactions, escrow-style completion confirmation |
| Business Service | Verified business profiles, offers, campaigns, analytics |
| AI Service | Matching, recommendations, assistant, moderation triage |
| Notification Service | Push, email, in-app digesting and delivery |
| Trust & Safety Service | Reports, moderation actions, appeals |

Each module owns its own tables and exposes a well-defined internal API — even inside the monolith — so future extraction into a microservice is a deployment change, not a rewrite.

---

## 7. Maps, GPS, and Proximity Discovery

- **Client-side:** request location permission with a clear, granular choice — Exact / Approximate (fuzzed to ~1km) / Off. Default recommendation shown to the user: Approximate.
- **Server-side geo-indexing:** PostgreSQL with PostGIS extension (or a geohash index) for efficient "find nearby" queries — avoid recalculating distance for every row; use spatial indexes.
- **Fuzzing at rest:** if a user selects "Approximate," the server stores a jittered/rounded coordinate, not the true exact one — this is enforced at the Location Service, not just the UI, so a compromised client can't recover precision the server never stored.
- **BLE (optional, Phase 5+):** proximity-based "nearby now" detection for opt-in, in-person contexts (e.g., an event check-in). BLE beacons are strictly opt-in per session, never silently always-on, and never used to build a persistent location trail without explicit, separate consent.

---

## 8. Real-Time Messaging & Notifications

- WebSocket-based Realtime Service, horizontally scaled behind a connection-aware load balancer (sticky sessions via Redis-backed session store).
- Messages persisted first (write-ahead) then fanned out — no message is "only in memory" during delivery.
- Notification Service consumes events from the message broker (e.g., `message.sent`, `event.reminder`, `community.mention`) and applies user notification preferences (push/email/digest/off) before dispatch.
- Delivery guarantees: at-least-once with client-side de-duplication via message IDs.

---

## 9. Recommendation Engine & Search

- **Embeddings-based matching:** user interests/skills, community descriptions, and listings are embedded into a shared vector space (pgvector or a dedicated vector DB) for semantic similarity matching (not just keyword tags).
- **Ranking signals combined:** semantic similarity + geographic proximity + recency + past engagement + (for marketplace) reputation score. Weighted scoring, not a single black-box score — so ranking logic is explainable and tunable.
- **Search:** hybrid full-text (Elasticsearch or Postgres FTS) + vector similarity for "fuzzy intent" queries (e.g., "find me something like a coding meetup" even if no listing uses that exact phrase).
- Full detail in Document 7 (AI Design Document).

---

## 10. Security Architecture

Security is treated as a first-class architectural concern, not a bolt-on. This section is intentionally the most detailed in this document per your request.

### 10.1 Data Protection & Encryption
- **In transit:** TLS 1.3 everywhere — client-to-gateway, and service-to-service inside the cluster (mutual TLS between internal services).
- **At rest:** database-level encryption (AES-256) for the primary datastore and backups; S3 buckets encrypted with SSE-KMS.
- **Sensitive fields:** message bodies stored encrypted at the application layer (not just disk-level), with keys managed by a KMS (AWS KMS / GCP KMS / HashiCorp Vault) — so a raw database dump does not expose readable message content.
- **Secrets management:** no secrets in code or environment files committed to version control; all secrets in Vault/KMS-backed secret stores, injected at runtime.

### 10.2 Authentication Hardening
- Argon2id password hashing with per-user salt.
- MFA (TOTP or WebAuthn) required for business and admin roles, optional but encouraged for all users.
- Refresh-token rotation with theft detection (Section 4.1).
- Device/session management screen so users can view and revoke active sessions.

### 10.3 Authorization & Least Privilege
- Server-side RBAC re-verification on every sensitive action (never trust client-supplied role claims).
- Internal services authenticate to each other via short-lived service tokens (mTLS + SPIFFE/SPIRE identity, or cloud-native workload identity) — no shared static API keys between internal services.
- Database access follows least privilege: each service has its own DB role scoped only to the tables it owns.

### 10.4 API & Network Security
- Web Application Firewall (WAF) at the API Gateway layer to filter common attack patterns (injection, malformed requests).
- Rate limiting per-user and per-IP, with stricter limits on auth endpoints (login, password reset, OTP) to blunt brute-force and credential-stuffing attempts.
- Input validation and output encoding enforced at the framework level (parameterized queries only — no raw string-concatenated SQL, ever) to prevent injection classes of vulnerabilities.
- CORS strictly scoped to known client origins.

### 10.5 Privacy by Design
- **Location privacy:** granular precision controls (Section 7), with exact coordinates never sent to the client for other users regardless of the viewing user's role.
- **Data minimization:** collect only what a feature strictly requires; avoid "just in case" data collection.
- **Right to deletion / export:** account deletion cascades to personal data across all modules (subject to legal retention requirements for financial/marketplace records); data export available as machine-readable JSON.
- **GDPR-style consent:** explicit, granular consent for location, marketing communications, and AI-personalization use of data — each independently revocable.

### 10.6 Trust & Safety / Content Security
- All user-generated content passes through automated moderation triage (AI-assisted spam/abuse detection) before wide distribution in public communities; flagged content routed to human review — no fully automated permanent account bans without a human-reviewable appeal path.
- Reporting pipeline (`Reports` table) with SLA-tracked review queues.
- Media uploads scanned for malware and, for images, run through content-safety classification before being served publicly.

### 10.7 Application Security Practices
- Dependency scanning (e.g., Dependabot/Snyk) integrated into CI — no build promotion with known critical CVEs unresolved.
- Static analysis (SAST) on every pull request.
- Regular third-party penetration testing before major public launches and at least annually thereafter.
- Security logging: authentication events, permission changes, and admin actions are immutably logged (append-only audit log) and retained per compliance requirements.

### 10.8 Incident Response
- Defined severity tiers and on-call escalation path.
- Runbook for credential leaks, data breach notification (aligned to applicable regional breach-notification laws), and account compromise response (forced logout, password reset, session revocation).

### 10.9 Compliance Posture
- Architecture designed to support GDPR-style principles (consent, minimization, right to erasure) from day one, even before formal regional compliance certification, so expansion into regulated markets doesn't require a retrofit.
- Full compliance matrix (data residency, region-specific requirements) tracked in Document 8 (Security Document) alongside legal review.

---

## 11. Cloud Architecture & Scalability Strategy

- Multi-AZ deployment within a single region at launch; multi-region expansion planned for Phase 6.
- Horizontal autoscaling for stateless application and realtime services based on CPU/connection-count metrics.
- Read replicas for PostgreSQL to offload discovery/search-heavy read traffic from the primary write path.
- CDN (Cloudflare/CloudFront) in front of all static assets and media.
- Database connection pooling (PgBouncer) to avoid connection exhaustion under scale.

---

## 12. Backup & Disaster Recovery

- Automated daily full backups + continuous WAL archiving for point-in-time recovery (PostgreSQL).
- Cross-region backup replication.
- Documented RPO (Recovery Point Objective) target: ≤15 minutes; RTO (Recovery Time Objective) target: ≤1 hour for core services.
- Quarterly restore drills to validate backups are actually restorable, not just present.

---

## 13. Analytics, Logging, and Monitoring

- **Analytics:** event-based tracking (product analytics pipeline, e.g., Amplitude/Mixpanel or a self-hosted equivalent) feeding the KPIs defined in the PRD — decoupled from operational logs.
- **Logging:** structured (JSON) logs shipped to a central log store (e.g., ELK/OpenSearch or a managed equivalent); PII redacted or tokenized in logs by default.
- **Monitoring:** metrics (Prometheus/Grafana) for service health, latency, error rates; alerting thresholds tied to on-call escalation.
- **Tracing:** distributed tracing (OpenTelemetry) across service boundaries to debug cross-module latency issues.

---

## 14. CI/CD Pipeline

```
PR opened → lint + unit tests + SAST scan → merge to main
   → build container image → dependency/vuln scan
   → deploy to staging → integration tests
   → manual approval gate (production)
   → progressive rollout (canary %) to production
   → automated rollback on error-rate spike
```

- Infrastructure as Code (Terraform) for all cloud resources — no manual console changes to production infrastructure.
- Feature flags for risky or partial rollouts, decoupling deploy from release.

---

*End of Document 2. Next: Document 3 — UI/UX Design System, or Document 5 — Database Design in full column-level detail, per your preference.*
