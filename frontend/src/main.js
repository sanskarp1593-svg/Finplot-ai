import "./style.css";

const status = document.querySelector("#api-status");
const apiBaseUrl = (import.meta.env.VITE_API_BASE_URL || "/api").replace(/\/$/, "");

async function checkBackend() {
  try {
    const response = await fetch(`${apiBaseUrl}/health`);
    if (!response.ok) {
      throw new Error(`Backend returned HTTP ${response.status}`);
    }

    const health = await response.json();
    if (health.status !== "ok") {
      throw new Error("Backend returned an unhealthy status");
    }

    status.textContent = "Backend connected";
    status.classList.add("connected");
  } catch (error) {
    status.textContent = `Backend unavailable: ${error.message}`;
    status.classList.add("error");
  }
}

checkBackend();
