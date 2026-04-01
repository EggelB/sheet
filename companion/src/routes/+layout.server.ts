import { error, redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';
import { getDb } from '$lib/db';

export const load: LayoutServerLoad = async ({ locals, platform }) => {
  const session = await locals.auth();
  if (!session?.user?.id) {
    throw redirect(302, '/auth/signin');
  }

  const db = await getDb(platform?.env);
  const result = await db.execute({
    sql: 'SELECT id, is_gm FROM players WHERE id = ?',
    args: [session.user.id],
  });

  const player = result.rows[0] as unknown as { id: string; is_gm: number } | undefined;
  if (!player) {
    throw error(500, 'Player record missing');
  }

  return {
    session,
    player,
  };
};
