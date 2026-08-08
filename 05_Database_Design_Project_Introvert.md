# Project Introvert — Database Design

**Document 5 of 10 — Full Schema Reference**
**Version:** 1.0
**Depends on:** Document 2 (Technical Architecture, Section 3 — entity summary)
**Engine:** PostgreSQL 15+ (with PostGIS and pgvector extensions)

---

## 0. Conventions

- All primary keys: `UUID` (generated via `gen_random_uuid()`), not auto-increment integers — avoids leaking record counts/order and simplifies future multi-region/sharded writes.
- All tables include `created_at TIMESTAMPTZ NOT NULL DEFAULT now()`; mutable tables also include `updated_at TIMESTAMPTZ`.
- Soft deletes (`deleted_at TIMESTAMPTZ NULL`) used for user-facing content (posts, listings, communities) so deletion is recoverable and auditable; hard deletes reserved for legally-mandated erasure requests.
- Foreign keys use `ON DELETE RESTRICT` by default; `CASCADE` only where explicitly noted, to avoid accidental data loss from an unrelated deletion.
- Normalized to 3NF for transactional tables; read-optimized materialized views layered on top for feeds/discovery (Section 10).

---

## 1. Identity Domain

### `users`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| email | CITEXT UNIQUE | nullable if phone-only signup |
| phone | VARCHAR(20) UNIQUE | nullable if email-only signup |
| password_hash | TEXT | Argon2id; null for OAuth-only accounts |
| mfa_secret_encrypted | TEXT | null if MFA not enabled |
| mfa_enabled | BOOLEAN DEFAULT false | |
| status | ENUM(active, suspended, deactivated) | |
| verified_at | TIMESTAMPTZ | null until email/phone verified |
| created_at / updated_at | TIMESTAMPTZ | |

### `profiles`
| Column | Type | Notes |
|---|---|---|
| user_id | UUID PK, FK → users.id | 1:1 |
| display_name | VARCHAR(80) | |
| bio | TEXT | |
| avatar_url | TEXT | |
| profile_types | TEXT[] | subset of {personal, professional, business} |
| interests | TEXT[] | free-tag list, also embedded (Section 9) |
| skills | TEXT[] | |
| language_pref | VARCHAR(10) | ISO locale code |

### `locations`
| Column | Type | Notes |
|---|---|---|
| user_id | UUID PK, FK → users.id | 1:1, separate table for privacy-scoped access control |
| geo_point | GEOGRAPHY(Point, 4326) | PostGIS type |
| precision_level | ENUM(exact, area, off) | governs fuzzing applied before storage, per Doc 3 §10.4 |
| updated_at | TIMESTAMPTZ | |

### `sessions`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | FK → users.id | |
| refresh_token_hash | TEXT | never store raw token |
| device_info | JSONB | |
| created_at / last_used_at / revoked_at | TIMESTAMPTZ | |

---

## 2. Community Domain

### `communities`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| owner_id | FK → users.id | ON DELETE RESTRICT (ownership must be transferred, not orphaned) |
| name | VARCHAR(100) | |
| description | TEXT | |
| type | ENUM(interest, professional, business, civic) | |
| join_policy | ENUM(open, request, invite_only) | |
| geo_center | GEOGRAPHY(Point, 4326) | nullable for non-location-bound communities |
| geo_radius_m | INTEGER | nullable |
| deleted_at | TIMESTAMPTZ NULL | soft delete |
| created_at / updated_at | TIMESTAMPTZ | |

### `community_members`
| Column | Type | Notes |
|---|---|---|
| community_id | FK → communities.id, ON DELETE CASCADE | composite PK with user_id |
| user_id | FK → users.id | |
| role | ENUM(member, moderator, owner) | |
| joined_at | TIMESTAMPTZ | |

### `community_posts`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| community_id | FK → communities.id, ON DELETE CASCADE | |
| author_id | FK → users.id | |
| body | TEXT | |
| media_urls | TEXT[] | |
| deleted_at | TIMESTAMPTZ NULL | |
| created_at | TIMESTAMPTZ | |

---

## 3. Messaging Domain

### `conversations`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| type | ENUM(dm, group, community) | |
| community_id | FK → communities.id NULL | set only if type = community |
| created_at | TIMESTAMPTZ | |

### `conversation_participants`
| Column | Type | Notes |
|---|---|---|
| conversation_id | FK → conversations.id, ON DELETE CASCADE | composite PK with user_id |
| user_id | FK → users.id | |
| joined_at / left_at | TIMESTAMPTZ | |

### `messages`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| conversation_id | FK → conversations.id, ON DELETE CASCADE | |
| sender_id | FK → users.id | |
| body_encrypted | BYTEA | app-layer encrypted (Doc 2 §10.1); key ref stored separately in KMS, not in this row |
| sent_at | TIMESTAMPTZ | |
| delivered_at / read_at | TIMESTAMPTZ NULL | |

---

## 4. Events Domain

### `events`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| community_id | FK → communities.id NULL | nullable — events can be standalone |
| creator_id | FK → users.id | |
| title | VARCHAR(150) | |
| description | TEXT | |
| geo_point | GEOGRAPHY(Point, 4326) | |
| start_at / end_at | TIMESTAMPTZ | |
| capacity | INTEGER NULL | |
| deleted_at | TIMESTAMPTZ NULL | |

### `event_rsvps`
| Column | Type | Notes |
|---|---|---|
| event_id | FK → events.id, ON DELETE CASCADE | composite PK with user_id |
| user_id | FK → users.id | |
| status | ENUM(going, interested, declined) | |
| responded_at | TIMESTAMPTZ | |

---

## 5. Marketplace Domain

### `listings`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| creator_id | FK → users.id | |
| type | ENUM(gig, service, offer) | |
| title | VARCHAR(150) | |
| description | TEXT | |
| price_amount | NUMERIC(12,2) NULL | |
| price_currency | CHAR(3) DEFAULT 'INR' | |
| geo_point | GEOGRAPHY(Point, 4326) NULL | |
| status | ENUM(open, in_progress, completed, cancelled) | |
| deleted_at | TIMESTAMPTZ NULL | |
| created_at / updated_at | TIMESTAMPTZ | |

### `transactions`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| listing_id | FK → listings.id | |
| buyer_id / seller_id | FK → users.id | |
| amount | NUMERIC(12,2) | |
| idempotency_key | VARCHAR(64) UNIQUE | prevents double-processing (Doc 2 §5) |
| status | ENUM(pending, buyer_confirmed, seller_confirmed, completed, disputed, refunded) | requires both confirmations before `completed` |
| payment_ref | VARCHAR(100) NULL | UPI transaction reference |
| created_at / completed_at | TIMESTAMPTZ | |

### `reviews`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| context_type | ENUM(gig, event, community) | |
| context_id | UUID | polymorphic reference, resolved by context_type |
| subject_id | FK → users.id | who is being reviewed |
| reviewer_id | FK → users.id | |
| rating | SMALLINT CHECK (rating BETWEEN 1 AND 5) | |
| body | TEXT NULL | |
| created_at | TIMESTAMPTZ | |

---

## 6. Business Domain

### `businesses`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| owner_user_id | FK → users.id | |
| legal_name | VARCHAR(150) | |
| verification_status | ENUM(unverified, pending, verified, rejected) | |
| verification_method | ENUM(manual, digilocker) NULL | |
| verification_docs_ref | TEXT NULL | pointer to encrypted document storage, not the document itself |
| created_at / updated_at | TIMESTAMPTZ | |

### `offers`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| business_id | FK → businesses.id, ON DELETE CASCADE | |
| title | VARCHAR(150) | |
| description | TEXT | |
| starts_at / ends_at | TIMESTAMPTZ | |
| redemption_count | INTEGER DEFAULT 0 | |

---

## 7. Trust & Safety Domain

### `reports`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| reporter_id | FK → users.id | |
| target_type | ENUM(user, post, message, listing, community, event) | |
| target_id | UUID | polymorphic reference |
| reason | ENUM(spam, harassment, fraud, inappropriate, other) | |
| details | TEXT NULL | |
| status | ENUM(open, in_review, resolved, dismissed) | |
| reviewed_by | FK → users.id NULL | admin/moderator user |
| reviewed_at | TIMESTAMPTZ NULL | |
| created_at | TIMESTAMPTZ | |

### `audit_log`
| Column | Type | Notes |
|---|---|---|
| id | BIGSERIAL PK | append-only, sequential fine here (not user-facing) |
| actor_id | FK → users.id NULL | null for system-initiated actions |
| action | VARCHAR(100) | e.g., "role.changed", "account.suspended" |
| target_type / target_id | VARCHAR(50) / UUID | |
| metadata | JSONB | |
| created_at | TIMESTAMPTZ | immutable, no updates permitted |

---

## 8. Notification Domain

### `notification_preferences`
| Column | Type | Notes |
|---|---|---|
| user_id | FK → users.id | composite PK with channel |
| channel | ENUM(push, email, digest) | |
| category | ENUM(messages, community, events, marketplace, ai_suggestions) | |
| enabled | BOOLEAN DEFAULT true | |

### `notifications`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| user_id | FK → users.id | |
| type | VARCHAR(50) | |
| payload | JSONB | |
| read_at | TIMESTAMPTZ NULL | |
| created_at | TIMESTAMPTZ | |

---

## 9. AI / Embeddings Domain

### `embeddings`
| Column | Type | Notes |
|---|---|---|
| id | UUID PK | |
| entity_type | ENUM(user, community, listing, event) | |
| entity_id | UUID | |
| vector | VECTOR(1536) | pgvector type; dimension matches chosen embedding model |
| updated_at | TIMESTAMPTZ | recalculated on relevant entity change (event-driven, Doc 2 §1) |

Indexed via an IVFFlat or HNSW index (pgvector) for approximate nearest-neighbor search at scale.

---

## 10. Indexing & Read-Model Strategy

- **Spatial indexes** (GiST, via PostGIS) on every `geo_point`/`geo_center` column — required for performant "nearby" queries.
- **Composite indexes** on high-traffic filters, e.g., `(community_id, created_at DESC)` on `community_posts` for feed pagination.
- **Materialized views** for expensive aggregate reads (e.g., `community_activity_summary` feeding discovery ranking) refreshed on a schedule or via event trigger — keeps hot read paths off the normalized transactional tables.
- **Partial indexes** on soft-deleted tables (e.g., `WHERE deleted_at IS NULL`) so common queries skip deleted rows without a full scan.

---

## 11. Data Retention & Deletion Mapping

Directly supports Document 2 §10.5 (privacy by design):

| Data | On account deletion |
|---|---|
| profiles, locations, notification_preferences | hard deleted |
| messages sent by user | anonymized (sender replaced with "deleted user" placeholder), not deleted — preserves conversation integrity for other participants |
| transactions | retained per financial record-keeping requirements, with personal identifiers minimized where legally permissible |
| audit_log entries referencing the user | retained (compliance/security requirement), user reference kept as an opaque ID only |

---

*End of Document 5. Next: Document 6 — API Documentation (endpoint-level, Swagger-ready).*
