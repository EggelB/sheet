<script lang="ts">
  import type { PageData, ActionData } from './$types';
  import CatalogForm from '$lib/components/CatalogForm.svelte';

  let { data, form }: { data: PageData; form: ActionData } = $props();

  let confirming = $state(false);
</script>

<nav><a href="/library/{data.catalog}">← {data.config.label}</a></nav>

<h1>Edit {data.config.label} — {data.item.name}</h1>

<CatalogForm
  config={data.config}
  entry={data.item}
  {form}
  action="?/update"
  cancelHref="/library/{data.catalog}"
/>

<section class="delete-section">
  <h2>Delete Entry</h2>

  {#if confirming}
    <p>Are you sure you want to delete <strong>{data.item.name}</strong>? This cannot be undone.</p>
    <form method="POST" action="?/delete" style="display: inline-flex; gap: 0.5rem; align-items: center;">
      <button type="submit" class="btn-danger">Yes, delete</button>
      <button type="button" class="btn-secondary" onclick={() => (confirming = false)}>Cancel</button>
    </form>
  {:else}
    <button type="button" class="btn-danger-outline" onclick={() => (confirming = true)}>Delete entry</button>
  {/if}
</section>

<style>
  .delete-section {
    margin-top: 3rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border, #e0e0e0);
  }
  .delete-section h2 { font-size: 1rem; color: var(--text-muted, #666); margin-bottom: 0.75rem; }
</style>
