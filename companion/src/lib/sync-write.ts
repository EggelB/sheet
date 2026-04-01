import type { Client, InValue } from '@libsql/client';

// ── Exported types ───────────────────────────────────────────────────────────

export interface SyncPayload {
  campaign_db_id: string;
  char_db_id: string | null;
  sync_version_from: number;
  scalars: Record<string, unknown>;
  repeating: Record<RepSection, RepRow[]>;
}

interface RepRow {
  roll20_row_id: string;
  [key: string]: unknown;
}

export interface SyncResult {
  char_db_id: string;
  sync_version: number;
}

export class SyncError extends Error {
  constructor(message: string, public readonly status: number) {
    super(message);
    this.name = 'SyncError';
  }
}

type RepSection =
  | 'skills'
  | 'mutations'
  | 'adept_powers'
  | 'spells'
  | 'foci'
  | 'weapons'
  | 'equipment'
  | 'contacts'
  | 'karma'
  | 'milestones';

// ── Security allowlists ──────────────────────────────────────────────────────
// Source: companion/db/schema.sql Blueprint 1.3 — characters CREATE TABLE.
// Backbone columns excluded: id, player_id, campaign_id, roll20_character_id,
//   sync_version, synced_at, created_at, updated_at.
// Column names come ONLY from this list — payload keys are never used as SQL identifiers.

const ALLOWED_SCALAR_COLUMNS: ReadonlyArray<string> = [
  // Attributes: base
  'body_base',
  'dex_base',
  'str_base',
  'cha_base',
  'int_base',
  'wil_base',
  'hum_base',
  'mag_base',
  // Attributes: mutation modifiers
  'body_mutations',
  'dex_mutations',
  'str_mutations',
  'cha_mutations',
  'int_mutations',
  'wil_mutations',
  'hum_mutations',
  // Attributes: magic modifiers
  'body_magic',
  'dex_magic',
  'str_magic',
  'cha_magic',
  'int_magic',
  'wil_magic',
  'hum_magic',
  // Attributes: misc modifiers
  'body_misc',
  'dex_misc',
  'str_misc',
  'cha_misc',
  'int_misc',
  'wil_misc',
  'hum_misc',
  'mag_misc',
  // Attributes: totals
  'body',
  'dex',
  'str',
  'cha',
  'int',
  'wil',
  'hum',
  'mag',
  // Reaction
  'reaction_base',
  'reaction_misc',
  'reaction',
  // Dice pools
  'pool_spell_base',
  'pool_spell_misc',
  'pool_spell',
  'pool_combat_base',
  'pool_combat_misc',
  'pool_combat',
  'pool_control_base',
  'pool_control_misc',
  'pool_control',
  'pool_astral_base',
  'pool_astral_misc',
  'pool_astral',
  // Initiative
  'init_dice',
  'init_reaction_mod',
  'init_misc_mod',
  'init_score',
  // Condition monitor: derived
  'cm_physical_overflow',
  'cm_tn_mod',
  'cm_init_mod',
  // Condition monitor: mental boxes
  'cm_mental_l1',
  'cm_mental_l2',
  'cm_mental_m1',
  'cm_mental_m2',
  'cm_mental_m3',
  'cm_mental_s1',
  'cm_mental_s2',
  'cm_mental_s3',
  'cm_mental_s4',
  'cm_mental_d',
  // Condition monitor: stun boxes
  'cm_stun_l1',
  'cm_stun_l2',
  'cm_stun_m1',
  'cm_stun_m2',
  'cm_stun_m3',
  'cm_stun_s1',
  'cm_stun_s2',
  'cm_stun_s3',
  'cm_stun_s4',
  'cm_stun_d',
  'cm_stun_u',
  // Condition monitor: physical boxes
  'cm_physical_l1',
  'cm_physical_l2',
  'cm_physical_m1',
  'cm_physical_m2',
  'cm_physical_m3',
  'cm_physical_s1',
  'cm_physical_s2',
  'cm_physical_s3',
  'cm_physical_s4',
  'cm_physical_d',
  'cm_physical_u',
  // Identity
  'char_name',
  'char_race_station',
  'char_sex',
  'char_age',
  'char_description',
  'char_notes',
  // Karma
  'karma_good',
  'karma_used',
  'karma_total',
  'karma_pool',
  // Encumberment
  'ep_total',
  'ep_max',
  // Armor (worn)
  'armor_torso_name',
  'armor_torso_piercing',
  'armor_torso_slashing',
  'armor_torso_impact',
  'armor_legs_name',
  'armor_legs_piercing',
  'armor_legs_slashing',
  'armor_legs_impact',
  'armor_head_name',
  'armor_head_piercing',
  'armor_head_slashing',
  'armor_head_impact',
  'armor_total_piercing',
  'armor_total_slashing',
  'armor_total_impact',
  // Adept power points (fractional)
  'power_points_max',
  'power_points_used',
  'power_points_remaining',
  // Spellcasting
  'spells_sustained',
  'sustained_tn_mod',
  'tn_warning_level',
  // Essence (fractional)
  'essence_total',
  // Money (Phase 0 additions)
  'money_gold',
  'money_silver',
  'money_copper',
];
// Total: 129 scalar columns

// Repeating-section allowlists — one per rep_* table.
// Backbone excluded for each: id, character_id, roll20_row_id.
const ALLOWED_SECTION_COLUMNS: Record<RepSection, ReadonlyArray<string>> = {
  skills: [
    'skill_name',
    'skill_linked_attr',
    'skill_general',
    'skill_spec',
    'skill_base',
    'skill_foci',
    'skill_misc',
    'skill_total',
  ],
  mutations: [
    'mutation_name',
    'mutation_level',
    'mutation_essence',
    'mutation_bp_cost',
    'mutation_effect',
  ],
  adept_powers: [
    'power_name',
    'power_level',
    'power_pp_cost',
    'power_pp_cost_value',
    'power_effect',
  ],
  spells: ['spell_name', 'spell_force', 'spell_drain'],
  foci: ['focus_name', 'focus_type', 'focus_force', 'focus_bonded', 'focus_notes'],
  weapons: [
    'weapon_name',
    'weapon_type',
    'weapon_modifiers',
    'weapon_power',
    'weapon_damage',
    'weapon_conceal',
    'weapon_reach',
    'weapon_ep',
    'weapon_range_short',
    'weapon_range_medium',
    'weapon_range_long',
    'weapon_range_extreme',
  ],
  equipment: ['equip_name', 'equip_description', 'equip_ep'],
  contacts: ['contact_name', 'contact_info', 'contact_level'],
  karma: ['karma_event', 'karma_amount'],
  milestones: [
    'milestone_trial',
    'milestone_tier1',
    'milestone_tier2',
    'milestone_tier3',
    'milestone_current',
  ],
};

const REP_SECTIONS: ReadonlyArray<RepSection> = [
  'skills',
  'mutations',
  'adept_powers',
  'spells',
  'foci',
  'weapons',
  'equipment',
  'contacts',
  'karma',
  'milestones',
];

// ── Main export ──────────────────────────────────────────────────────────────

export async function syncWrite(
  db: Client,
  body: SyncPayload,
  campaignId: string,
): Promise<SyncResult> {
  // ── 2c. First-sync vs subsequent-sync branching ──────────────────────────
  const isFirstSync = body.char_db_id === null;
  let charId: string;
  let newSyncVersion: number;

  if (isFirstSync) {
    charId = crypto.randomUUID();
    newSyncVersion = 1;
  } else {
    const charResult = await db.execute({
      sql: 'SELECT id, sync_version FROM characters WHERE id = ? AND campaign_id = ?',
      args: [body.char_db_id as string, campaignId],
    });
    if (charResult.rows.length === 0) {
      throw new SyncError('Character not found', 404);
    }
    const existingVersion = charResult.rows[0].sync_version as number;
    // 2d. Stale sync detection
    if (existingVersion !== body.sync_version_from) {
      throw new SyncError(
        'Sync conflict: version mismatch. Reload character and retry.',
        409,
      );
    }
    charId = body.char_db_id as string;
    newSyncVersion = existingVersion + 1;
  }

  // ── 2e. Build Turso batch ────────────────────────────────────────────────
  // Batch order: PRAGMA → characters write → 10× DELETE → N× INSERT per section
  const statements: { sql: string; args: InValue[] }[] = [];

  // [0] PRAGMA — enforce FK constraints within the batch transaction
  statements.push({ sql: 'PRAGMA foreign_keys = ON', args: [] });

  // [1] characters INSERT (first sync) or UPDATE (subsequent sync)
  const scalarValues: InValue[] = ALLOWED_SCALAR_COLUMNS.map((col) => {
    const v = body.scalars[col];
    return v === undefined || v === null ? null : String(v);
  });

  if (isFirstSync) {
    // 2f. First sync: INSERT
    const colList = ALLOWED_SCALAR_COLUMNS.join(', ');
    const phList = ALLOWED_SCALAR_COLUMNS.map(() => '?').join(', ');
    statements.push({
      sql: `INSERT INTO characters (id, campaign_id, player_id, roll20_character_id, sync_version, synced_at, created_at, updated_at, ${colList}) VALUES (?, ?, NULL, NULL, 1, datetime('now'), datetime('now'), datetime('now'), ${phList})`,
      args: [charId, campaignId, ...scalarValues],
    });
  } else {
    // 2f. Subsequent sync: UPDATE
    const setClause = ALLOWED_SCALAR_COLUMNS.map((col) => `${col} = ?`).join(
      ', ',
    );
    statements.push({
      sql: `UPDATE characters SET sync_version = ?, synced_at = datetime('now'), updated_at = datetime('now'), ${setClause} WHERE id = ? AND campaign_id = ?`,
      args: [newSyncVersion, ...scalarValues, charId, campaignId],
    });
  }

  // [2–11] DELETE all repeating rows for this character — clears before re-insert
  // Explicit DELETE required because we UPDATE (not replace) the parent characters row,
  // so ON DELETE CASCADE does not fire.
  for (const section of REP_SECTIONS) {
    statements.push({
      sql: `DELETE FROM rep_${section} WHERE character_id = ?`,
      args: [charId],
    });
  }

  // [12+] INSERT repeating rows
  // 2g: For each section, for each payload row, build a fresh UUID and insert allowed cols only.
  for (const section of REP_SECTIONS) {
    const rows = (body.repeating[section] ?? []) as RepRow[];
    const allowedCols = ALLOWED_SECTION_COLUMNS[section];
    for (const row of rows) {
      const rowId = crypto.randomUUID();
      const roll20RowId = String(row.roll20_row_id ?? '');
      const colList = allowedCols.join(', ');
      const phList = allowedCols.map(() => '?').join(', ');
      const rowValues: InValue[] = allowedCols.map((col) => {
        const v = row[col];
        return v === undefined || v === null ? null : String(v);
      });
      statements.push({
        sql: `INSERT INTO rep_${section} (id, character_id, roll20_row_id, ${colList}) VALUES (?, ?, ?, ${phList})`,
        args: [rowId, charId, roll20RowId, ...rowValues],
      });
    }
  }

  // ── Execute batch (atomic — all succeed or all roll back) ────────────────
  try {
    await db.batch(statements, 'write');
  } catch (err) {
    console.error('[sync-write] batch error:', err);
    throw new Error('[sync] DB batch failed');
  }

  // 2h. Return
  return { char_db_id: charId, sync_version: newSyncVersion };
}
