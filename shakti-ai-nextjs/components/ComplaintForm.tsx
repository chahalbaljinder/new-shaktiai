"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { AlertCircle, CheckCircle2, Send, Shield, AlertTriangle } from 'lucide-react';

export default function ComplaintForm() {
  const [isAnonymous, setIsAnonymous] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [complaintNumber, setComplaintNumber] = useState('');
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState({
    is_anonymous: false,
    complainant_name: '',
    employee_id: '',
    designation: '',
    email: '',
    phone: '',
    complaint_type: 'grievance',
    category: '',
    incident_date: '',
    incident_location: '',
    incident_time: '',
    persons_involved: '',
    witness_names: '',
    detailed_description: '',
    previous_attempts: '',
    desired_outcome: '',
    urgency: 'normal',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const payload = {
        ...formData,
        is_anonymous: isAnonymous,
      };

      const response = await fetch('http://localhost:8000/api/complaints/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.detail || 'Submission failed');

      setComplaintNumber(data.complaint_number);
      setSubmitted(true);

    } catch (err: any) {
      setError(err.message);
    } finally {
      setSubmitting(false);
    }
  };

  if (submitted) {
    return (
      <Card className="max-w-2xl mx-auto mt-8">
        <CardContent className="pt-6">
          <div className="text-center space-y-4">
            <Shield className="w-16 h-16 text-green-500 mx-auto" />
            <h3 className="text-2xl font-bold">Complaint Received</h3>
            <div className="p-4 bg-green-50 rounded-lg">
              <p className="text-sm font-medium text-green-900">Complaint Number:</p>
              <p className="text-2xl font-bold text-green-700">{complaintNumber}</p>
            </div>
            <p className="text-muted-foreground">
              Your complaint has been registered and will be investigated according to policy.
              {formData.category === 'harassment' && ' The Internal Complaints Committee (ICC) has been notified.'}
            </p>
            {isAnonymous && (
              <p className="text-sm text-blue-600">
                ✓ Your complaint was submitted anonymously
              </p>
            )}
            <div className="text-sm text-left space-y-2 p-4 bg-blue-50 rounded-lg">
              <p className="font-medium">Next Steps:</p>
              <ul className="list-disc list-inside space-y-1">
                <li>Acknowledgment within 3-7 days</li>
                <li>Case officer assignment within 15 days</li>
                <li>Preliminary inquiry within 30 days</li>
                <li>Save your complaint number for tracking</li>
              </ul>
            </div>
            <Button onClick={() => window.location.href = '/'}>Return to Home</Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Card className="border-l-4 border-l-red-500">
        <CardHeader>
          <div className="flex items-center gap-2">
            <AlertTriangle className="w-6 h-6 text-red-600" />
            <CardTitle className="text-2xl">Complaint & Grievance Form</CardTitle>
          </div>
          <CardDescription>
            This form is for reporting serious workplace issues including harassment, discrimination, 
            and policy violations. All complaints are handled with utmost confidentiality.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Anonymous Toggle */}
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg border-2 border-blue-200">
              <div className="space-y-1">
                <Label htmlFor="anonymous" className="text-base font-medium flex items-center gap-2">
                  <Shield className="w-5 h-5 text-blue-600" />
                  Submit Anonymously
                </Label>
                <p className="text-sm text-muted-foreground">
                  Your identity will be protected. Only case officers will have access.
                </p>
              </div>
              <Switch
                id="anonymous"
                checked={isAnonymous}
                onCheckedChange={setIsAnonymous}
              />
            </div>

            {/* Complainant Information (if not anonymous) */}
            {!isAnonymous && (
              <div className="space-y-4 p-4 border rounded-lg">
                <h3 className="font-semibold text-lg">Your Information</h3>
                <p className="text-sm text-muted-foreground">
                  This information will be kept confidential and used only for case management.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="name">Full Name {!isAnonymous && '*'}</Label>
                    <Input
                      id="name"
                      required={!isAnonymous}
                      value={formData.complainant_name}
                      onChange={(e) => setFormData({...formData, complainant_name: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="emp_id">Employee ID {!isAnonymous && '*'}</Label>
                    <Input
                      id="emp_id"
                      required={!isAnonymous}
                      value={formData.employee_id}
                      onChange={(e) => setFormData({...formData, employee_id: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="designation">Designation</Label>
                    <Input
                      id="designation"
                      value={formData.designation}
                      onChange={(e) => setFormData({...formData, designation: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="email">Email {!isAnonymous && '*'}</Label>
                    <Input
                      id="email"
                      type="email"
                      required={!isAnonymous}
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="phone">Phone</Label>
                    <Input
                      id="phone"
                      type="tel"
                      value={formData.phone}
                      onChange={(e) => setFormData({...formData, phone: e.target.value})}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Complaint Category */}
            <div className="space-y-4">
              <div>
                <Label htmlFor="category">Complaint Category *</Label>
                <Select
                  value={formData.category}
                  onValueChange={(value) => setFormData({...formData, category: value})}
                  required
                >
                  <SelectTrigger id="category">
                    <SelectValue placeholder="Select complaint type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="harassment">Harassment (POSH Act)</SelectItem>
                    <SelectItem value="discrimination">Gender Discrimination</SelectItem>
                    <SelectItem value="promotion">Promotion Delay / Unfair Treatment</SelectItem>
                    <SelectItem value="transfer">Transfer Issue / Harassment</SelectItem>
                    <SelectItem value="safety">Safety Concerns</SelectItem>
                    <SelectItem value="other">Other Grievance</SelectItem>
                  </SelectContent>
                </Select>
                {formData.category === 'harassment' && (
                  <p className="text-sm text-red-600 mt-2 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4" />
                    This will be immediately escalated to the Internal Complaints Committee (ICC)
                  </p>
                )}
              </div>

              {/* Incident Details */}
              <div className="p-4 bg-gray-50 rounded-lg space-y-4">
                <h3 className="font-semibold">Incident Details</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div>
                    <Label htmlFor="date">Date of Incident</Label>
                    <Input
                      id="date"
                      type="date"
                      value={formData.incident_date}
                      onChange={(e) => setFormData({...formData, incident_date: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="time">Approximate Time</Label>
                    <Input
                      id="time"
                      placeholder="e.g., 2:30 PM"
                      value={formData.incident_time}
                      onChange={(e) => setFormData({...formData, incident_time: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="location">Location</Label>
                    <Input
                      id="location"
                      placeholder="e.g., Lab Wing B"
                      value={formData.incident_location}
                      onChange={(e) => setFormData({...formData, incident_location: e.target.value})}
                    />
                  </div>
                </div>
                <div>
                  <Label htmlFor="persons">Persons Involved</Label>
                  <Input
                    id="persons"
                    placeholder="Names/designations of persons involved (if known)"
                    value={formData.persons_involved}
                    onChange={(e) => setFormData({...formData, persons_involved: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="witnesses">Witness Names (if any)</Label>
                  <Input
                    id="witnesses"
                    placeholder="Names of witnesses present"
                    value={formData.witness_names}
                    onChange={(e) => setFormData({...formData, witness_names: e.target.value})}
                  />
                </div>
              </div>

              {/* Detailed Description */}
              <div>
                <Label htmlFor="description">Detailed Description *</Label>
                <Textarea
                  id="description"
                  required
                  rows={10}
                  placeholder="Provide a detailed, factual account of the incident(s). Include specific dates, times, locations, and what was said or done. Be as specific as possible."
                  value={formData.detailed_description}
                  onChange={(e) => setFormData({...formData, detailed_description: e.target.value})}
                />
              </div>

              <div>
                <Label htmlFor="previous">Previous Attempts to Resolve</Label>
                <Textarea
                  id="previous"
                  rows={4}
                  placeholder="Have you tried to address this issue before? If yes, describe what steps you took and the outcome."
                  value={formData.previous_attempts}
                  onChange={(e) => setFormData({...formData, previous_attempts: e.target.value})}
                />
              </div>

              <div>
                <Label htmlFor="outcome">Desired Outcome / Resolution Requested</Label>
                <Textarea
                  id="outcome"
                  rows={4}
                  placeholder="What resolution or action are you seeking? (e.g., investigation, policy change, disciplinary action)"
                  value={formData.desired_outcome}
                  onChange={(e) => setFormData({...formData, desired_outcome: e.target.value})}
                />
              </div>

              <div>
                <Label htmlFor="urgency">Urgency Level</Label>
                <Select
                  value={formData.urgency}
                  onValueChange={(value) => setFormData({...formData, urgency: value})}
                >
                  <SelectTrigger id="urgency">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="normal">Normal</SelectItem>
                    <SelectItem value="high">High (ongoing issue)</SelectItem>
                    <SelectItem value="urgent">Urgent (immediate safety concern)</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Confidentiality Notice */}
            <div className="p-4 bg-yellow-50 border-l-4 border-yellow-500">
              <p className="text-sm font-medium text-yellow-900">⚠️ Confidentiality & Legal Notice</p>
              <ul className="text-sm text-yellow-800 mt-2 space-y-1 list-disc list-inside">
                <li>All complaints are treated with strict confidentiality</li>
                <li>False/malicious complaints may result in disciplinary action</li>
                <li>You have the right to external legal recourse if internal resolution fails</li>
                <li>Retaliation against complainants is strictly prohibited</li>
              </ul>
            </div>

            {/* Error Display */}
            {error && (
              <div className="flex items-center gap-2 p-4 bg-red-50 text-red-700 rounded-lg">
                <AlertCircle className="w-5 h-5" />
                <span>{error}</span>
              </div>
            )}

            {/* Submit Button */}
            <Button
              type="submit"
              disabled={submitting || !formData.category}
              className="w-full bg-red-600 hover:bg-red-700"
              size="lg"
            >
              {submitting ? (
                <span>Submitting Securely...</span>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Submit Complaint
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
