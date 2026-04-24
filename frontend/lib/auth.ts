import { fetchWithAuth } from "./api";

export interface Counselor {
  id: string;
  full_name: string;
  email: string;
  referral_code?: string;
  subscription?: {
    status: string;
    trial_ends_at?: string;
  };
}

export async function getMe(): Promise<Counselor> {
  // Sprint 1: Backend currently returns a mock counselor for all requests
  return fetchWithAuth("/auth/me");
}

export async function logout() {
  if (typeof window !== "undefined") {
    localStorage.removeItem("token");
    window.location.href = "/login";
  }
}
