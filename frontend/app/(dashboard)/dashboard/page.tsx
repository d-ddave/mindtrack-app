"use client";

import { useEffect, useState } from "react";
import { getMe, Counselor } from "@/lib/auth";

export default function DashboardPage() {
  const [profile, setProfile] = useState<Counselor | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMe()
      .then(setProfile)
      .catch(() => setProfile(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center pt-16">
        <div className="w-10 h-10 border-4 border-muted border-t-primary rounded-full animate-spin" />
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="text-center pt-16 text-muted-foreground">
        Unable to load profile. Please try refreshing.
      </div>
    );
  }

  const trialDays = profile.subscription?.trial_ends_at
    ? Math.max(0, Math.ceil((new Date(profile.subscription.trial_ends_at).getTime() - Date.now()) / 86400000))
    : 0;

  const stats = [
    { label: "Total Patients", value: "12", icon: "👥", trend: "+2 this month" },
    { label: "Sessions this Week", value: "8", icon: "📅", trend: "3 remaining" },
    { label: "Monthly Revenue", value: "₹24,500", icon: "💰", trend: "+15% vs last month" },
    { label: "Unfiled Notes", value: "4", icon: "📝", trend: "Priority: High" },
  ];

  const firstName = profile.full_name.split(" ").find(w => !["Dr.", "Mr.", "Ms.", "Mrs.", "Prof."].includes(w)) || profile.full_name.split(" ")[0];

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-in fade-in duration-500">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">
          Welcome back, {firstName} 👋
        </h1>
        <p className="text-muted-foreground mt-1">
          Here&apos;s what your practice looks like today.
        </p>
      </div>

      {profile.subscription?.status === "trialing" && (
        <div className="p-6 rounded-xl border border-primary/20 bg-primary/5 flex items-center justify-between">
          <div className="space-y-1">
            <h3 className="font-semibold text-lg">Free Trial Active</h3>
            <p className="text-sm text-muted-foreground">
              You have <span className="text-primary font-bold">{trialDays} days</span> left in your professional trial.
            </p>
          </div>
          <button className="px-5 py-2.5 bg-primary text-primary-foreground rounded-lg font-semibold hover:opacity-90 transition-opacity">
            Upgrade Practice
          </button>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat) => (
          <div key={stat.label} className="p-6 rounded-xl border border-border bg-card hover:border-primary/30 transition-colors">
            <div className="flex items-center justify-between mb-4">
              <span className="text-sm font-medium text-muted-foreground uppercase tracking-wider">{stat.label}</span>
              <span className="text-2xl">{stat.icon}</span>
            </div>
            <div className="space-y-1">
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-muted-foreground font-medium">{stat.trend}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 p-6 rounded-xl border border-border bg-card space-y-4">
          <h2 className="text-xl font-bold">Upcoming Appointments</h2>
          <div className="space-y-3">
            {[1, 2, 3].map((i) => (
              <div key={i} className="flex items-center justify-between p-4 rounded-lg bg-muted/30 border border-border/50">
                <div className="flex items-center space-x-4">
                  <div className="w-10 h-10 rounded-full bg-secondary flex items-center justify-center font-bold">P{i}</div>
                  <div>
                    <p className="font-medium text-sm">Patient Sample {i}</p>
                    <p className="text-xs text-muted-foreground">CBT Session • 45 mins</p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="text-sm font-medium">4:00 PM</p>
                  <p className="text-xs text-muted-foreground text-primary">Join Call</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="p-6 rounded-xl border border-border bg-card space-y-6">
          <h2 className="text-xl font-bold">Practice Growth</h2>
          <div className="space-y-4">
             <div className="p-4 rounded-lg bg-accent/20 border border-accent/30 space-y-2">
                <p className="text-sm font-medium">Your Referral Code</p>
                <div className="text-2xl font-mono font-bold text-primary tracking-widest bg-background/50 p-3 rounded text-center">
                  {profile.referral_code || "MND001"}
                </div>
                <p className="text-[10px] text-muted-foreground text-center uppercase tracking-tighter">
                  Share & earn 1 month free for every signup
                </p>
             </div>
             
             <div className="space-y-2">
               <p className="text-xs font-semibold text-muted-foreground uppercase">Next Milestones</p>
               <div className="space-y-1">
                  <div className="flex justify-between text-xs font-medium">
                    <span>Patient Load</span>
                    <span>12/20</span>
                  </div>
                  <div className="w-full h-1.5 bg-muted rounded-full overflow-hidden">
                    <div className="w-[60%] h-full bg-primary" />
                  </div>
               </div>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
