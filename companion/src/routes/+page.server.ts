import { redirect } from '@sveltejs/kit';
import { getDb } from '$lib/db';
import type { PageServerLoad } from './$types';

export const load: PageServerLoad = async ({ parent, platform }) => {
  const { player } = await parent();
  const db = await getDb(platform?.env);
  const result = await db.execute({
    sql: 'SELECT id FROM characters WHERE player_id = ? LIMIT 1',
    args: [player.id],
  });
  if (result.rows.length > 0) throw redirect(303, '/characters');
  return {};
};
