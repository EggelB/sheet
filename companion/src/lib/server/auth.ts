import { error } from '@sveltejs/kit';
import { getDb } from '$lib/db';
import type { Client } from '@libsql/client';

/**
 * Validates the current session belongs to a GM player.
 * Returns the DB client for downstream reuse.
 *
 * Use in form actions where parent() layout data is unavailable.
 */
export async function requireGm(
  locals: App.Locals,
  platform: App.Platform | undefined
): Promise<{ db: Client; userId: string }> {
  const session = await locals.auth();
  if (!session?.user?.id) throw error(401, 'Unauthorized');

  const db = await getDb(platform?.env);
  const result = await db.execute({
    sql: 'SELECT is_gm FROM players WHERE id = ?',
    args: [session.user.id],
  });
  if ((result.rows[0] as unknown as { is_gm: number } | undefined)?.is_gm !== 1) {
    throw error(403, 'Forbidden');
  }

  return { db, userId: session.user.id };
}
