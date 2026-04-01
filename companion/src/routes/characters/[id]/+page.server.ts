import { error } from '@sveltejs/kit';
import type { PageServerLoad } from './$types';
import { getDb } from '$lib/db';
import { computeCharacter } from '$lib/computed';
import type { CharacterRow, RepData } from '$lib/types';

export const load: PageServerLoad = async ({ parent, params, platform }) => {
  const { player } = await parent();
  const db = await getDb(platform?.env);

  // 1. Fetch character scalar row
  const charResult = await db.execute({
    sql: 'SELECT * FROM characters WHERE id = ?',
    args: [params.id],
  });
  if (charResult.rows.length === 0) throw error(404, 'Character not found');

  const character = charResult.rows[0] as unknown as CharacterRow;

  // 2. Access control: owner OR GM
  if (player.is_gm !== 1 && character.player_id !== player.id) {
    throw error(403, 'Forbidden');
  }

  // 3. All 10 rep tables in parallel — one HTTP round-trip each over Turso HTTP transport
  const [
    skills,
    mutations,
    adept_powers,
    spells,
    foci,
    weapons,
    equipment,
    contacts,
    karma,
    milestones,
  ] = await Promise.all([
    db.execute({
      sql: 'SELECT * FROM rep_skills WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_mutations WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_adept_powers WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_spells WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_foci WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_weapons WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_equipment WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_contacts WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_karma WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
    db.execute({
      sql: 'SELECT * FROM rep_milestones WHERE character_id = ? ORDER BY id ASC',
      args: [params.id],
    }),
  ]);

  const repData: RepData = {
    skills: (skills.rows as unknown[]) as unknown as RepData['skills'],
    mutations: (mutations.rows as unknown[]) as unknown as RepData['mutations'],
    adept_powers: (adept_powers.rows as unknown[]) as unknown as RepData['adept_powers'],
    spells: (spells.rows as unknown[]) as unknown as RepData['spells'],
    foci: (foci.rows as unknown[]) as unknown as RepData['foci'],
    weapons: (weapons.rows as unknown[]) as unknown as RepData['weapons'],
    equipment: (equipment.rows as unknown[]) as unknown as RepData['equipment'],
    contacts: (contacts.rows as unknown[]) as unknown as RepData['contacts'],
    karma: (karma.rows as unknown[]) as unknown as RepData['karma'],
    milestones: (milestones.rows as unknown[]) as unknown as RepData['milestones'],
  };

  // 4. Pure computation — no side effects, no DB calls
  const computed = computeCharacter(character, repData);

  return { character, repData, computed };
};
