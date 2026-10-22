import { request } from "./client";

export function getKnowledgeDocs() {
  return request("/api/knowledge");
}
