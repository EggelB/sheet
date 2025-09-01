# Phase 1, Sub-Objective 1: Data Modeling Plan (Revised)

This document details the structure of the main character data object, incorporating clarifications and design decisions.

## 1. Character Data Object Schema (Revised)

The schema has been updated based on user feedback to accurately model the character sheet's mechanics.

```javascript
const characterData = {
    description: {
        playerName: "",
        characterName: "",
        age: 0,
        sex: "",
        race: "",
        station: "",
        height: "",
        weight: "",
        notes: ""
    },

    attributes: {
        body: { base: 1, mutations: 0, magic: 0, misc: 0 },
        dexterity: { base: 1, mutations: 0, magic: 0, misc: 0 },
        strength: { base: 1, mutations: 0, magic: 0, misc: 0 },
        charisma: { base: 1, mutations: 0, magic: 0, misc: 0 },
        intelligence: { base: 1, mutations: 0, magic: 0, misc: 0 },
        willpower: { base: 1, mutations: 0, magic: 0, misc: 0 },
        humanity: { base: 100, mutations: 0, magic: 0, misc: 0 },
        magic: { base: 6, mutations: 0, magic: 0, misc: 0 }
    },

    // REVISED: Condition model updated to handle tiered penalties.
    condition: {
        mental:   { light: 0, moderate: 0, serious: 0 }, // Max boxes: light: 2, moderate: 3, serious: 3
        stun:     { light: 0, moderate: 0, serious: 0 },
        physical: { light: 0, moderate: 0, serious: 0 }
    },
    
    // NEW: A base Target Number that can be modified by condition.
    targetNumber: {
        base: 2
    },

    karma: {
        good: 0,
        used: 0
    },
    
    equipment: [],
    contacts: [],
    skills: [],
    mutations: [],
    spells: [],

    // This section is for storing the results of our calculations.
    derived: {
        attributes: {
            reaction: 0
        },
        dice_pools: {
            combat: 0,
            spell: 0,
            control: 0,
            astral: 0
        },
        // NEW: Condition penalties are calculated and stored here.
        condition_penalties: {
            tn: 0,
            initiative: 0
        },
        // NEW: Final TN is derived from base and penalties.
        final_tn: 0,
        initiative: {
            base: 0,
            total: 0
        },
        karma: {
            total: 0,
            pool: 0
        }
    }
};
```

## 2. Calculations Plan (Revised)

The `calculateDerivedStats()` function will be updated with the following logic.

*   **Attribute Totals:** For each attribute: `total = base + mutations + magic + misc`.
*   **Derived Reaction:** `derived.attributes.reaction = Math.floor((attributes.intelligence.total + attributes.dexterity.total) / 2)`.
*   **Dice Pools (Corrected Formulas):**
    *   `derived.dice_pools.combat = Math.floor((attributes.dexterity.total + attributes.intelligence.total + attributes.willpower.total) / 2)`.
    *   `derived.dice_pools.spell = Math.floor((attributes.charisma.total + attributes.intelligence.total + attributes.willpower.total) / 2)`.
    *   `derived.dice_pools.control = derived.attributes.reaction`.
    *   `derived.dice_pools.astral = Math.floor((attributes.intelligence.total + attributes.willpower.total + attributes.magic.total) / 3)`.
*   **Condition Penalties:**
    *   Determine the highest level of damage taken across *any* track (mental, stun, or physical).
    *   If any `serious` box is filled > 0, then `derived.condition_penalties = { tn: 3, initiative: -3 }`.
    *   Else if any `moderate` box is filled > 0, then `derived.condition_penalties = { tn: 2, initiative: -2 }`.
    *   Else if any `light` box is filled > 0, then `derived.condition_penalties = { tn: 1, initiative: -1 }`.
    *   Else, penalties are `{ tn: 0, initiative: 0 }`.
*   **Final Target Number:** `derived.final_tn = targetNumber.base + derived.condition_penalties.tn`.
*   **Initiative:**
    *   `derived.initiative.base = derived.attributes.reaction + derived.condition_penalties.initiative`.
    *   `derived.initiative.total` will be calculated at roll time (`base + dice roll + misc modifiers`).
*   **Karma:**
    *   `derived.karma.total = karma.good - karma.used`.
    *   `derived.karma.pool = Math.floor(derived.karma.total / 10) + 1`.

## 3. Design Decisions Summary

This section documents the key decisions made based on user feedback.

1.  **Dice Pool Formulas:** The formulas implemented in `Test.html` are confirmed to be the correct ones. Combat is based on DEX, Spell is based on CHA.
2.  **Astral Pool:** The Astral dice pool is not a confirmed mechanic and will be excluded from the initial implementation.
3.  **Condition Monitor:** The monitor will be implemented as three tracks (Mental, Stun, Physical), each with three tiers of damage (Light, Moderate, Serious). The penalties to TN and Initiative are determined by the highest tier of damage taken across all tracks, not the total number of boxes.
4.  **Target Number (TN):** TN is a core mechanic. The sheet will have a settable "base TN" which is then modified by condition penalties to produce a "final TN".
