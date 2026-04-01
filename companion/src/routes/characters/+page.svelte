<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();

  function formatSyncedAt(raw: string | null): string {
    if (!raw) return 'Never';
    // SQLite datetime('now') stores 'YYYY-MM-DD HH:MM:SS' UTC
    return raw.replace('T', ' ').slice(0, 16) + ' UTC';
  }
</script>

<svelte:head>
  <title>Characters</title>
</svelte:head>

<div class="container">
  <h1>Characters</h1>

  {#if data.characters.length === 0}
    <p class="empty-state">No characters assigned.</p>
  {:else}
    <ul class="character-list">
      {#each data.characters as char}
        <li>
          <a href="/characters/{char.id}" class="character-card">
            <strong>{char.char_name ?? '(Unnamed)'}</strong>
            <span class="campaign">{char.campaign_name}</span>
            <span class="synced">Last synced: {formatSyncedAt(char.synced_at)}</span>
          </a>
        </li>
      {/each}
    </ul>
  {/if}
</div>

<style>
  .container {
    max-width: 600px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  h1 {
    font-size: 2rem;
    margin-bottom: 2rem;
    color: #333;
  }

  .empty-state {
    color: #666;
    font-style: italic;
    margin-top: 1rem;
  }

  .character-list {
    list-style: none;
    padding: 0;
    margin: 0;
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }

  .character-card {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: #f9f9f9;
    text-decoration: none;
    color: inherit;
    transition: all 0.2s ease-in-out;
  }

  .character-card:hover {
    background: #f0f0f0;
    border-color: #999;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  }

  .character-card strong {
    font-size: 1.1rem;
    color: #000;
  }

  .campaign {
    font-size: 0.9rem;
    color: #666;
  }

  .synced {
    font-size: 0.85rem;
    color: #999;
  }
</style>
