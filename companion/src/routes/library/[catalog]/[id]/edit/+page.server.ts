import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { getDb } from '$lib/db';
import { getCatalogConfig } from '$lib/catalog-config';
import { requireGm } from '$lib/server/auth';

export const load: PageServerLoad = async ({ params, parent, platform }) => {
  // Validate GM access
  const { player } = await parent();
  if (player.is_gm !== 1) {
    throw error(403, 'Forbidden');
  }

  // Validate and load catalog config
  let config;
  try {
    config = getCatalogConfig(params.catalog);
  } catch {
    throw error(404, 'Catalog not found');
  }

  // Fetch the existing item
  const db = await getDb(platform?.env);
  const result = await db.execute({
    sql: `SELECT * FROM ${config.table} WHERE id = ?`,
    args: [parseInt(params.id, 10)],
  });

  const item = result.rows[0];
  if (!item) {
    throw error(404, 'Item not found');
  }

  return {
    catalog: params.catalog,
    id: parseInt(params.id, 10),
    config,
    item,
  };
};

export const actions: Actions = {
  update: async ({ params, request, locals, platform }) => {
    // GM validation + db access
    const { db } = await requireGm(locals, platform);

    // Get catalog config
    let config;
    try {
      config = getCatalogConfig(params.catalog);
    } catch {
      throw error(404, 'Catalog not found');
    }

    const itemId = parseInt(params.id, 10);

    // Parse form data
    const formData = await request.formData();
    const values: Record<string, any> = {};
    const errors: Record<string, string> = {};

    // Validate and extract form fields
    for (const field of config.formFields) {
      const rawValue = formData.get(field.key);
      const stringValue = rawValue ? String(rawValue).trim() : '';

      // Required: name field
      if (field.key === 'name') {
        if (!stringValue) {
          errors[field.key] = 'Name is required';
          continue;
        }
      }

      // Type conversion
      if (field.type === 'number') {
        const parsed = parseFloat(stringValue);
        values[field.key] = Number.isFinite(parsed) ? parsed : null;
      } else {
        values[field.key] = stringValue || null;
      }
    }

    if (Object.keys(errors).length > 0) {
      return { errors };
    }

    // Build UPDATE statement — column names from trusted config only
    const setClauses = Object.keys(values).map((k) => `${k} = ?`);
    setClauses.push("updated_at = datetime('now')");
    const vals = [...Object.values(values), itemId];

    try {
      await db.execute({
        sql: `UPDATE ${config.table} SET ${setClauses.join(', ')} WHERE id = ?`,
        args: vals,
      });
    } catch (err: any) {
      if (err.message?.includes('UNIQUE constraint failed')) {
        return { errors: { name: 'An entry with this name already exists' } };
      }
      throw error(500, 'Database error');
    }

    throw redirect(303, `/library/${params.catalog}`);
  },

  delete: async ({ params, locals, platform }) => {
    // GM validation + db access
    const { db } = await requireGm(locals, platform);

    // Get catalog config
    let config;
    try {
      config = getCatalogConfig(params.catalog);
    } catch {
      throw error(404, 'Catalog not found');
    }

    const itemId = parseInt(params.id, 10);

    try {
      await db.execute({
        sql: `DELETE FROM ${config.table} WHERE id = ?`,
        args: [itemId],
      });
    } catch (err) {
      throw error(500, 'Database error');
    }

    throw redirect(303, `/library/${params.catalog}`);
  },
};
