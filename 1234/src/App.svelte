<script lang="ts">
  import CalendarIcon from "lucide-svelte/icons/calendar";
  import Sun from "lucide-svelte/icons/sun";
  import Moon from "lucide-svelte/icons/moon";
  import Terminal from "lucide-svelte/icons/terminal";
  import * as Alert from "$lib/components/ui/alert";
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

  let totalKw: number | null = null;
  let startDate: string = '';
let endDate: string = '';

const df = new DateFormatter("en-US", {
  dateStyle: "medium"
});

let value: DateRange | undefined = {
  start: new CalendarDate(2022, 1, 20),
  end: new CalendarDate(2022, 1, 20).add({ days: 20 })
};

let startValue: DateValue | undefined = undefined;

$: {
  if (value && value.start && value.end) {
    // Update the module-level variables
    startDate = df.format(value.start.toDate(getLocalTimeZone()));
    endDate = df.format(value.end.toDate(getLocalTimeZone()));

    console.log(startDate);
    console.log(endDate);
  }
}

let mprnInput: HTMLInputElement;
let emailInput: HTMLInputElement;
let passwordInput: HTMLInputElement;

const handleFormSubmit = async (event: Event) => {
  event.preventDefault();

  emailInput = document.getElementById('email') as HTMLInputElement;
  mprnInput = document.getElementById('mprn') as HTMLInputElement;
  passwordInput = document.getElementById('current') as HTMLInputElement;

  console.log(emailInput.value);
  console.log(mprnInput.value);
  console.log(passwordInput.value);
  console.log(startDate); // Use the module-level variable
  console.log(endDate); // Use the module-level variable

  console.log("Submitting");

  const data = {
    mprn: mprnInput.value,
    email: emailInput.value,
    password: passwordInput.value,
    startTime: startDate, // Use the module-level variable
    endTime: endDate // Use the module-level variable
  };

  const response = await fetch("http://127.0.0.1:5000/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(data)
  });

  if (response.ok) {
    const result = await response.json();
    totalKw = result.total_kw; // Update the variable name to match the response field name
    console.log(result);
    // Handle the result as needed
  } else {
    console.error('Error:', response.status);
    // Handle the error
  }
};

  

  $: {
    if (totalKw !== null) {
      console.log(totalKw); // Make sure the value is correct in the console
    }
  }


  
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
    <Popover.Root openFocus>
    <Popover.Trigger asChild let:builder>
      <Button
        variant="outline"
        class={cn(
          "w-[300px] justify-start text-left font-normal",
          !value && "text-muted-foreground"
        )}
        builders={[builder]}
      >
        <CalendarIcon class="mr-2 h-4 w-4" />
        {#if value && value.start}
          {#if value.end}
            {df.format(value.start.toDate(getLocalTimeZone()))} - {df.format(
              value.end.toDate(getLocalTimeZone())
            )}
          {:else}
            {df.format(value.start.toDate(getLocalTimeZone()))}
          {/if}
        {:else if startValue}
          {df.format(startValue.toDate(getLocalTimeZone()))}
        {:else}
          Pick a date
        {/if}
      </Button>
    </Popover.Trigger>
    <Popover.Content class="w-auto p-0" align="start">
      <RangeCalendar
        bind:value
        bind:startValue
        initialFocus
        numberOfMonths={2}
        placeholder={value?.start}
      />
    </Popover.Content>
  </Popover.Root>
  
    

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
            <Button on:click={handleFormSubmit}>Submit</Button>
          </Card.Footer>          
        </Card.Root>
      </Tabs.Content>
    </Tabs.Root>
    {#if totalKw !== null}
      <Alert.Root>
        <Terminal class="h-4 w-4" />
        <Alert.Title>Total kW Usage</Alert.Title>
        <Alert.Description>
            Your total kW usage for the selected date range is: {totalKw}
        </Alert.Description>
      </Alert.Root>
    {/if}
  </div>
</div>
