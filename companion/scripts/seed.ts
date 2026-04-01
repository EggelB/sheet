import { createClient, type Client } from '@libsql/client/node';
import XLSX from 'xlsx';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { readFileSync, existsSync } from 'node:fs';

const __dirname = dirname(fileURLToPath(import.meta.url));

// Load .dev.vars into process.env (Node 18 compat)
const devVarsPath = resolve(__dirname, '../.dev.vars');
if (existsSync(devVarsPath)) {
  for (const line of readFileSync(devVarsPath, 'utf-8').split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq > 0) process.env[trimmed.slice(0, eq)] ??= trimmed.slice(eq + 1);
  }
}

// Workbook directory: plans/ at repo root (contains .xlsx game-data files).
const WORKBOOKS_DIR = resolve(__dirname, '../../plans');

const WORKBOOK_FILES = {
  spells: 'Spells.xlsx',
  equipment: 'Equipment.xlsx',
  skills: 'Skills.xlsx',
  adeptPowersMutations: 'Adept Powers and Mutations.xlsx',
  totemsSpirits: 'Totems and Spirits.xlsx',
} as const;

// ── Row Interfaces ──────────────────────────────────────────

interface SpellRow {
  name: string;
  category: string;
  type: string | null;
  target: string | null;
  duration: string | null;
  drain: string | null;
  description: string | null;
}

interface WeaponRow {
  name: string;
  type: string | null;
  conceal: number | null;
  reach: number | null;
  damage: string | null;
  ep: number | null;
  cost: number | null;
}

interface ArmorRow {
  name: string;
  location: string | null;
  conceal: number | null;
  rating_p: number | null;
  rating_s: number | null;
  rating_i: number | null;
  ep: number | null;
  cost: number | null;
}

interface EquipmentRow {
  name: string;
  conceal: number | null;
  ep: number | null;
  cost: number | null;
  notes: string | null;
}

interface SkillRow {
  name: string;
  linked_attr: string | null;
  category: string | null;
  specializations: string | null;
}

interface AdeptPowerRow {
  name: string;
  pp_cost: string | null;
  description: string | null;
  game_effect: string | null;
}

interface MutationRow {
  name: string;
  essence: string | null;
  bp_cost: number | null;
  description: string | null;
  game_effect: string | null;
}

interface TotemRow {
  name: string;
  type: string;
  environment: string | null;
  description: string | null;
  advantages: string | null;
  disadvantages: string | null;
}

interface SpiritRow {
  name: string;
  category: string;
  formula_b: string | null;
  formula_q: string | null;
  formula_s: string | null;
  formula_c: string | null;
  formula_i: string | null;
  formula_w: string | null;
  formula_e: string | null;
  formula_r: string | null;
  formula_initiative: string | null;
  attack: string | null;
  powers: string | null;
  weaknesses: string | null;
}

interface SpiritPowerRow {
  name: string;
  type: string | null;
  action: string | null;
  range: string | null;
  duration: string | null;
  description: string | null;
}

interface ElementalServiceRow {
  name: string;
  description: string | null;
}

interface SeedStats {
  table: string;
  upserted: number;
  errors: number;
}

// ── Utility Functions ───────────────────────────────────────

type DataRow = (string | number | null | undefined)[];

function str(val: any): string | null {
  if (val === null || val === undefined) return null;
  const s = String(val).trim();
  return s || null;
}

function num(val: any): number | null {
  if (typeof val === 'number') return val;
  if (typeof val === 'string') {
    const n = parseFloat(val);
    return isNaN(n) ? null : n;
  }
  return null;
}

function getRows(wb: XLSX.WorkBook, sheet: string): DataRow[] {
  const ws = wb.Sheets[sheet];
  if (!ws) return [];
  return XLSX.utils.sheet_to_json(ws, { header: 1, defval: null });
}

// ── Parsers ─────────────────────────────────────────────────

/**
 * Spells use a card layout: multiple spells side-by-side in column groups.
 * Each spell card occupies 5 columns. Row pattern per card:
 *   Name at col C | "Type:" at C, val at C+1 | "Target:" at C+2, val at C+3
 *   "Duration:" at C, val at C+1 | "Drain:" at C+2, val at C+3
 *   Description text at C (may span rows)
 * Spell sheets: "Combat Spells", "Detection Spells", etc.
 */
function parseSpells(wb: XLSX.WorkBook): SpellRow[] {
  const results: SpellRow[] = [];
  const SPELL_SHEETS = wb.SheetNames.filter(
    n => n.endsWith(' Spells') || n.endsWith(' Spe')
  );

  for (const sheetName of SPELL_SHEETS) {
    const data = getRows(wb, sheetName);
    if (!data.length) continue;
    const category = sheetName
      .replace(/ Spells?$/, '')
      .replace(/ Spe$/, ' Spells');

    // Detect column offsets where "Type:" appears
    const colOffsets = new Set<number>();
    for (const row of data) {
      if (!row) continue;
      for (let c = 0; c < row.length; c++) {
        if (str(row[c]) === 'Type:') colOffsets.add(c);
      }
    }

    for (const C of colOffsets) {
      let current: SpellRow | null = null;

      for (let r = 1; r < data.length; r++) {
        const row = data[r];
        if (!row) continue;
        const cell = str(row[C]);
        if (!cell) continue;

        if (cell === 'Type:') {
          if (current) {
            current.type = str(row[C + 1]);
            current.target = str(row[C + 3]);
          }
        } else if (cell === 'Duration:') {
          if (current) {
            current.duration = str(row[C + 1]);
            current.drain = str(row[C + 3]);
          }
        } else {
          // Determine if this is a new spell name or description text
          // by checking if the next non-null cell at C is "Type:"
          let nextIsType = false;
          for (let nr = r + 1; nr < data.length; nr++) {
            const nc = str(data[nr]?.[C]);
            if (nc) { nextIsType = nc === 'Type:'; break; }
          }

          if (nextIsType) {
            if (current) results.push(current);
            current = {
              name: cell, category,
              type: null, target: null, duration: null, drain: null,
              description: null,
            };
          } else if (current) {
            current.description = current.description
              ? current.description + '\n' + cell : cell;
          }
        }
      }
      if (current) results.push(current);
    }
  }
  return results;
}

/**
 * Weapons: grouped tabular layout in the "Weapons" sheet.
 * Row 2 has headers. Category rows have name at col 0 and nothing in data cols.
 * Data rows have name at col 0 and values at cols 2-6.
 */
function parseWeapons(wb: XLSX.WorkBook): WeaponRow[] {
  const data = getRows(wb, 'Weapons');
  if (!data.length) return [];
  const results: WeaponRow[] = [];
  let currentType: string | null = null;

  for (let r = 3; r < data.length; r++) {
    const row = data[r];
    if (!row) continue;
    const name = str(row[0]);
    if (!name) continue;

    const hasData = row.slice(2, 7).some(v => v !== null && v !== undefined);
    if (!hasData) {
      currentType = name;
      continue;
    }

    results.push({
      name,
      type: currentType,
      conceal: num(row[2]),
      reach: num(row[3]),
      damage: str(row[4]),
      ep: num(row[5]),
      cost: num(row[6]),
    });
  }
  return results;
}

/**
 * Armor: grouped tabular in the "Armor" sheet.
 * Headers at row 2: Location(2), Concealability(3), Piercing(4),
 * Slashing(5), Impact(6), Weight/EP(7), Cost(8), Notes(9).
 */
function parseArmor(wb: XLSX.WorkBook): ArmorRow[] {
  const data = getRows(wb, 'Armor');
  if (!data.length) return [];
  const results: ArmorRow[] = [];

  for (let r = 3; r < data.length; r++) {
    const row = data[r];
    if (!row) continue;
    const name = str(row[0]);
    if (!name) continue;

    const hasData = row.slice(2, 9).some(v => v !== null && v !== undefined);
    if (!hasData) continue; // category header row — skip (not stored)

    results.push({
      name,
      location: str(row[2]),
      conceal: num(row[3]),
      rating_p: num(row[4]),
      rating_s: num(row[5]),
      rating_i: num(row[6]),
      ep: num(row[7]),
      cost: num(row[8]),
    });
  }
  return results;
}

/**
 * Equipment: grouped tabular in the "Equipment" sheet.
 * Headers at row 2: Concealability(2), Weight/EP(3), Cost(4), Notes(5).
 */
function parseEquipment(wb: XLSX.WorkBook): EquipmentRow[] {
  const data = getRows(wb, 'Equipment');
  if (!data.length) return [];
  const results: EquipmentRow[] = [];

  for (let r = 3; r < data.length; r++) {
    const row = data[r];
    if (!row) continue;
    const name = str(row[0]);
    if (!name) continue;

    const hasData = row.slice(2, 6).some(v => v !== null && v !== undefined);
    if (!hasData) continue; // category header

    results.push({
      name,
      conceal: num(row[2]),
      ep: num(row[3]),
      cost: num(row[4]),
      notes: str(row[5]),
    });
  }
  return results;
}

/**
 * Skills: individual category sheets with prose format.
 * Each skill: "Name (Linked Attr)" at col 0,
 * description at col 1, "Default:..." at col 1,
 * "Specializations:..." at col 2.
 */
function parseSkills(wb: XLSX.WorkBook): SkillRow[] {
  const results: SkillRow[] = [];
  // Knowledge Skills and Language Skills sheets are rulebook prose, not skill tables — skip them
  const PROSE_SHEETS = new Set(['Knowledge Skills', 'Language Skills']);
  const SKILL_SHEETS = wb.SheetNames.filter(n => n.endsWith(' Skills') && !PROSE_SHEETS.has(n));

  for (const sheetName of SKILL_SHEETS) {
    const data = getRows(wb, sheetName);
    if (!data.length) continue;
    const category = sheetName.replace(/ Skills$/, '');

    let current: SkillRow | null = null;

    for (let r = 0; r < data.length; r++) {
      const row = data[r];
      if (!row) continue;
      const cell0 = str(row[0]);

      if (cell0) {
        // Skill name row: "Skill Name (Linked Attr)"
        if (current) results.push(current);
        const match = cell0.match(/^(.+?)\s*\(([^)]+)\)\s*$/);
        current = {
          name: match ? match[1].trim() : cell0,
          linked_attr: match ? match[2].trim() : null,
          category,
          specializations: null,
        };
        continue;
      }

      // Check col 2 for specializations
      const cell2 = str(row[2]);
      if (cell2 && current) {
        const specMatch = cell2.match(/^Specializations?:\s*(.+)/i);
        if (specMatch) current.specializations = specMatch[1].trim();
      }
    }
    if (current) results.push(current);
  }
  return results;
}

/**
 * Adept Powers: tabular with optional Level sub-rows.
 * Row 0: headers (Name, Point Cost, Description, Game Effect, Compatibilities)
 * Powers without levels: single row with all fields.
 * Powers with levels: parent row (name, desc, game_effect), then
 *   "Level N" rows with their own pp_cost and game_effect → separate DB rows.
 */
function parseAdeptPowers(wb: XLSX.WorkBook): AdeptPowerRow[] {
  const data = getRows(wb, 'Physical Adept Powers');
  if (!data.length) return [];
  const results: AdeptPowerRow[] = [];

  interface Pending {
    name: string;
    pp_cost: string | null;
    description: string | null;
    game_effect: string | null;
    levels: { label: string; pp_cost: string | null; game_effect: string | null }[];
  }
  let pending: Pending | null = null;

  function flush() {
    if (!pending) return;
    if (pending.levels.length > 0) {
      for (const lv of pending.levels) {
        results.push({
          name: `${pending.name} - ${lv.label}`,
          pp_cost: lv.pp_cost,
          description: pending.description,
          game_effect: lv.game_effect,
        });
      }
    } else {
      results.push({
        name: pending.name,
        pp_cost: pending.pp_cost,
        description: pending.description,
        game_effect: pending.game_effect,
      });
    }
    pending = null;
  }

  for (let r = 1; r < data.length; r++) {
    const row = data[r];
    if (!row) continue;
    const name = str(row[0]);
    if (!name) continue;

    const isLevel = /^Level \d+$/i.test(name) || /^(Obvious|Silent)$/i.test(name);

    if (isLevel && pending) {
      pending.levels.push({
        label: name,
        pp_cost: str(row[1]),
        game_effect: str(row[3]),
      });
    } else {
      flush();
      pending = {
        name,
        pp_cost: str(row[1]),
        description: str(row[2]),
        game_effect: str(row[3]),
        levels: [],
      };
    }
  }
  flush();
  return results;
}

/**
 * Mutations: semi-tabular with optional Level sub-rows.
 * Row 1: headers (Name, Essence, Cost(BP), Description, Game Effect, Incompatibilities)
 */
function parseMutations(wb: XLSX.WorkBook): MutationRow[] {
  const data = getRows(wb, 'Mutations');
  if (!data.length) return [];
  const results: MutationRow[] = [];

  interface Pending {
    name: string;
    essence: string | null;
    bp_cost: number | null;
    description: string | null;
    game_effect: string | null;
    levels: { label: string; essence: string | null; bp_cost: number | null; game_effect: string | null }[];
  }
  let pending: Pending | null = null;

  function flush() {
    if (!pending) return;
    if (pending.levels.length > 0) {
      for (const lv of pending.levels) {
        results.push({
          name: `${pending.name} - ${lv.label}`,
          essence: lv.essence ?? pending.essence,
          bp_cost: lv.bp_cost ?? pending.bp_cost,
          description: pending.description,
          game_effect: lv.game_effect ?? pending.game_effect,
        });
      }
    } else {
      results.push({
        name: pending.name,
        essence: pending.essence,
        bp_cost: pending.bp_cost,
        description: pending.description,
        game_effect: pending.game_effect,
      });
    }
    pending = null;
  }

  for (let r = 2; r < data.length; r++) {
    const row = data[r];
    if (!row) continue;
    const name = str(row[0]);
    if (!name) continue;

    const isLevel = /^Level \d+$/i.test(name);

    if (isLevel && pending) {
      pending.levels.push({
        label: name,
        essence: str(row[1]),
        bp_cost: num(row[2]),
        game_effect: str(row[4]),
      });
    } else {
      flush();
      pending = {
        name,
        essence: str(row[1]),
        bp_cost: num(row[2]),
        description: str(row[3]),
        game_effect: str(row[4]),
        levels: [],
      };
    }
  }
  flush();
  return results;
}

/**
 * Totems: card layout across 4 sheets (Animal A-E, F-O, P-Z, Nature).
 * Each totem card spans 10 columns. Pattern:
 *   Name at C, "Description:" at C+1 (next row), text at C+2 (row after),
 *   "Environment:" at C+1, value at C+2, etc.
 */
function parseTotems(wb: XLSX.WorkBook): TotemRow[] {
  const results: TotemRow[] = [];
  const TOTEM_SHEETS = wb.SheetNames.filter(n => n.includes('Totem'));

  for (const sheetName of TOTEM_SHEETS) {
    const data = getRows(wb, sheetName);
    if (!data.length) continue;
    const type = sheetName.includes('Animal') ? 'Animal' : 'Nature';

    // Find column offsets by locating "Description:" labels
    const descCols = new Set<number>();
    for (const row of data) {
      if (!row) continue;
      for (let c = 0; c < row.length; c++) {
        if (str(row[c]) === 'Description:') descCols.add(c);
      }
    }

    for (const dc of descCols) {
      const C = dc - 1; // name column is one left of "Description:" label

      // Find all name rows: value at C where next row has "Description:" at C+1
      for (let r = 0; r < data.length; r++) {
        const name = str(data[r]?.[C]);
        if (!name) continue;
        // Verify it's a totem name by checking for "Description:" nearby
        let foundDesc = false;
        for (let nr = r + 1; nr <= r + 2 && nr < data.length; nr++) {
          if (str(data[nr]?.[C + 1]) === 'Description:') { foundDesc = true; break; }
        }
        if (!foundDesc) continue;

        // Collect fields from subsequent rows
        let description: string | null = null;
        let environment: string | null = null;
        let advantages: string | null = null;
        let disadvantages: string | null = null;

        for (let sr = r + 1; sr < Math.min(r + 20, data.length); sr++) {
          const label = str(data[sr]?.[C + 1]);
          // Value is at C+2 in the NEXT row after the label
          const valSame = str(data[sr]?.[C + 2]);
          const valNext = sr + 1 < data.length ? str(data[sr + 1]?.[C + 2]) : null;
          const val = valSame || valNext;

          if (label === 'Description:' && !description) description = val;
          else if (label === 'Environment:' && !environment) environment = val;
          else if (label === 'Advantages:' && !advantages) advantages = val;
          else if (label === 'Disadvantages:' && !disadvantages) disadvantages = val;
        }

        results.push({ name, type, environment, description, advantages, disadvantages });
      }
    }
  }
  return results;
}

/**
 * Spirits: complex multi-column layout in the "Spirits" sheet.
 * Column groups: cols 0-1 (Elementals), cols 7-8 and 14-15 (Nature Spirits).
 * Elementals have complete stat blocks + POWERS + WEAKNESSES.
 * Nature spirit families have shared stat blocks; sub-spirits have only POWERS.
 */
function parseSpirits(wb: XLSX.WorkBook): SpiritRow[] {
  const data = getRows(wb, 'Spirits');
  if (!data.length) return [];
  const results: SpiritRow[] = [];

  const STAT_LABELS = new Set(['B', 'Q', 'S', 'C', 'I', 'W', 'E', 'R', 'INTV', 'ATTACK', 'POWERS', 'WEAKNESSES']);
  const SECTION_HEADERS = new Set(['SPIRITS', 'ELEMENTALS', 'NATURE SPIRITS', 'CONJURING DRAIN']);

  const GROUPS: [number, number, boolean][] = [[0, 1, true], [7, 8, false], [14, 15, false]];

  for (const [C, V, isElemental] of GROUPS) {
    let familyName: string | null = null;
    let stats: Record<string, string | null> = {};
    let pendingSubName: string | null = null;

    // Collect all entries at this column group
    const entries: { row: number; cell: string; val: string | null }[] = [];
    for (let r = 8; r < data.length; r++) {
      const cell = str(data[r]?.[C]);
      if (!cell) continue;
      entries.push({ row: r, cell, val: str(data[r]?.[V]) });
    }

    for (let i = 0; i < entries.length; i++) {
      const { cell, val } = entries[i];
      const upper = cell.toUpperCase();

      if (SECTION_HEADERS.has(upper)) continue;

      if (STAT_LABELS.has(upper)) {
        switch (upper) {
          case 'B': stats.b = val; break;
          case 'Q': stats.q = val; break;
          case 'S': stats.s = val; break;
          case 'C': stats.c = val; break;
          case 'I': stats.i = val; break;
          case 'W': stats.w = val; break;
          case 'E': stats.e = val; break;
          case 'R': stats.r = val; break;
          case 'INTV': stats.initiative = val; break;
          case 'ATTACK': stats.attack = val; break;
          case 'POWERS': {
            const spiritName = pendingSubName || familyName;
            if (spiritName) {
              results.push({
                name: spiritName,
                category: isElemental ? 'Elemental' : (familyName || 'Nature'),
                formula_b: stats.b ?? null, formula_q: stats.q ?? null,
                formula_s: stats.s ?? null, formula_c: stats.c ?? null,
                formula_i: stats.i ?? null, formula_w: stats.w ?? null,
                formula_e: stats.e ?? null, formula_r: stats.r ?? null,
                formula_initiative: stats.initiative ?? null,
                attack: stats.attack ?? null,
                powers: val, weaknesses: null,
              });
            }
            pendingSubName = null;
            break;
          }
          case 'WEAKNESSES':
            if (results.length > 0) results[results.length - 1].weaknesses = val;
            break;
        }
      } else {
        // Name entry — determine if family (has stat block) or sub-spirit
        const nextStat = entries.slice(i + 1).find(
          e => STAT_LABELS.has(e.cell.toUpperCase()) && !SECTION_HEADERS.has(e.cell.toUpperCase())
        );
        if (nextStat && nextStat.cell.toUpperCase() === 'B') {
          familyName = cell;
          stats = {};
          pendingSubName = null;
        } else {
          pendingSubName = cell;
        }
      }
    }
  }
  return results;
}

/**
 * Spirit Powers: card layout in the "Spirit Powers" sheet.
 * Column offsets determined by where "Type" labels appear.
 * Each card: Name at C, then Type/Action/Range/Duration/Description at (C, C+1).
 * Descriptions may span multiple rows at C+1.
 */
function parseSpiritPowers(wb: XLSX.WorkBook): SpiritPowerRow[] {
  const data = getRows(wb, 'Spirit Powers');
  if (!data.length) return [];
  const results: SpiritPowerRow[] = [];
  const FIELD_LABELS = new Set(['Type', 'Action', 'Range', 'Duration', 'Description']);

  // Detect column offsets where "Type" appears
  const colOffsets = new Set<number>();
  for (const row of data) {
    if (!row) continue;
    for (let c = 0; c < row.length; c++) {
      if (str(row[c]) === 'Type') colOffsets.add(c);
    }
  }

  for (const C of colOffsets) {
    let current: SpiritPowerRow | null = null;
    let pastDescription = false;

    for (let r = 1; r < data.length; r++) {
      const row = data[r];
      if (!row) continue;
      const cell = str(row[C]);
      const val = str(row[C + 1]);

      if (!cell && !val) continue;

      if (cell && FIELD_LABELS.has(cell)) {
        if (!current) continue;
        switch (cell) {
          case 'Type': current.type = val; break;
          case 'Action': current.action = val; break;
          case 'Range': current.range = val; break;
          case 'Duration': current.duration = val; break;
          case 'Description':
            current.description = val;
            pastDescription = true;
            break;
        }
      } else if (cell && !FIELD_LABELS.has(cell)) {
        // New power name
        if (current) results.push(current);
        current = { name: cell, type: null, action: null, range: null, duration: null, description: null };
        pastDescription = false;
      } else if (!cell && val && current && pastDescription) {
        // Description continuation at C+1 for this column
        current.description = current.description
          ? current.description + '\n' + val : val;
      }
    }
    if (current) results.push(current);
  }
  return results;
}

/**
 * Elemental Services: simple name/description pairs.
 * Name at col 0, description at col 1 in the next row.
 */
function parseElementalServices(wb: XLSX.WorkBook): ElementalServiceRow[] {
  const data = getRows(wb, 'Elemental Services');
  if (!data.length) return [];
  const results: ElementalServiceRow[] = [];

  for (let r = 1; r < data.length; r++) {
    const name = str(data[r]?.[0]);
    if (!name || name === 'Elemental Services') continue;
    // Description is at col 1 in the next row
    const desc = r + 1 < data.length ? str(data[r + 1]?.[1]) : null;
    results.push({ name, description: desc });
  }
  return results;
}

// ── Seeders ─────────────────────────────────────────────────

async function seedSpells(db: Client, rows: SpellRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_spells (name, category, type, target, duration, drain, description)
              VALUES (?, ?, ?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                category=excluded.category, type=excluded.type,
                target=excluded.target, duration=excluded.duration,
                drain=excluded.drain, description=excluded.description,
                updated_at=datetime('now')`,
        args: [r.name, r.category, r.type, r.target, r.duration, r.drain, r.description],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedSpells batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_spells', upserted, errors };
}

async function seedWeapons(db: Client, rows: WeaponRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_weapons (name, type, conceal, reach, damage, ep, cost)
              VALUES (?, ?, ?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                type=excluded.type, conceal=excluded.conceal,
                reach=excluded.reach, damage=excluded.damage,
                ep=excluded.ep, cost=excluded.cost,
                updated_at=datetime('now')`,
        args: [r.name, r.type, r.conceal, r.reach, r.damage, r.ep, r.cost],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedWeapons batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_weapons', upserted, errors };
}

async function seedArmor(db: Client, rows: ArmorRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_armor (name, location, conceal, rating_p, rating_s, rating_i, ep, cost)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                location=excluded.location, conceal=excluded.conceal,
                rating_p=excluded.rating_p, rating_s=excluded.rating_s,
                rating_i=excluded.rating_i, ep=excluded.ep,
                cost=excluded.cost, updated_at=datetime('now')`,
        args: [r.name, r.location, r.conceal, r.rating_p, r.rating_s, r.rating_i, r.ep, r.cost],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedArmor batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_armor', upserted, errors };
}

async function seedEquipment(db: Client, rows: EquipmentRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_equipment (name, conceal, ep, cost, notes)
              VALUES (?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                conceal=excluded.conceal, ep=excluded.ep,
                cost=excluded.cost, notes=excluded.notes,
                updated_at=datetime('now')`,
        args: [r.name, r.conceal, r.ep, r.cost, r.notes],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedEquipment batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_equipment', upserted, errors };
}

async function seedSkills(db: Client, rows: SkillRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_skills (name, linked_attr, category, specializations)
              VALUES (?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                linked_attr=excluded.linked_attr, category=excluded.category,
                specializations=excluded.specializations,
                updated_at=datetime('now')`,
        args: [r.name, r.linked_attr, r.category, r.specializations],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedSkills batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_skills', upserted, errors };
}

async function seedAdeptPowers(db: Client, rows: AdeptPowerRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_adept_powers (name, pp_cost, description, game_effect)
              VALUES (?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                pp_cost=excluded.pp_cost, description=excluded.description,
                game_effect=excluded.game_effect,
                updated_at=datetime('now')`,
        args: [r.name, r.pp_cost, r.description, r.game_effect],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedAdeptPowers batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_adept_powers', upserted, errors };
}

async function seedMutations(db: Client, rows: MutationRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_mutations (name, essence, bp_cost, description, game_effect)
              VALUES (?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                essence=excluded.essence, bp_cost=excluded.bp_cost,
                description=excluded.description, game_effect=excluded.game_effect,
                updated_at=datetime('now')`,
        args: [r.name, r.essence, r.bp_cost, r.description, r.game_effect],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedMutations batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_mutations', upserted, errors };
}

async function seedTotems(db: Client, rows: TotemRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_totems (name, type, environment, description, advantages, disadvantages)
              VALUES (?, ?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                type=excluded.type, environment=excluded.environment,
                description=excluded.description, advantages=excluded.advantages,
                disadvantages=excluded.disadvantages,
                updated_at=datetime('now')`,
        args: [r.name, r.type, r.environment, r.description, r.advantages, r.disadvantages],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedTotems batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_totems', upserted, errors };
}

async function seedSpirits(db: Client, rows: SpiritRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_spirits (name, category, formula_b, formula_q, formula_s, formula_c, formula_i, formula_w, formula_e, formula_r, formula_initiative, attack, powers, weaknesses)
              VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                category=excluded.category, formula_b=excluded.formula_b,
                formula_q=excluded.formula_q, formula_s=excluded.formula_s,
                formula_c=excluded.formula_c, formula_i=excluded.formula_i,
                formula_w=excluded.formula_w, formula_e=excluded.formula_e,
                formula_r=excluded.formula_r, formula_initiative=excluded.formula_initiative,
                attack=excluded.attack, powers=excluded.powers,
                weaknesses=excluded.weaknesses, updated_at=datetime('now')`,
        args: [r.name, r.category, r.formula_b, r.formula_q, r.formula_s, r.formula_c, r.formula_i, r.formula_w, r.formula_e, r.formula_r, r.formula_initiative, r.attack, r.powers, r.weaknesses],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedSpirits batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_spirits', upserted, errors };
}

async function seedSpiritPowers(db: Client, rows: SpiritPowerRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_spirit_powers (name, type, action, range, duration, description)
              VALUES (?, ?, ?, ?, ?, ?)
              ON CONFLICT(name) DO UPDATE SET
                type=excluded.type, action=excluded.action,
                range=excluded.range, duration=excluded.duration,
                description=excluded.description,
                updated_at=datetime('now')`,
        args: [r.name, r.type, r.action, r.range, r.duration, r.description],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedSpiritPowers batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_spirit_powers', upserted, errors };
}

async function seedElementalServices(db: Client, rows: ElementalServiceRow[]): Promise<SeedStats> {
  const BATCH = 50;
  let upserted = 0, errors = 0;
  for (let i = 0; i < rows.length; i += BATCH) {
    const batch = rows.slice(i, i + BATCH);
    try {
      await db.batch(batch.map(r => ({
        sql: `INSERT INTO ref_elemental_services (name, description)
              VALUES (?, ?)
              ON CONFLICT(name) DO UPDATE SET
                description=excluded.description,
                updated_at=datetime('now')`,
        args: [r.name, r.description],
      })));
      upserted += batch.length;
    } catch (e) {
      console.error(`seedElementalServices batch error at row ${i}:`, e);
      errors += batch.length;
    }
  }
  return { table: 'ref_elemental_services', upserted, errors };
}

// ── Main ────────────────────────────────────────────────────

let db: Client;

async function main(): Promise<void> {
  const dryRun = process.argv.includes('--dry-run');

  // Load workbooks
  const wbs = {
    spells: XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.spells)),
    equipment: XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.equipment)),
    skills: XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.skills)),
    adeptPowersMutations: XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.adeptPowersMutations)),
    totemsSpirits: XLSX.readFile(resolve(WORKBOOKS_DIR, WORKBOOK_FILES.totemsSpirits)),
  };

  // Parse all workbooks
  const spells = parseSpells(wbs.spells);
  const weapons = parseWeapons(wbs.equipment);
  const armor = parseArmor(wbs.equipment);
  const equipment = parseEquipment(wbs.equipment);
  const skills = parseSkills(wbs.skills);
  const powers = parseAdeptPowers(wbs.adeptPowersMutations);
  const mutations = parseMutations(wbs.adeptPowersMutations);
  const totems = parseTotems(wbs.totemsSpirits);
  const spirits = parseSpirits(wbs.totemsSpirits);
  const spiritPowers = parseSpiritPowers(wbs.totemsSpirits);
  const services = parseElementalServices(wbs.totemsSpirits);

  // Print parse counts
  console.log('Parsed record counts:');
  console.log(`  spells:      ${spells.length}`);
  console.log(`  weapons:     ${weapons.length}`);
  console.log(`  armor:       ${armor.length}`);
  console.log(`  equipment:   ${equipment.length}`);
  console.log(`  skills:      ${skills.length}`);
  console.log(`  adeptPowers: ${powers.length}`);
  console.log(`  mutations:   ${mutations.length}`);
  console.log(`  totems:      ${totems.length}`);
  console.log(`  spirits:     ${spirits.length}`);
  console.log(`  spiritPowers: ${spiritPowers.length}`);
  console.log(`  elemServices: ${services.length}`);

  if (dryRun) {
    console.log('\n--dry-run: Skipping database seeding.');
    // Print sample records for verification
    if (spells.length) console.log('\nSample spell:', JSON.stringify(spells[0], null, 2));
    if (weapons.length) console.log('\nSample weapon:', JSON.stringify(weapons[0], null, 2));
    if (skills.length) console.log('\nSample skill:', JSON.stringify(skills[0], null, 2));
    if (totems.length) console.log('\nSample totem:', JSON.stringify(totems[0], null, 2));
    if (spirits.length) console.log('\nSample spirit:', JSON.stringify(spirits[0], null, 2));
    if (spiritPowers.length) console.log('\nSample spirit power:', JSON.stringify(spiritPowers[0], null, 2));
    if (services.length) console.log('\nSample elemental service:', JSON.stringify(services[0], null, 2));
    process.exit(0);
  }

  db = createClient({
    url: process.env.TURSO_DATABASE_URL!,
    authToken: process.env.TURSO_AUTH_TOKEN!,
  });

  // Seed sequentially
  console.log('Seeding companion_app reference tables...');
  const seeders: [string, () => Promise<SeedStats>][] = [
    ['ref_spells', () => seedSpells(db, spells)],
    ['ref_weapons', () => seedWeapons(db, weapons)],
    ['ref_armor', () => seedArmor(db, armor)],
    ['ref_equipment', () => seedEquipment(db, equipment)],
    ['ref_skills', () => seedSkills(db, skills)],
    ['ref_adept_powers', () => seedAdeptPowers(db, powers)],
    ['ref_mutations', () => seedMutations(db, mutations)],
    ['ref_totems', () => seedTotems(db, totems)],
    ['ref_spirits', () => seedSpirits(db, spirits)],
    ['ref_spirit_powers', () => seedSpiritPowers(db, spiritPowers)],
    ['ref_elemental_services', () => seedElementalServices(db, services)],
  ];
  const results: SeedStats[] = [];
  for (const [, fn] of seeders) {
    results.push(await fn());
  }

  // Print stats
  let total = 0;
  for (const r of results) {
    console.log(`  ${r.table.padEnd(24)} upserted=${r.upserted}   errors=${r.errors}`);
    total += r.upserted;
  }
  console.log(`Done. ${total} total records processed.`);

  db.close();
  process.exit(results.some(r => r.errors > 0) ? 1 : 0);
}

main().catch(e => {
  console.error(e);
  db?.close();
  process.exit(1);
});
