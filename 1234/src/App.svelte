<script lang="ts">
  import CalendarIcon from "lucide-svelte/icons/calendar";
  import Sun from "lucide-svelte/icons/sun";
  import Moon from "lucide-svelte/icons/moon";
  import * as Tabs from "$lib/components/ui/tabs";
  import * as Card from "$lib/components/ui/card";
  import { Label } from "$lib/components/ui/label";
  import { toggleMode } from "mode-watcher";
  import { Input } from "$lib/components/ui/input";
  import { today, getLocalTimeZone } from "@internationalized/date";
  import type { DateRange } from "bits-ui";
  import {
    CalendarDate,
    DateFormatter,
    type DateValue
  } from "@internationalized/date";
  import { cn } from "$lib/utils";
  import { Button } from "$lib/components/ui/button";
  import { RangeCalendar } from "$lib/components/ui/range-calendar";
  import * as Popover from "$lib/components/ui/popover";

  const df = new DateFormatter("en-US", {
    dateStyle: "medium"
  });

  let value: DateRange | undefined = {
    start: new CalendarDate(2022, 1, 20),
    end: new CalendarDate(2022, 1, 20).add({ days: 20 })
  };

  let startValue: DateValue | undefined = undefined;
  const start = today(getLocalTimeZone());
  const end = start.add({ days: 7 });

  let rangeValue = {
    start,
    end
  };
</script>

<div class="flex flex-col items-center justify-center min-h-screen relative">
  <div class="absolute top-4 right-4">
    <Button on:click={toggleMode} variant="outline" size="icon">
      <Sun
        class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"
      />
      <Moon
        class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"
      />
      <span class="sr-only">Toggle theme</span>
    </Button>
  </div>
  <div class="grid gap-4">
    <!-- New component -->
    <RangeCalendar bind:value={rangeValue} class="rounded-md border" />

    <Tabs.Root value="account" class="w-[400px]">
      <Tabs.List class="grid w-full grid-cols-2">
        <Tabs.Trigger value="account">Account</Tabs.Trigger>
        <Tabs.Trigger value="password">Password</Tabs.Trigger>
      </Tabs.List>
      <Tabs.Content value="account">
        <Card.Root>
          <Card.Header>
            <Card.Title>Account Details</Card.Title>
            <Card.Description>
              Enter your account details and then go to the password section.
            </Card.Description>
          </Card.Header>
          <Card.Content class="space-y-2">
            <div class="space-y-1">
              <Label for="email">Email</Label>
              <Input id="email" value="123@gmail.com" />
            </div>
            <div class="space-y-1">
              <Label for="mprn">MPRN</Label>
              <Input id="mprn" value="123456789" />
            </div>
          </Card.Content>
          <Card.Footer>
            <Button>Submit</Button>
          </Card.Footer>
        </Card.Root>
      </Tabs.Content>
      <Tabs.Content value="password">
        <Card.Root>
          <Card.Header>
            <Card.Title>Password</Card.Title>
            <Card.Description>
              Enter your password for your ESB account here.
            </Card.Description>
          </Card.Header>
          <Card.Content class="space-y-2">
            <div class="space-y-1">
              <Label for="current">Current password</Label>
              <Input id="current" type="password" />
            </div>
            
          </Card.Content>
          <Card.Footer>
            <Button>Submit</Button>
          </Card.Footer>
        </Card.Root>
      </Tabs.Content>
    </Tabs.Root>
  </div>
</div>