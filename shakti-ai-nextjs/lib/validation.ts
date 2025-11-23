// Comprehensive validation utilities

export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

// Email validation
export const validateEmail = (email: string): ValidationResult => {
  if (!email || email.trim() === '') {
    return { isValid: false, error: 'Email is required' };
  }
  
  const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailRegex.test(email)) {
    return { isValid: false, error: 'Please enter a valid email address (e.g., user@example.com)' };
  }
  
  // Check for common mistakes
  if (email.includes('..') || email.startsWith('.') || email.endsWith('.')) {
    return { isValid: false, error: 'Email cannot contain consecutive dots or start/end with a dot' };
  }
  
  return { isValid: true };
};

// Phone number validation (Indian format)
export const validatePhone = (phone: string): ValidationResult => {
  if (!phone || phone.trim() === '') {
    return { isValid: false, error: 'Phone number is required' };
  }
  
  // Remove spaces, hyphens, parentheses
  const cleanPhone = phone.replace(/[\s\-\(\)\+]/g, '');
  
  // Check if it's all digits
  if (!/^\d+$/.test(cleanPhone)) {
    return { isValid: false, error: 'Phone number must contain only digits' };
  }
  
  // Indian phone numbers (with or without country code)
  if (cleanPhone.length === 10) {
    // Standard 10-digit Indian number
    if (!/^[6-9]\d{9}$/.test(cleanPhone)) {
      return { isValid: false, error: 'Please enter a valid 10-digit phone number starting with 6-9' };
    }
  } else if (cleanPhone.length === 12 && cleanPhone.startsWith('91')) {
    // With +91 country code
    const numberPart = cleanPhone.slice(2);
    if (!/^[6-9]\d{9}$/.test(numberPart)) {
      return { isValid: false, error: 'Please enter a valid Indian phone number' };
    }
  } else {
    return { isValid: false, error: 'Phone number must be 10 digits (or 12 with +91)' };
  }
  
  return { isValid: true };
};

// Name validation
export const validateName = (name: string, fieldName: string = 'Name'): ValidationResult => {
  if (!name || name.trim() === '') {
    return { isValid: false, error: `${fieldName} is required` };
  }
  
  if (name.trim().length < 2) {
    return { isValid: false, error: `${fieldName} must be at least 2 characters long` };
  }
  
  if (name.trim().length > 100) {
    return { isValid: false, error: `${fieldName} must be less than 100 characters` };
  }
  
  // Allow letters, spaces, hyphens, apostrophes (for names like O'Brien, Mary-Jane)
  if (!/^[a-zA-Z\s\-'\.]+$/.test(name)) {
    return { isValid: false, error: `${fieldName} can only contain letters, spaces, hyphens, and apostrophes` };
  }
  
  return { isValid: true };
};

// Password validation
export const validatePassword = (password: string): ValidationResult => {
  if (!password || password.trim() === '') {
    return { isValid: false, error: 'Password is required' };
  }
  
  if (password.length < 8) {
    return { isValid: false, error: 'Password must be at least 8 characters long' };
  }
  
  if (password.length > 50) {
    return { isValid: false, error: 'Password must be less than 50 characters' };
  }
  
  // Check for at least one uppercase letter
  if (!/[A-Z]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one uppercase letter' };
  }
  
  // Check for at least one lowercase letter
  if (!/[a-z]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one lowercase letter' };
  }
  
  // Check for at least one digit
  if (!/\d/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one number' };
  }
  
  // Check for at least one special character
  if (!/[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password)) {
    return { isValid: false, error: 'Password must contain at least one special character (!@#$%^&* etc.)' };
  }
  
  return { isValid: true };
};

// Confirm password validation
export const validateConfirmPassword = (password: string, confirmPassword: string): ValidationResult => {
  if (!confirmPassword || confirmPassword.trim() === '') {
    return { isValid: false, error: 'Please confirm your password' };
  }
  
  if (password !== confirmPassword) {
    return { isValid: false, error: 'Passwords do not match' };
  }
  
  return { isValid: true };
};

// PAN number validation (Indian)
export const validatePAN = (pan: string): ValidationResult => {
  if (!pan || pan.trim() === '') {
    return { isValid: false, error: 'PAN number is required' };
  }
  
  const panRegex = /^[A-Z]{5}[0-9]{4}[A-Z]{1}$/;
  if (!panRegex.test(pan.toUpperCase())) {
    return { isValid: false, error: 'Please enter a valid PAN number (e.g., ABCDE1234F)' };
  }
  
  return { isValid: true };
};

// Aadhaar number validation (Indian)
export const validateAadhaar = (aadhaar: string): ValidationResult => {
  if (!aadhaar || aadhaar.trim() === '') {
    return { isValid: false, error: 'Aadhaar number is required' };
  }
  
  const cleanAadhaar = aadhaar.replace(/[\s\-]/g, '');
  
  if (!/^\d{12}$/.test(cleanAadhaar)) {
    return { isValid: false, error: 'Aadhaar must be a 12-digit number' };
  }
  
  // Verhoeff algorithm validation for Aadhaar
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
  const reversedAadhaar = cleanAadhaar.split('').reverse().join('');
  
  for (let i = 0; i < reversedAadhaar.length; i++) {
    c = d[c][p[(i % 8)][parseInt(reversedAadhaar[i])]];
  }
  
  if (c !== 0) {
    return { isValid: false, error: 'Invalid Aadhaar number (checksum failed)' };
  }
  
  return { isValid: true };
};

// Bank account number validation
export const validateBankAccount = (accountNumber: string): ValidationResult => {
  if (!accountNumber || accountNumber.trim() === '') {
    return { isValid: false, error: 'Bank account number is required' };
  }
  
  const cleanAccount = accountNumber.replace(/[\s\-]/g, '');
  
  if (!/^\d+$/.test(cleanAccount)) {
    return { isValid: false, error: 'Account number must contain only digits' };
  }
  
  if (cleanAccount.length < 9 || cleanAccount.length > 18) {
    return { isValid: false, error: 'Account number must be between 9 and 18 digits' };
  }
  
  return { isValid: true };
};

// IFSC code validation
export const validateIFSC = (ifsc: string): ValidationResult => {
  if (!ifsc || ifsc.trim() === '') {
    return { isValid: false, error: 'IFSC code is required' };
  }
  
  const ifscRegex = /^[A-Z]{4}0[A-Z0-9]{6}$/;
  if (!ifscRegex.test(ifsc.toUpperCase())) {
    return { isValid: false, error: 'Please enter a valid IFSC code (e.g., SBIN0001234)' };
  }
  
  return { isValid: true };
};

// Pincode validation (Indian)
export const validatePincode = (pincode: string): ValidationResult => {
  if (!pincode || pincode.trim() === '') {
    return { isValid: false, error: 'Pincode is required' };
  }
  
  if (!/^\d{6}$/.test(pincode)) {
    return { isValid: false, error: 'Pincode must be a 6-digit number' };
  }
  
  return { isValid: true };
};

// Date validation (DOB, joining date, etc.)
export const validateDate = (date: string, fieldName: string = 'Date', options?: {
  minAge?: number;
  maxAge?: number;
  futureAllowed?: boolean;
}): ValidationResult => {
  if (!date || date.trim() === '') {
    return { isValid: false, error: `${fieldName} is required` };
  }
  
  const dateObj = new Date(date);
  if (isNaN(dateObj.getTime())) {
    return { isValid: false, error: `Please enter a valid ${fieldName.toLowerCase()}` };
  }
  
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  
  // Check if future date is allowed
  if (!options?.futureAllowed && dateObj > today) {
    return { isValid: false, error: `${fieldName} cannot be in the future` };
  }
  
  // Check age constraints (for DOB)
  if (options?.minAge || options?.maxAge) {
    const age = Math.floor((today.getTime() - dateObj.getTime()) / (365.25 * 24 * 60 * 60 * 1000));
    
    if (options.minAge && age < options.minAge) {
      return { isValid: false, error: `Age must be at least ${options.minAge} years` };
    }
    
    if (options.maxAge && age > options.maxAge) {
      return { isValid: false, error: `Age must be less than ${options.maxAge} years` };
    }
  }
  
  return { isValid: true };
};

// Required field validation
export const validateRequired = (value: any, fieldName: string): ValidationResult => {
  if (value === null || value === undefined || (typeof value === 'string' && value.trim() === '')) {
    return { isValid: false, error: `${fieldName} is required` };
  }
  
  return { isValid: true };
};

// Number validation
export const validateNumber = (value: string, fieldName: string, options?: {
  min?: number;
  max?: number;
  decimals?: boolean;
}): ValidationResult => {
  if (!value || value.trim() === '') {
    return { isValid: false, error: `${fieldName} is required` };
  }
  
  const numberRegex = options?.decimals ? /^-?\d+(\.\d+)?$/ : /^-?\d+$/;
  if (!numberRegex.test(value)) {
    return { isValid: false, error: `${fieldName} must be a valid number` };
  }
  
  const numValue = parseFloat(value);
  
  if (options?.min !== undefined && numValue < options.min) {
    return { isValid: false, error: `${fieldName} must be at least ${options.min}` };
  }
  
  if (options?.max !== undefined && numValue > options.max) {
    return { isValid: false, error: `${fieldName} must be less than or equal to ${options.max}` };
  }
  
  return { isValid: true };
};

// URL validation
export const validateURL = (url: string): ValidationResult => {
  if (!url || url.trim() === '') {
    return { isValid: false, error: 'URL is required' };
  }
  
  try {
    new URL(url);
    return { isValid: true };
  } catch (e) {
    return { isValid: false, error: 'Please enter a valid URL (e.g., https://example.com)' };
  }
};

// Validate multiple fields at once
export const validateFields = (validations: { field: string; validator: () => ValidationResult }[]): {
  isValid: boolean;
  errors: { [key: string]: string };
} => {
  const errors: { [key: string]: string } = {};
  let isValid = true;
  
  for (const { field, validator } of validations) {
    const result = validator();
    if (!result.isValid) {
      errors[field] = result.error || 'Invalid value';
      isValid = false;
    }
  }
  
  return { isValid, errors };
};

// Format phone number for display
export const formatPhoneNumber = (phone: string): string => {
  const cleanPhone = phone.replace(/[\s\-\(\)\+]/g, '');
  
  if (cleanPhone.length === 10) {
    return `+91-${cleanPhone.slice(0, 5)}-${cleanPhone.slice(5)}`;
  } else if (cleanPhone.length === 12 && cleanPhone.startsWith('91')) {
    const numberPart = cleanPhone.slice(2);
    return `+91-${numberPart.slice(0, 5)}-${numberPart.slice(5)}`;
  }
  
  return phone;
};

// Format Aadhaar for display
export const formatAadhaar = (aadhaar: string): string => {
  const cleanAadhaar = aadhaar.replace(/[\s\-]/g, '');
  if (cleanAadhaar.length === 12) {
    return `${cleanAadhaar.slice(0, 4)}-${cleanAadhaar.slice(4, 8)}-${cleanAadhaar.slice(8)}`;
  }
  return aadhaar;
};

// Sanitize input (prevent XSS)
export const sanitizeInput = (input: string): string => {
  return input
    .replace(/[<>]/g, '') // Remove < and >
    .replace(/javascript:/gi, '') // Remove javascript: protocol
    .replace(/on\w+=/gi, '') // Remove inline event handlers
    .trim();
};
