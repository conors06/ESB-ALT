<script lang="ts">
  import { RangeCalendar } from "$lib/components/ui/range-calendar";
  import { today, getLocalTimeZone } from "@internationalized/date";
  import { Button } from "$lib/components/ui/button";
  import Sun from "lucide-svelte/icons/sun";
  import Moon from "lucide-svelte/icons/moon";
 
  import { toggleMode } from "mode-watcher";
 
  const start = today(getLocalTimeZone());
  const end = start.add({ days: 7 });
 
  let value = {
    start,
    end
  };
</script>
 
<RangeCalendar bind:value class="rounded-md border" />
<Button on:click={toggleMode} variant="outline" size="icon">
  <Sun
    class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
  />
  <Moon
    class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
  />
  <span class="sr-only">Toggle theme</span>
</Button>