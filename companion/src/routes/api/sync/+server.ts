import type { RequestEvent } from '@sveltejs/kit';
import { getDb } from '$lib/db';
import { syncWrite, SyncError } from '$lib/sync-write';
import type { SyncPayload } from '$lib/sync-write';

const REQUIRED_REPEATING_KEYS = [
  'skills',
  'mutations',
  'adept_powers',
  'spells',
  'foci',
  'weapons',
  'equipment',
  'contacts',
  'karma',
  'milestones',
] as const;

const CORS_ORIGIN = 'https://app.roll20.net';
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': CORS_ORIGIN,
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-Campaign-Secret',
};

function jsonResp(body: unknown, status: number): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 
      'Content-Type': 'application/json',
      ...CORS_HEADERS,
    },
  });
}

/**
 * Timing-safe comparison: SHA-256 hash the incoming plaintext, then XOR every
 * byte of both 64-char hex strings. Loop always runs to completion — no
 * short-circuit regardless of first mismatch (prevents timing oracle).
 */
async function timingSafeHexCompare(
  incoming: string,
  storedHex: string,
): Promise<boolean> {
  const hashBuffer = await crypto.subtle.digest(
    'SHA-256',
    new TextEncoder().encode(incoming),
  );
  const incomingHex = Array.from(new Uint8Array(hashBuffer))
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');

  // Both are always 64-char hex strings — length mismatch = corrupted stored hash
  if (incomingHex.length !== storedHex.length) return false;

  const a = new TextEncoder().encode(incomingHex);
  const b = new TextEncoder().encode(storedHex);
  let diff = 0;
  for (let i = 0; i < a.length; i++) {
    diff |= a[i] ^ b[i];
  }
  return diff === 0;
}

export async function POST({ request, platform }: RequestEvent): Promise<Response> {
  // 1b. Body size guard — application-level 1 MB ceiling
  const contentLength = request.headers.get('content-length');
  if (contentLength !== null && parseInt(contentLength, 10) > 1_048_576) {
    return jsonResp({ ok: false, error: 'Payload too large' }, 413);
  }

  // 1c. Content-Type guard
  if (!request.headers.get('content-type')?.includes('application/json')) {
    return jsonResp({ ok: false, error: 'Unsupported Media Type' }, 415);
  }

  // 1d. Body parse
  let body: Record<string, unknown>;
  try {
    body = await request.json();
  } catch {
    return jsonResp({ ok: false, error: 'Invalid JSON' }, 400);
  }

  // 1e. Required-field validation — checked in spec order, first failure wins
  if (!body.campaign_db_id || typeof body.campaign_db_id !== 'string') {
    return jsonResp({ ok: false, error: 'campaign_db_id required' }, 400);
  }
  if (!('char_db_id' in body)) {
    return jsonResp({ ok: false, error: 'char_db_id required' }, 400);
  }
  if (
    typeof body.sync_version_from !== 'number' ||
    !Number.isInteger(body.sync_version_from) ||
    body.sync_version_from < 0 ||
    !Number.isSafeInteger(body.sync_version_from)
  ) {
    return jsonResp(
      { ok: false, error: 'sync_version_from must be a non-negative integer' },
      400,
    );
  }
  if (
    !body.scalars ||
    typeof body.scalars !== 'object' ||
    Array.isArray(body.scalars)
  ) {
    return jsonResp({ ok: false, error: 'scalars required' }, 400);
  }
  if (
    !body.repeating ||
    typeof body.repeating !== 'object' ||
    Array.isArray(body.repeating)
  ) {
    return jsonResp({ ok: false, error: 'repeating required' }, 400);
  }

  const rep = body.repeating as Record<string, unknown>;
  for (const key of REQUIRED_REPEATING_KEYS) {
    if (!(key in rep)) {
      return jsonResp({ ok: false, error: `repeating.${key} required` }, 400);
    }
    if (!Array.isArray(rep[key])) {
      return jsonResp(
        { ok: false, error: `repeating.${key} must be an array` },
        400,
      );
    }
  }

  // 1f. Secret header presence check
  // Same 401 body for all unauthorized states — never distinguish missing vs wrong
  const incomingSecret = request.headers.get('X-Campaign-Secret');
  if (!incomingSecret) {
    return jsonResp({ ok: false, error: 'Unauthorized' }, 401);
  }

  // 1g. Campaign lookup
  let db: Awaited<ReturnType<typeof getDb>>;
  try {
    db = await getDb(platform?.env);
  } catch (err) {
    console.error('[sync] db init error:', err);
    return jsonResp({ ok: false, error: 'Internal server error' }, 500);
  }

  let campaignRow: { campaign_secret_hash: string } | undefined;
  try {
    const result = await db.execute({
      sql: 'SELECT campaign_secret_hash FROM campaigns WHERE id = ?',
      args: [body.campaign_db_id as string],
    });
    campaignRow = result.rows[0] as unknown as
      | { campaign_secret_hash: string }
      | undefined;
  } catch (err) {
    console.error('[sync] campaign lookup error:', err);
    return jsonResp({ ok: false, error: 'Internal server error' }, 500);
  }

  // Return 401 (not 404) — never disclose whether a campaign ID is valid (prevents enumeration)
  if (!campaignRow) {
    return jsonResp({ ok: false, error: 'Unauthorized' }, 401);
  }

  // 1h. Timing-safe secret verification
  const secretValid = await timingSafeHexCompare(
    incomingSecret,
    campaignRow.campaign_secret_hash,
  );
  if (!secretValid) {
    return jsonResp({ ok: false, error: 'Unauthorized' }, 401);
  }

  // 1i. Invoke sync write logic
  try {
    const result = await syncWrite(
      db,
      body as unknown as SyncPayload,
      body.campaign_db_id as string,
    );
    // Response contract: { ok: true, char_db_id, sync_version }
    // Roll20 handler reads response.char_db_id and response.sync_version — key names are binding
    return jsonResp(
      {
        ok: true,
        char_db_id: result.char_db_id,
        sync_version: result.sync_version,
      },
      200,
    );
  } catch (err) {
    if (err instanceof SyncError) {
      return jsonResp({ ok: false, error: err.message }, err.status);
    }
    console.error('[sync] error:', err);
    return jsonResp({ ok: false, error: 'Internal server error' }, 500);
  }
}

export function OPTIONS(): Response {
  return new Response(null, {
    status: 204,
    headers: CORS_HEADERS,
  });
}
