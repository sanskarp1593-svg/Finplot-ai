import { request } from "./client";

export function getDashboard(month) {
  const query = month ? `?month=${encodeURIComponent(month)}` : "";
  return request(`/api/dashboard${query}`);
}
