<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let startTime = '';
  let endTime = '';
  let mprn = '';
  let email = '';
  let password = '';
  let totalKw = null;

  async function handleSubmit(event) {
    event.preventDefault();

    const data = {
      startTime: formatDate(startTime),
      endTime: formatDate(endTime),
      mprn,
      email,
      password
    };

    const response = await fetch('http://127.0.0.1:5000/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
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
  }

  function formatDate(dateString) {
    const [year, month, day] = dateString.split('-');
    return `${day}/${month}/${year.slice(-2)}`;
  }

  $: {
    if (totalKw !== null) {
      console.log(totalKw); // Make sure the value is correct in the console
    }
  }
</script>

<style>
  form {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  input[type="date"],
  input[type="mprn"],
  input[type="email"],
  input[type="password"],
  button {
    border-radius: 10px;
    padding: 8px;
    margin-bottom: 10px;
  }
</style>

<form on:submit={handleSubmit}>
  <label for="start-time">Start Time</label>
  <input type="date" id="start-time" bind:value={startTime} required>

  <label for="end-time">End Time</label>
  <input type="date" id="end-time" bind:value={endTime} required>

  <label for="mprn">MPRN</label>
  <input type="text" id="mprn" bind:value={mprn} required>

  <label for="email">Email</label>
  <input type="email" id="email" bind:value={email} required>

  <label for="password">Password</label>
  <input type="password" id="password" bind:value={password} required>

  <button type="submit">Submit</button>
</form>

{#if totalKw !== null}
  <p>Total kW: {totalKw}</p>
{/if}