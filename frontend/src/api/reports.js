import { request } from "./client";

export function getPnLReport() {
  return request("/api/reports/pnl");
}

export function getCategoryReport(month) {
  const query = month ? `?month=${encodeURIComponent(month)}` : "";
  return request(`/api/reports/categories${query}`);
}
