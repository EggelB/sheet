import { error } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ parent }) => {
  const { player } = await parent();
  if (player.is_gm !== 1) {
    throw error(403, 'Forbidden');
  }

  return {};
};
