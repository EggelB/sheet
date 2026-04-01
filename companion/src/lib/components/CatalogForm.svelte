<script lang="ts">
  import type { CatalogEntry } from '$lib/catalog-config';

  interface Props {
    config: CatalogEntry;
    entry?: Record<string, unknown>;
    form?: { errors?: Record<string, string> } | null;
    action: string;
    cancelHref: string;
  }

  let { config, entry = undefined, form = null, action, cancelHref }: Props = $props();
</script>

<form method="POST" {action} class="catalog-form">
  {#each config.formFields as field}
    <div class="field-group">
      <label for={field.key}>{field.label}</label>

      {#if field.type === 'textarea'}
        <textarea id={field.key} name={field.key} rows="4">{entry?.[field.key] ?? ''}</textarea>

      {:else if field.type === 'select'}
        <select id={field.key} name={field.key}>
          <option value="">— select —</option>
          {#each field.options ?? [] as opt}
            <option value={opt} selected={entry?.[field.key] === opt}>{opt}</option>
          {/each}
        </select>

      {:else if field.type === 'number'}
        <input type="number" id={field.key} name={field.key}
          step="any" value={entry?.[field.key] ?? ''} />

      {:else}
        <input type="text" id={field.key} name={field.key}
          value={String(entry?.[field.key] ?? '')} />
      {/if}

      {#if form?.errors?.[field.key]}
        <p class="field-error" role="alert">{form.errors[field.key]}</p>
      {/if}
    </div>
  {/each}

  <div class="form-actions">
    <button type="submit" class="btn-primary">Save</button>
    <a href={cancelHref} class="btn-secondary">Cancel</a>
  </div>
</form>

<style>
  .catalog-form  { max-width: 640px; }
  .field-group   { display: flex; flex-direction: column; gap: 0.25rem; margin-bottom: 1rem; }
  label          { font-weight: bold; font-size: 0.9rem; }
  input, select, textarea { width: 100%; padding: 0.4rem 0.5rem; font-size: 0.95rem; box-sizing: border-box; }
  textarea       { resize: vertical; }
  .field-error   { color: var(--error, #c00); font-size: 0.85rem; margin: 0; }
  .form-actions  { display: flex; gap: 1rem; align-items: center; margin-top: 1.5rem; }
</style>
