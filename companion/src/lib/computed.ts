/**
 * Pure computation functions for derived character attributes and condition monitor.
 * No DB access, no side effects. Functions take a Character row and return derived values.
 */

import type { CharacterRow, RepData } from './types';

/**
 * Compute total for a single attribute (base + mutations + magic + misc).
 */
function computeAttributeTotal(
  base: number | null,
  mutations: number | null,
  magic: number | null,
  misc: number | null,
): number {
  return (base ?? 0) + (mutations ?? 0) + (magic ?? 0) + (misc ?? 0);
}

/**
 * Compute all 8 attribute totals from base + modifiers.
 * Returns a record of attribute names to totals.
 */
export function computeAttributeTotals(char: CharacterRow): Record<string, number> {
  return {
    body: computeAttributeTotal(char.body_base, char.body_mutations, char.body_magic, char.body_misc),
    dex: computeAttributeTotal(char.dex_base, char.dex_mutations, char.dex_magic, char.dex_misc),
    str: computeAttributeTotal(char.str_base, char.str_mutations, char.str_magic, char.str_misc),
    cha: computeAttributeTotal(char.cha_base, char.cha_mutations, char.cha_magic, char.cha_misc),
    int: computeAttributeTotal(char.int_base, char.int_mutations, char.int_magic, char.int_misc),
    wil: computeAttributeTotal(char.wil_base, char.wil_mutations, char.wil_magic, char.wil_misc),
    hum: computeAttributeTotal(char.hum_base, char.hum_mutations, char.hum_magic, char.hum_misc),
    mag: computeAttributeTotal(char.mag_base, null, null, char.mag_misc),
  };
}

/**
 * Compute condition monitor box counts based on WIL total.
 * Standard Shadowrun 3e: Mental = (WIL // 2) + 8, Stun = (WIL // 2) + 8, Physical = (BOD // 2) + 8
 * BOD for overflow calculation.
 */
export function computeConditionMonitor(char: CharacterRow): {
  mental: number;
  stun: number;
  physical: number;
} {
  const wilTotal = char.wil ?? 0;
  const bodTotal = char.body ?? 0;

  return {
    mental: Math.ceil(wilTotal / 2) + 8,
    stun: Math.ceil(wilTotal / 2) + 8,
    physical: Math.ceil(bodTotal / 2) + 8,
  };
}

/**
 * Compute initiative base from REA + INT totals (2d6 base, then add REA + INT).
 */
export function computeInitiative(char: CharacterRow): number {
  return char.reaction ?? 0;
}

/**
 * Compute movement speed from QCK (DEX) total.
 * Walk = QCK × 2, Run = QCK × 4
 */
export function computeMovement(char: CharacterRow): {
  walk: number;
  run: number;
} {
  const qckTotal = computeAttributeTotal(char.dex_base, char.dex_mutations, char.dex_magic, char.dex_misc);
  return {
    walk: qckTotal * 2,
    run: qckTotal * 4,
  };
}

/**
 * Compute karma ledger running totals.
 * Takes all karma entries, sorts by ID ascending, and produces a ledger with cumulative sum.
 */
export function computeKarmaLedgerRunningTotals(
  karma: Array<{ id: string; karma_amount: number | null }>,
): Array<{
  id: string;
  karma_amount: number | null;
  running_total: number;
}> {
  let runningTotal = 0;
  return karma
    .sort((a, b) => (a.id < b.id ? -1 : a.id > b.id ? 1 : 0))
    .map(entry => {
      runningTotal += entry.karma_amount ?? 0;
      return {
        id: entry.id,
        karma_amount: entry.karma_amount,
        running_total: runningTotal,
      };
    });
}

/**
 * Master compute function: combines all derived attributes into a single object.
 * Used by character detail page load function.
 */
export function computeCharacter(
  char: CharacterRow,
  repData: RepData,
): {
  attributeTotals: Record<string, number>;
  conditionMonitor: { mental: number; stun: number; physical: number };
  initiative: number;
  movement: { walk: number; run: number };
  totalKarma: number;
  formattedMoney: { gold: number; silver: number; copper: number };
  karmaLedgerRunningTotals: Array<{ id: string; karma_amount: number | null; running_total: number }>;
} {
  const totalKarma = repData.karma.reduce((sum, entry) => sum + (entry.karma_amount ?? 0), 0);

  return {
    attributeTotals: computeAttributeTotals(char),
    conditionMonitor: computeConditionMonitor(char),
    initiative: computeInitiative(char),
    movement: computeMovement(char),
    totalKarma,
    formattedMoney: {
      gold: char.money_gold ?? 0,
      silver: char.money_silver ?? 0,
      copper: char.money_copper ?? 0,
    },
    karmaLedgerRunningTotals: computeKarmaLedgerRunningTotals(repData.karma),
  };
}
