"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Users, UserPlus, Search, Filter, MoreVertical, Edit2, Trash2,
  Eye, EyeOff, UserCheck, UserX, Copy, CheckCircle, XCircle,
  AlertCircle, RefreshCw, Download, Upload, Settings, BarChart3,
  Calendar, Building, Briefcase, Mail, Phone, Shield, Lock,
  TrendingUp, Activity, Database, ArrowLeft, User
} from "lucide-react";
import { useRouter } from "next/navigation";
import {
  validateEmail,
  validatePhone,
  validateName,
  validatePassword,
  validateRequired
} from "@/lib/validation";

const SuperAdminDashboard = () => {
  const router = useRouter();
  const [activeView, setActiveView] = useState<"dashboard" | "users" | "create" | "edit">("dashboard");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  
  // Data states
  const [users, setUsers] = useState<any[]>([]);
  const [stats, setStats] = useState({
    totalUsers: 0,
    activeUsers: 0,
    onboardingPending: 0,
    newThisMonth: 0
  });
  const [searchTerm, setSearchTerm] = useState("");
  const [filterRole, setFilterRole] = useState("all");
  const [filterStatus, setFilterStatus] = useState("all");
  const [selectedUser, setSelectedUser] = useState<any>(null);
  const [showUserMenu, setShowUserMenu] = useState<number | null>(null);
  const [showPasswordModal, setShowPasswordModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [showUserProfile, setShowUserProfile] = useState(false);

  // Form states
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    designation: "",
    establishment: "",
    department: "",
    role: "user",
    temp_password: ""
  });
  const [showPassword, setShowPassword] = useState(false);
  const [validationErrors, setValidationErrors] = useState<Record<string, string>>({});

  useEffect(() => {
    fetchUsers();
    fetchStats();
  }, []);

  const showMessage = (type: "success" | "error", text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 4000);
  };

  const fetchUsers = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/admin/users/list");
      const data = await response.json();
      setUsers(data.users || []);
    } catch (error) {
      showMessage("error", "Failed to fetch users");
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch("http://localhost:8000/api/admin/stats");
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error("Failed to fetch stats:", error);
    }
  };

  const fetchUserProfile = async (userId: number) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/settings/employee/complete?user_id=${userId}`);
      const data = await response.json();
      setSelectedUser(data);
      setShowUserProfile(true);
    } catch (error) {
      showMessage("error", "Failed to fetch user profile");
    } finally {
      setLoading(false);
    }
  };

  const generatePassword = () => {
    const chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnpqrstuvwxyz23456789!@#$%";
    let password = "Welcome@";
    for (let i = 0; i < 6; i++) {
      password += chars.charAt(Math.floor(Math.random() * chars.length));
    }
    setFormData({ ...formData, temp_password: password });
  };

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationErrors({});
    
    // Comprehensive validation
    const errors: Record<string, string> = {};

    // Validate name
    const nameValidation = validateName(formData.name, 'Full name');
    if (!nameValidation.isValid) {
      errors.name = nameValidation.error!;
    }

    // Validate email
    const emailValidation = validateEmail(formData.email);
    if (!emailValidation.isValid) {
      errors.email = emailValidation.error!;
    }

    // Validate designation
    const designationValidation = validateRequired(formData.designation, 'Designation');
    if (!designationValidation.isValid) {
      errors.designation = designationValidation.error!;
    }

    // Validate establishment
    const establishmentValidation = validateRequired(formData.establishment, 'Establishment');
    if (!establishmentValidation.isValid) {
      errors.establishment = establishmentValidation.error!;
    }

    // Validate password
    if (!formData.temp_password) {
      errors.temp_password = "Please generate a temporary password";
    } else {
      const passwordValidation = validatePassword(formData.temp_password);
      if (!passwordValidation.isValid) {
        errors.temp_password = passwordValidation.error!;
      }
    }

    if (Object.keys(errors).length > 0) {
      setValidationErrors(errors);
      showMessage("error", "Please fix validation errors before submitting");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/admin/create-employee", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await response.json();
      
      if (response.ok) {
        showMessage("success", "User created successfully!");
        setFormData({
          name: "",
          email: "",
          designation: "",
          establishment: "",
          department: "",
          role: "user",
          temp_password: ""
        });
        fetchUsers();
        fetchStats();
        setActiveView("users");
      } else {
        showMessage("error", data.error || "Failed to create user");
      }
    } catch (error) {
      showMessage("error", "Failed to create user");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateUser = async (userId: number, updates: any) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/admin/users/${userId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates),
      });

      if (response.ok) {
        showMessage("success", "User updated successfully!");
        fetchUsers();
        setShowUserMenu(null);
      } else {
        const data = await response.json();
        showMessage("error", data.error || "Failed to update user");
      }
    } catch (error) {
      showMessage("error", "Failed to update user");
    } finally {
      setLoading(false);
    }
  };

  const handleToggleUserStatus = async (userId: number, currentStatus: boolean) => {
    await handleUpdateUser(userId, { is_active: !currentStatus });
  };

  const handleDeleteUser = async (userId: number) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/admin/users/${userId}`, {
        method: "DELETE",
      });

      if (response.ok) {
        showMessage("success", "User deleted successfully!");
        fetchUsers();
        fetchStats();
        setShowDeleteModal(false);
        setSelectedUser(null);
      } else {
        const data = await response.json();
        showMessage("error", data.error || "Failed to delete user");
      }
    } catch (error) {
      showMessage("error", "Failed to delete user");
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (userId: number) => {
    const newPassword = `Reset@${Math.floor(Math.random() * 9000 + 1000)}`;
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/admin/users/${userId}/reset-password`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ new_password: newPassword }),
      });

      if (response.ok) {
        showMessage("success", `Password reset! New password: ${newPassword}`);
        setShowPasswordModal(false);
      } else {
        showMessage("error", "Failed to reset password");
      }
    } catch (error) {
      showMessage("error", "Failed to reset password");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    showMessage("success", `${label} copied to clipboard!`);
  };

  const filteredUsers = users.filter(user => {
    const matchesSearch = 
      user.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.employee_id?.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesRole = filterRole === "all" || user.role === filterRole;
    const matchesStatus = 
      filterStatus === "all" ||
      (filterStatus === "active" && user.is_active) ||
      (filterStatus === "inactive" && !user.is_active) ||
      (filterStatus === "pending" && !user.onboarding_completed);
    
    return matchesSearch && matchesRole && matchesStatus;
  });

  return (
    <div className="min-h-screen bg-[#F1F5F9] dark:bg-[#1C2434]">
      {/* Header */}
      <div className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => router.push("/")}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  SuperAdmin Dashboard
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Complete user management system
                </p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button
                onClick={fetchUsers}
                className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                title="Refresh"
              >
                <RefreshCw className={`w-5 h-5 ${loading ? 'animate-spin' : ''}`} />
              </button>
              <button
                onClick={() => setActiveView("create")}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <UserPlus className="w-4 h-4" />
                Create User
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Success/Error Message */}
      <AnimatePresence>
        {message && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0 }}
            className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-4"
          >
            <div
              className={`p-4 rounded-lg flex items-center gap-3 ${
                message.type === "success"
                  ? "bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300"
                  : "bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300"
              }`}
            >
              {message.type === "success" ? <CheckCircle className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
              <span>{message.text}</span>
            </div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6">
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-2">
          <div className="flex gap-2">
            <button
              onClick={() => setActiveView("dashboard")}
              className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all ${
                activeView === "dashboard"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              Dashboard
            </button>
            <button
              onClick={() => setActiveView("users")}
              className={`flex items-center gap-2 px-4 py-2 rounded-md font-medium transition-all ${
                activeView === "users"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
              }`}
            >
              <Users className="w-4 h-4" />
              Users ({users.length})
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <AnimatePresence mode="wait">
          <motion.div
            key={activeView}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
          >
            {/* Dashboard View */}
            {activeView === "dashboard" && (
              <div className="space-y-6">
                {/* Stats Cards */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Users</h3>
                      <Users className="w-8 h-8 text-blue-600" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.totalUsers}</p>
                    <p className="text-sm text-gray-500 mt-2">All registered users</p>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Active Users</h3>
                      <UserCheck className="w-8 h-8 text-green-600" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.activeUsers}</p>
                    <p className="text-sm text-gray-500 mt-2">Currently active</p>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">Pending Onboarding</h3>
                      <AlertCircle className="w-8 h-8 text-amber-600" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.onboardingPending}</p>
                    <p className="text-sm text-gray-500 mt-2">Not completed setup</p>
                  </div>

                  <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                    <div className="flex items-center justify-between mb-4">
                      <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">New This Month</h3>
                      <TrendingUp className="w-8 h-8 text-purple-600" />
                    </div>
                    <p className="text-3xl font-bold text-gray-900 dark:text-white">{stats.newThisMonth}</p>
                    <p className="text-sm text-gray-500 mt-2">Joined this month</p>
                  </div>
                </div>

                {/* Quick Actions */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                  <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <button
                      onClick={() => setActiveView("create")}
                      className="p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-blue-600 dark:hover:border-blue-500 transition-colors text-left"
                    >
                      <UserPlus className="w-6 h-6 text-blue-600 mb-2" />
                      <div className="font-medium">Create New User</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Add employee account</div>
                    </button>

                    <button
                      onClick={() => setActiveView("users")}
                      className="p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-green-600 dark:hover:border-green-500 transition-colors text-left"
                    >
                      <Users className="w-6 h-6 text-green-600 mb-2" />
                      <div className="font-medium">Manage Users</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">View and edit users</div>
                    </button>

                    <button
                      className="p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg hover:border-purple-600 dark:hover:border-purple-500 transition-colors text-left"
                    >
                      <Database className="w-6 h-6 text-purple-600 mb-2" />
                      <div className="font-medium">Export Data</div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Download user data</div>
                    </button>
                  </div>
                </div>

                {/* Recent Activity */}
                <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                  <h2 className="text-xl font-semibold mb-4">Recent Users</h2>
                  <div className="space-y-3">
                    {users.slice(0, 5).map((user) => (
                      <div
                        key={user.id}
                        className="flex items-center justify-between p-3 border border-gray-200 dark:border-gray-700 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors"
                      >
                        <div className="flex items-center gap-3">
                          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                            {user.name?.charAt(0).toUpperCase()}
                          </div>
                          <div>
                            <div className="font-medium">{user.name}</div>
                            <div className="text-sm text-gray-600 dark:text-gray-400">{user.email}</div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2">
                          {user.onboarding_completed ? (
                            <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 rounded-full">
                              Complete
                            </span>
                          ) : (
                            <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 rounded-full">
                              Pending
                            </span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* Users List View */}
            {activeView === "users" && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
                {/* Filters */}
                <div className="p-4 border-b border-gray-200 dark:border-gray-700">
                  <div className="flex flex-col md:flex-row gap-4">
                    <div className="flex-1 relative">
                      <Search className="w-5 h-5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
                      <input
                        type="text"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                        placeholder="Search by name, email, or employee ID..."
                        className="w-full pl-10 pr-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                      />
                    </div>
                    <select
                      value={filterRole}
                      onChange={(e) => setFilterRole(e.target.value)}
                      className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                    >
                      <option value="all">All Roles</option>
                      <option value="user">User</option>
                      <option value="admin">Admin</option>
                      <option value="manager">Manager</option>
                      <option value="superadmin">SuperAdmin</option>
                    </select>
                    <select
                      value={filterStatus}
                      onChange={(e) => setFilterStatus(e.target.value)}
                      className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                    >
                      <option value="all">All Status</option>
                      <option value="active">Active</option>
                      <option value="inactive">Inactive</option>
                      <option value="pending">Pending Onboarding</option>
                    </select>
                  </div>
                </div>

                {/* Users Table */}
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead className="bg-gray-50 dark:bg-gray-700">
                      <tr>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          User
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          Employee ID
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          Role
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          Department
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          Onboarding
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          Status
                        </th>
                        <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                          Actions
                        </th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                      {filteredUsers.length === 0 ? (
                        <tr>
                          <td colSpan={7} className="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                            No users found
                          </td>
                        </tr>
                      ) : (
                        filteredUsers.map((user) => (
                          <tr key={user.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="flex items-center gap-3">
                                <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-semibold">
                                  {user.name?.charAt(0).toUpperCase()}
                                </div>
                                <div>
                                  <div className="font-medium">{user.name}</div>
                                  <div className="text-sm text-gray-600 dark:text-gray-400">{user.email}</div>
                                </div>
                              </div>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="font-mono text-sm">{user.employee_id || '-'}</span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                                user.role === 'superadmin' ? 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-400' :
                                user.role === 'admin' ? 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400' :
                                'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400'
                              }`}>
                                {user.role}
                              </span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <span className="text-sm">{user.department || '-'}</span>
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              {user.onboarding_completed ? (
                                <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 rounded-full">
                                  Complete
                                </span>
                              ) : (
                                <span className="px-2 py-1 text-xs font-medium bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-400 rounded-full">
                                  Pending
                                </span>
                              )}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              {user.is_active ? (
                                <span className="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-400 rounded-full flex items-center gap-1 w-fit">
                                  <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                                  Active
                                </span>
                              ) : (
                                <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400 rounded-full flex items-center gap-1 w-fit">
                                  <div className="w-2 h-2 bg-gray-600 rounded-full"></div>
                                  Inactive
                                </span>
                              )}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap">
                              <div className="relative">
                                <button
                                  onClick={() => setShowUserMenu(showUserMenu === user.id ? null : user.id)}
                                  className="p-2 hover:bg-gray-100 dark:hover:bg-gray-600 rounded transition-colors"
                                >
                                  <MoreVertical className="w-4 h-4" />
                                </button>
                                
                                {showUserMenu === user.id && (
                                  <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-700 rounded-lg shadow-lg border border-gray-200 dark:border-gray-600 z-10">
                                    <button
                                      onClick={() => {
                                        fetchUserProfile(user.id);
                                        setShowUserMenu(null);
                                      }}
                                      className="w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-600 flex items-center gap-2 rounded-t-lg"
                                    >
                                      <Eye className="w-4 h-4" />
                                      View Profile
                                    </button>
                                    <button
                                      onClick={() => {
                                        handleToggleUserStatus(user.id, user.is_active);
                                        setShowUserMenu(null);
                                      }}
                                      className="w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-600 flex items-center gap-2"
                                    >
                                      {user.is_active ? <UserX className="w-4 h-4" /> : <UserCheck className="w-4 h-4" />}
                                      {user.is_active ? 'Disable' : 'Enable'}
                                    </button>
                                    <button
                                      onClick={() => {
                                        setSelectedUser(user);
                                        setShowPasswordModal(true);
                                        setShowUserMenu(null);
                                      }}
                                      className="w-full px-4 py-2 text-left hover:bg-gray-100 dark:hover:bg-gray-600 flex items-center gap-2"
                                    >
                                      <Lock className="w-4 h-4" />
                                      Reset Password
                                    </button>
                                    <button
                                      onClick={() => {
                                        setSelectedUser(user);
                                        setShowDeleteModal(true);
                                        setShowUserMenu(null);
                                      }}
                                      className="w-full px-4 py-2 text-left hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 flex items-center gap-2 rounded-b-lg"
                                    >
                                      <Trash2 className="w-4 h-4" />
                                      Delete User
                                    </button>
                                  </div>
                                )}
                              </div>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Create User View */}
            {activeView === "create" && (
              <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
                <h2 className="text-xl font-semibold mb-6">Create New User</h2>
                
                <form onSubmit={handleCreateUser} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium mb-2">Full Name *</label>
                      <input
                        type="text"
                        value={formData.name}
                        onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                        className={`w-full px-4 py-3 border rounded-lg dark:bg-gray-700 ${
                          validationErrors.name 
                            ? 'border-red-500 focus:ring-red-500' 
                            : 'border-gray-300 dark:border-gray-600'
                        }`}
                        placeholder="John Doe"
                      />
                      {validationErrors.name && (
                        <p className="text-red-500 text-xs mt-1 flex items-center gap-1">
                          <AlertCircle className="w-3 h-3" />
                          {validationErrors.name}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">Email *</label>
                      <input
                        type="email"
                        value={formData.email}
                        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                        className={`w-full px-4 py-3 border rounded-lg dark:bg-gray-700 ${
                          validationErrors.email 
                            ? 'border-red-500 focus:ring-red-500' 
                            : 'border-gray-300 dark:border-gray-600'
                        }`}
                        placeholder="john.doe@drdo.gov.in"
                      />
                      {validationErrors.email && (
                        <p className="text-red-500 text-xs mt-1 flex items-center gap-1">
                          <AlertCircle className="w-3 h-3" />
                          {validationErrors.email}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">Designation *</label>
                      <input
                        type="text"
                        value={formData.designation}
                        onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
                        className={`w-full px-4 py-3 border rounded-lg dark:bg-gray-700 ${
                          validationErrors.designation 
                            ? 'border-red-500 focus:ring-red-500' 
                            : 'border-gray-300 dark:border-gray-600'
                        }`}
                        placeholder="Senior Scientist"
                      />
                      {validationErrors.designation && (
                        <p className="text-red-500 text-xs mt-1 flex items-center gap-1">
                          <AlertCircle className="w-3 h-3" />
                          {validationErrors.designation}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">Department</label>
                      <input
                        type="text"
                        value={formData.department}
                        onChange={(e) => setFormData({ ...formData, department: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                        placeholder="Research & Development"
                      />
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">Establishment *</label>
                      <input
                        type="text"
                        value={formData.establishment}
                        onChange={(e) => setFormData({ ...formData, establishment: e.target.value })}
                        className={`w-full px-4 py-3 border rounded-lg dark:bg-gray-700 ${
                          validationErrors.establishment 
                            ? 'border-red-500 focus:ring-red-500' 
                            : 'border-gray-300 dark:border-gray-600'
                        }`}
                        placeholder="DRDO Delhi"
                      />
                      {validationErrors.establishment && (
                        <p className="text-red-500 text-xs mt-1 flex items-center gap-1">
                          <AlertCircle className="w-3 h-3" />
                          {validationErrors.establishment}
                        </p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium mb-2">Role</label>
                      <select
                        value={formData.role}
                        onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                        className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                      >
                        <option value="user">User</option>
                        <option value="admin">Admin</option>
                        <option value="manager">Manager</option>
                      </select>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium mb-2">Temporary Password *</label>
                    <div className="flex gap-2">
                      <div className="relative flex-1">
                        <input
                          type={showPassword ? "text" : "password"}
                          value={formData.temp_password}
                          onChange={(e) => setFormData({ ...formData, temp_password: e.target.value })}
                          className={`w-full px-4 py-3 border rounded-lg dark:bg-gray-700 pr-10 ${
                            validationErrors.temp_password 
                              ? 'border-red-500 focus:ring-red-500' 
                              : 'border-gray-300 dark:border-gray-600'
                          }`}
                          placeholder="Click generate or enter manually"
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500"
                        >
                          {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                        </button>
                      </div>
                      <button
                        type="button"
                        onClick={generatePassword}
                        className="px-4 py-3 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
                      >
                        <RefreshCw className="w-5 h-5" />
                      </button>
                    </div>
                    {validationErrors.temp_password && (
                      <p className="text-red-500 text-xs mt-1 flex items-center gap-1">
                        <AlertCircle className="w-3 h-3" />
                        {validationErrors.temp_password}
                      </p>
                    )}
                    <p className="text-xs text-gray-500 mt-1">User will be required to change this on first login</p>
                  </div>

                  <div className="flex gap-3 pt-4">
                    <button
                      type="submit"
                      disabled={loading}
                      className="flex-1 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                    >
                      <UserPlus className="w-4 h-4" />
                      {loading ? "Creating..." : "Create User"}
                    </button>
                    <button
                      type="button"
                      onClick={() => setActiveView("users")}
                      className="px-6 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    >
                      Cancel
                    </button>
                  </div>
                </form>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* User Profile Modal */}
      {showUserProfile && selectedUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-y-auto"
          >
            <div className="p-6">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-2xl font-semibold">User Profile</h3>
                <button
                  onClick={() => {
                    setShowUserProfile(false);
                    setSelectedUser(null);
                  }}
                  className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                >
                  <XCircle className="w-6 h-6" />
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-3 flex items-center gap-2">
                    <User className="w-4 h-4" />
                    Personal Information
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div><span className="text-gray-600 dark:text-gray-400">Name:</span> {selectedUser.name || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Email:</span> {selectedUser.email || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Phone:</span> {selectedUser.phone || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">DOB:</span> {selectedUser.date_of_birth || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Gender:</span> {selectedUser.gender || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Blood Group:</span> {selectedUser.blood_group || '-'}</div>
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold mb-3 flex items-center gap-2">
                    <Briefcase className="w-4 h-4" />
                    Employment Details
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div><span className="text-gray-600 dark:text-gray-400">Employee ID:</span> {selectedUser.employee_id || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Designation:</span> {selectedUser.designation || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Department:</span> {selectedUser.department || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Division:</span> {selectedUser.division || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Establishment:</span> {selectedUser.establishment || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Grade:</span> {selectedUser.grade_level || '-'}</div>
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold mb-3 flex items-center gap-2">
                    <Phone className="w-4 h-4" />
                    Contact Information
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div><span className="text-gray-600 dark:text-gray-400">Emergency Contact:</span> {selectedUser.emergency_contact_name || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">Emergency Phone:</span> {selectedUser.emergency_contact_number || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">City:</span> {selectedUser.city || '-'}</div>
                    <div><span className="text-gray-600 dark:text-gray-400">State:</span> {selectedUser.state || '-'}</div>
                  </div>
                </div>

                <div>
                  <h4 className="font-semibold mb-3 flex items-center gap-2">
                    <Activity className="w-4 h-4" />
                    Account Status
                  </h4>
                  <div className="space-y-2 text-sm">
                    <div><span className="text-gray-600 dark:text-gray-400">Status:</span> 
                      {selectedUser.is_active ? 
                        <span className="ml-2 text-green-600">Active</span> : 
                        <span className="ml-2 text-gray-600">Inactive</span>
                      }
                    </div>
                    <div><span className="text-gray-600 dark:text-gray-400">Role:</span> <span className="ml-2 capitalize">{selectedUser.role || '-'}</span></div>
                    <div><span className="text-gray-600 dark:text-gray-400">Onboarding:</span> 
                      {selectedUser.onboarding_completed ? 
                        <span className="ml-2 text-green-600">Complete</span> : 
                        <span className="ml-2 text-yellow-600">Pending</span>
                      }
                    </div>
                    <div><span className="text-gray-600 dark:text-gray-400">Last Login:</span> {selectedUser.last_login || 'Never'}</div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      )}

      {/* Password Reset Modal */}
      {showPasswordModal && selectedUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6"
          >
            <h3 className="text-xl font-semibold mb-4">Reset Password</h3>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Are you sure you want to reset the password for <strong>{selectedUser.name}</strong>? 
              A new temporary password will be generated.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => handleResetPassword(selectedUser.id)}
                disabled={loading}
                className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {loading ? "Resetting..." : "Reset Password"}
              </button>
              <button
                onClick={() => {
                  setShowPasswordModal(false);
                  setSelectedUser(null);
                }}
                className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
            </div>
          </motion.div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteModal && selectedUser && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6"
          >
            <div className="flex items-center gap-3 text-red-600 mb-4">
              <AlertCircle className="w-6 h-6" />
              <h3 className="text-xl font-semibold">Delete User</h3>
            </div>
            <p className="text-gray-600 dark:text-gray-400 mb-6">
              Are you sure you want to delete <strong>{selectedUser.name}</strong>? 
              This action cannot be undone and will permanently remove all user data.
            </p>
            <div className="flex gap-3">
              <button
                onClick={() => handleDeleteUser(selectedUser.id)}
                disabled={loading}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors disabled:opacity-50"
              >
                {loading ? "Deleting..." : "Delete User"}
              </button>
              <button
                onClick={() => {
                  setShowDeleteModal(false);
                  setSelectedUser(null);
                }}
                className="px-4 py-2 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
              >
                Cancel
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default SuperAdminDashboard;
