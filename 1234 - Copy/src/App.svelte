<script lang="ts">
  import { onMount } from 'svelte';
  import Plotly from 'plotly.js-basic-dist';

  onMount(async () => {
    const response = await fetch('http://localhost:5000/chart_data');
    const chartData = await response.json();
    console.log(chartData);

    // Assuming chartData has data and labels
    const data = chartData.data;
    const labels = chartData.labels;

    // Create a plot using plotly.js
    const plotData: Plotly.Data[] = [{
      x: labels,
      y: data,
      type: 'scatter'
    }];

    Plotly.newPlot('yourDivId', plotData);
  });
</script>
<div id="yourDivId"></div>