<script lang="ts">
	import { ModeWatcher } from 'mode-watcher';
  import { onMount } from 'svelte';
  import { setMode } from 'mode-watcher';
  onMount(() => {
    setMode('dark');
  });
</script>

<main>
  <ModeWatcher defaultMode="dark" />
  <slot />
</main>