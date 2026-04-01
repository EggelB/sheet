// companion/scripts/seed-campaign.ts
// Usage: npm run seed-campaign -- --name "Campaign Name" --secret "plaintext_secret"

import crypto from 'node:crypto';
import { createClient } from '@libsql/client/node';
import { readFileSync, existsSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

// Load .dev.vars into process.env (Node 18 compat)
const __dirname = dirname(fileURLToPath(import.meta.url));
const devVarsPath = resolve(__dirname, '../.dev.vars');
if (existsSync(devVarsPath)) {
  for (const line of readFileSync(devVarsPath, 'utf-8').split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const eq = trimmed.indexOf('=');
    if (eq > 0) process.env[trimmed.slice(0, eq)] ??= trimmed.slice(eq + 1);
  }
}

// Uses @libsql/client/node (NOT /web) — this script runs in Node.js (tsx),
// not a CF Worker. /node uses net/tls; /web requires Fetch API.

function parseArgs(): { name: string; secret: string } {
  const args = process.argv.slice(2);
  const get = (flag: string): string | undefined => {
    const idx = args.indexOf(flag);
    return idx !== -1 ? args[idx + 1] : undefined;
  };
  const name = get('--name');
  const secret = get('--secret');
  if (!name || !secret) {
    console.error(
      'Usage: npm run seed-campaign -- --name "Campaign Name" --secret "plaintext_secret"',
    );
    process.exit(1);
  }
  return { name, secret };
}

async function main(): Promise<void> {
  const { name, secret } = parseArgs();

  const hash = crypto.createHash('sha256').update(secret).digest('hex');
  const id = crypto.randomUUID();

  if (!process.env.TURSO_DATABASE_URL) {
    console.error(
      'TURSO_DATABASE_URL not set. Run with --env-file=.dev.vars or set env vars.',
    );
    process.exit(1);
  }

  const db = createClient({
    url: process.env.TURSO_DATABASE_URL,
    authToken: process.env.TURSO_AUTH_TOKEN,
  });

  try {
    await db.execute({
      sql: `INSERT INTO campaigns (id, name, campaign_secret_hash, created_at) VALUES (?, ?, ?, datetime('now'))`,
      args: [id, name, hash],
    });
  } finally {
    db.close();
  }

  console.log(`Campaign seeded. ID: ${id}`);
  console.log('');
  console.log('Next steps:');
  console.log(`  1. Set attr_campaign_db_id in Roll20 to: ${id}`);
  console.log(
    `  2. Ensure CAMPAIGN_SECRET in .dev.vars (and CF Pages env) equals: ${secret}`,
  );
}

main().catch((err: unknown) => {
  console.error('Seed failed:', err);
  process.exit(1);
});
