import { request } from "./client";

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface ChatRequest {
  message: string;
  history: ChatMessage[];
  model?: string;
  user_id?: string;
  user_profile?: {
    departure_city?: string;
    home_city?: string;
    preferences?: string[];
    food_preferences?: string[];
    budget_level?: string;
    note?: string;
  };
}

export interface ChatResponse {
  reply: string;
  model_used: string;
}

export function sendChat(payload: ChatRequest): Promise<ChatResponse> {
  return request<ChatResponse>("/chat", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
