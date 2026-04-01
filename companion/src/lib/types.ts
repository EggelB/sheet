/**
 * Shared TypeScript types for companion_app.
 * Single source of truth for all character and rep-table row shapes.
 * Imported by +page.server.ts, computed.ts, and Svelte components.
 */

// ── CharacterRow ─────────────────────────────────────────────
// Backbone (8 columns) + key scalar columns typed explicitly.
// All 129+ scalar columns are present at runtime via SELECT *;
// the index signature [key: string]: unknown captures the remainder.
export interface CharacterRow {
  // Backbone
  id:                  string;
  player_id:           string | null;
  campaign_id:         string;
  roll20_character_id: string | null;
  sync_version:        number;
  synced_at:           string | null;
  created_at:          string | null;
  updated_at:          string | null;

  // Attribute bases (8 attributes)
  body_base: number | null;
  dex_base:  number | null;
  str_base:  number | null;
  cha_base:  number | null;
  int_base:  number | null;
  wil_base:  number | null;
  hum_base:  number | null;
  mag_base:  number | null;

  // Attribute mutation modifiers (7 attributes)
  body_mutations: number | null;
  dex_mutations:  number | null;
  str_mutations:  number | null;
  cha_mutations:  number | null;
  int_mutations:  number | null;
  wil_mutations:  number | null;
  hum_mutations:  number | null;

  // Attribute magic modifiers (7 attributes)
  body_magic: number | null;
  dex_magic:  number | null;
  str_magic:  number | null;
  cha_magic:  number | null;
  int_magic:  number | null;
  wil_magic:  number | null;
  hum_magic:  number | null;

  // Attribute misc modifiers (8 attributes)
  body_misc: number | null;
  dex_misc:  number | null;
  str_misc:  number | null;
  cha_misc:  number | null;
  int_misc:  number | null;
  wil_misc:  number | null;
  hum_misc:  number | null;
  mag_misc:  number | null;

  // Attribute totals (8 attributes)
  body: number | null;
  dex:  number | null;
  str:  number | null;
  cha:  number | null;
  int:  number | null;
  wil:  number | null;
  hum:  number | null;
  mag:  number | null;

  // Reaction
  reaction_base:  number | null;
  reaction_misc:  number | null;
  reaction:       number | null;

  // Dice pools (4 pools × 3 columns each)
  pool_spell_base:   number | null;
  pool_spell_misc:   number | null;
  pool_spell:        number | null;
  pool_combat_base:  number | null;
  pool_combat_misc:  number | null;
  pool_combat:       number | null;
  pool_control_base: number | null;
  pool_control_misc: number | null;
  pool_control:      number | null;
  pool_astral_base:  number | null;
  pool_astral_misc:  number | null;
  pool_astral:       number | null;

  // Initiative
  init_dice:            number | null;
  init_reaction_mod:    number | null;
  init_misc_mod:        number | null;
  init_score:           number | null;

  // Condition monitor derived
  cm_physical_overflow: number | null;
  cm_tn_mod:            number | null;
  cm_init_mod:          number | null;

  // Condition monitor: mental boxes (0/1 checkboxes) — 10 boxes
  cm_mental_l1: number | null;
  cm_mental_l2: number | null;
  cm_mental_m1: number | null;
  cm_mental_m2: number | null;
  cm_mental_m3: number | null;
  cm_mental_s1: number | null;
  cm_mental_s2: number | null;
  cm_mental_s3: number | null;
  cm_mental_s4: number | null;
  cm_mental_d:  number | null;

  // Condition monitor: stun boxes (0/1 checkboxes) — 12 boxes
  cm_stun_l1: number | null;
  cm_stun_l2: number | null;
  cm_stun_m1: number | null;
  cm_stun_m2: number | null;
  cm_stun_m3: number | null;
  cm_stun_s1: number | null;
  cm_stun_s2: number | null;
  cm_stun_s3: number | null;
  cm_stun_s4: number | null;
  cm_stun_d:  number | null;
  cm_stun_u:  number | null;

  // Condition monitor: physical boxes (0/1 checkboxes) — 12 boxes
  cm_physical_l1: number | null;
  cm_physical_l2: number | null;
  cm_physical_m1: number | null;
  cm_physical_m2: number | null;
  cm_physical_m3: number | null;
  cm_physical_s1: number | null;
  cm_physical_s2: number | null;
  cm_physical_s3: number | null;
  cm_physical_s4: number | null;
  cm_physical_d:  number | null;
  cm_physical_u:  number | null;

  // Identity (Bio tab)
  char_name:         string | null;
  char_race_station: string | null;
  char_sex:          string | null;
  char_age:          string | null;
  char_description:  string | null;
  char_notes:        string | null;

  // Karma scalars (Bio tab header)
  karma_good:  number | null;
  karma_used:  number | null;
  karma_total: number | null;
  karma_pool:  number | null;

  // Encumberment
  ep_total: number | null;
  ep_max:   number | null;

  // Armor (worn) — torso, legs, head × Pierce/Slash/Impact
  armor_torso_name:       string | null;
  armor_torso_piercing:   number | null;
  armor_torso_slashing:   number | null;
  armor_torso_impact:     number | null;
  armor_legs_name:        string | null;
  armor_legs_piercing:    number | null;
  armor_legs_slashing:    number | null;
  armor_legs_impact:      number | null;
  armor_head_name:        string | null;
  armor_head_piercing:    number | null;
  armor_head_slashing:    number | null;
  armor_head_impact:      number | null;
  armor_total_piercing:   number | null;
  armor_total_slashing:   number | null;
  armor_total_impact:     number | null;

  // Adept power points
  power_points_max:       number | null;
  power_points_used:      number | null;
  power_points_remaining: number | null;

  // Spellcasting
  spells_sustained:   number | null;
  sustained_tn_mod:   number | null;
  tn_warning_level:   number | null;

  // Essence (fractional)
  essence_total: number | null;

  // Money (Phase 0 additions)
  money_gold:   number | null;
  money_silver: number | null;
  money_copper: number | null;

  // ... all remaining scalar columns captured by index signature
  [key: string]: unknown;
}

// ── Rep-table row interfaces ─────────────────────────────────

export interface RepSkillRow {
  id:               string;
  character_id:     string;
  roll20_row_id:    string;
  skill_name:       string | null;
  skill_linked_attr: string | null;
  skill_general:    string | null;
  skill_spec:       number | null;
  skill_base:       number | null;
  skill_foci:       number | null;
  skill_misc:       number | null;
  skill_total:      number | null;
}

export interface RepMutationRow {
  id:               string;
  character_id:     string;
  roll20_row_id:    string;
  mutation_name:    string | null;
  mutation_level:   number | null;
  mutation_essence: number | null;
  mutation_bp_cost: number | null;
  mutation_effect:  string | null;
}

export interface RepAdeptPowerRow {
  id:                  string;
  character_id:        string;
  roll20_row_id:       string;
  power_name:          string | null;
  power_level:         number | null;
  power_pp_cost:       string | null;
  power_pp_cost_value: number | null;
  power_effect:        string | null;
}

export interface RepSpellRow {
  id:           string;
  character_id: string;
  roll20_row_id: string;
  spell_name:   string | null;
  spell_force:  number | null;
  spell_drain:  string | null;
}

export interface RepFocusRow {
  id:           string;
  character_id: string;
  roll20_row_id: string;
  focus_name:   string | null;
  focus_type:   string | null;
  focus_force:  number | null;
  focus_bonded: number | null;
  focus_notes:  string | null;
}

export interface RepWeaponRow {
  id:                   string;
  character_id:         string;
  roll20_row_id:        string;
  weapon_name:          string | null;
  weapon_type:          string | null;
  weapon_modifiers:     string | null;
  weapon_power:         number | null;
  weapon_damage:        string | null;
  weapon_conceal:       number | null;
  weapon_reach:         number | null;
  weapon_ep:            number | null;
  weapon_range_short:   string | null;
  weapon_range_medium:  string | null;
  weapon_range_long:    string | null;
  weapon_range_extreme: string | null;
}

export interface RepEquipmentRow {
  id:               string;
  character_id:     string;
  roll20_row_id:    string;
  equip_name:       string | null;
  equip_description: string | null;
  equip_ep:         number | null;
}

export interface RepContactRow {
  id:            string;
  character_id:  string;
  roll20_row_id: string;
  contact_name:  string | null;
  contact_info:  string | null;
  contact_level: string | null;
}

export interface RepKarmaRow {
  id:            string;
  character_id:  string;
  roll20_row_id: string;
  karma_event:   string | null;
  karma_amount:  number | null;
}

export interface RepMilestoneRow {
  id:                  string;
  character_id:        string;
  roll20_row_id:       string;
  milestone_trial:     string | null;
  milestone_tier1:     string | null;
  milestone_tier2:     string | null;
  milestone_tier3:     string | null;
  milestone_current:   number | null;
}

export interface RepData {
  skills:       RepSkillRow[];
  mutations:    RepMutationRow[];
  adept_powers: RepAdeptPowerRow[];
  spells:       RepSpellRow[];
  foci:         RepFocusRow[];
  weapons:      RepWeaponRow[];
  equipment:    RepEquipmentRow[];
  contacts:     RepContactRow[];
  karma:        RepKarmaRow[];
  milestones:   RepMilestoneRow[];
}
