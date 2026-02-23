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
}

export interface ModelOption {
  value: string;
  label: string;
  desc: string;
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
