"use client";

import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/AuthProvider";
import SuperAdminDashboard from "@/components/SuperAdminDashboard";

export default function AdminPage() {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push("/login");
      } else if (user.role !== "superadmin") {
        router.push("/");
      } else {
        setAuthorized(true);
      }
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#F1F5F9] dark:bg-[#1C2434]">
        <div className="text-xl text-[#3C50E0] font-semibold">Loading...</div>
      </div>
    );
  }

  if (!authorized) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#F1F5F9] dark:bg-[#1C2434]">
        <div className="text-center">
          <h1 className="text-2xl font-bold text-red-600 mb-2">Access Denied</h1>
          <p className="text-gray-600 dark:text-gray-400">You don't have permission to access this page.</p>
        </div>
      </div>
    );
  }

  return <SuperAdminDashboard />;
}
