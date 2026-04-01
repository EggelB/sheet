<script lang="ts">
  import type { PageData } from './$types';

  interface Props {
    data: PageData;
  }

  let { data }: Props = $props();

  // Client-side state — reset when catalog changes
  let searchTerm = $state('');
  let activeFilters = $state<Record<string, string>>({});
  let expandedItemId = $state<number | null>(null);

  $effect(() => {
    activeFilters = Object.fromEntries(data.config.filterFields.map((f: string) => [f, 'all']));
    searchTerm = '';
    expandedItemId = null;
  });

  // Derived: filtered items based on search and filter selections
  let filteredItems = $derived.by(() => {
    return (data.items as any[]).filter((item) => {
      // Search filter
      const searchMatch = item.name
        ?.toLowerCase()
        .includes(searchTerm.toLowerCase()) ?? true;
      if (!searchMatch) return false;

      // Field filters
      for (const field of data.config.filterFields) {
        const filterValue = activeFilters[field];
        if (filterValue !== 'all' && item[field] !== filterValue) {
          return false;
        }
      }

      return true;
    });
  });

  function toggleExpanded(itemId: number) {
    expandedItemId = expandedItemId === itemId ? null : itemId;
  }
</script>

<div class="catalog-container">
  <div class="header-section">
    <h1>{data.config.label}</h1>
    {#if data.isGm}
      <a href="/library/{data.catalog}/new" class="new-item-btn">+ New Item</a>
    {/if}
  </div>

  <!-- Search and Filters -->
  <div class="controls">
    <div class="search-box">
      <input
        type="text"
        placeholder="Search by name..."
        bind:value={searchTerm}
      />
    </div>

    {#if data.config.filterFields.length > 0}
      <div class="filters">
        {#each data.config.filterFields as field}
          <div class="filter-group">
            <label for="filter-{field}">{field}</label>
            <select id="filter-{field}" bind:value={activeFilters[field]}>
              <option value="all">All</option>
              {#each data.filterValues[field] ?? [] as value}
                <option value={value}>{value}</option>
              {/each}
            </select>
          </div>
        {/each}
      </div>
    {/if}
  </div>

  <!-- Result count -->
  <p class="result-count">
    Showing {filteredItems.length} of {data.items.length}
    {data.items.length === 1 ? 'entry' : 'entries'}
  </p>

  <!-- Table -->
  <table class="catalog-table">
    <thead>
      <tr>
        <th></th>
        {#each data.config.listColumns as col}
          <th>{col.label}</th>
        {/each}
        {#if data.isGm}
          <th class="actions-header">Actions</th>
        {/if}
      </tr>
    </thead>
    <tbody>
      {#each filteredItems as item (item.id)}
        <tr class={expandedItemId === item.id ? 'expanded' : ''}>
          <td class="expand-cell">
            {#if data.config.detailFields.length > 0}
              <button
                onclick={() => toggleExpanded(item.id)}
                class="expand-btn"
                aria-label={expandedItemId === item.id ? 'Collapse' : 'Expand'}
              >
                {expandedItemId === item.id ? '▼' : '▶'}
              </button>
            {/if}
          </td>
          {#each data.config.listColumns as col}
            <td>{item[col.key] ?? '—'}</td>
          {/each}
          {#if data.isGm}
            <td class="actions-cell">
              <a href="/library/{data.catalog}/{item.id}/edit" class="action-link">Edit</a>
            </td>
          {/if}
        </tr>

        {#if expandedItemId === item.id && data.config.detailFields.length > 0}
          <tr class="detail-row">
            <td colspan={data.config.listColumns.length + 1}>
              <div class="detail-panel">
                {#if data.config.table === 'ref_spirits'}
                  <div class="spirit-stat-block">
                    {#each data.config.detailFields.filter((f) => f.key.startsWith('formula_')) as field}
                      <div class="spirit-stat">
                        <span class="stat-label">{field.label}</span>
                        <span class="stat-value">{item[field.key] ?? '—'}</span>
                      </div>
                    {/each}
                  </div>
                  {#each data.config.detailFields.filter((f) => !f.key.startsWith('formula_')) as field}
                    <div class="detail-field">
                      <strong>{field.label}:</strong>
                      <span>{item[field.key] ?? '—'}</span>
                    </div>
                  {/each}
                {:else}
                  {#each data.config.detailFields as field}
                    <div class="detail-field">
                      <strong>{field.label}:</strong>
                      <span>{item[field.key] ?? '—'}</span>
                    </div>
                  {/each}
                {/if}
              </div>
            </td>
          </tr>
        {/if}
      {/each}
    </tbody>
  </table>

  {#if filteredItems.length === 0}
    <p class="empty-state">No entries match your search.</p>
  {/if}
</div>

<style>
  .catalog-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  .header-section {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
  }

  h1 {
    margin: 0;
    color: #333;
  }

  .new-item-btn {
    padding: 0.75rem 1.5rem;
    background-color: #333;
    color: white;
    text-decoration: none;
    border-radius: 4px;
    font-weight: 500;
    transition: background-color 0.2s ease;
  }

  .new-item-btn:hover {
    background-color: #555;
  }

  .controls {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-bottom: 1.5rem;
    padding: 1rem;
    background-color: #f5f5f5;
    border-radius: 4px;
  }

  .search-box {
    display: flex;
  }

  .search-box input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 1rem;
  }

  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
  }

  .filter-group {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .filter-group label {
    font-weight: 500;
    font-size: 0.875rem;
    color: #555;
  }

  .filter-group select {
    padding: 0.4rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    font-size: 0.875rem;
  }

  .result-count {
    margin: 1rem 0;
    color: #666;
    font-size: 0.875rem;
  }

  .catalog-table {
    width: 100%;
    border-collapse: collapse;
    border: 1px solid #ddd;
    background: white;
  }

  .catalog-table thead {
    background-color: #f9f9f9;
    border-bottom: 2px solid #ddd;
  }

  .catalog-table th,
  .catalog-table td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid #eee;
  }

  .catalog-table th {
    font-weight: 600;
    color: #333;
  }

  .expand-cell {
    width: 2rem;
    text-align: center;
    padding: 0.5rem;
  }

  .expand-btn {
    background: none;
    border: none;
    cursor: pointer;
    font-size: 0.875rem;
    padding: 0;
    color: #0066cc;
  }

  .expand-btn:hover {
    color: #0052a3;
  }

  .detail-row {
    background-color: #f9f9f9;
  }

  .detail-panel {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 1rem;
    padding: 1rem;
  }

  .spirit-stat-block {
    display: flex;
    gap: 0.5rem;
    padding: 0.75rem;
    background: #e8eef4;
    border-radius: 4px;
    margin-bottom: 0.75rem;
    grid-column: 1 / -1;
  }

  .spirit-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 3rem;
  }

  .spirit-stat .stat-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #555;
  }

  .spirit-stat .stat-value {
    font-size: 1rem;
    font-weight: 700;
    color: #333;
  }

  .detail-field {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
  }

  .detail-field strong {
    color: #555;
    font-size: 0.875rem;
  }

  .detail-field span {
    color: #333;
    word-break: break-word;
  }

  .empty-state {
    text-align: center;
    color: #999;
    padding: 2rem;
    font-style: italic;
  }

  .actions-header {
    width: 100px;
    text-align: center;
  }

  .actions-cell {
    text-align: center;
    width: 100px;
  }

  .action-link {
    color: #0066cc;
    text-decoration: none;
    font-size: 0.875rem;
    padding: 0.25rem 0.5rem;
    border-radius: 3px;
    transition: background-color 0.2s ease;
  }

  .action-link:hover {
    background-color: #e6f0ff;
    text-decoration: underline;
  }
</style>
