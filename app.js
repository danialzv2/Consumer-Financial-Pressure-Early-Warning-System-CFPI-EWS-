const API_URL = "https://cfpi-api.onrender.com/";

const stateSelect = document.getElementById("stateSelect");

function formatToday() {
  return new Date().toLocaleDateString("en-MY", {
    day: "2-digit",
    month: "short",
    year: "numeric"
  });
}

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

      let context = null;

      if (forecast && Array.isArray(data.historical)) {
        context = data.historical.find(h =>
          h.state === forecast.state &&
          h.date === forecast.date
        );
      }

      renderForecast(forecast, context);
      renderChart(data.historical);
    });
}


//Forecast panel (ML output)
function renderForecast(forecast, context) {
  const forecastDiv = document.getElementById("forecast");
  const today = formatToday();

  if (!forecast) {
    forecastDiv.innerHTML = "<p>No forecast available.</p>";
    return;
  }

  const prob = (forecast.prob_cfpi_up_next_month * 100).toFixed(1);
  const direction = forecast.direction_signal;

  forecastDiv.innerHTML = `
    <div class="forecast-header">
      <span>Updated as of: <strong>${today}</strong></span>
    </div>

    <div class="forecast-grid">
    
      <div class="forecast-left">
        <h3>Early Warning Signal</h3>
        <p><strong>Direction:</strong> ${direction}</p>
        <p><strong>Probability CFPI ↑ next month:</strong> ${prob}%</p>
        <p><strong>Risk Flag:</strong> ${context?.risk_flag ?? "N/A"}</p>
      </div>

      <div class="forecast-right">
        <h3>Market Context</h3>
        <p><strong>RON95 (BUDI):</strong> ${context?.ron95_budi95 ?? "N/A"}</p>
        <p><strong>RON97:</strong> ${context?.ron97 ?? "N/A"}</p>
        <p><strong>USD/MYR:</strong> ${context?.usd ?? "N/A"}</p>
        <p>
          <strong>Inflation Score as (${context?.date ?? "N/A"}):</strong>
          ${context?.index ?? "N/A"}
        </p>
      </div>

    </div>
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


