import { request } from "./client";

export interface PlanPayload {
  destination: string;
  days: number;
  travel_style: string;
  travelers: string;
  preferences: string[];
  constraints: string[];
  budget_level: string;
  model?: string;
  clothing_style?: string;
  food_preference?: string[];
  accommodation_type?: string;
  transport_preference?: string;
}

export interface PlanResult {
  summary: string;
  itinerary: Array<{
    day: number;
    period: string;
    activity: string;
    reason: string;
  }>;
  culture_tips: string[];
  risk_alerts: string[];
  signal_basis: string[];
  social_events?: Array<{
    title: string;
    type: string;
    location: string;
    time_desc: string;
    source: string;
    url: string;
    tags: string[];
    desc: string;
  }>;
}

export interface ModelOption {
  value: string;
  label: string;
  desc: string;
}

export interface SavedPlan {
  id: string;
  timestamp: number;
  payload: PlanPayload;
  result: PlanResult;
}

export interface FakeSignalEvent {
  id: string;
  created_at: number;
  event_type: "weather" | "crowd";
  destination: string;
  day_index: number;
  old_value: string;
  new_value: string;
  note: string;
}

export interface FakeSignalEventResponse {
  events: FakeSignalEvent[];
}

export function createPlan(payload: PlanPayload): Promise<PlanResult> {
  return request<PlanResult>("/plan", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function fetchModels(): Promise<ModelOption[]> {
  return request<ModelOption[]>("/models");
}

export function fetchWeather(city: string, days: number = 1): Promise<any> {
  const isTestMode = localStorage.getItem("chaoyun_test_mode") === "true";
  return request<any>(`/weather?city=${encodeURIComponent(city)}&days=${days}&test_mode=${isTestMode}`);
}

export function fetchFakeEvents(): Promise<FakeSignalEventResponse> {
  return request<FakeSignalEventResponse>("/fake/events/consume?limit=20");
}
