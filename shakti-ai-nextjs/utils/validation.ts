/**
 * Validation Utilities
 * Comprehensive validation functions for the application
 */

// Email validation
export const validateEmail = (email: string): { valid: boolean; error?: string } => {
  if (!email || email.trim() === '') {
    return { valid: false, error: 'Email is required' };
  }

  // RFC 5322 compliant email regex
  const emailRegex = /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$/;
  
  if (!emailRegex.test(email.trim())) {
    return { valid: false, error: 'Invalid email format' };
  }

  // Check for common government email domains
  const govDomains = ['gov.in', 'nic.in', 'drdo.gov.in'];
  const domain = email.split('@')[1]?.toLowerCase();
  
  // Optional: Uncomment to enforce government email only
  // if (!govDomains.some(govDomain => domain?.endsWith(govDomain))) {
  //   return { valid: false, error: 'Only government email addresses are allowed' };
  // }

  return { valid: true };
};

// Phone number validation (Indian format)
export const validatePhone = (phone: string): { valid: boolean; error?: string } => {
  if (!phone || phone.trim() === '') {
    return { valid: false, error: 'Phone number is required' };
  }

  // Remove all non-digit characters
  const cleanPhone = phone.replace(/\D/g, '');

  // Check for valid Indian mobile number (10 digits starting with 6-9)
  const mobileRegex = /^[6-9]\d{9}$/;
  
  // Check for landline with STD code (10-11 digits)
  const landlineRegex = /^0?\d{10,11}$/;

  if (mobileRegex.test(cleanPhone)) {
    return { valid: true };
  }

  if (landlineRegex.test(cleanPhone)) {
    return { valid: true };
  }

  return { 
    valid: false, 
    error: 'Invalid phone number. Must be 10 digits for mobile or 10-11 digits for landline' 
  };
};

// Format phone number for display
export const formatPhone = (phone: string): string => {
  const cleanPhone = phone.replace(/\D/g, '');
  
  if (cleanPhone.length === 10) {
    return cleanPhone.replace(/(\d{5})(\d{5})/, '$1-$2');
  }
  
  return phone;
};

// Pincode validation (Indian)
export const validatePincode = (pincode: string): { valid: boolean; error?: string } => {
  if (!pincode || pincode.trim() === '') {
    return { valid: false, error: 'Pincode is required' };
  }

  const cleanPincode = pincode.replace(/\D/g, '');
  const pincodeRegex = /^[1-9]\d{5}$/;

  if (!pincodeRegex.test(cleanPincode)) {
    return { 
      valid: false, 
      error: 'Invalid pincode. Must be 6 digits and cannot start with 0' 
    };
  }

  return { valid: true };
};

// Aadhaar validation
export const validateAadhaar = (aadhaar: string): { valid: boolean; error?: string } => {
  if (!aadhaar || aadhaar.trim() === '') {
    return { valid: false, error: 'Aadhaar number is required' };
  }

  const cleanAadhaar = aadhaar.replace(/\D/g, '');

  if (cleanAadhaar.length !== 12) {
    return { valid: false, error: 'Aadhaar must be 12 digits' };
  }

  // Verhoeff algorithm for Aadhaar validation
  const d = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
  ];

  const p = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8]
  ];

  let c = 0;
  const invertedArray = cleanAadhaar.split('').map(Number).reverse();

  invertedArray.forEach((val, i) => {
    c = d[c][p[(i % 8)][val]];
  });

  if (c !== 0) {
    return { valid: false, error: 'Invalid Aadhaar number' };
  }

  return { valid: true };
};

// Format Aadhaar for display (XXXX-XXXX-XXXX)
export const formatAadhaar = (aadhaar: string): string => {
  const cleanAadhaar = aadhaar.replace(/\D/g, '');
  return cleanAadhaar.replace(/(\d{4})(\d{4})(\d{4})/, '$1-$2-$3');
};

// PAN validation
export const validatePAN = (pan: string): { valid: boolean; error?: string } => {
  if (!pan || pan.trim() === '') {
    return { valid: false, error: 'PAN is required' };
  }

  const panRegex = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;

  if (!panRegex.test(pan.toUpperCase())) {
    return { 
      valid: false, 
      error: 'Invalid PAN format. Format: ABCDE1234F' 
    };
  }

  return { valid: true };
};

// Bank account number validation
export const validateBankAccount = (accountNumber: string): { valid: boolean; error?: string } => {
  if (!accountNumber || accountNumber.trim() === '') {
    return { valid: false, error: 'Bank account number is required' };
  }

  const cleanAccount = accountNumber.replace(/\D/g, '');

  if (cleanAccount.length < 9 || cleanAccount.length > 18) {
    return { 
      valid: false, 
      error: 'Bank account number must be between 9 and 18 digits' 
    };
  }

  return { valid: true };
};

// IFSC code validation
export const validateIFSC = (ifsc: string): { valid: boolean; error?: string } => {
  if (!ifsc || ifsc.trim() === '') {
    return { valid: false, error: 'IFSC code is required' };
  }

  const ifscRegex = /^[A-Z]{4}0[A-Z0-9]{6}$/;

  if (!ifscRegex.test(ifsc.toUpperCase())) {
    return { 
      valid: false, 
      error: 'Invalid IFSC code format. Format: ABCD0123456' 
    };
  }

  return { valid: true };
};

// Password validation
export const validatePassword = (password: string): { valid: boolean; error?: string; strength?: string } => {
  if (!password || password.trim() === '') {
    return { valid: false, error: 'Password is required' };
  }

  if (password.length < 8) {
    return { 
      valid: false, 
      error: 'Password must be at least 8 characters long' 
    };
  }

  const hasUpperCase = /[A-Z]/.test(password);
  const hasLowerCase = /[a-z]/.test(password);
  const hasNumbers = /\d/.test(password);
  const hasSpecialChar = /[!@#$%^&*(),.?":{}|<>]/.test(password);

  let strength = 0;
  if (hasUpperCase) strength++;
  if (hasLowerCase) strength++;
  if (hasNumbers) strength++;
  if (hasSpecialChar) strength++;
  if (password.length >= 12) strength++;

  if (!hasUpperCase || !hasLowerCase || !hasNumbers || !hasSpecialChar) {
    return { 
      valid: false, 
      error: 'Password must contain uppercase, lowercase, number, and special character',
      strength: strength >= 3 ? 'Medium' : 'Weak'
    };
  }

  return { 
    valid: true, 
    strength: strength >= 4 ? 'Strong' : 'Medium'
  };
};

// Date validation (not in future for DOB)
export const validateDateOfBirth = (date: string): { valid: boolean; error?: string } => {
  if (!date || date.trim() === '') {
    return { valid: false, error: 'Date of birth is required' };
  }

  const dob = new Date(date);
  const today = new Date();
  
  if (isNaN(dob.getTime())) {
    return { valid: false, error: 'Invalid date format' };
  }

  if (dob >= today) {
    return { valid: false, error: 'Date of birth cannot be in the future' };
  }

  // Check minimum age (18 years)
  const age = today.getFullYear() - dob.getFullYear();
  const monthDiff = today.getMonth() - dob.getMonth();
  const actualAge = monthDiff < 0 || (monthDiff === 0 && today.getDate() < dob.getDate()) ? age - 1 : age;

  if (actualAge < 18) {
    return { valid: false, error: 'Must be at least 18 years old' };
  }

  // Check maximum age (100 years)
  if (actualAge > 100) {
    return { valid: false, error: 'Invalid date of birth' };
  }

  return { valid: true };
};

// Name validation
export const validateName = (name: string, fieldName: string = 'Name'): { valid: boolean; error?: string } => {
  if (!name || name.trim() === '') {
    return { valid: false, error: `${fieldName} is required` };
  }

  if (name.trim().length < 2) {
    return { valid: false, error: `${fieldName} must be at least 2 characters` };
  }

  if (name.trim().length > 100) {
    return { valid: false, error: `${fieldName} must not exceed 100 characters` };
  }

  // Only letters, spaces, dots, and hyphens
  const nameRegex = /^[a-zA-Z\s.\-]+$/;
  if (!nameRegex.test(name)) {
    return { valid: false, error: `${fieldName} can only contain letters, spaces, dots, and hyphens` };
  }

  return { valid: true };
};

// URL validation
export const validateURL = (url: string): { valid: boolean; error?: string } => {
  if (!url || url.trim() === '') {
    return { valid: false, error: 'URL is required' };
  }

  try {
    new URL(url);
    return { valid: true };
  } catch {
    return { valid: false, error: 'Invalid URL format' };
  }
};

// File validation
export const validateFile = (
  file: File,
  options: {
    maxSize?: number; // in MB
    allowedTypes?: string[];
  } = {}
): { valid: boolean; error?: string } => {
  const { maxSize = 5, allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'] } = options;

  if (!file) {
    return { valid: false, error: 'No file selected' };
  }

  // Check file size
  const fileSizeMB = file.size / (1024 * 1024);
  if (fileSizeMB > maxSize) {
    return { valid: false, error: `File size must not exceed ${maxSize}MB` };
  }

  // Check file type
  if (!allowedTypes.includes(file.type)) {
    return { valid: false, error: `Invalid file type. Allowed: ${allowedTypes.join(', ')}` };
  }

  return { valid: true };
};

// Generic required field validation
export const validateRequired = (value: any, fieldName: string): { valid: boolean; error?: string } => {
  if (value === null || value === undefined || value === '' || (typeof value === 'string' && value.trim() === '')) {
    return { valid: false, error: `${fieldName} is required` };
  }
  return { valid: true };
};

// Numeric validation
export const validateNumber = (
  value: string | number,
  fieldName: string,
  options: {
    min?: number;
    max?: number;
    integer?: boolean;
  } = {}
): { valid: boolean; error?: string } => {
  const { min, max, integer = false } = options;

  const num = typeof value === 'string' ? parseFloat(value) : value;

  if (isNaN(num)) {
    return { valid: false, error: `${fieldName} must be a valid number` };
  }

  if (integer && !Number.isInteger(num)) {
    return { valid: false, error: `${fieldName} must be a whole number` };
  }

  if (min !== undefined && num < min) {
    return { valid: false, error: `${fieldName} must be at least ${min}` };
  }

  if (max !== undefined && num > max) {
    return { valid: false, error: `${fieldName} must not exceed ${max}` };
  }

  return { valid: true };
};

// Comprehensive form validation
export const validateForm = (
  formData: Record<string, any>,
  rules: Record<string, (value: any) => { valid: boolean; error?: string }>
): { valid: boolean; errors: Record<string, string> } => {
  const errors: Record<string, string> = {};

  Object.keys(rules).forEach(field => {
    const result = rules[field](formData[field]);
    if (!result.valid && result.error) {
      errors[field] = result.error;
    }
  });

  return {
    valid: Object.keys(errors).length === 0,
    errors
  };
};
