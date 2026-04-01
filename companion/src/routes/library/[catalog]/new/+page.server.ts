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

  return {
    catalog: params.catalog,
    config,
  };
};

export const actions: Actions = {
  create: async ({ params, request, locals, platform }) => {
    // GM validation + db access
    const { db } = await requireGm(locals, platform);

    // Get catalog config
    let config;
    try {
      config = getCatalogConfig(params.catalog);
    } catch {
      throw error(404, 'Catalog not found');
    }

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

    // Build INSERT statement
    const keys = Object.keys(values);
    const placeholders = keys.map(() => '?').join(', ');
    const vals = keys.map((k) => values[k]);

    try {
      await db.execute({
        sql: `INSERT INTO ${config.table} (${keys.join(', ')}) VALUES (${placeholders})`,
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
};
