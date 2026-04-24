import { redirect } from "next/navigation";

export default function Home() {
  // Sprint 1: Auto-redirect to dashboard for testing
  redirect("/dashboard");
}
