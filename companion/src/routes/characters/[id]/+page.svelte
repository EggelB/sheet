<script lang="ts">
  import type { PageData } from './$types';

  type TabId = 'overview' | 'skills' | 'magic' | 'gear' | 'bio';

  let { data }: { data: PageData } = $props();
  let activeTab: TabId = $state('overview');

  function renderAttributeBox(value: number | null | undefined): string {
    return value !== null && value !== undefined ? String(value) : '—';
  }

  function formatCmInitMod(value: number | null | undefined): string {
    if (value === null || value === undefined) return '—';
    return String(value);
  }
</script>

<svelte:head>
  <title>{data.character.char_name ?? 'Unnamed Character'}</title>
</svelte:head>

<div class="container">
  <header>
    <h1>{data.character.char_name ?? '(Unnamed)'}</h1>
    <p class="sync-meta">
      Sync version {data.character.sync_version} ·
      Last synced: {data.character.synced_at ?? 'never'}
    </p>
  </header>

  <nav class="tab-bar">
    {#each (['overview', 'skills', 'magic', 'gear', 'bio'] as TabId[]) as tab}
      <button
        class:active={activeTab === tab}
        onclick={() => (activeTab = tab)}
      >
        {tab.charAt(0).toUpperCase() + tab.slice(1)}
      </button>
    {/each}
  </nav>

  <main class="tab-content">
    {#if activeTab === 'overview'}
      <section class="overview-section">
        <h2>Attributes</h2>
        <div class="attribute-grid">
          {#each [
            { name: 'BOD', key: 'body' },
            { name: 'DEX', key: 'dex' },
            { name: 'STR', key: 'str' },
            { name: 'CHA', key: 'cha' },
            { name: 'INT', key: 'int' },
            { name: 'WIL', key: 'wil' },
            { name: 'HUM', key: 'hum' },
            { name: 'MAG', key: 'mag' },
          ] as const as Array<{ name: string; key: keyof typeof data.computed.attributeTotals }> as [] }
            let attr
          >
            <div class="attribute-box">
              <span class="attr-label">{attr.name}</span>
              <span class="attr-value">{renderAttributeBox(data.computed.attributeTotals[attr.key])}</span>
            </div>
          {/each}
        </div>

        <h2>Condition Monitor</h2>
        <div class="cm-summary">
          <div class="cm-type">
            <strong>Mental:</strong> {data.computed.conditionMonitor.mental} boxes
            <span class="cm-mod">TN Mod: {formatCmInitMod(data.character.cm_tn_mod)}</span>
          </div>
          <div class="cm-type">
            <strong>Stun:</strong> {data.computed.conditionMonitor.stun} boxes
          </div>
          <div class="cm-type">
            <strong>Physical:</strong> {data.computed.conditionMonitor.physical} boxes
            <span class="cm-overflow">(+{Math.ceil((data.character.body ?? 0) / 2)} overflow)</span>
            <span class="cm-mod">Init Mod: {formatCmInitMod(data.character.cm_init_mod)}</span>
          </div>
        </div>

        <h2>Initiative & Movement</h2>
        <div class="init-movement">
          <div class="stat-box">
            <strong>Initiative:</strong> {data.computed.initiative} + 2d6
          </div>
          <div class="stat-box">
            <strong>Walk:</strong> {data.computed.movement.walk}m
          </div>
          <div class="stat-box">
            <strong>Run:</strong> {data.computed.movement.run}m
          </div>
        </div>

        <h2>Dice Pools</h2>
        <div class="pool-grid">
          {#each [
            { name: 'Spell', value: data.character.pool_spell },
            { name: 'Combat', value: data.character.pool_combat },
            { name: 'Control', value: data.character.pool_control },
            { name: 'Astral', value: data.character.pool_astral },
          ] as pool}
            <div class="pool-box">
              <span class="pool-label">{pool.name}</span>
              <span class="pool-value">{renderAttributeBox(pool.value)}</span>
            </div>
          {/each}
        </div>
      </section>

    {:else if activeTab === 'skills'}
      <section class="skills-section">
        <h2>Skills</h2>
        {#if data.repData.skills.length === 0}
          <p class="empty">No skills recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Rating</th>
                <th>Pool</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repData.skills as skill}
                <tr>
                  <td><strong>{skill.skill_name ?? '—'}</strong></td>
                  <td>{skill.skill_total ?? '—'}</td>
                  <td class="pool-info">
                    {#if skill.skill_linked_attr}
                      {skill.skill_linked_attr}
                    {:else}
                      —
                    {/if}
                  </td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}
      </section>

    {:else if activeTab === 'magic'}
      <section class="magic-section">
        <h2>Spells</h2>
        {#if data.repData.spells.length === 0}
          <p class="empty">No spells recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Force</th>
                <th>Drain</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repData.spells as spell}
                <tr>
                  <td>{spell.spell_name ?? '—'}</td>
                  <td>{spell.spell_force ?? '—'}</td>
                  <td>{spell.spell_drain ?? '—'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}

        <h2>Foci</h2>
        {#if data.repData.foci.length === 0}
          <p class="empty">No foci recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Force</th>
                <th>Bonded</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repData.foci as focus}
                <tr>
                  <td>{focus.focus_name ?? '—'}</td>
                  <td>{focus.focus_type ?? '—'}</td>
                  <td>{focus.focus_force ?? '—'}</td>
                  <td>{focus.focus_bonded ? 'Yes' : 'No'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}

        <h2>Adept Powers</h2>
        {#if data.repData.adept_powers.length === 0}
          <p class="empty">No adept powers recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Level</th>
                <th>Cost</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repData.adept_powers as power}
                <tr>
                  <td>{power.power_name ?? '—'}</td>
                  <td>{power.power_level ?? '—'}</td>
                  <td>{power.power_pp_cost ?? '—'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}

        <h2>Mutations</h2>
        {#if data.repData.mutations.length === 0}
          <p class="empty">No mutations recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Level</th>
                <th>Essence</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repData.mutations as mutation}
                <tr>
                  <td>{mutation.mutation_name ?? '—'}</td>
                  <td>{mutation.mutation_level ?? '—'}</td>
                  <td>{mutation.mutation_essence ?? '—'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}
      </section>

    {:else if activeTab === 'gear'}
      <section class="gear-section">
        <h2>Weapons</h2>
        {#if data.repData.weapons.length === 0}
          <p class="empty">No weapons recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Type</th>
                <th>Damage</th>
                <th>Reach</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repData.weapons as weapon}
                <tr>
                  <td>{weapon.weapon_name ?? '—'}</td>
                  <td>{weapon.weapon_type ?? '—'}</td>
                  <td>{weapon.weapon_damage ?? '—'}</td>
                  <td>{weapon.weapon_reach ?? '—'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}

        <h2>Equipment</h2>
        {#if data.repData.equipment.length === 0}
          <p class="empty">No equipment recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repData.equipment as equip}
                <tr>
                  <td>{equip.equip_name ?? '—'}</td>
                  <td>{equip.equip_description ?? '—'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}

        <h2>Money</h2>
        <div class="money-display">
          <div class="money-item">
            <span class="money-label">Gold:</span>
            <span class="money-value">{data.computed.formattedMoney.gold}¥</span>
          </div>
          <div class="money-item">
            <span class="money-label">Silver:</span>
            <span class="money-value">{data.computed.formattedMoney.silver}¥</span>
          </div>
          <div class="money-item">
            <span class="money-label">Copper:</span>
            <span class="money-value">{data.computed.formattedMoney.copper}¥</span>
          </div>
        </div>
      </section>

    {:else if activeTab === 'bio'}
      <section class="bio-section">
        <h2>Identity</h2>
        <div class="identity-info">
          <div class="identity-item">
            <span class="label">Name:</span>
            <span>{data.character.char_name ?? '—'}</span>
          </div>
          <div class="identity-item">
            <span class="label">Race/Station:</span>
            <span>{data.character.char_race_station ?? '—'}</span>
          </div>
          <div class="identity-item">
            <span class="label">Sex:</span>
            <span>{data.character.char_sex ?? '—'}</span>
          </div>
          <div class="identity-item">
            <span class="label">Age:</span>
            <span>{data.character.char_age ?? '—'}</span>
          </div>
          <div class="identity-item">
            <span class="label">Description:</span>
            <span>{data.character.char_description ?? '—'}</span>
          </div>
          <div class="identity-item">
            <span class="label">Notes:</span>
            <span>{data.character.char_notes ?? '—'}</span>
          </div>
        </div>

        <h2>Karma</h2>
        <div class="karma-header">
          <span>Total Karma Spent: {data.computed.totalKarma}</span>
        </div>
        {#if data.repData.karma.length === 0}
          <p class="empty">No karma entries recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Event</th>
                <th>Amount</th>
                <th>Running Total</th>
              </tr>
            </thead>
            <tbody>
              {#each data.computed.karmaLedgerRunningTotals as entry}
                <tr>
                  <td>{data.repData.karma.find(k => k.id === entry.id)?.karma_event ?? '—'}</td>
                  <td>{entry.karma_amount ?? '—'}</td>
                  <td><strong>{entry.running_total}</strong></td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}

        <h2>Milestones</h2>
        {#if data.repData.milestones.length === 0}
          <p class="empty">No milestones recorded.</p>
        {:else}
          <div class="milestone-list">
            {#each data.repData.milestones as milestone}
              <div class="milestone-item">
                <strong>{milestone.milestone_trial ?? 'Unnamed Trial'}</strong>
                <span class="progress">(Tier {milestone.milestone_current ?? 0})</span>
              </div>
            {/each}
          </div>
        {/if}

        <h2>Contacts</h2>
        {#if data.repData.contacts.length === 0}
          <p class="empty">No contacts recorded.</p>
        {:else}
          <table class="rep-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Info</th>
                <th>Level</th>
              </tr>
            </thead>
            <tbody>
              {#each data.repData.contacts as contact}
                <tr>
                  <td>{contact.contact_name ?? '—'}</td>
                  <td>{contact.contact_info ?? '—'}</td>
                  <td>{contact.contact_level ?? '—'}</td>
                </tr>
              {/each}
            </tbody>
          </table>
        {/if}
      </section>
    {/if}
  </main>
</div>

<style>
  .container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 2rem 1rem;
  }

  header {
    margin-bottom: 2rem;
    border-bottom: 2px solid #333;
    padding-bottom: 1rem;
  }

  h1 {
    font-size: 2.5rem;
    margin: 0 0 0.5rem 0;
    color: #000;
  }

  .sync-meta {
    margin: 0;
    color: #666;
    font-size: 0.9rem;
  }

  .tab-bar {
    display: flex;
    gap: 0.5rem;
    margin-bottom: 2rem;
    border-bottom: 1px solid #ddd;
  }

  .tab-bar button {
    padding: 0.75rem 1.5rem;
    background: none;
    border: none;
    border-bottom: 3px solid transparent;
    cursor: pointer;
    font-size: 1rem;
    color: #666;
    transition: all 0.2s ease-in-out;
  }

  .tab-bar button:hover {
    color: #000;
  }

  .tab-bar button.active {
    color: #000;
    border-bottom-color: #000;
    font-weight: bold;
  }

  .tab-content {
    min-height: 400px;
  }

  section h2 {
    font-size: 1.5rem;
    margin-top: 2rem;
    margin-bottom: 1rem;
    color: #333;
    border-bottom: 1px solid #eee;
    padding-bottom: 0.5rem;
  }

  section h2:first-child {
    margin-top: 0;
  }

  .overview-section {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }

  .attribute-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
    gap: 1rem;
  }

  .attribute-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: #f9f9f9;
    text-align: center;
  }

  .attr-label {
    font-size: 0.8rem;
    font-weight: bold;
    color: #666;
    text-transform: uppercase;
  }

  .attr-value {
    font-size: 1.5rem;
    font-weight: bold;
    color: #000;
    margin-top: 0.25rem;
  }

  .cm-summary {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem;
    background: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .cm-type {
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 1rem;
  }

  .cm-mod,
  .cm-overflow {
    font-size: 0.85rem;
    color: #666;
    margin-left: auto;
  }

  .init-movement {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
    gap: 1rem;
  }

  .stat-box {
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: #f9f9f9;
    text-align: center;
  }

  .pool-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
    gap: 1rem;
  }

  .pool-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: #f9f9f9;
  }

  .pool-label {
    font-size: 0.9rem;
    font-weight: bold;
    color: #666;
  }

  .pool-value {
    font-size: 1.3rem;
    font-weight: bold;
    color: #000;
    margin-top: 0.25rem;
  }

  .empty {
    color: #999;
    font-style: italic;
    padding: 1rem;
    text-align: center;
  }

  .rep-table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 1rem;
  }

  .rep-table thead {
    background: #f0f0f0;
    border-bottom: 2px solid #ddd;
  }

  .rep-table th {
    padding: 0.75rem;
    text-align: left;
    font-weight: bold;
    color: #333;
  }

  .rep-table td {
    padding: 0.75rem;
    border-bottom: 1px solid #eee;
  }

  .rep-table tbody tr:hover {
    background: #f9f9f9;
  }

  .pool-info {
    font-size: 0.9rem;
    color: #666;
  }

  .money-display {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
    gap: 1rem;
    margin-top: 1rem;
  }

  .money-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: #f9f9f9;
  }

  .money-label {
    font-weight: bold;
    color: #666;
  }

  .money-value {
    font-size: 1.2rem;
    font-weight: bold;
    color: #000;
  }

  .identity-info {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    padding: 1rem;
    background: #f9f9f9;
    border: 1px solid #ddd;
    border-radius: 4px;
  }

  .identity-item {
    display: flex;
    gap: 1rem;
    align-items: flex-start;
  }

  .identity-item .label {
    min-width: 120px;
    font-weight: bold;
    color: #666;
  }

  .karma-header {
    padding: 1rem;
    background: #f0f0f0;
    border-radius: 4px;
    font-weight: bold;
    margin-bottom: 1rem;
  }

  .milestone-list {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    margin-top: 1rem;
  }

  .milestone-item {
    padding: 0.75rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: #f9f9f9;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .progress {
    color: #666;
    font-size: 0.9rem;
  }
</style>
