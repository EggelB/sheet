-- ============================================================
-- companion_app/db/schema.sql
-- Authoritative DDL. Execute in full; foreign_keys enforcement
-- requires PRAGMA foreign_keys = ON at runtime (see db.ts).
-- ============================================================

-- ── 1. campaigns ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS campaigns (
  id                   TEXT PRIMARY KEY,
  name                 TEXT NOT NULL,
  campaign_secret_hash TEXT NOT NULL,
  created_at           TEXT DEFAULT (datetime('now'))
);

-- ── 2. players ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS players (
  id           TEXT PRIMARY KEY,
  username     TEXT NOT NULL,
  display_name TEXT,
  avatar       TEXT,
  is_gm        INTEGER NOT NULL DEFAULT 0,
  created_at   TEXT DEFAULT (datetime('now')),
  updated_at   TEXT DEFAULT (datetime('now'))
);

-- ── 3. characters ───────────────────────────────────────────
-- Backbone + all scalar game-data columns (1:1 with scalarFields post-Phase-0)
CREATE TABLE IF NOT EXISTS characters (
  -- Backbone
  id                    TEXT PRIMARY KEY,
  player_id             TEXT REFERENCES players(id),
  campaign_id           TEXT NOT NULL REFERENCES campaigns(id),
  roll20_character_id   TEXT UNIQUE,
  sync_version          INTEGER NOT NULL DEFAULT 0,
  synced_at             TEXT DEFAULT (datetime('now')),
  created_at            TEXT DEFAULT (datetime('now')),
  updated_at            TEXT DEFAULT (datetime('now')),

  -- Attributes: base
  body_base  INTEGER, dex_base  INTEGER, str_base  INTEGER, cha_base  INTEGER,
  int_base   INTEGER, wil_base  INTEGER, hum_base  INTEGER, mag_base  INTEGER,

  -- Attributes: mutation modifiers
  body_mutations INTEGER, dex_mutations INTEGER, str_mutations INTEGER, cha_mutations INTEGER,
  int_mutations  INTEGER, wil_mutations  INTEGER, hum_mutations  INTEGER,

  -- Attributes: magic modifiers
  body_magic INTEGER, dex_magic INTEGER, str_magic INTEGER, cha_magic INTEGER,
  int_magic  INTEGER, wil_magic  INTEGER, hum_magic  INTEGER,

  -- Attributes: misc modifiers
  body_misc INTEGER, dex_misc INTEGER, str_misc INTEGER, cha_misc INTEGER,
  int_misc  INTEGER, wil_misc  INTEGER, hum_misc  INTEGER, mag_misc  INTEGER,

  -- Attributes: totals
  body INTEGER, dex INTEGER, str INTEGER, cha INTEGER,
  int  INTEGER, wil INTEGER, hum INTEGER, mag INTEGER,

  -- Reaction
  reaction_base INTEGER, reaction_misc INTEGER, reaction INTEGER,

  -- Dice pools
  pool_spell_base   INTEGER, pool_spell_misc   INTEGER, pool_spell   INTEGER,
  pool_combat_base  INTEGER, pool_combat_misc  INTEGER, pool_combat  INTEGER,
  pool_control_base INTEGER, pool_control_misc INTEGER, pool_control INTEGER,
  pool_astral_base  INTEGER, pool_astral_misc  INTEGER, pool_astral  INTEGER,

  -- Initiative
  init_dice INTEGER, init_reaction_mod INTEGER, init_misc_mod INTEGER, init_score INTEGER,

  -- Condition monitor derived
  cm_physical_overflow INTEGER, cm_tn_mod INTEGER, cm_init_mod INTEGER,

  -- Condition monitor: mental boxes (0/1 checkboxes)
  cm_mental_l1 INTEGER, cm_mental_l2 INTEGER,
  cm_mental_m1 INTEGER, cm_mental_m2 INTEGER, cm_mental_m3 INTEGER,
  cm_mental_s1 INTEGER, cm_mental_s2 INTEGER, cm_mental_s3 INTEGER, cm_mental_s4 INTEGER,
  cm_mental_d  INTEGER,

  -- Condition monitor: stun boxes (0/1 checkboxes)
  cm_stun_l1 INTEGER, cm_stun_l2 INTEGER,
  cm_stun_m1 INTEGER, cm_stun_m2 INTEGER, cm_stun_m3 INTEGER,
  cm_stun_s1 INTEGER, cm_stun_s2 INTEGER, cm_stun_s3 INTEGER, cm_stun_s4 INTEGER,
  cm_stun_d  INTEGER, cm_stun_u  INTEGER,

  -- Condition monitor: physical boxes (0/1 checkboxes)
  cm_physical_l1 INTEGER, cm_physical_l2 INTEGER,
  cm_physical_m1 INTEGER, cm_physical_m2 INTEGER, cm_physical_m3 INTEGER,
  cm_physical_s1 INTEGER, cm_physical_s2 INTEGER, cm_physical_s3 INTEGER, cm_physical_s4 INTEGER,
  cm_physical_d  INTEGER, cm_physical_u  INTEGER,

  -- Identity
  char_name TEXT, char_race_station TEXT, char_sex TEXT, char_age TEXT,
  char_description TEXT, char_notes TEXT,

  -- Karma
  karma_good INTEGER, karma_used INTEGER, karma_total INTEGER, karma_pool INTEGER,

  -- Encumberment
  ep_total INTEGER, ep_max INTEGER,

  -- Armor (worn)
  armor_torso_name TEXT, armor_torso_piercing INTEGER, armor_torso_slashing INTEGER, armor_torso_impact INTEGER,
  armor_legs_name  TEXT, armor_legs_piercing  INTEGER, armor_legs_slashing  INTEGER, armor_legs_impact  INTEGER,
  armor_head_name  TEXT, armor_head_piercing  INTEGER, armor_head_slashing  INTEGER, armor_head_impact  INTEGER,
  armor_total_piercing INTEGER, armor_total_slashing INTEGER, armor_total_impact INTEGER,

  -- Adept power points (fractional)
  power_points_max REAL, power_points_used REAL, power_points_remaining REAL,

  -- Spellcasting
  spells_sustained INTEGER, sustained_tn_mod INTEGER, tn_warning_level INTEGER,

  -- Essence (fractional)
  essence_total REAL,

  -- Money (Phase 0 additions)
  money_gold INTEGER, money_silver INTEGER, money_copper INTEGER
);

-- ── 4. rep_skills ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_skills (
  id               TEXT PRIMARY KEY,
  character_id     TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id    TEXT NOT NULL,
  skill_name       TEXT,
  skill_linked_attr TEXT,
  skill_general    TEXT,
  skill_spec       INTEGER,
  skill_base       INTEGER,
  skill_foci       INTEGER,
  skill_misc       INTEGER,
  skill_total      INTEGER,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 5. rep_mutations ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_mutations (
  id               TEXT PRIMARY KEY,
  character_id     TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id    TEXT NOT NULL,
  mutation_name    TEXT,
  mutation_level   INTEGER,
  mutation_essence REAL,
  mutation_bp_cost INTEGER,
  mutation_effect  TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 6. rep_adept_powers ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_adept_powers (
  id                  TEXT PRIMARY KEY,
  character_id        TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id       TEXT NOT NULL,
  power_name          TEXT,
  power_level         INTEGER,
  power_pp_cost       TEXT,
  power_pp_cost_value REAL,
  power_effect        TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 7. rep_spells ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_spells (
  id            TEXT PRIMARY KEY,
  character_id  TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id TEXT NOT NULL,
  spell_name    TEXT,
  spell_force   INTEGER,
  spell_drain   TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 8. rep_foci ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_foci (
  id            TEXT PRIMARY KEY,
  character_id  TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id TEXT NOT NULL,
  focus_name    TEXT,
  focus_type    TEXT,
  focus_force   INTEGER,
  focus_bonded  INTEGER,
  focus_notes   TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 9. rep_weapons ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_weapons (
  id                  TEXT PRIMARY KEY,
  character_id        TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id       TEXT NOT NULL,
  weapon_name         TEXT,
  weapon_type         TEXT,
  weapon_modifiers    TEXT,
  weapon_power        INTEGER,
  weapon_damage       TEXT,
  weapon_conceal      INTEGER,
  weapon_reach        INTEGER,
  weapon_ep           INTEGER,
  weapon_range_short  TEXT,
  weapon_range_medium TEXT,
  weapon_range_long   TEXT,
  weapon_range_extreme TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 10. rep_equipment ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_equipment (
  id               TEXT PRIMARY KEY,
  character_id     TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id    TEXT NOT NULL,
  equip_name       TEXT,
  equip_description TEXT,
  equip_ep         INTEGER,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 11. rep_contacts ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_contacts (
  id            TEXT PRIMARY KEY,
  character_id  TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id TEXT NOT NULL,
  contact_name  TEXT,
  contact_info  TEXT,
  contact_level TEXT,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 12. rep_karma ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_karma (
  id            TEXT PRIMARY KEY,
  character_id  TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id TEXT NOT NULL,
  karma_event   TEXT,
  karma_amount  INTEGER,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 13. rep_milestones ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS rep_milestones (
  id                TEXT PRIMARY KEY,
  character_id      TEXT NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
  roll20_row_id     TEXT NOT NULL,
  milestone_trial   TEXT,
  milestone_tier1   TEXT,
  milestone_tier2   TEXT,
  milestone_tier3   TEXT,
  milestone_current INTEGER,
  UNIQUE (character_id, roll20_row_id)
);

-- ── 14. ref_spells ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_spells (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  category    TEXT NOT NULL,
  type        TEXT,
  target      TEXT,
  duration    TEXT,
  drain       TEXT,
  description TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 15. ref_weapons ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_weapons (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  type       TEXT,
  conceal    INTEGER,
  reach      INTEGER,
  damage     TEXT,
  ep         INTEGER,
  cost       INTEGER,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 16. ref_armor ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_armor (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  location   TEXT,
  conceal    INTEGER,
  rating_p   INTEGER,
  rating_s   INTEGER,
  rating_i   INTEGER,
  ep         INTEGER,
  cost       INTEGER,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 17. ref_equipment ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_equipment (
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  conceal    INTEGER,
  ep         INTEGER,
  cost       INTEGER,
  notes      TEXT,
  created_at TEXT DEFAULT (datetime('now')),
  updated_at TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 18. ref_skills ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_skills (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  name            TEXT NOT NULL,
  linked_attr     TEXT,
  category        TEXT,
  specializations TEXT,
  created_at      TEXT DEFAULT (datetime('now')),
  updated_at      TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 19. ref_adept_powers ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_adept_powers (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  pp_cost     TEXT,
  description TEXT,
  game_effect TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 20. ref_mutations ────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_mutations (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  essence     TEXT,
  bp_cost     INTEGER,
  description TEXT,
  game_effect TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 21. ref_totems ───────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_totems (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  name          TEXT NOT NULL,
  type          TEXT NOT NULL,
  environment   TEXT,
  description   TEXT,
  advantages    TEXT,
  disadvantages TEXT,
  created_at    TEXT DEFAULT (datetime('now')),
  updated_at    TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 22. ref_spirits ──────────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_spirits (
  id                 INTEGER PRIMARY KEY AUTOINCREMENT,
  name               TEXT NOT NULL,
  category           TEXT NOT NULL,
  formula_b          TEXT,
  formula_q          TEXT,
  formula_s          TEXT,
  formula_c          TEXT,
  formula_i          TEXT,
  formula_w          TEXT,
  formula_e          TEXT,
  formula_r          TEXT,
  formula_initiative TEXT,
  attack             TEXT,
  powers             TEXT,
  weaknesses         TEXT,
  created_at         TEXT DEFAULT (datetime('now')),
  updated_at         TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 23. ref_spirit_powers ────────────────────────────────────
CREATE TABLE IF NOT EXISTS ref_spirit_powers (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  type        TEXT,
  action      TEXT,
  range       TEXT,
  duration    TEXT,
  description TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── 24. ref_elemental_services ───────────────────────────────
CREATE TABLE IF NOT EXISTS ref_elemental_services (
  id          INTEGER PRIMARY KEY AUTOINCREMENT,
  name        TEXT NOT NULL,
  description TEXT,
  created_at  TEXT DEFAULT (datetime('now')),
  updated_at  TEXT DEFAULT (datetime('now')),
  UNIQUE (name)
);

-- ── Indices ──────────────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_characters_player    ON characters (player_id);
CREATE INDEX IF NOT EXISTS idx_characters_campaign  ON characters (campaign_id);
CREATE INDEX IF NOT EXISTS idx_rep_skills_char      ON rep_skills (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_mutations_char   ON rep_mutations (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_adept_powers_char ON rep_adept_powers (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_spells_char      ON rep_spells (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_foci_char        ON rep_foci (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_weapons_char     ON rep_weapons (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_equipment_char   ON rep_equipment (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_contacts_char    ON rep_contacts (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_karma_char       ON rep_karma (character_id);
CREATE INDEX IF NOT EXISTS idx_rep_milestones_char  ON rep_milestones (character_id);
CREATE INDEX IF NOT EXISTS idx_ref_spells_category  ON ref_spells (category);
CREATE INDEX IF NOT EXISTS idx_ref_spells_type      ON ref_spells (type);
CREATE INDEX IF NOT EXISTS idx_ref_weapons_type     ON ref_weapons (type);
CREATE INDEX IF NOT EXISTS idx_ref_totems_type      ON ref_totems (type);
CREATE INDEX IF NOT EXISTS idx_ref_spirits_category ON ref_spirits (category);
