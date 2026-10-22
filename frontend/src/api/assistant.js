import { request } from "./client";

export function queryAssistant(question, language = "en") {
  return request("/api/assistant/query", {
    method: "POST",
    body: JSON.stringify({ question, language }),
  });
}

export function getAssistantHistory() {
  return request("/api/assistant/history");
}
