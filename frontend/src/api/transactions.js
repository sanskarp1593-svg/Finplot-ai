import { request, API_BASE } from "./client";

export function getTransactions(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, val]) => {
    if (val !== undefined && val !== null && val !== "") {
      query.append(key, val);
    }
  });
  const qs = query.toString() ? `?${query.toString()}` : "";
  return request(`/api/transactions${qs}`);
}

export function createTransaction(data) {
  return request("/api/transactions", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export function deleteTransaction(id) {
  return request(`/api/transactions/${id}`, {
    method: "DELETE",
  });
}

export function importCSV(file) {
  const formData = new FormData();
  formData.append("file", file);
  return request("/api/transactions/import", {
    method: "POST",
    body: formData,
  });
}

export function getExportCSVUrl(params = {}) {
  const query = new URLSearchParams();
  Object.entries(params).forEach(([key, val]) => {
    if (val !== undefined && val !== null && val !== "") {
      query.append(key, val);
    }
  });
  const qs = query.toString() ? `?${query.toString()}` : "";
  return `${API_BASE}/api/transactions/export${qs}`;
}
