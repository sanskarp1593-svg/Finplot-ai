import { request } from "./client";

export function getSettings() {
  return request("/api/settings");
}

export function updateSettings(data) {
  return request("/api/settings", {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export function updateBudgets(budgets) {
  return request("/api/settings/budgets", {
    method: "PUT",
    body: JSON.stringify(budgets),
  });
}
