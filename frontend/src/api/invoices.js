import { request } from "./client";

export function uploadInvoice(file) {
  const formData = new FormData();
  formData.append("file", file);
  return request("/api/invoices/upload", {
    method: "POST",
    body: formData,
  });
}

export function confirmInvoice(id, payload = {}) {
  return request(`/api/invoices/${id}/confirm`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function rejectInvoice(id) {
  return request(`/api/invoices/${id}`, {
    method: "DELETE",
  });
}
