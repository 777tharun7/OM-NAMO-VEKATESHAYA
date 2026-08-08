# Project Introvert — UI/UX Design System

**Document 3 of 10 — The Design Bible**
**Version:** 1.0
**Depends on:** Document 1 (PRD), Document 2 (Technical Architecture)

---

## 0. Design Thesis

Project Introvert is not a feed you scroll — it's a **map of real, nearby life**. The design language should feel less like a social network and more like looking at a living, rooted network: things close to you are vivid and near; things further away recede. The signature visual idea running through this whole system is the **banyan network** — India's banyan tree spreads by dropping new roots from its branches, each one capable of becoming its own trunk while staying connected to the whole. That's the platform's actual structure: every community, business, or person is a node that can grow its own roots while staying part of one connected canopy. This is not decoration — it directly informs how we visualize communities, connections, and the "nearby" map.

We deliberately avoid the three most common AI-generated design defaults (cream-and-terracotta warmth, near-black-with-neon-accent, hairline-rule broadsheet). Instead, the palette and type system below are chosen specifically for this product and this market.

---

## 1. Brand

### 1.1 Logo System
- **Mark:** an abstract node-and-root glyph — a small solid circle (the user/business/community "you are here") with two to four curved root-lines branching downward-outward, echoing a banyan root drop. At small sizes it reads as a simple connected dot; at large sizes the root detail becomes visible.
- **Wordmark:** set in the display typeface (Section 2), lowercase, tightly tracked — deliberately quiet so the mark carries the personality.
- **Lockup rule:** mark never stretches or rotates; minimum clear space equal to the mark's own width on all sides.

### 1.2 Design Philosophy
1. **Proximity is the organizing principle** — not popularity, not recency-only feeds.
2. **Calm over noise** — no infinite-scroll dark patterns, no manufactured urgency badges.
3. **Legible at every scale** — this product must work as well in low-bandwidth conditions and on budget Android devices as on flagship phones, since local, everyday use across India is the core use case, not a stretch case.
4. **One visual idea, disciplined execution** — the root/network motif appears in the logo, in how connections are drawn on the map, and in how community hierarchies are visualized — nowhere else. We do not decorate with it.

---

## 2. Typography

| Role | Typeface | Why |
|---|---|---|
| Display (headlines, wordmark) | **Fraunces** (variable, soft-serif) | Has warmth and character without falling into generic "AI-cream-serif" territory when paired with a cool palette instead of cream/terracotta |
| Body / UI | **IBM Plex Sans** + **IBM Plex Sans Devanagari** | Genuinely built for multi-script Indian use — real practical reason to choose it over generic Inter/Helvetica, since the same family renders Latin and Devanagari with matched metrics |
| Utility / data / timestamps | **IBM Plex Mono** | Numeric alignment for distances ("1.2 km"), prices, timestamps |

**Type scale (base 16px, ratio 1.25):**
`12 / 14 / 16 / 20 / 25 / 31 / 39 / 49 / 61px`

**Rules:**
- Display face used only for H1/H2 and the wordmark — never for body copy or buttons.
- Line length capped at ~65 characters for body text.
- Minimum body size 14px; no text below 12px anywhere (accessibility floor).

---

## 3. Color System

Named, deliberate palette — not a generic accent-on-neutral template.

### Core Palette
| Token | Hex | Use |
|---|---|---|
| `indigo-root` (primary) | `#1E2A4A` | Primary actions, nav, wordmark |
| `turmeric` (accent) | `#E8A33D` | Highlights, active states, "nearby now" indicators |
| `banyan-green` (secondary) | `#2F6F4E` | Communities, growth/success contexts |
| `clay-red` (tertiary) | `#B23A2E` | Reserved for marketplace/urgent contexts only, used sparingly |

### Semantic Colors
| Token | Hex | Use |
|---|---|---|
| `success` | `#2F8F5B` | Confirmations, completed gigs |
| `warning` | `#D98E2B` | Pending states, moderation flags |
| `error` | `#C0392B` | Errors, destructive actions |
| `info` | `#3568A8` | Informational banners |

### Neutrals (warm-tinted gray scale, not pure gray)
`#0E1116 · #23262E · #4A4E58 · #8A8D96 · #C7C9CE · #ECEDEF · #F7F7F8`

### Dark Mode
- Background shifts to `#0E1116`, surfaces at `#181B22`.
- `turmeric` accent is *desaturated slightly* (`#E3A852`) in dark mode to avoid vibrating against dark backgrounds.
- Text: `#F7F7F8` primary, `#8A8D96` secondary — never pure white on pure black (accessibility + eye strain).

### Light Mode
- Background `#FBFAF8` (very slightly warm off-white, not the common cream-#F4F1EA default), surfaces pure white `#FFFFFF` with a 1px `#ECEDEF` border for separation instead of heavy shadow.

---

## 4. Spacing & Layout

- **8-point grid** as the base unit; all spacing, padding, and component sizing are multiples of 8 (with 4px allowed only for icon-to-label micro-gaps).
- Standard content margin: 16px mobile, 24px tablet, 32px desktop.
- Card padding: 16px internal, 8px between stacked cards.
- Touch targets: minimum 44×44px (mobile accessibility floor).

---

## 5. Components

| Component | Key Rules |
|---|---|
| **Buttons** | Primary = `indigo-root` fill, white text, 8px radius. Secondary = outline, `indigo-root` text. Tertiary = text-only. Never more than one primary button per screen section. |
| **Cards** | 12px radius, 1px hairline border in light mode, subtle elevation only in dark mode. "Opportunity cards" (gigs/offers) get a small `turmeric` corner tag; "AI cards" (recommendations) get a subtle root-motif watermark in the corner — the *only* place the root motif appears inside product UI beyond the map. |
| **Inputs** | 8px radius, label always visible above field (never placeholder-as-label), clear error state in `error` red with inline message, never a color-only error indicator (accessibility). |
| **Navigation (bottom tabs)** | 4–5 items max: Discover, Communities, Messages, Create, Profile. Active tab uses `turmeric` indicator dot, not a full color fill, to keep the bar calm. |
| **Floating Action (FAB)** | Single FAB for primary "create" action (post/gig/event) — context-aware label, never generic "+" alone; always paired with a one-word label on first use. |
| **Sheets / Modals** | Bottom sheets for mobile-native feel; full modals reserved for multi-step flows (e.g., business verification). |
| **Chips / Badges** | Chips for filters (interest tags, distance radius); badges for counts only (never for vanity metrics like "views"). |
| **Maps** | Custom map style: warm neutral base, `indigo-root` for user's own pin, `banyan-green` for communities, `turmeric` for live/active events — connections between nearby nodes drawn as soft curved root-lines, not straight lines, reinforcing the signature motif functionally (it shows relationship, not just position). |

---

## 6. User Flows (Screen-Level)

- **Login/Registration:** single screen, progressive disclosure — email/OAuth first, profile detail (interests, skills, profile type) requested only after account creation, never all at once.
- **Discover:** map + list toggle, default to list on first launch (map requires location permission, which is requested contextually, not on app open).
- **Profile:** tab structure — About / Communities / Activity / Reviews.
- **Marketplace:** browse → listing detail → contact → (Phase 3) transaction confirmation screen with clear "both parties must confirm" language.
- **Communities:** overview → feed / members / events tabs within a community.
- **AI Assistant:** accessible via a persistent but unobtrusive entry point (not a takeover chat-first home screen) — conversational only when invoked, never forced as the primary navigation paradigm.
- **Settings:** location precision control is its own top-level settings section, not buried — given how central and sensitive it is.

---

## 7. Wireframes

Full per-screen wireframes (desktop/tablet/mobile) for every flow live as a separate Figma/Framer deliverable once visual design begins — this document defines the tokens and structural rules that those wireframes must follow. Below is the structural wireframe for the highest-priority screen, Discover:

```
┌─────────────────────────────┐
│  ≡   Discover        🔔  👤  │  <- top bar, minimal
├─────────────────────────────┤
│ [ List ]  [ Map ]           │  <- view toggle
├─────────────────────────────┤
│ 🔍  Search nearby...        │
│ [Interest] [Distance] [+2]  │  <- filter chips
├─────────────────────────────┤
│ ┌─────────────────────────┐ │
│ │ 🟢 Community card        │ │
│ │  Name · 1.2km · 34 mem.  │ │
│ └─────────────────────────┘ │
│ ┌─────────────────────────┐ │
│ │ 🟡 Opportunity card       │ │
│ │  Gig title · ₹ · 0.8km   │ │
│ └─────────────────────────┘ │
│ ┌─────────────────────────┐ │
│ │ ✨ AI recommendation      │ │
│ │  "3 events match you"    │ │
│ └─────────────────────────┘ │
├─────────────────────────────┤
│  Discover  Communities  ➕  Messages  Profile │ <- bottom tabs
└─────────────────────────────┘
```

---

## 8. Motion

- **Principle:** motion should feel like *settling*, not *bouncing* — cards ease-in with a gentle 200ms cubic-bezier(0.2,0.8,0.2,1), no springy overshoot (overshoot reads as "playful app," not the calm, trustworthy register this product needs).
- **Map connections:** root-line connections between nearby nodes draw in with a subtle 400ms path animation on first load only — not on every re-render.
- **Loading states:** skeleton screens, not spinners, for feed/list content.
- **Empty states:** always paired with one direct action ("No communities yet nearby — start one" + button), never just an illustration with no path forward.
- **Error states:** plain-language, specific, in the interface's voice ("Couldn't post — check your connection and try again"), never a generic "Something went wrong."
- **Reduced motion:** all animations respect `prefers-reduced-motion`; functional motion (e.g., map path draw) degrades to an instant state, not skipped information.

---

## 9. Open Integration Layer — Designing for Future-Proof, Nationwide Interoperability

You asked for this system to be designed so it *could* plug into a much larger ecosystem — potentially including government-grade digital infrastructure — rather than being a closed app. This is an architectural and design posture we can absolutely build toward now, described honestly:

### 9.1 What "future-proof and interoperable" actually means here
India has a strong precedent for **open, interoperable digital public infrastructure** — UPI for payments, DigiLocker for documents, Account Aggregator for consented data-sharing, and ONDC for open commerce networks. The common thread across all of them: **open APIs, verifiable digital identity, and consent-based data sharing**, rather than any single app owning the whole experience.

Project Introvert's design system can follow that same philosophy at the product level:
- **Open API-first design:** every core capability (identity, community membership, listings, events) is designed with a public, documented API surface (see Document 6) from day one — so third-party apps, local governments, or civic organizations could integrate rather than being locked out.
- **Consent-based data sharing:** any data shared with a third-party integration is explicit, scoped, and revocable per integration — mirroring the Account Aggregator consent model rather than a blanket permissions grant.
- **Verifiable identity hooks:** the Identity module (Document 2, Section 4) is structured so it *could* accept a verified credential (e.g., a government-issued digital ID or business registration credential) as one trust signal among others, without making the whole platform dependent on any single credential system.
- **A plug-in surface, not a monolith:** communities, business verification, and marketplace modules are built as swappable, well-bounded services (Document 2, Section 1) specifically so an external integrator — a city government portal, a university, an NGO — could eventually build on top of Project Introvert's open layer rather than needing to be Project Introvert itself.

### 9.2 An honest boundary
This section describes a **design posture and architectural choice you can make today** — building open, well-documented, consent-respecting APIs. It is **not** a claim of any existing partnership, endorsement, or integration with any government body, and none should be implied in product marketing or investor materials until such a relationship actually exists and is formally agreed. "Future-proof for national-scale interoperability" is achievable as an engineering discipline; "government adoption" is a business and policy outcome that depends on relationships, procurement, and regulatory approval far beyond what any design system can promise. I'd treat any public claim along those lines as something to earn, not assert.

### 9.3 Practical next step if you want to pursue this seriously
If real government or large-institution integration is a genuine goal, the actionable next steps are: (1) build to open standards now (this section), (2) engage India's Digital Public Infrastructure ecosystem through its actual public channels (e.g., published API standards for Account Aggregator, ONDC's onboarding process) rather than assuming access, and (3) treat any such integration as its own workstream with legal, security, and policy review — not something the design system alone unlocks.

---

*End of Document 3. Next: Document 4 — Development Roadmap, Document 5 — Database Design, or a rendered visual mockup of the Discover screen using these tokens — your call.*
