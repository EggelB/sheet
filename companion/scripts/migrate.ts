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

async function main(): Promise<void> {
  // Guard: require explicit --force flag to prevent accidental re-run
  // on a populated database.
  //   Usage: npm run migrate -- --force
  const force = process.argv.includes('--force');
  if (!force) {
    console.error('Pass --force to execute migration.');
    process.exit(1);
  }

  const url = process.env.TURSO_DATABASE_URL!;
  const authToken = process.env.TURSO_AUTH_TOKEN!;
  const schemaPath = resolve(__dirname, '../db/schema.sql');
  const sql = readFileSync(schemaPath, 'utf-8');

  const db = createClient({ url, authToken });

  // Strip SQL line comments first (avoids ';' inside comments causing bad splits)
  const cleaned = sql.replace(/--.*$/gm, '');
  // Split on statement boundaries and execute sequentially
  const statements = cleaned.split(';').map(s => s.trim()).filter(Boolean);
  for (const stmt of statements) {
    await db.execute(stmt);
  }

  console.log(`Migration complete — ${statements.length} statements executed.`);
  db.close();
}

main().catch(e => { console.error(e); process.exit(1); });
