import { defineConfig } from 'vite';
import { sveltekit } from '@sveltejs/kit/vite';

import { readFileSync } from 'node:fs';

function loadDevVars() {
  try {
    const text = readFileSync('.dev.vars', 'utf-8');
    for (const line of text.split('\n')) {
      const m = line.match(/^([A-Z_]+)=(.+)$/);
      if (m) process.env[m[1]] = m[2];
    }
  } catch { /* file may not exist in CI */ }
}

loadDevVars();

export default defineConfig({
  plugins: [sveltekit()]
});
