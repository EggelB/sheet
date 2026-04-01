<script lang="ts">
  import type { PageData } from './$types';

  let { data }: { data: PageData } = $props();
</script>

<h1>Assign Characters</h1>

{#if data.unclaimedCharacters.length === 0}
  <p>All characters have been assigned.</p>
{:else}
  {#each data.unclaimedCharacters as character}
    <form method="POST" action="?/assign" class="assign-row">
      <input type="hidden" name="characterId" value={character.id} />
      <span class="char-name">{character.char_name}</span>
      <select name="playerId" required>
        <option value="" disabled selected>Select player…</option>
        {#each data.players as player}
          <option value={player.id}>{player.username}</option>
        {/each}
      </select>
      <button type="submit">Assign</button>
    </form>
  {/each}
{/if}
