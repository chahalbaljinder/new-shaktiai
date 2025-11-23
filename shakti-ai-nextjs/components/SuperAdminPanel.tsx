"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import {
  UserPlus, Users, Mail, Briefcase, Building, Eye,
  EyeOff, Copy, CheckCircle, XCircle, Search, Filter,
  Download, Trash2, RefreshCw
} from "lucide-react";

const SuperAdminPanel = () => {
  const [activeTab, setActiveTab] = useState<"create" | "list">("create");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  const [employees, setEmployees] = useState<any[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    designation: "",
    establishment: "",
    department: "",
    role: "user",
    temp_password: ""
  });

  const [generatedCreds, setGeneratedCreds] = useState<any>(null);
  const [showPassword, setShowPassword] = useState(false);

  useEffect(() => {
    if (activeTab === "list") {
      fetchEmployees();
    }
  }, [activeTab]);

  const showMessage = (type: "success" | "error", text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 4000);
  };

  const generatePassword = () => {
    const password = `Welcome@${Math.floor(Math.random() * 9000 + 1000)}`;
    setFormData({ ...formData, temp_password: password });
  };

  const fetchEmployees = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:8000/api/admin/employees");
      const data = await response.json();
      setEmployees(data.employees || []);
    } catch (error) {
      showMessage("error", "Failed to fetch employees");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateEmployee = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!formData.name || !formData.email || !formData.designation || !formData.establishment) {
      showMessage("error", "Please fill all required fields");
      return;
    }

    if (!formData.temp_password) {
      showMessage("error", "Please generate a temporary password");
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
        showMessage("success", "Employee created successfully!");
        setGeneratedCreds({
          ...data.employee,
          temp_password: formData.temp_password
        });
        
        // Reset form
        setFormData({
          name: "",
          email: "",
          designation: "",
          establishment: "",
          department: "",
          role: "user",
          temp_password: ""
        });
      } else {
        showMessage("error", data.error || "Failed to create employee");
      }
    } catch (error) {
      showMessage("error", "Failed to create employee");
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    showMessage("success", `${label} copied to clipboard!`);
  };

  const filteredEmployees = employees.filter(emp =>
    emp.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    emp.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    emp.employee_id?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          SuperAdmin Panel
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Create and manage employee accounts
        </p>
      </div>

      {/* Success/Error Message */}
      {message && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0 }}
          className={`mb-4 p-4 rounded-lg flex items-center gap-3 ${
            message.type === "success"
              ? "bg-green-50 dark:bg-green-900/20 text-green-800 dark:text-green-300"
              : "bg-red-50 dark:bg-red-900/20 text-red-800 dark:text-red-300"
          }`}
        >
          {message.type === "success" ? <CheckCircle className="w-5 h-5" /> : <XCircle className="w-5 h-5" />}
          <span>{message.text}</span>
        </motion.div>
      )}

      {/* Tabs */}
      <div className="mb-6 bg-white dark:bg-gray-800 rounded-lg shadow p-2">
        <div className="flex gap-2">
          <button
            onClick={() => setActiveTab("create")}
            className={`flex items-center gap-2 px-6 py-3 rounded-md font-medium transition-all ${
              activeTab === "create"
                ? "bg-blue-600 text-white shadow-md"
                : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            <UserPlus className="w-4 h-4" />
            Create Employee
          </button>
          <button
            onClick={() => setActiveTab("list")}
            className={`flex items-center gap-2 px-6 py-3 rounded-md font-medium transition-all ${
              activeTab === "list"
                ? "bg-blue-600 text-white shadow-md"
                : "text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700"
            }`}
          >
            <Users className="w-4 h-4" />
            Employee List ({employees.length})
          </button>
        </div>
      </div>

      {/* Create Employee Tab */}
      {activeTab === "create" && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Form */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-6">Create New Employee</h2>
            
            <form onSubmit={handleCreateEmployee} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">Full Name *</label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  placeholder="John Doe"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Email *</label>
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  placeholder="john.doe@example.com"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Designation *</label>
                <input
                  type="text"
                  value={formData.designation}
                  onChange={(e) => setFormData({ ...formData, designation: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  placeholder="Senior Scientist"
                />
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
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  placeholder="DRDO Delhi"
                />
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

              <div>
                <label className="block text-sm font-medium mb-2">Temporary Password *</label>
                <div className="flex gap-2">
                  <div className="relative flex-1">
                    <input
                      type={showPassword ? "text" : "password"}
                      value={formData.temp_password}
                      onChange={(e) => setFormData({ ...formData, temp_password: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 pr-10"
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
                <p className="text-xs text-gray-500 mt-1">Employee will be required to change this on first login</p>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
              >
                <UserPlus className="w-4 h-4" />
                {loading ? "Creating..." : "Create Employee"}
              </button>
            </form>
          </div>

          {/* Generated Credentials Display */}
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-6">Employee Credentials</h2>
            
            {generatedCreds ? (
              <div className="space-y-4">
                <div className="p-4 bg-green-50 dark:bg-green-900/20 rounded-lg">
                  <p className="text-sm text-green-800 dark:text-green-300 mb-3 flex items-center gap-2">
                    <CheckCircle className="w-4 h-4" />
                    Employee created successfully! Share these credentials:
                  </p>
                </div>

                <div className="space-y-3">
                  <div className="p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Employee ID</div>
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-lg font-bold">{generatedCreds.employee_id}</span>
                      <button
                        onClick={() => copyToClipboard(generatedCreds.employee_id, "Employee ID")}
                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Name</div>
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{generatedCreds.name}</span>
                      <button
                        onClick={() => copyToClipboard(generatedCreds.name, "Name")}
                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="p-4 border-2 border-gray-200 dark:border-gray-700 rounded-lg">
                    <div className="text-sm text-gray-600 dark:text-gray-400 mb-1">Email</div>
                    <div className="flex items-center justify-between">
                      <span className="font-medium">{generatedCreds.email}</span>
                      <button
                        onClick={() => copyToClipboard(generatedCreds.email, "Email")}
                        className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  <div className="p-4 border-2 border-red-200 dark:border-red-700 rounded-lg bg-red-50 dark:bg-red-900/10">
                    <div className="text-sm text-red-600 dark:text-red-400 mb-1 font-medium">Temporary Password</div>
                    <div className="flex items-center justify-between">
                      <span className="font-mono text-lg font-bold">{generatedCreds.temp_password}</span>
                      <button
                        onClick={() => copyToClipboard(generatedCreds.temp_password, "Password")}
                        className="p-2 hover:bg-red-100 dark:hover:bg-red-900/20 rounded"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                    <p className="text-xs text-red-600 dark:text-red-400 mt-2">
                      ⚠️ Employee must change this password on first login
                    </p>
                  </div>
                </div>

                <button
                  onClick={() => {
                    const text = `Employee Credentials:\n\nEmployee ID: ${generatedCreds.employee_id}\nName: ${generatedCreds.name}\nEmail: ${generatedCreds.email}\nTemporary Password: ${generatedCreds.temp_password}\n\nPlease change your password on first login.`;
                    copyToClipboard(text, "All credentials");
                  }}
                  className="w-full px-4 py-3 bg-gray-200 dark:bg-gray-700 rounded-lg hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors flex items-center justify-center gap-2"
                >
                  <Copy className="w-4 h-4" />
                  Copy All Credentials
                </button>
              </div>
            ) : (
              <div className="text-center py-12">
                <Users className="w-16 h-16 mx-auto mb-4 text-gray-400" />
                <p className="text-gray-600 dark:text-gray-400">
                  Create an employee to see their credentials here
                </p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Employee List Tab */}
      {activeTab === "list" && (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow">
          {/* Search Bar */}
          <div className="p-4 border-b border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-4">
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
              <button
                onClick={fetchEmployees}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <RefreshCw className="w-4 h-4" />
                Refresh
              </button>
            </div>
          </div>

          {/* Table */}
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50 dark:bg-gray-700">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Employee ID
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Name
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                    Designation
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
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 dark:divide-gray-700">
                {filteredEmployees.length === 0 ? (
                  <tr>
                    <td colSpan={7} className="px-6 py-8 text-center text-gray-500 dark:text-gray-400">
                      No employees found
                    </td>
                  </tr>
                ) : (
                  filteredEmployees.map((emp) => (
                    <tr key={emp.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="font-mono text-sm font-medium">{emp.employee_id}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="font-medium">{emp.name}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm text-gray-600 dark:text-gray-400">{emp.email}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm">{emp.designation || '-'}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="text-sm">{emp.department || '-'}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {emp.onboarding_completed ? (
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
                        {emp.is_active ? (
                          <span className="px-2 py-1 text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-400 rounded-full">
                            Active
                          </span>
                        ) : (
                          <span className="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-400 rounded-full">
                            Inactive
                          </span>
                        )}
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
};

export default SuperAdminPanel;
