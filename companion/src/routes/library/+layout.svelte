<script lang="ts">
  import { page } from '$app/state';
  import { CATALOG_CONFIG, getAllCatalogSlugs } from '$lib/catalog-config';

  let { children } = $props();

  const activeSlug = $derived(
    page.url.pathname.split('/').filter(Boolean)[1] ?? null
  );

  const allSlugs = getAllCatalogSlugs();
</script>

<div class="library-container">
  <nav class="library-subnav" aria-label="Game Library sections">
    <a
      href="/library"
      class="subnav-link"
      class:active={page.url.pathname === '/library'}
      aria-current={page.url.pathname === '/library' ? 'page' : undefined}
    >
      All Catalogs
    </a>
    {#each allSlugs as slug}
      {@const config = CATALOG_CONFIG[slug]}
      {@const isActive = activeSlug === slug}
      <a
        href="/library/{slug}"
        class="subnav-link"
        class:active={isActive}
        aria-current={isActive ? 'page' : undefined}
      >
        {config.label}
      </a>
    {/each}
  </nav>

  <div class="library-content">
    {@render children()}
  </div>
</div>

<style>
  .library-container {
    display: flex;
    flex-direction: column;
    max-width: 1200px;
    margin: 0 auto;
  }

  .library-subnav {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    padding: 1rem;
    background-color: #f0f0f0;
    border-bottom: 2px solid #ddd;
    margin: 0 1rem;
  }

  .subnav-link {
    padding: 0.5rem 1rem;
    background-color: white;
    color: #333;
    text-decoration: none;
    border: 1px solid #ccc;
    border-radius: 4px;
    transition: all 0.2s ease;
  }

  .subnav-link:hover {
    background-color: #e8e8e8;
    border-color: #999;
  }

  .subnav-link.active {
    background-color: #333;
    color: white;
    border-color: #333;
    font-weight: 600;
  }

  .library-content {
    flex: 1;
  }
</style>
