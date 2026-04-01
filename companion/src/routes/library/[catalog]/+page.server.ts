import { error, redirect } from '@sveltejs/kit';
import type { PageServerLoad, Actions } from './$types';
import { getDb } from '$lib/db';
import { getCatalogConfig } from '$lib/catalog-config';
import { requireGm } from '$lib/server/auth';

export const load: PageServerLoad = async ({ params, platform, parent }) => {
  // Get player info for isGm flag
  const { player } = await parent();

  // Validate catalog slug against config
  let config;
  try {
    config = getCatalogConfig(params.catalog);
  } catch {
    throw error(404, 'Catalog not found');
  }

  const db = await getDb(platform?.env);

  // Load all rows + distinct filter values in parallel
  const filterQueries = config.filterFields.map((field) =>
    db.execute(
      `SELECT DISTINCT ${field} FROM ${config.table} WHERE ${field} IS NOT NULL ORDER BY ${field} ASC`,
    ),
  );

  const [rowsResult, ...filterResults] = await Promise.all([
    db.execute(`SELECT * FROM ${config.table} ORDER BY name ASC`),
    ...filterQueries,
  ]);

  const items = rowsResult.rows;

  const filterValues: Record<string, string[]> = {};
  config.filterFields.forEach((field, i) => {
    filterValues[field] = filterResults[i].rows
      .map((row: any) => row[field] as string)
      .filter((val): val is string => val != null);
  });

  return {
    catalog: params.catalog,
    config,
    items,
    filterValues,
    isGm: player.is_gm === 1,
  };
};

export const actions: Actions = {
  delete: async ({ request, locals, params, platform }) => {
    const { db } = await requireGm(locals, platform);

    const config = getCatalogConfig(params.catalog);
    if (!config) throw error(404, 'Unknown catalog section');

    const formData = await request.formData();
    const id = formData.get('id');
    if (!id || typeof id !== 'string' || id.trim() === '') {
      throw error(400, 'Missing or invalid entry id');
    }

    await db.execute({
      sql: `DELETE FROM ${config.table} WHERE id = ?`,
      args: [id],
    });

    throw redirect(303, `/library/${params.catalog}`);
  },
};
