import type { PageServerLoad } from './$types';
import { getDb } from '$lib/db';
import { getAllCatalogSlugs, CATALOG_CONFIG } from '$lib/catalog-config';

export const load: PageServerLoad = async ({ platform }) => {
  const db = await getDb(platform?.env);

  // Run COUNT queries for all catalogs in parallel
  const countPromises = getAllCatalogSlugs().map(async (slug) => {
    const config = CATALOG_CONFIG[slug];
    const result = await db.execute(
      `SELECT COUNT(*) as count FROM ${config.table}`,
    );
    const count = Number((result.rows[0] as unknown as { count: number }).count);
    return { slug, count };
  });

  const counts = await Promise.all(countPromises);

  const catalogCounts: Record<string, number> = {};
  for (const { slug, count } of counts) {
    catalogCounts[slug] = count;
  }

  return {
    catalogCounts,
  };
};
