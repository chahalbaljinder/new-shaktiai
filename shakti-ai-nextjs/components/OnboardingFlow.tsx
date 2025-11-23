"use client";

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  User, Mail, Phone, MapPin, Briefcase, GraduationCap,
  Award, CheckCircle, ArrowRight, ArrowLeft, Lock,
  Calendar, Globe, Heart, Home, Building, CreditCard,
  Shield, Eye, EyeOff, AlertCircle
} from "lucide-react";
import { useAuth } from "./AuthProvider";

interface OnboardingStep {
  id: number;
  title: string;
  description: string;
  icon: any;
  fields: string[];
}

const OnboardingFlow = ({ onComplete }: { onComplete: () => void }) => {
  const { user } = useAuth();
  const [currentStep, setCurrentStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<{ type: "success" | "error"; text: string } | null>(null);
  
  // Form data for each step
  const [passwordData, setPasswordData] = useState({
    newPassword: "",
    confirmPassword: "",
    showPassword: false,
    showConfirm: false
  });
  
  const [personalData, setPersonalData] = useState({
    name: "",
    email: "",
    phone: "",
    mobileNumber: "",
    dateOfBirth: "",
    gender: "",
    bloodGroup: "",
    maritalStatus: "",
    nationality: "Indian"
  });

  const [contactData, setContactData] = useState({
    alternateEmail: "",
    emergencyContactName: "",
    emergencyContactNumber: "",
    emergencyContactRelation: "",
    currentAddress: "",
    permanentAddress: "",
    city: "",
    state: "",
    pincode: ""
  });

  const [employmentData, setEmploymentData] = useState({
    designation: "",
    department: "",
    division: "",
    section: "",
    establishment: "",
    gradeLevel: "",
    workLocation: "",
    officeRoom: "",
    extensionNumber: ""
  });

  const [educationData, setEducationData] = useState({
    highestDegree: "",
    specialization: "",
    university: "",
    graduationYear: ""
  });

  const [skillsData, setSkillsData] = useState({
    technicalSkills: "",
    certifications: "",
    languages: "",
    yearsOfExperience: ""
  });

  const steps: OnboardingStep[] = [
    {
      id: 0,
      title: "Change Password",
      description: "Set a secure password for your account",
      icon: Lock,
      fields: ["password"]
    },
    {
      id: 1,
      title: "Personal Information",
      description: "Tell us about yourself",
      icon: User,
      fields: ["name", "email", "phone", "dateOfBirth", "gender"]
    },
    {
      id: 2,
      title: "Contact Details",
      description: "How can we reach you?",
      icon: Phone,
      fields: ["alternateEmail", "emergencyContact", "address"]
    },
    {
      id: 3,
      title: "Employment Information",
      description: "Your role and department details",
      icon: Briefcase,
      fields: ["designation", "department", "division"]
    },
    {
      id: 4,
      title: "Education & Skills",
      description: "Your qualifications and expertise",
      icon: GraduationCap,
      fields: ["education", "skills"]
    }
  ];

  useEffect(() => {
    if (user?.id) {
      fetchUserData();
    }
  }, [user]);

  const fetchUserData = async () => {
    const userId = user?.id || 3;
    try {
      const response = await fetch(`http://localhost:8000/api/settings/employee/complete?user_id=${userId}`);
      const data = await response.json();
      
      // Pre-fill existing data
      setPersonalData({
        name: data.name || "",
        email: data.email || "",
        phone: data.phone || "",
        mobileNumber: data.mobile_number || "",
        dateOfBirth: data.date_of_birth || "",
        gender: data.gender || "",
        bloodGroup: data.blood_group || "",
        maritalStatus: data.marital_status || "",
        nationality: data.nationality || "Indian"
      });

      setEmploymentData({
        designation: data.designation || "",
        department: data.department || "",
        division: data.division || "",
        section: data.section || "",
        establishment: data.establishment || "",
        gradeLevel: data.grade_level || "",
        workLocation: data.work_location || "",
        officeRoom: data.office_room || "",
        extensionNumber: data.extension_number || ""
      });

      // Check if user needs to change password
      if (data.must_change_password) {
        setCurrentStep(0);
      } else if (data.onboarding_step !== undefined) {
        setCurrentStep(data.onboarding_step);
      }
    } catch (error) {
      console.error("Failed to fetch user data:", error);
    }
  };

  const showMessage = (type: "success" | "error", text: string) => {
    setMessage({ type, text });
    setTimeout(() => setMessage(null), 3000);
  };

  const validateStep = () => {
    switch (currentStep) {
      case 0: // Password
        if (!passwordData.newPassword || passwordData.newPassword.length < 6) {
          showMessage("error", "Password must be at least 6 characters");
          return false;
        }
        if (passwordData.newPassword !== passwordData.confirmPassword) {
          showMessage("error", "Passwords do not match");
          return false;
        }
        return true;

      case 1: // Personal Info
        if (!personalData.name || !personalData.email || !personalData.phone) {
          showMessage("error", "Please fill all required fields (marked with *)");
          return false;
        }
        return true;

      case 2: // Contact
        if (!contactData.emergencyContactName || !contactData.emergencyContactNumber) {
          showMessage("error", "Emergency contact details are required");
          return false;
        }
        return true;

      case 3: // Employment
        if (!employmentData.designation || !employmentData.department) {
          showMessage("error", "Designation and department are required");
          return false;
        }
        return true;

      case 4: // Education & Skills
        return true; // Optional fields

      default:
        return true;
    }
  };

  const saveStepData = async () => {
    const userId = user?.id || 3;
    setLoading(true);

    try {
      switch (currentStep) {
        case 0: // Password
          const pwResponse = await fetch("http://localhost:8000/api/settings/password", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: userId,
              new_password: passwordData.newPassword,
              is_first_time: true
            }),
          });
          if (!pwResponse.ok) throw new Error("Password change failed");
          break;

        case 1: // Personal Info
          const personalResponse = await fetch("http://localhost:8000/api/settings/employee/personal", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, ...personalData }),
          });
          if (!personalResponse.ok) throw new Error("Failed to save personal info");
          break;

        case 2: // Contact
          const contactResponse = await fetch("http://localhost:8000/api/settings/employee/contact", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, ...contactData }),
          });
          if (!contactResponse.ok) throw new Error("Failed to save contact info");
          break;

        case 3: // Employment
          const empResponse = await fetch("http://localhost:8000/api/settings/employee/employment", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, ...employmentData }),
          });
          if (!empResponse.ok) throw new Error("Failed to save employment info");
          break;

        case 4: // Education & Skills
          const eduResponse = await fetch("http://localhost:8000/api/settings/employee/education", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, ...educationData }),
          });
          const skillResponse = await fetch("http://localhost:8000/api/settings/employee/skills", {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, ...skillsData }),
          });
          if (!eduResponse.ok || !skillResponse.ok) throw new Error("Failed to save education/skills");
          break;
      }

      // Update onboarding step
      await fetch("http://localhost:8000/api/auth/onboarding/update-step", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: userId, step: currentStep + 1 }),
      });

      return true;
    } catch (error) {
      showMessage("error", "Failed to save data. Please try again.");
      return false;
    } finally {
      setLoading(false);
    }
  };

  const handleNext = async () => {
    if (!validateStep()) return;

    const saved = await saveStepData();
    if (!saved) return;

    if (currentStep === steps.length - 1) {
      // Complete onboarding
      await fetch("http://localhost:8000/api/auth/onboarding/complete", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: user?.id || 3 }),
      });
      showMessage("success", "Onboarding completed successfully!");
      setTimeout(() => onComplete(), 1500);
    } else {
      setCurrentStep(currentStep + 1);
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const renderStepContent = () => {
    const step = steps[currentStep];

    switch (currentStep) {
      case 0: // Password
        return (
          <div className="space-y-4">
            <div className="p-4 bg-amber-50 dark:bg-amber-900/20 rounded-lg flex items-start gap-3 mb-6">
              <AlertCircle className="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-amber-800 dark:text-amber-300">
                <p className="font-medium mb-1">First Time Setup</p>
                <p>Please change your temporary password to a secure one that you'll remember.</p>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">New Password *</label>
              <div className="relative">
                <input
                  type={passwordData.showPassword ? "text" : "password"}
                  value={passwordData.newPassword}
                  onChange={(e) => setPasswordData({ ...passwordData, newPassword: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 pr-10"
                  placeholder="Enter new password (min 6 characters)"
                />
                <button
                  type="button"
                  onClick={() => setPasswordData({ ...passwordData, showPassword: !passwordData.showPassword })}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500"
                >
                  {passwordData.showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Confirm Password *</label>
              <div className="relative">
                <input
                  type={passwordData.showConfirm ? "text" : "password"}
                  value={passwordData.confirmPassword}
                  onChange={(e) => setPasswordData({ ...passwordData, confirmPassword: e.target.value })}
                  className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700 pr-10"
                  placeholder="Re-enter password"
                />
                <button
                  type="button"
                  onClick={() => setPasswordData({ ...passwordData, showConfirm: !passwordData.showConfirm })}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500"
                >
                  {passwordData.showConfirm ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                </button>
              </div>
            </div>
          </div>
        );

      case 1: // Personal Info
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Full Name *</label>
              <input
                type="text"
                value={personalData.name}
                onChange={(e) => setPersonalData({ ...personalData, name: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Email *</label>
              <input
                type="email"
                value={personalData.email}
                onChange={(e) => setPersonalData({ ...personalData, email: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Phone Number *</label>
              <input
                type="tel"
                value={personalData.phone}
                onChange={(e) => setPersonalData({ ...personalData, phone: e.target.value })}
                placeholder="+91-9876543210"
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Mobile Number</label>
              <input
                type="tel"
                value={personalData.mobileNumber}
                onChange={(e) => setPersonalData({ ...personalData, mobileNumber: e.target.value })}
                placeholder="+91-9876543210"
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Date of Birth</label>
              <input
                type="date"
                value={personalData.dateOfBirth}
                onChange={(e) => setPersonalData({ ...personalData, dateOfBirth: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Gender</label>
              <select
                value={personalData.gender}
                onChange={(e) => setPersonalData({ ...personalData, gender: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              >
                <option value="">Select Gender</option>
                <option value="Male">Male</option>
                <option value="Female">Female</option>
                <option value="Other">Other</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Blood Group</label>
              <select
                value={personalData.bloodGroup}
                onChange={(e) => setPersonalData({ ...personalData, bloodGroup: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              >
                <option value="">Select Blood Group</option>
                <option value="A+">A+</option>
                <option value="A-">A-</option>
                <option value="B+">B+</option>
                <option value="B-">B-</option>
                <option value="O+">O+</option>
                <option value="O-">O-</option>
                <option value="AB+">AB+</option>
                <option value="AB-">AB-</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Marital Status</label>
              <select
                value={personalData.maritalStatus}
                onChange={(e) => setPersonalData({ ...personalData, maritalStatus: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              >
                <option value="">Select Status</option>
                <option value="Single">Single</option>
                <option value="Married">Married</option>
                <option value="Divorced">Divorced</option>
                <option value="Widowed">Widowed</option>
              </select>
            </div>
          </div>
        );

      case 2: // Contact
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Heart className="w-5 h-5 text-red-600" />
                Emergency Contact *
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Name *</label>
                  <input
                    type="text"
                    value={contactData.emergencyContactName}
                    onChange={(e) => setContactData({ ...contactData, emergencyContactName: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Phone *</label>
                  <input
                    type="tel"
                    value={contactData.emergencyContactNumber}
                    onChange={(e) => setContactData({ ...contactData, emergencyContactNumber: e.target.value })}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Relation</label>
                  <input
                    type="text"
                    value={contactData.emergencyContactRelation}
                    onChange={(e) => setContactData({ ...contactData, emergencyContactRelation: e.target.value })}
                    placeholder="Spouse, Parent, etc."
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  />
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <Home className="w-5 h-5 text-blue-600" />
                Address Details
              </h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Current Address</label>
                  <textarea
                    value={contactData.currentAddress}
                    onChange={(e) => setContactData({ ...contactData, currentAddress: e.target.value })}
                    rows={2}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  />
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <label className="block text-sm font-medium mb-2">City</label>
                    <input
                      type="text"
                      value={contactData.city}
                      onChange={(e) => setContactData({ ...contactData, city: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">State</label>
                    <input
                      type="text"
                      value={contactData.state}
                      onChange={(e) => setContactData({ ...contactData, state: e.target.value })}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                    />
                  </div>
                  <div>
                    <label className="block text-sm font-medium mb-2">Pincode</label>
                    <input
                      type="text"
                      value={contactData.pincode}
                      onChange={(e) => setContactData({ ...contactData, pincode: e.target.value })}
                      maxLength={6}
                      className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        );

      case 3: // Employment
        return (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">Designation *</label>
              <input
                type="text"
                value={employmentData.designation}
                onChange={(e) => setEmploymentData({ ...employmentData, designation: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Department *</label>
              <input
                type="text"
                value={employmentData.department}
                onChange={(e) => setEmploymentData({ ...employmentData, department: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Division</label>
              <input
                type="text"
                value={employmentData.division}
                onChange={(e) => setEmploymentData({ ...employmentData, division: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Section</label>
              <input
                type="text"
                value={employmentData.section}
                onChange={(e) => setEmploymentData({ ...employmentData, section: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Establishment</label>
              <input
                type="text"
                value={employmentData.establishment}
                onChange={(e) => setEmploymentData({ ...employmentData, establishment: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Grade Level</label>
              <select
                value={employmentData.gradeLevel}
                onChange={(e) => setEmploymentData({ ...employmentData, gradeLevel: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              >
                <option value="">Select Grade</option>
                <option value="A1">A1 - Junior Scientist</option>
                <option value="A2">A2 - Scientist</option>
                <option value="B1">B1 - Senior Scientist</option>
                <option value="B2">B2 - Principal Scientist</option>
                <option value="C">C - Director</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Work Location</label>
              <input
                type="text"
                value={employmentData.workLocation}
                onChange={(e) => setEmploymentData({ ...employmentData, workLocation: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Office Room</label>
              <input
                type="text"
                value={employmentData.officeRoom}
                onChange={(e) => setEmploymentData({ ...employmentData, officeRoom: e.target.value })}
                className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
              />
            </div>
          </div>
        );

      case 4: // Education & Skills
        return (
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold mb-4">Education</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Highest Degree</label>
                  <input
                    type="text"
                    value={educationData.highestDegree}
                    onChange={(e) => setEducationData({ ...educationData, highestDegree: e.target.value })}
                    placeholder="e.g., M.Tech, PhD"
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Specialization</label>
                  <input
                    type="text"
                    value={educationData.specialization}
                    onChange={(e) => setEducationData({ ...educationData, specialization: e.target.value })}
                    placeholder="e.g., Computer Science"
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  />
                </div>
              </div>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Skills & Experience</h3>
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Technical Skills</label>
                  <input
                    type="text"
                    value={skillsData.technicalSkills}
                    onChange={(e) => setSkillsData({ ...skillsData, technicalSkills: e.target.value })}
                    placeholder="Python, Machine Learning, etc. (comma separated)"
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium mb-2">Years of Experience</label>
                  <input
                    type="number"
                    value={skillsData.yearsOfExperience}
                    onChange={(e) => setSkillsData({ ...skillsData, yearsOfExperience: e.target.value })}
                    min="0"
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg dark:bg-gray-700"
                  />
                </div>
              </div>
            </div>
          </div>
        );

      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center p-4">
      <div className="max-w-4xl w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            Welcome to APEX! 👋
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Let's complete your profile setup to get started
          </p>
        </div>

        {/* Progress Bar */}
        <div className="mb-8">
          <div className="flex justify-between mb-2">
            {steps.map((step, index) => (
              <div
                key={step.id}
                className={`flex-1 text-center ${
                  index < steps.length - 1 ? "mr-2" : ""
                }`}
              >
                <div
                  className={`w-full h-2 rounded-full transition-all ${
                    index <= currentStep
                      ? "bg-blue-600"
                      : "bg-gray-300 dark:bg-gray-700"
                  }`}
                />
                <p
                  className={`text-xs mt-1 ${
                    index <= currentStep
                      ? "text-blue-600 font-medium"
                      : "text-gray-400"
                  }`}
                >
                  {index + 1}/{steps.length}
                </p>
              </div>
            ))}
          </div>
        </div>

        {/* Success/Error Message */}
        <AnimatePresence>
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
              {message.type === "success" ? (
                <CheckCircle className="w-5 h-5" />
              ) : (
                <AlertCircle className="w-5 h-5" />
              )}
              <span>{message.text}</span>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Main Card */}
        <motion.div
          key={currentStep}
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          exit={{ opacity: 0, x: -20 }}
          className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl p-8"
        >
          {/* Step Header */}
          <div className="mb-6">
            <div className="flex items-center gap-4 mb-4">
              <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center">
                {React.createElement(steps[currentStep].icon, {
                  className: "w-6 h-6 text-white",
                })}
              </div>
              <div>
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  {steps[currentStep].title}
                </h2>
                <p className="text-gray-600 dark:text-gray-400">
                  {steps[currentStep].description}
                </p>
              </div>
            </div>
          </div>

          {/* Step Content */}
          <div className="mb-8">{renderStepContent()}</div>

          {/* Navigation Buttons */}
          <div className="flex justify-between gap-4">
            <button
              onClick={handleBack}
              disabled={currentStep === 0 || loading}
              className="px-6 py-3 border-2 border-gray-300 dark:border-gray-600 rounded-lg hover:border-blue-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              <ArrowLeft className="w-4 h-4" />
              Back
            </button>

            <button
              onClick={handleNext}
              disabled={loading}
              className="px-8 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center gap-2"
            >
              {loading ? (
                "Saving..."
              ) : currentStep === steps.length - 1 ? (
                <>
                  Complete Setup <CheckCircle className="w-4 h-4" />
                </>
              ) : (
                <>
                  Next <ArrowRight className="w-4 h-4" />
                </>
              )}
            </button>
          </div>
        </motion.div>

        {/* Step Indicators */}
        <div className="flex justify-center gap-2 mt-6">
          {steps.map((step, index) => (
            <div
              key={step.id}
              className={`w-2 h-2 rounded-full transition-all ${
                index === currentStep
                  ? "w-8 bg-blue-600"
                  : index < currentStep
                  ? "bg-green-600"
                  : "bg-gray-300 dark:bg-gray-700"
              }`}
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default OnboardingFlow;
