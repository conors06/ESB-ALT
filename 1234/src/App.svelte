<script lang="ts">
  import { fade, blur, scale, fly, slide } from "svelte/transition";
  import { quintOut } from "svelte/easing";
  import * as Drawer from "$lib/components/ui/drawer/index.js";
  import * as Resizable from "$lib/components/ui/resizable";
  import { LineChart } from "lucide-svelte";
  import CalendarIcon from "lucide-svelte/icons/calendar";
  import { Separator } from "$lib/components/ui/separator";
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
    type DateValue,
  } from "@internationalized/date";
  import { cn } from "$lib/utils";
  import { Button } from "$lib/components/ui/button";
  import { RangeCalendar } from "$lib/components/ui/range-calendar";
  import * as Popover from "$lib/components/ui/popover";
  import { onMount } from "svelte";
  import Plotly from "plotly.js-basic-dist";

  let totalKw: number | null = null;
  let chart_data: number | null = null;
  let startDate: string = "";
  let endDate: string = "";
  let chartInstance: Plotly.PlotlyHTMLElement;
  let showModal = false;
  let isTyping = false; // Add a flag for typing animation

  const df = new DateFormatter("en-US", {
    dateStyle: "medium",
  });

  let value: DateRange | undefined = {
    start: new CalendarDate(2022, 5, 16),
    end: new CalendarDate(2022, 5, 16).add({ days: 20 }),
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

    emailInput = document.getElementById("email") as HTMLInputElement;
    mprnInput = document.getElementById("mprn") as HTMLInputElement;
    passwordInput = document.getElementById("current") as HTMLInputElement;

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
      endTime: endDate, // Use the module-level variable
    };

    const response = await fetch("http://127.0.0.1:5000/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response.ok) {
      const result = await response.json();
      totalKw = result.total_kw; // Update the variable name to match the response field name
      console.log(result);
      // Handle the result as needed
    } else {
      console.error("Error:", response.status);
      // Handle the error
    }

    const response2 = await fetch("http://localhost:5000/chart", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (response2.ok) {
      const result = await response2.json();
      chart_data = result.chart_data; // Update the variable name to match the response field name
      console.log(chart_data);
      // Handle the result as needed
    } else {
      console.error("Error:", response2.status);
      // Handle the error
    }
  };

  $: {
    if (totalKw !== null) {
      console.log(totalKw); // Make sure the value is correct in the console
    }
  }

  $: {
    if (chart_data !== null && typeof chart_data === "object") {
      const { data, labels } = chart_data;

      const trace: Partial<Plotly.ScatterData> = {
        x: labels,
        y: data,
        type: "scatter",
        mode: "lines",
      };

      const layout = {
        title: "Energy Usage",
        xaxis: {
          title: "Time",
        },
        yaxis: {
          title: "Energy Usage (kW)",
        },
      };

      const config = {
        responsive: true,
      };

      Plotly.newPlot("chart", [trace], layout, config).then((instance) => {
        chartInstance = instance;
      });
    }
  }
</script>

<Drawer.Root>
  <Drawer.Trigger asChild let:builder>
    <div class="text-center">
    <Button   
      builders={[builder]}
      variant="outline"
      class="rounded-full mt-6 mx-auto inline-block"
    >
      Open Drawer
    </Button>
  </Drawer.Trigger>
  <Drawer.Content>
    <div class="mx-auto w-full max-w-8xl">
      <Drawer.Header>
        <Drawer.Title>Docs</Drawer.Title>
      </Drawer.Header>
      <Resizable.PaneGroup
        direction="horizontal"
        class="min-h-[600px] max-h-[600px] max-w-8xl rounded-lg border"
      >
        <Resizable.Pane defaultSize={50}>
          <div class="relative h-full overflow-hidden">
            <div class="absolute inset-0 overflow-auto">
              <img src="image.png" alt="Source" class="w-full h-auto" />
            </div>
          </div>
        </Resizable.Pane>
        <Resizable.Handle withHandle />
        <Resizable.Pane defaultSize={50}>
          <div class="relative h-full overflow-hidden">
            <div class="absolute inset-0 overflow-auto">
              <iframe
                src="https://docs.google.com/document/d/e/2PACX-1vS_56PrCnlvJ_DV_MZMZ9vkGubaKtPx0lUeiGN6_ctRUNMkUEXCCXByO4OmGlJ02F1TEPDG2e6taIa_/pub?embedded=true"
                class="w-full h-full"
                title="Docs"
              ></iframe>
            </div>
          </div>
        </Resizable.Pane>
      </Resizable.PaneGroup>
      <Drawer.Footer>
        <Drawer.Close asChild let:builder>
          <Button builders={[builder]} variant="outline">Cancel</Button>
        </Drawer.Close>
      </Drawer.Footer>
    </div>
  </Drawer.Content>
</Drawer.Root>

<div
  style="position: absolute; top: 30px; right: 10px; padding: 10px;"
  in:slide={{ duration: 500, easing: quintOut }}
>
  <div class="space-y-1">
    <h4 class="text-sm font-medium leading-none">ESB Calculator</h4>
    <p class="text-sm text-muted-foreground">
      An ESB Electricity Usage Calculator
    </p>
  </div>
</div>

<div class="flex flex-col items-center justify-center min-h-screen relative">
  <div
    class="absolute top-4 right-4"
    in:scale={{ delay: 200, duration: 500, easing: quintOut }}
  >
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
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="1em"
          height="1em"
          viewBox="0 0 512 512"
          {...$$props}
        >
          <path
            fill="#fdb436"
            d="m479.23 258.78l-197.7-36.571c-4.891-.905-7.09-6.667-4.044-10.6L427.065 18.432c4.498-5.808-2.366-13.542-8.667-9.766L21.336 246.595c-5.216 3.126-3.84 11.036 2.126 12.216l180.068 35.606c4.694.928 6.897 6.365 4.173 10.299L77.05 493.386c-4.05 5.849 2.684 13.111 8.821 9.513l395.511-231.856c5.308-3.111 3.899-11.144-2.152-12.263"
          />
        </svg>
        <Alert.Title>Total kW Usage</Alert.Title>
        <Alert.Description>
          Your total kW usage for the selected date range is: {totalKw}
        </Alert.Description>
      </Alert.Root>
    {/if}
  </div>
</div>

<div id="chart"></div>
