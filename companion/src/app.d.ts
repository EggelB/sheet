// See https://kit.svelte.dev/docs/types#app

import type { DefaultSession } from '@auth/sveltekit';

declare module '@auth/sveltekit' {
  interface Session {
    user: DefaultSession['user'] & { id: string };
  }
}

declare global {
  namespace App {
    interface Platform {
      env: {
        TURSO_DATABASE_URL: string;
        TURSO_AUTH_TOKEN: string;
        CAMPAIGN_SECRET: string;
        AUTH_SECRET: string;
        DISCORD_CLIENT_ID: string;
        DISCORD_CLIENT_SECRET: string;
      };
    }
    interface Locals {
      auth: () => Promise<import('@auth/sveltekit').Session | null>;
    }
  }
}

export {};
