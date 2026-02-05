const API_URL = "http://127.0.0.1:8000";

const stateSelect = document.getElementById("stateSelect");

//Load states dynamically

fetch(`${API_URL}/historical/states`)
  .then(res => res.json())
  .then(states => {
    states.forEach(state => {
      const option = document.createElement("option");
      option.value = state;
      option.textContent = state;
      stateSelect.appendChild(option);
    });

    if (states.length > 0) {
      loadDashboard(states[0]);
    }
  });


  //Load dashboard data for a state
stateSelect.addEventListener("change", () => {
  loadDashboard(stateSelect.value);
});

function loadDashboard(state) {
  fetch(`${API_URL}/dashboard/state/${state}`)
    .then(response => response.json())
    .then(data => {
      const forecast =
        Array.isArray(data.forecast) && data.forecast.length > 0
          ? data.forecast[0]
          : null;

      renderForecast(forecast);
      renderChart(data.historical);
    });
}


//Forecast panel (ML output)
function renderForecast(forecast) {
  const forecastDiv = document.getElementById("forecast");

  if (!forecast) {
    forecastDiv.innerHTML = "<p>No forecast available.</p>";
    return;
  }

  const prob = (forecast.prob_cfpi_up_next_month * 100).toFixed(1);
  const direction = forecast.direction_signal;

  forecastDiv.innerHTML = `
    <h3>Early Warning Signal</h3>
    <p>
      Direction:
      <strong>${direction}</strong>
    </p>
    <p>
      Probability CFPI ↑ next month:
      <strong>${prob}%</strong>
    </p>
  `;
}


//Historical CFPI chart
let chart;

function renderChart(history) {
  const labels = history.map(d => d.date);
  const cfpi = history.map(d => d.cfpi);

  const ctx = document.getElementById("cfpiChart").getContext("2d");

  if (chart) {
    chart.destroy();
  }

  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: labels,
      datasets: [{
        label: "CFPI",
        data: cfpi,
        tension: 0.3
      }]
    },
    options: {
      responsive: true,
      scales: {
        x: {
          title: { display: true, text: "Date" }
        },
        y: {
          title: { display: true, text: "CFPI" }
        }
      }
    }
  });
}


