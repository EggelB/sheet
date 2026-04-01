<script lang="ts">
  import type { LayoutData } from './$types';
  import { signOut } from '@auth/sveltekit/client';

  let { data, children }: { data: LayoutData; children: any } = $props();
  
  async function handleSignOut() {
    await signOut();
  }
</script>

<nav class="navbar">
  <div class="nav-container">
    <div class="nav-links">
      <a href="/characters">Characters</a>
      <a href="/library">Library</a>
      {#if data.player.is_gm === 1}
        <a href="/admin/assign">Assign Characters</a>
      {/if}
    </div>
    <div class="nav-user">
      <span>{data.session.user?.name || 'User'}</span>
      <button onclick={handleSignOut}>Sign Out</button>
    </div>
  </div>
</nav>

<main class="app-content">
  {@render children()}
</main>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }

  .navbar {
    background-color: #333;
    color: white;
    padding: 1rem 0;
    border-bottom: 1px solid #555;
  }

  .nav-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 1rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .nav-links {
    display: flex;
    gap: 2rem;
  }

  .nav-links a {
    color: white;
    text-decoration: none;
  }

  .nav-links a:hover {
    text-decoration: underline;
  }

  .nav-user {
    display: flex;
    gap: 1rem;
    align-items: center;
  }

  .nav-user button {
    background-color: #555;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    cursor: pointer;
    border-radius: 4px;
  }

  .nav-user button:hover {
    background-color: #777;
  }

  .app-content {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }
</style>
