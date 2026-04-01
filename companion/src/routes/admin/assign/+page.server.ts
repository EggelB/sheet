import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { getDb } from '$lib/db';
import { requireGm } from '$lib/server/auth';

export const load: PageServerLoad = async ({ parent, platform }) => {
  const { player } = await parent();
  if (player.is_gm !== 1) throw error(403, 'Forbidden');

  const db = await getDb(platform?.env);

  const [unclaimedResult, playersResult] = await Promise.all([
    db.execute('SELECT id, char_name FROM characters WHERE player_id IS NULL ORDER BY char_name ASC'),
    db.execute('SELECT id, username FROM players ORDER BY username ASC'),
  ]);

  return {
    unclaimedCharacters: unclaimedResult.rows as unknown as Array<{ id: string; char_name: string }>,
    players: playersResult.rows as unknown as Array<{ id: string; username: string }>,
  };
};

export const actions: Actions = {
  assign: async ({ request, locals, platform }) => {
    const { db } = await requireGm(locals, platform);

    const formData = await request.formData();
    const characterId = formData.get('characterId');
    const playerId = formData.get('playerId');

    if (
      typeof characterId !== 'string' || characterId.length === 0 ||
      typeof playerId !== 'string' || playerId.length === 0
    ) {
      throw error(400, 'Missing required fields');
    }

    await db.execute({
      sql: `UPDATE characters SET player_id = ?, updated_at = datetime('now') WHERE id = ? AND player_id IS NULL`,
      args: [playerId, characterId],
    });

    throw redirect(303, '/admin/assign');
  },
};
