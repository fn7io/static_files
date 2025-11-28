# Insight Families - Enhanced Taxonomy with Hook Pattern Mapping

**Complete list of insight tokens and sub-tokens with meanings** — unified and prioritized for DTC beauty/wellness/supplements.
Structured by **priority tiers** for mining, with **hook patterns as a facet** for packaging insights.

---

## Priority Stack (What to Mine First)

### **Tier 0 — Moment & Fit (Most Leverage)**
1. **Intent Signals**
2. **Topic Trends & Social Buzz**
3. **Audience Segments & Identity**
4. **Cultural & Localization Cues**

### **Tier 1 — Conversion Core**
5. **Pain & Problem Discovery**
6. **Outcome & Validation**
7. **Value, Price & Justification**
8. **Comparisons, Alternatives & Switching**

### **Tier 2 — Behavior & Technical Fit**
9. **Routines, Workflows & Behavior**
10. **Performance, Fit & Integration**

### **Tier 3 — External Signals & Context**
11. **Marketing Trends & Campaigns**
12. **Industry News & Regulatory Updates**
13. **Context, Seasonality & Environment**
14. **Knowledge, Myths & Learning**

### **Tier 4 — Packaging & Funnel**
15. **Creative, Engagement & Proof Formats**
16. **Meta & Journey-Level Insight**

## 🔎 1. **Intent Signals (Public Web & Social)** [TIER 0]

Signals observable from public posts, profiles, groups, forums, job boards, and news. Score by **recency × frequency × explicitness**.

| Token                         | Meaning                                                                                         |
| ----------------------------- | ------------------------------------------------------------------------------------------------ |
| `help_seeking_question`       | Explicit asks: "how do I…?", "recommend a…?", "what's the best…?".                              |
| `comparison_language`         | "X vs Y", "alternative to", "switch from", "replace".                                           |
| `urgency_timing`              | Timeboxed need: "by Friday", "this week", "urgent", "ASAP".                                     |
| `budget_mention`              | Mentions price/budget/discounts/coupons; "is this worth it?", "any codes?".                     |
| `trial_feedback_public`       | "trying/tested/on trial", sharing first-use results or blockers.                                |
| `churn_risk_complaint`        | Complaints about a competitor/vendor outage or bad results.                                      |
| `success_adoption_brags`      | Public wins that imply adoption: "migrated to…", "clear in 14 days", "rolled out to team".       |
| `social_proof_seek`           | Requests for reviews/testimonials: "any real results?", "share before/after?".                  |
| `creator_collab_call`         | Brand or founder publicly seeking UGC creators/testers (e-com signal to activate ads).          |
| `hiring_relevant_role`        | Job posts for roles implying adoption (e.g., MktOps, RevOps, DevOps, Esthetician).               |
| `leadership_change_public`    | New CMO/CTO/Head of Growth post that often precedes tool/process changes.                        |
| `funding_news_public`         | Funding or grant announcements indicating new budgets/projects.                                   |
| `event_presence`              | Posts about attending industry events (e.g., SaaStr, CosmoProf) tied to solution categories.     |
| `tech_stack_change_public`    | Posts about migrations/upgrades ("moving from X to Y", "sunsetting Z").                          |
| `compliance_deadline_public`  | SOC2/FDA/HIPAA/TGA deadlines driving urgent adoption.                                            |
| `seasonality_need_now`        | Weather/holiday/problem spikes: "summer frizz", "Black Friday load", "tax time".                 |
| `location_intent`             | "Visiting [city]", "nearest clinic/store?", "delivery to [region]?".                             |
| `group_join_request`          | "Any groups for [topic]?" → early exploration intent.                                            |
| `influencer_tag_follow`       | Tagging experts or asking "who to follow for [topic]?"                                           |
| `purchasing_signal_callout`   | "Link please", "where to buy?", "DM price", "invoice me", sharing cart/checkout screenshots.     |
| **NEW:**                      |                                                                                                  |
| `intent_tier`                 | Low/Med/High derived from signal mix (e.g., help_seeking + urgency + budget ⇒ High).            |
| `buy_context`                 | Gift/self/event purchasing context.                                                              |
| `purchase_mode`               | One-off vs subscribe preference signals.                                                         |
| `channel_preference`          | DM/comment/landing page preference from explicit asks.                                           |

---

## 👥 2. **Audience Segments & Identity** [TIER 0]

| Token                        | Meaning                                                                                          |
| ---------------------------- | ------------------------------------------------------------------------------------------------ |
| **Demographics & Firmographics** |                                                                                           |
| `segment_archetype`          | Concise label for a micro-segment (e.g., "curly-girl athlete", "ops-led PLG startup").          |
| `geo_region`                 | Country/state/city or store locale explicitly mentioned in profiles, posts, or groups.          |
| `climate_zone`               | Hot/humid/dry/cold; weather context that changes problems (e.g., frizz, dryness, sweat-proof).  |
| `language_locale`            | Language/locale variants implied by profile or community (translation/idiom needs).             |
| `platform_affinity`          | Platforms, sub-reddits, groups, or forums where this segment is most active.                    |
| `demographic_age_band`       | Age band when explicit in bios/posts (13–17, 18–24, 25–34, 35–44, 45+).                         |
| `life_stage`                 | Student, new parent, athlete, shift worker, traveler, etc.                                      |
| `price_sensitivity_band`     | Value-seeker / mid-market / premium cues from language ("budget", "dupe", "investment").        |
| `routine_intensity`          | Low-effort vs high-ritual segments (e.g., "5-step routine" vs "60-sec fix").                     |
| `problem_context_segment`    | Domain-specific need clusters (e.g., acne-prone, sensitive skin; hiring surge, compliance burden). |
| **Tribe & Identity**         |                                                                                                  |
| `tribe_identity`             | Community a user belongs to (e.g. curly-girl, devops, clean beauty).                            |
| `community_tribe`            | Identity clusters/hashtags (e.g., #curlygirlmethod, #bodybuilding, #cleanbeauty, #indiehacker). |
| `language_slang`             | In-group words and tone used by that tribe.                                                     |
| `status_signals`             | What users post to show belonging or pride.                                                     |
| `lifestyle_microstory`       | POV scenes describing relatable micro-moments.                                                  |
| `tribe_badge`                | Symbolic markers like "what's in my bag/stack".                                                 |
| `community_memes`            | Recurring jokes, idioms, or shared humor.                                                       |
| **Emotional Drivers**        |                                                                                                  |
| `emotional_drivers`          | Feelings behind motivation (confidence, anxiety, relief, FOMO, pride).                          |
| `concern_cluster`            | Acne, pigmentation, hair fall, gut, sleep - specific problem groupings.                         |
| `dupe_preference`            | Dupe hunters vs prestige buyers.                                                                |
| `region_climate`             | Combined regional and climate factors affecting product needs.                                   |
| **B2B Specific**             |                                                                                                  |
| `role_function`              | Job function expressed publicly (marketing, ops, HR, engineering, founder).                     |
| `seniority_level`            | IC, Manager, Director, VP/CXO (from titles/bios).                                               |
| `firmographic_industry`      | Industry/vertical when stated (retail, healthcare, fintech, etc.).                              |
| `firmographic_company_size`  | Company size hints (solo/micro/SMB/mid/enterprise) from headcount mentions or "team of X".      |
| `revenue_band`               | <$100k, $100k–$1M, $1–5M, $5–20M+ when publicly disclosed.                                      |
| `funding_stage`              | Bootstrapped, pre-seed, seed, Series A+ as seen on profiles/news.                               |
| `technographic_stack`        | Publicly visible stack (Shopify, Klaviyo, GA4, HubSpot, ATS, etc.).                             |
| **Purchase Behavior**        |                                                                                                  |
| `purchase_cadence`           | Replenisher vs one-off buyer cues in posts ("monthly top-ups", "one-time fix").                 |
| `channel_preference`         | Prefers DM/comments/forums/email based on explicit asks ("DM me", "email me").                  |

---

## 🧩 3. **Pain & Problem Discovery** [TIER 1]

| Token                  | Meaning                                                       |
| ---------------------- | ------------------------------------------------------------- |
| `pain_points`          | Specific problems users face with the product or process.     |
| `objections`           | Reasons users hesitate or refuse to buy (e.g. price, safety). |
| `frustrations`         | Emotional reactions to recurring failures or disappointments. |
| `effort_burden`        | Tasks that feel too time-consuming or complicated.            |
| `safety_fears`         | Concerns about risk, side effects, or reliability.            |
| `compatibility_issues` | Product not working with existing setup or habits.            |
| `failed_fixes`         | Attempts that didn't work and why.                            |
| `trigger_moments`      | Specific times/contexts when the pain shows up.               |
| `problem_context`      | Situations in which the issue becomes noticeable.             |
| **NEW:**               |                                                               |
| `tolerance_side_effects` | Breakouts, bloating, other tolerated negative effects.      |
| `sensitivity_triggers` | Fragrance, dairy, specific ingredients causing reactions.     |
| `access_hurdles`       | Stock-outs, shipping delays, availability issues.             |

---

## 🎯 4. **Outcome & Validation** [TIER 1]

| Token               | Meaning                                              |
| ------------------- | ---------------------------------------------------- |
| `desired_outcomes`  | What "success" looks like for users.                 |
| `before_after`      | Transformation snapshots (proof of change).          |
| `one_change_proof`  | Single tweaks that cause visible improvement.        |
| `benchmark_metrics` | Comparative measures (speed, hold %, uptime).        |
| `leaderboards`      | Ranked or benchmarked outcomes users trust.          |
| `social_proof`      | Ratings, reviews, repurchase mentions, testimonials. |
| `media_evidence`    | Photos, screenshots, videos showing results.         |
| `kpi_improvement`   | Measurable change in a user's key metric.            |
| **NEW:**            |                                                      |
| `day_count_to_change` | 7/14/28-day proof timelines.                      |
| `derm_grade_evidence` | Dermatologist-approved or clinical backing.       |
| `third_party_labs`  | Independent lab verification.                        |
| `user_cohort_proof` | Results for specific user groups (e.g., 40+ skin).  |

---

## 💰 5. **Value, Price & Justification** [TIER 1]

| Token                  | Meaning                                  |
| ---------------------- | ---------------------------------------- |
| `price_math`           | Cost breakdowns and affordability logic. |
| `per_use_cost`         | Cost per application/use or seat.        |
| `roi_calc`             | Return-on-investment evidence.           |
| `risk_reversal`        | Guarantees, refund policies, SLAs.       |
| `deal_offer`           | Time-bound promotions, bundles, trials.  |
| `scarcity_signal`      | Stock limits or launch windows.          |
| `financial_constraint` | Affordability or budgeting issues.       |
| **NEW:**               |                                          |
| `dupe_index`           | Comparison to premium brand pricing.     |
| `subscription_savings` | Discount for subscription vs one-off.    |
| `bundle_mix_value`     | Value proposition of product bundles.    |

---

## 🔁 6. **Comparisons, Alternatives & Switching** [TIER 1]

| Token                  | Meaning                                                    |
| ---------------------- | ---------------------------------------------------------- |
| `alternatives`         | Competing or substitute products.                          |
| `comparisons`          | A vs B contrasts and feature deltas.                       |
| `switching_drivers`    | Reasons users left one product for another.                |
| `contrarian_takes`     | "Do the opposite" or non-mainstream opinions.              |
| `ethical_curiosity`    | "Everyone does X; winners do Y" format insights.           |
| `migration_guides`     | How users change over, replace, or roll back.              |
| `feature_gaps`         | Missing or inferior features identified during comparison. |
| **NEW:**               |                                                            |
| `ingredient_equivalence` | Retinol alternatives, creatine types, etc.              |
| `clinical_claims_delta` | Difference in clinical backing between options.          |
| `switch_pain`          | Specific reasons why users abandoned competitor.           |

---

## ⚙️ 7. **Routines, Workflows & Behavior** [TIER 2]

| Token                  | Meaning                                                             |
| ---------------------- | ------------------------------------------------------------------- |
| `routines`             | Step-by-step user habits or daily flows.                            |
| `workarounds`          | Creative user fixes when the ideal solution is missing.             |
| `rituals`              | Repeated community or personal practices (e.g. "morning wash-day"). |
| `stack_order`          | The order or sequence of tools/products used.                       |
| `time_to_result`       | Duration between use and outcome.                                   |
| `do_this_not_that`     | Swaps or simplified alternative routines.                           |
| `checklists_playbooks` | Common saved templates or SOPs used to complete a task.             |
| `hacks_shortcuts`      | Small actions that bring fast results.                              |
| **NEW:**               |                                                                     |
| `tempo_cadence`        | AM/PM/weekly routine timing.                                        |
| `sequence_conflicts`   | Actives or ingredients that clash when used together.               |
| `device_dependency`    | Derma roller, shaker, other tools needed.                           |

---

## 📈 8. **Performance, Fit & Integration** [TIER 2]

| Token                        | Meaning                                   |
| ---------------------------- | ----------------------------------------- |
| `performance_metrics`        | Speed, uptime, or measurable output.      |
| `scalability_limits`         | How performance changes with scale.       |
| `integration_compatibility`  | Fit with other products, APIs, workflows. |
| `errors_troubleshooting`     | Bugs, error codes, and fixes.             |
| `procurement_security_legal` | SOC2, DPA, MSA, compliance mentions.      |
| `safety_compliance`          | Physical or regulatory safety claims.     |
| `reliability_proof`          | Long-term stability data.                 |
| **NEW (Beauty):**            |                                           |
| `texture_absorbency`         | How quickly product absorbs into skin.    |
| `pilling`                    | Product balling up on skin.               |
| `white_cast`                 | Visible residue on darker skin tones.     |
| **NEW (Supplements):**       |                                           |
| `taste_mixability`           | Flavor and how well it mixes.             |
| `stomach_comfort`            | Digestive tolerance.                      |

---

## 🌍 9. **Context, Seasonality & Environment** [TIER 3]

| Token                     | Meaning                                                       |
| ------------------------- | ------------------------------------------------------------- |
| `seasonality_trends`      | Time- or weather-based variations (summer frizz, tax season). |
| `localization_region_fit` | Adaptation to region (language, payment, climate).            |
| `context_of_use`          | Situational environments (commute, gym, school run).          |
| `trend_jack`              | Using trending sounds, memes, or hashtags.                    |
| `launch_events`           | Product drops, restocks, or updates.                          |
| `community_activity`      | Collective events like challenges or polls.                   |
| **NEW:**                  |                                                               |
| `event_hooks`             | Wedding, festival, holiday timing.                            |
| `weather_impacts`         | Humidity/frizz, winter dryness effects.                       |

---

## 🧠 10. **Knowledge, Myths & Learning** [TIER 3]

| Token                       | Meaning                                                   |
| --------------------------- | --------------------------------------------------------- |
| `myths_misconceptions`      | Common false beliefs corrected by data or experts.        |
| `ingredient_tech_mechanism` | Plain-language explanation of how something works.        |
| `simple_science`            | Short, understandable cause-and-effect reasoning.         |
| `expert_quotes`             | Credible endorsements, credentials, or disclaimers.       |
| `knowledge_gaps`            | Questions users ask when they don't understand something. |
| `tutorial_steps`            | How-to sequences or explainers.                           |
| `mistakes_patterns`         | Recurrent user errors and their fixes.                    |
| **NEW:**                    |                                                           |
| `regulatory_facts`          | TGA/FDA disclaimers and requirements.                     |
| `dose_myths`                | Misconceptions about dosing or frequency.                 |

---

## 🎥 11. **Creative, Engagement & Proof Formats** [TIER 4]

| Token                      | Meaning                                                 |
| -------------------------- | ------------------------------------------------------- |
| `ugc_challenge`            | Community test or stitch formats.                       |
| `interactive_save_comment` | Polls, comment-trigger posts, templates.                |
| `asrm_sensory`             | Sound or texture-based satisfying visuals.              |
| `founder_confession`       | Transparent admissions or changelog posts.              |
| `anti_ad`                  | Honest marketing that admits faults.                    |
| `hook_language`            | Scroll-stopping phrases mined from social.              |
| `visual_motifs`            | Props, camera angles, or repetitive framing styles.     |
| `format_affinity`          | Platform-specific format preference (reel vs carousel). |
| `expert_format`            | Thought-leader or educator content style.               |
| **NEW:**                   |                                                         |
| `lofi_ugc`                 | Low-production user-generated content style.            |
| `kinetic_text`             | Moving text overlays for engagement.                    |
| `caption_density`          | 100% sound-off ready content.                           |

---
| `sarcasm_style`            | Dry/ironic lines; sarcastic tone controls.                 |
| `cheeky_double_meaning`    | PG‑13 wordplay with innocent + suggestive read.            |
| `wordplay_puns`            | Local puns/rhyme/alliteration/portmanteau.                  |
| `observational_comedy`     | Everyday micro‑pain jokes audiences relate to.              |
| `roast_banter_safe`        | Light, non-hostile roast of habits/competitors.             |
| `deadpan_one_liner`        | Short, flat delivery zingers.                                |
| `bait_and_switch`          | Setup that flips expectations in final beat.                 |
| `meme_wit_remix`           | Remix trending meme formats with category twist.             |
| `setup_payoff_structure`   | Classic joke structure (setup → twist → payoff).             |
| `risk_boundary_level`      | Low/Med/High cap for edginess per campaign/segment.         |

## 🔍 12. **Meta & Journey-Level Insight** [TIER 4]

| Token                      | Meaning                                                        |
| -------------------------- | -------------------------------------------------------------- |
| `sentiment_trend`          | Positive, neutral, or negative tone shifts.                    |
| `journey_stage`            | Awareness → Consideration → Purchase → Onboarding → Retention. |
| `replenishment_cycle`      | Frequency of reorder or engagement.                            |
| `community_engagement`     | Level of participation, saves, shares.                         |
| `constraint_barriers`      | Time, budget, or technical limits affecting conversion.        |
| `knowledge_discovery_path` | How users learn, compare, and decide.                          |
| `emerging_topics`          | New ideas, ingredients, or tech gaining traction.              |
| `competitor_moves`         | Announcements, launches, or sunsets from rivals.               |
| `onboarding_dropoffs`      | Where users abandon during setup/first use.                    |

---

## 🔔 13. **Marketing Trends & Campaigns** [TIER 3 — Market Signals]
*Purpose:* Track emerging marketing strategies and creative campaign tactics across channels (DTC & SaaS), by demographic and region. Use to inspire hooks, formats, and budget‑efficient tests.

| Token                     | Meaning                                                                 |
|---------------------------|-------------------------------------------------------------------------|
| `ai_augmented_creative`   | Use of generative AI in creative, copy, and personalization.            |
| `lofi_ugc_aesthetic`      | Raw/lo‑fi UGC styles outperforming polished ads in trust/CTR.           |
| `interactive_campaigns`   | AR try‑ons, quizzes, live shopping, shoppable video.                    |
| `community_driven`        | Community‑led/ambassador programs, challenges, brand squads.            |
| `micro_influencer_collabs`| Niche creators matched to micro‑segments/regions.                       |
| `platform_shift_response` | Tactics reacting to algorithm/policy changes or new networks.           |
| `budget_hacks`            | “Do more with less” creative/bid/targeting efficiencies.                |
| `sustainability_claims`   | Eco/ethical angles used as core value props.                            |
| `video_trends`            | Dominant short‑form patterns; “sound‑off” design; captions first.       |
| `voice_ar_vr`             | Voice search prompts; AR/VR/immersive ad experiments.                   |

## 🔔 14. **Topic Trends & Social Buzz** [TIER 0 — Moment & Fit]
*Purpose:* Monitor fast‑moving cultural/topic trends around the chosen Scout objective (ingredients, features, use‑cases), including memes, hashtags, and influencer‑sparked spikes.

| Token                  | Meaning                                                                  |
|------------------------|--------------------------------------------------------------------------|
| `viral_hashtag`        | New or resurging hashtags/challenges with sharp volume spikes.           |
| `meme_format`          | Popular meme/joke templates brands can safely remix.                     |
| `influencer_fad`       | Short‑lived trends triggered by creator/celebrity posts.                 |
| `trending_ingredient`  | Ingredient/tech/use‑case suddenly gaining interest.                      |
| `feature_fad`          | Feature/UI pattern that’s trending in user talk (B2B/SaaS included).     |
| `community_slang`      | Fresh slang/catchphrases tied to tribe identity.                         |
| `ugc_trend`            | Predominant UGC edit styles (cuts, captions, ASMR, POV).                 |
| `hashtag_momentum`     | Growth trajectory of relevant hashtags week‑over‑week.                   |
| `emerging_subtopics`   | New sub‑themes within the main topic cluster.                            |
| `sentiment_swings`     | Rapid positive/negative tone changes around a topic.                     |
| `key_influencers`      | Accounts repeatedly triggering spikes in the topic.                      |
| `regional_variations`  | Geo/locale differences (phrasing, platforms, cultural cues).             |
| `paid_media_buzz`      | Ad‑amplified chatter distinct from organic momentum.                     |
| `advocacy_stories`     | Viral customer‑help or rescue stories fueling goodwill.                  |
| `content_length_pref`  | Short‑form vs long‑form preference signals by segment/platform.          |

## 🔔 15. **Industry News & Regulatory Updates** [TIER 3 — Market Signals]
*Purpose:* Surface external signals—authoritative news, regulatory changes, macro trends, and platform/tech updates—that reshape messaging, compliance, and timing.

| Token                      | Meaning                                                                 |
|----------------------------|-------------------------------------------------------------------------|
| `regulatory_update`        | New/changed laws & standards affecting marketing/claims/privacy.        |
| `platform_policy_change`   | Network‑level policy or feature changes (ads, APIs, attribution).       |
| `macro_consumer_trend`     | Economy & culture shifts altering demand, channels, or sentiment.       |
| `industry_newsflash`       | Headline reports, research, M&A, funding, launches in the category.     |
| `competitive_landscape`    | Notable competitor moves/events beyond simple X‑vs‑Y comparisons.       |
| `policy_controversy`       | Public debates/crises (privacy, safety, AI ethics) impacting trust.     |
| `ai_platform_news`         | Major AI or ad‑tech announcements shaping expectations/possibilities.   |
| `macro_budget_signals`     | Budget cuts/expansions impacting spend mix and offer design.            |
| `tech_advances`            | New tools/formats (e.g., gen‑AI features, measurement, creator tools).  |

## 🌐 16. **Cultural & Localization Cues** [TIER 0 — Moment & Fit]
*Purpose:* Capture region‑specific cultural triggers and guardrails so copy feels native and avoids missteps. Localize humor, slang, references, etiquette, and timing.

| Token                       | Meaning                                                                 |
|----------------------------|-------------------------------------------------------------------------|
| `slang_localisms`          | Region/tribe slang and idioms audiences actually use.                   |
| `code_switching`           | Mixing languages/alphabets (e.g., Hinglish) that boosts relatability.   |
| `humor_style_preference`   | What lands locally (sarcasm, cheeky wit, deadpan, wholesome).           |
| `sarcasm_tolerance_band`   | Low/Med/High comfort with sarcasm/roast on that platform/culture.       |
| `cheeky_double_meaning_ok` | Whether playful double‑entendre is acceptable (PG‑13 only).             |
| `taboo_zones`              | Topics/tones to avoid (religion, politics, modesty norms, etc.).        |
| `authority_cues`           | Expert/elder/institution signals that carry weight locally.             |
| `formality_norms`          | Expected politeness level, honorifics, emoji use.                       |
| `festival_hooks`           | Local festivals/holidays/cultural moments that drive shares.            |
| `sports_hooks`             | National/club sports moments that spark mass conversation.              |
| `pop_culture_anchors`      | Films, music, influencers, inside jokes to reference safely.            |
| `honorifics_etiquette`     | Titles/phrases that show respect; when to use them.                     |
| `proverb_twist`            | Local proverbs/phrases re‑written for comedic effect.                   |
| `regional_register`        | Formal vs casual dialect/English variant expected by the audience.      |


# Hook Patterns (Facet) — Click-Bait Mapping

> Attach 1–3 patterns to any insight. Hooks are a **facet** (how we package), not a family (what we learned).

## Hook Pattern Set (22)

1. **Myth-Bust / Surprising Stat**
2. **Stop-Doing-This**
3. **Insider Secret**
4. **One-Change Trick**
5. **Time-Boxed Challenge**
6. **Single-Ingredient Shock**
7. **Price-Math Flip**
8. **Social-Proof Micro-Stack**
9. **Tribe Callout**
10. **Visual Pattern Interrupt**
11. **Contrarian Take**
12. **Limited-Drop FOMO**
13. **X-vs-Y (fast compare)**
14. **Founder Confession / Anti-Ad**
15. **Open Loop Tease**
16. **Safety-Reassurance**

17. **Sarcastic PSA**
18. **Relatable Roast**
19. **Pun / Wordplay**
20. **Bait‑and‑Switch Reveal**
21. **Deadpan One‑liner**
22. **Meme Remix**

## Fast Mapping (What to Pair with What)

| Insight Family | Recommended Hook Patterns |
| -------------- | ------------------------- |
| **Intent Signals** | Time-Boxed, FOMO, Price-Math, X-vs-Y |
| **Audience Segments & Identity** | Tribe Callout, Insider Secret, Status Signal, Emotional Hook |
| **Pain & Problem** | Stop-Doing-This, One-Change, Insider Secret |
| **Outcome & Validation** | Social-Proof Stack, Open Loop, Time-Boxed |
| **Value & Price** | Price-Math Flip, FOMO, Dupe/Compare |
| **Comparisons & Switching** | X-vs-Y, Contrarian Take, Founder Confession |
| **Routines & Behavior** | One-Change, Stop-Doing-This, Insider Secret |
| **Performance & Fit** | Safety-Reassurance, Visual Interrupt (texture/mix test) |
| **Context & Seasonality** | Time-Boxed, FOMO, Tribe Callout |
| **Knowledge & Myths** | Myth-Bust, Insider Secret, Contrarian Take |
| **Creative & Proof** | Visual Interrupt, Founder Confession, Open Loop |
| **Meta & Journey** | Open Loop, Social-Proof Stack at retargeting |

---

# Ready-to-Use Examples (Per Top Families)

## Intent Signals → (Time-Boxed / FOMO / Price-Math / X-vs-Y)

* *Beauty*: "**7-day glow challenge**—save your spot; only 1,000 kits."
* *Supplements*: "**Collagen vs whey in 10s**—see which actually helps hair."
* *Wellness*: "**Subscribe & save** ₹12/day—cheaper than your chai."

## Pain & Problem → (Stop-Doing / One-Change / Insider Secret)

* "**Stop** mixing your pre-workout like this—**kills absorption**."
* "**One swap** fixed my frizz in Mumbai humidity."
* "Derm's **inside secret**: niacinamide before vitamin C."

## Outcome & Validation → (Social-Proof Stack / Open Loop / Time-Boxed)

* "**14 days, 3 photos, 4.7★**—tap to see the last pic."
* "I tried this **for 2 weeks**—wait for day 10…"

## Value & Price → (Price-Math / FOMO)

* "₹**19/day** skin routine—less than a rideshare tip."
* "**48-hour drop**: bundle replaces ₹6k of 'dupes'."

## Comparisons & Switching → (X-vs-Y / Contrarian / Confession)

* "**Retinol vs bakuchiol**—which won my 28-day test?"
* "We **ditched** synthetic flavoring—taste test inside."

## Performance & Fit → (Safety-Reassurance / Visual Interrupt)

* "**No white cast** test on 5 skin tones—watch the swipe."
* "**Dissolves in 5 sec**—no grit, no bloat."

---

# How Scout Should Pick Hooks (Simple Rules)

* If `deal_seek` or `urgency_timing` → **FOMO** or **Time-Boxed** + **Price-Math**
* If `comparison_language` → **X-vs-Y** + **Contrarian**
* If `help_seeking_question` → **Insider Secret** + **One-Change**
* If `churn_risk_complaint` → **Founder Confession/Anti-Ad** + **Switching**
* If `safety_fears` → **Safety-Reassurance** + **Social-Proof Stack**
* Always layer **Audience Segment** tokens into the hook line (tribe callout)

---

## Why This Structure

* Keeps **insight families** clean and MECE (what the market says) while hooks remain a **reusable facet** (how we package)
* Prioritizes **Intent + Audience** (biggest lift), then **Pain/Outcome/Value/Compare** (conversion core)
* Gives Scout deterministic rules to select **hook patterns** from the detected signals and segment
* Ready for JSON schema export (families + tokens + hook facet enums + selection rules) for direct Scout integration