import { SvelteKitAuth } from '@auth/sveltekit';
import Discord from '@auth/sveltekit/providers/discord';
import { getDb } from '$lib/db';

function e(cf: Record<string, string> | undefined, key: string): string {
  return cf?.[key] ?? process.env[key] ?? '';
}

export const { handle: authHandle, signIn, signOut } = SvelteKitAuth(async (event) => {
  const cf = event.platform?.env as Record<string, string> | undefined;

  return {
    trustHost: true,
    providers: [
      Discord({
        clientId: e(cf, 'DISCORD_CLIENT_ID'),
        clientSecret: e(cf, 'DISCORD_CLIENT_SECRET'),
      }),
    ],
    secret: e(cf, 'AUTH_SECRET'),

    callbacks: {
      async jwt({ token, account, profile }) {
        if (account?.providerAccountId && profile) {
          const dp = profile as {
            id: string;
            username: string;
            global_name?: string | null;
            avatar?: string | null;
          };

          const db = await getDb(cf);
          await db.execute({
            sql: `
              INSERT INTO players
                (id, username, display_name, avatar, is_gm, created_at, updated_at)
              VALUES
                (?, ?, ?, ?, 0, datetime('now'), datetime('now'))
              ON CONFLICT(id) DO UPDATE SET
                username     = excluded.username,
                display_name = excluded.display_name,
                avatar       = excluded.avatar,
                updated_at   = datetime('now')
            `,
            args: [
              account.providerAccountId,
              dp.username,
              dp.global_name ?? null,
              dp.avatar ?? null,
            ],
          });

          token.sub = account.providerAccountId;
        }
        return token;
      },

      async session({ session, token }) {
        session.user.id = token.sub!;
        return session;
      },
    },
  };
});
