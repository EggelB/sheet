/**
 * Central configuration for all game library catalogs.
 * Single source of truth — all list pages derive from this config.
 * Table names are trusted constants (from schema).
 */

export type CatalogKey =
  | 'spells'
  | 'weapons'
  | 'armor'
  | 'equipment'
  | 'skills'
  | 'adept-powers'
  | 'mutations'
  | 'totems'
  | 'spirits'
  | 'spirit-powers'
  | 'elemental-services';

export interface ListColumn {
  key: string;
  label: string;
}

export interface FormField {
  key: string;
  label: string;
  type: 'text' | 'textarea' | 'number' | 'select';
  options?: string[];
}

export interface CatalogEntry {
  /** URL slug (matches CatalogKey) */
  slug: CatalogKey;
  /** Human-readable label */
  label: string;
  /** Database table name (trusted constant) */
  table: string;
  /** Columns to display in list view */
  listColumns: ListColumn[];
  /** Fields for client-side filter dropdowns (SELECT DISTINCT) */
  filterFields: string[];
  /** Fields shown in expanded detail panel */
  detailFields: ListColumn[];
  /** Editable form fields for create/edit pages */
  formFields: FormField[];
}

export const CATALOG_CONFIG: Record<CatalogKey, CatalogEntry> = {
  spells: {
    slug: 'spells',
    label: 'Spells',
    table: 'ref_spells',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'category', label: 'Category' },
      { key: 'type', label: 'Type' },
      { key: 'drain', label: 'Drain' },
    ],
    filterFields: ['category', 'type'],
    detailFields: [
      { key: 'target', label: 'Target' },
      { key: 'duration', label: 'Duration' },
      { key: 'description', label: 'Description' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'category', label: 'Category', type: 'text' },
      { key: 'type', label: 'Type', type: 'text' },
      { key: 'target', label: 'Target', type: 'text' },
      { key: 'duration', label: 'Duration', type: 'text' },
      { key: 'drain', label: 'Drain', type: 'text' },
      { key: 'description', label: 'Description', type: 'textarea' },
    ],
  },

  weapons: {
    slug: 'weapons',
    label: 'Weapons',
    table: 'ref_weapons',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'type', label: 'Type' },
      { key: 'damage', label: 'Damage' },
      { key: 'conceal', label: 'Conceal' },
    ],
    filterFields: ['type'],
    detailFields: [
      { key: 'reach', label: 'Reach' },
      { key: 'ep', label: 'EP' },
      { key: 'cost', label: 'Cost' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'type', label: 'Type', type: 'text' },
      { key: 'damage', label: 'Damage', type: 'text' },
      { key: 'conceal', label: 'Conceal', type: 'number' },
      { key: 'reach', label: 'Reach', type: 'number' },
      { key: 'ep', label: 'EP', type: 'number' },
      { key: 'cost', label: 'Cost', type: 'number' },
    ],
  },

  armor: {
    slug: 'armor',
    label: 'Armor',
    table: 'ref_armor',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'location', label: 'Location' },
      { key: 'rating_p', label: 'Rating P' },
      { key: 'rating_s', label: 'Rating S' },
    ],
    filterFields: ['location'],
    detailFields: [
      { key: 'rating_i', label: 'Rating I' },
      { key: 'conceal', label: 'Conceal' },
      { key: 'ep', label: 'EP' },
      { key: 'cost', label: 'Cost' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'location', label: 'Location', type: 'text' },
      { key: 'conceal', label: 'Conceal', type: 'number' },
      { key: 'rating_p', label: 'Rating P', type: 'number' },
      { key: 'rating_s', label: 'Rating S', type: 'number' },
      { key: 'rating_i', label: 'Rating I', type: 'number' },
      { key: 'ep', label: 'EP', type: 'number' },
      { key: 'cost', label: 'Cost', type: 'number' },
    ],
  },

  equipment: {
    slug: 'equipment',
    label: 'Equipment',
    table: 'ref_equipment',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'conceal', label: 'Conceal' },
      { key: 'ep', label: 'EP' },
    ],
    filterFields: [],
    detailFields: [
      { key: 'cost', label: 'Cost' },
      { key: 'notes', label: 'Notes' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'conceal', label: 'Conceal', type: 'number' },
      { key: 'ep', label: 'EP', type: 'number' },
      { key: 'cost', label: 'Cost', type: 'number' },
      { key: 'notes', label: 'Notes', type: 'textarea' },
    ],
  },

  skills: {
    slug: 'skills',
    label: 'Skills',
    table: 'ref_skills',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'linked_attr', label: 'Linked Attr' },
      { key: 'category', label: 'Category' },
    ],
    filterFields: ['linked_attr', 'category'],
    detailFields: [{ key: 'specializations', label: 'Specializations' }],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'linked_attr', label: 'Linked Attr', type: 'text' },
      { key: 'category', label: 'Category', type: 'text' },
      { key: 'specializations', label: 'Specializations', type: 'textarea' },
    ],
  },

  'adept-powers': {
    slug: 'adept-powers',
    label: 'Adept Powers',
    table: 'ref_adept_powers',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'pp_cost', label: 'PP Cost' },
    ],
    filterFields: [],
    detailFields: [
      { key: 'description', label: 'Description' },
      { key: 'game_effect', label: 'Game Effect' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'pp_cost', label: 'PP Cost', type: 'text' },
      { key: 'description', label: 'Description', type: 'textarea' },
      { key: 'game_effect', label: 'Game Effect', type: 'textarea' },
    ],
  },

  mutations: {
    slug: 'mutations',
    label: 'Mutations',
    table: 'ref_mutations',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'essence', label: 'Essence' },
      { key: 'bp_cost', label: 'BP Cost' },
    ],
    filterFields: [],
    detailFields: [
      { key: 'description', label: 'Description' },
      { key: 'game_effect', label: 'Game Effect' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'essence', label: 'Essence', type: 'text' },
      { key: 'bp_cost', label: 'BP Cost', type: 'number' },
      { key: 'description', label: 'Description', type: 'textarea' },
      { key: 'game_effect', label: 'Game Effect', type: 'textarea' },
    ],
  },

  totems: {
    slug: 'totems',
    label: 'Totems',
    table: 'ref_totems',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'type', label: 'Type' },
      { key: 'environment', label: 'Environment' },
    ],
    filterFields: ['type'],
    detailFields: [
      { key: 'description', label: 'Description' },
      { key: 'advantages', label: 'Advantages' },
      { key: 'disadvantages', label: 'Disadvantages' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'type', label: 'Type', type: 'text' },
      { key: 'environment', label: 'Environment', type: 'text' },
      { key: 'description', label: 'Description', type: 'textarea' },
      { key: 'advantages', label: 'Advantages', type: 'textarea' },
      { key: 'disadvantages', label: 'Disadvantages', type: 'textarea' },
    ],
  },

  spirits: {
    slug: 'spirits',
    label: 'Spirits',
    table: 'ref_spirits',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'category', label: 'Category' },
    ],
    filterFields: ['category'],
    detailFields: [
      { key: 'formula_b', label: 'B' },
      { key: 'formula_q', label: 'Q' },
      { key: 'formula_s', label: 'S' },
      { key: 'formula_c', label: 'C' },
      { key: 'formula_i', label: 'I' },
      { key: 'formula_w', label: 'W' },
      { key: 'formula_e', label: 'E' },
      { key: 'formula_r', label: 'R' },
      { key: 'formula_initiative', label: 'Initiative' },
      { key: 'attack', label: 'Attack' },
      { key: 'powers', label: 'Powers' },
      { key: 'weaknesses', label: 'Weaknesses' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'category', label: 'Category', type: 'text' },
      { key: 'formula_b', label: 'Formula B', type: 'text' },
      { key: 'formula_q', label: 'Formula Q', type: 'text' },
      { key: 'formula_s', label: 'Formula S', type: 'text' },
      { key: 'formula_c', label: 'Formula C', type: 'text' },
      { key: 'formula_i', label: 'Formula I', type: 'text' },
      { key: 'formula_w', label: 'Formula W', type: 'text' },
      { key: 'formula_e', label: 'Formula E', type: 'text' },
      { key: 'formula_r', label: 'Formula R', type: 'text' },
      { key: 'formula_initiative', label: 'Formula Initiative', type: 'text' },
      { key: 'attack', label: 'Attack', type: 'textarea' },
      { key: 'powers', label: 'Powers', type: 'textarea' },
      { key: 'weaknesses', label: 'Weaknesses', type: 'textarea' },
    ],
  },

  'spirit-powers': {
    slug: 'spirit-powers',
    label: 'Spirit Powers',
    table: 'ref_spirit_powers',
    listColumns: [
      { key: 'name', label: 'Name' },
      { key: 'type', label: 'Type' },
      { key: 'action', label: 'Action' },
    ],
    filterFields: ['type'],
    detailFields: [
      { key: 'range', label: 'Range' },
      { key: 'duration', label: 'Duration' },
      { key: 'description', label: 'Description' },
    ],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'type', label: 'Type', type: 'text' },
      { key: 'action', label: 'Action', type: 'text' },
      { key: 'range', label: 'Range', type: 'text' },
      { key: 'duration', label: 'Duration', type: 'text' },
      { key: 'description', label: 'Description', type: 'textarea' },
    ],
  },

  'elemental-services': {
    slug: 'elemental-services',
    label: 'Elemental Services',
    table: 'ref_elemental_services',
    listColumns: [{ key: 'name', label: 'Name' }],
    filterFields: [],
    detailFields: [{ key: 'description', label: 'Description' }],
    formFields: [
      { key: 'name', label: 'Name', type: 'text' },
      { key: 'description', label: 'Description', type: 'textarea' },
    ],
  },
};

/** Get config by slug; throw 404 if not found */
export function getCatalogConfig(slug: string): CatalogEntry {
  const config = CATALOG_CONFIG[slug as CatalogKey];
  if (!config) throw new Error(`Unknown catalog: ${slug}`);
  return config;
}

/** Get all catalog slugs in order */
export function getAllCatalogSlugs(): CatalogKey[] {
  return Object.keys(CATALOG_CONFIG) as CatalogKey[];
}
