const API_BASE = "http://localhost:8000/api/v1";

export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });

  if (!response.ok) {
    throw new Error(`接口请求失败: ${response.status}`);
  }
  return (await response.json()) as T;
}
