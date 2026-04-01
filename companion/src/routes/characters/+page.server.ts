import type { PageServerLoad } from './$types';
import { getDb } from '$lib/db';

interface CharacterSummary {
  id:            string;
  char_name:     string | null;
  campaign_name: string;
  synced_at:     string | null;
}

export const load: PageServerLoad = async ({ parent, platform }) => {
  const { player } = await parent();
  const db = await getDb(platform?.env);

  const sql = player.is_gm === 1
    ? `SELECT c.id, c.char_name, c.synced_at, ca.name AS campaign_name
         FROM characters c
         JOIN campaigns ca ON c.campaign_id = ca.id
        ORDER BY c.char_name ASC`
    : `SELECT c.id, c.char_name, c.synced_at, ca.name AS campaign_name
         FROM characters c
         JOIN campaigns ca ON c.campaign_id = ca.id
        WHERE c.player_id = ?
        ORDER BY c.char_name ASC`;

  const args = player.is_gm === 1 ? [] : [player.id];
  const result = await db.execute({ sql, args });

  const characters: CharacterSummary[] = (result.rows as unknown[]).map(row => ({
    id:            (row as Record<string, unknown>).id as string,
    char_name:     (row as Record<string, unknown>).char_name as string | null,
    campaign_name: (row as Record<string, unknown>).campaign_name as string,
    synced_at:     (row as Record<string, unknown>).synced_at as string | null,
  }));

  return { characters };
};
