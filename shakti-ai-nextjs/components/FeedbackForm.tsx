"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Switch } from '@/components/ui/switch';
import { AlertCircle, CheckCircle2, Send } from 'lucide-react';

interface FeedbackSection {
  rating?: number;
  comments?: string;
}

interface FeedbackData {
  employee_name?: string;
  employee_id?: string;
  designation?: string;
  lab_center?: string;
  email?: string;
  years_of_service?: number;
  is_anonymous: boolean;
  work_environment: FeedbackSection;
  leadership_management: FeedbackSection;
  inclusion_culture: FeedbackSection;
  workload_balance: FeedbackSection;
  career_development: FeedbackSection;
  safety_conduct: FeedbackSection;
  additional_comments: string;
}

export default function FeedbackForm() {
  const [isAnonymous, setIsAnonymous] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const [formData, setFormData] = useState<FeedbackData>({
    employee_name: '',
    employee_id: '',
    designation: '',
    lab_center: '',
    email: '',
    years_of_service: undefined,
    is_anonymous: false,
    work_environment: {},
    leadership_management: {},
    inclusion_culture: {},
    workload_balance: {},
    career_development: {},
    safety_conduct: {},
    additional_comments: '',
  });

  const sections = [
    { key: 'work_environment', title: 'Work Environment', 
      questions: [
        'Rate overall lab/workplace environment',
        'Are facilities adequate for your research needs?',
        'Describe any infrastructure bottlenecks'
      ]
    },
    { key: 'leadership_management', title: 'Leadership & Management',
      questions: [
        'Quality of communication from supervisors',
        'Fairness and transparency in decision making',
        'Support for career progression and learning'
      ]
    },
    { key: 'inclusion_culture', title: 'Inclusion & Culture',
      questions: [
        'Respectful treatment irrespective of gender',
        'Presence/absence of bias in meetings or assignments',
        'Suggestions to improve inclusion and psychological safety'
      ]
    },
    { key: 'workload_balance', title: 'Workload & Balance',
      questions: [
        'Is workload distribution reasonable?',
        'Challenges balancing professional and family responsibilities',
        'Any schedule/shift related constraints impacting well-being'
      ]
    },
    { key: 'career_development', title: 'Career & Development',
      questions: [
        'Access to mentorship and guidance',
        'Opportunities for training, conferences, publications',
        'Barriers encountered in promotion/advancement pathways'
      ]
    },
    { key: 'safety_conduct', title: 'Safety & Conduct',
      questions: [
        'Any safety concerns (labs, late hours, travel)',
        'Comfort reporting harassment or misconduct incidents',
        'Recommendations for improving safety protocols'
      ]
    },
  ];

  const handleSectionUpdate = (sectionKey: string, field: 'rating' | 'comments', value: any) => {
    setFormData(prev => {
      const sectionData = prev[sectionKey as keyof Omit<FeedbackData, 'is_anonymous' | 'additional_comments'>];
      return {
        ...prev,
        [sectionKey]: {
          ...(typeof sectionData === 'object' && sectionData !== null ? sectionData : {}),
          [field]: value
        }
      };
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const payload = {
        ...formData,
        is_anonymous: isAnonymous,
        employee_name: isAnonymous ? undefined : formData.employee_name,
        employee_id: isAnonymous ? undefined : formData.employee_id,
      };

      const response = await fetch('http://localhost:8000/api/feedback/annual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.detail || 'Submission failed');

      setSubmitted(true);
      setTimeout(() => {
        window.location.reload();
      }, 3000);

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
            <CheckCircle2 className="w-16 h-16 text-green-500 mx-auto" />
            <h3 className="text-2xl font-bold">Feedback Submitted Successfully!</h3>
            <p className="text-muted-foreground">
              Thank you for your valuable feedback. Your responses help us improve our workplace.
            </p>
            {isAnonymous && (
              <p className="text-sm text-blue-600">
                Your submission was anonymous as requested.
              </p>
            )}
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <div className="max-w-4xl mx-auto p-6 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Annual Employee Feedback Form</CardTitle>
          <CardDescription>
            Your feedback helps us create a better workplace. All responses are confidential and aggregated for analysis.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Anonymous Toggle */}
            <div className="flex items-center justify-between p-4 bg-blue-50 rounded-lg">
              <div className="space-y-1">
                <Label htmlFor="anonymous" className="text-base font-medium">Submit Anonymously</Label>
                <p className="text-sm text-muted-foreground">
                  Your identity will not be recorded with your responses
                </p>
              </div>
              <Switch
                id="anonymous"
                checked={isAnonymous}
                onCheckedChange={setIsAnonymous}
              />
            </div>

            {/* Identity Section (if not anonymous) */}
            {!isAnonymous && (
              <div className="space-y-4 p-4 border rounded-lg">
                <h3 className="font-semibold text-lg">Employee Information</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="name">Full Name *</Label>
                    <Input
                      id="name"
                      required={!isAnonymous}
                      value={formData.employee_name}
                      onChange={(e) => setFormData({...formData, employee_name: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="emp_id">Employee ID *</Label>
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
                    <Label htmlFor="lab">Lab / Center</Label>
                    <Input
                      id="lab"
                      value={formData.lab_center}
                      onChange={(e) => setFormData({...formData, lab_center: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      value={formData.email}
                      onChange={(e) => setFormData({...formData, email: e.target.value})}
                    />
                  </div>
                  <div>
                    <Label htmlFor="years">Years of Service</Label>
                    <Input
                      id="years"
                      type="number"
                      value={formData.years_of_service || ''}
                      onChange={(e) => setFormData({...formData, years_of_service: parseInt(e.target.value) || undefined})}
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Feedback Sections */}
            {sections.map((section) => (
              <Card key={section.key} className="border-l-4 border-l-blue-500">
                <CardHeader>
                  <CardTitle className="text-lg">{section.title}</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div>
                    <Label>Overall Rating (1-5)</Label>
                    <div className="flex gap-2 mt-2">
                      {[1, 2, 3, 4, 5].map((rating) => (
                        <button
                          key={rating}
                          type="button"
                          onClick={() => handleSectionUpdate(section.key, 'rating', rating)}
                          className={`w-10 h-10 rounded-full border-2 transition-colors ${
                            (formData[section.key as keyof Omit<FeedbackData, 'is_anonymous' | 'additional_comments'>] as FeedbackSection)?.rating === rating
                              ? 'bg-blue-600 text-white border-blue-600'
                              : 'border-gray-300 hover:border-blue-400'
                          }`}
                        >
                          {rating}
                        </button>
                      ))}
                    </div>
                  </div>
                  <div>
                    <Label>Comments / Feedback</Label>
                    <Textarea
                      rows={4}
                      placeholder={`Feedback on: ${section.questions.join('; ')}`}
                      value={(formData[section.key as keyof Omit<FeedbackData, 'is_anonymous' | 'additional_comments'>] as FeedbackSection)?.comments || ''}
                      onChange={(e) => handleSectionUpdate(section.key, 'comments', e.target.value)}
                      className="mt-2"
                    />
                  </div>
                </CardContent>
              </Card>
            ))}

            {/* Additional Comments */}
            <div>
              <Label>Additional Comments / Suggestions</Label>
              <Textarea
                rows={6}
                placeholder="Any additional feedback, suggestions, or concerns you'd like to share..."
                value={formData.additional_comments}
                onChange={(e) => setFormData({...formData, additional_comments: e.target.value})}
                className="mt-2"
              />
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
              disabled={submitting}
              className="w-full"
              size="lg"
            >
              {submitting ? (
                <span>Submitting...</span>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Submit Feedback
                </>
              )}
            </Button>

            <p className="text-xs text-center text-muted-foreground">
              Confidentiality Note: Aggregated insights may be shared; individual identifiable responses handled per policy.
            </p>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
