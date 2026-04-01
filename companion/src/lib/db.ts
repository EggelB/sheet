import { createClient } from '@libsql/client/web';
import type { Client } from '@libsql/client';

/**
 * Creates a fresh libSQL client for each request.
 * Issues PRAGMA foreign_keys = ON before returning.
 *
 * @param env - CF Pages platform env (event.platform.env in +server.ts)
 * @returns Client with FK enforcement active
 *
 * IMPORTANT: Use @libsql/client/web (Fetch API) — NOT /node.
 * CF Workers have no Node.js net/tls module; /web uses fetch only.
 */
export async function getDb(env?: Record<string, string>): Promise<Client> {
  // CF Workers: env comes from platform.env. Local dev (wrangler): process.env works via nodejs_compat flag.
  const url = env?.TURSO_DATABASE_URL ?? process.env.TURSO_DATABASE_URL ?? '';
  const authToken = env?.TURSO_AUTH_TOKEN ?? process.env.TURSO_AUTH_TOKEN ?? '';
  const client = createClient({ url, authToken });
  await client.execute('PRAGMA foreign_keys = ON');
  return client;
}
