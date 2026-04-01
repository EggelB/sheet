<script lang="ts">
  import { CATALOG_CONFIG, getAllCatalogSlugs } from '$lib/catalog-config';
  import type { PageData } from './$types';

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();
</script>

<div class="library-container">
  <h1>Library</h1>
  <p>Browse curated catalogs of game elements.</p>

  <div class="catalog-grid">
    {#each getAllCatalogSlugs() as slug}
      {@const config = CATALOG_CONFIG[slug]}
      {@const count = data.catalogCounts[slug] ?? 0}
      <a href="/library/{slug}" class="catalog-card">
        <div class="card-header">{config.label}</div>
        <div class="card-count">{count} {count === 1 ? 'entry' : 'entries'}</div>
      </a>
    {/each}
  </div>
</div>

<style>
  .library-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  h1 {
    margin-top: 0;
    margin-bottom: 0.5rem;
    color: #333;
  }

  p {
    margin: 0 0 2rem 0;
    color: #666;
  }

  .catalog-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 1rem;
  }

  .catalog-card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 2rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 8px;
    color: white;
    text-decoration: none;
    transition: transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  }

  .catalog-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  }

  .card-header {
    font-size: 1.25rem;
    font-weight: 600;
    margin-bottom: 0.5rem;
    text-align: center;
  }

  .card-count {
    font-size: 0.875rem;
    opacity: 0.9;
  }
</style>
