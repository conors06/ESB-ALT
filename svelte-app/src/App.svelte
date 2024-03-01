<script>
  import { onMount } from 'svelte';
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  let startTime = '';
  let endTime = '';
  let mprn = '';
  let email = '';
  let password = '';

  function handleSubmit() {
    // Perform necessary validations and data manipulation

    // Create a payload object with the form data
    const payload = {
      startTime,
      endTime,
      mprn,
      email,
      password
    };

    // Dispatch an event with the payload
    dispatch('formSubmit', payload);
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
  <input type="mprn" id="mprn" bind:value={mprn} required>

  <label for="email">Email</label>
  <input type="email" id="email" bind:value={email} required>

  <label for="password">Password</label>
  <input type="password" id="password" bind:value={password} required>

  <button type="submit">Submit</button>
</form>


