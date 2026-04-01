<script lang="ts">
  import type { PageData, ActionData } from './$types';
  import CatalogForm from '$lib/components/CatalogForm.svelte';

  let { data, form }: { data: PageData; form: ActionData } = $props();
</script>

<nav><a href="/library/{data.catalog}">&larr; {data.config.label}</a></nav>
<h1>Add {data.config.label} Entry</h1>

<CatalogForm config={data.config} {form} action="?/create" cancelHref="/library/{data.catalog}" />
