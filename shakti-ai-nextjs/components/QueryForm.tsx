"use client";

import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { AlertCircle, CheckCircle2, Send, Info } from 'lucide-react';

interface EscalationRoute {
  department: string;
  cell: string;
}

export default function QueryEscalationForm() {
  const [submitting, setSubmitting] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [routes, setRoutes] = useState<Record<string, EscalationRoute>>({});
  const [selectedCategory, setSelectedCategory] = useState<string>('');

  const [formData, setFormData] = useState({
    employee_name: '',
    employee_id: '',
    email: '',
    phone: '',
    query_type: 'general',
    category: '',
    subject: '',
    description: '',
    priority: 'normal',
  });

  useEffect(() => {
    // Fetch escalation routes
    fetch('http://localhost:8000/api/feedback/routes')
      .then(res => res.json())
      .then(data => {
        if (data.success) {
          setRoutes(data.routes);
        }
      })
      .catch(console.error);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);

    try {
      const response = await fetch('http://localhost:8000/api/queries/submit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (!response.ok) throw new Error(data.detail || 'Submission failed');

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
            <CheckCircle2 className="w-16 h-16 text-green-500 mx-auto" />
            <h3 className="text-2xl font-bold">Query Submitted Successfully!</h3>
            <p className="text-muted-foreground">
              Your query has been routed to the appropriate department and will be addressed soon.
            </p>
            {routes[formData.category] && (
              <div className="text-sm text-blue-600 space-y-1">
                <p><strong>Routed to:</strong> {routes[formData.category].department}</p>
                <p><strong>Cell:</strong> {routes[formData.category].cell}</p>
              </div>
            )}
            <Button onClick={() => window.location.reload()}>Submit Another Query</Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  const currentRoute = routes[formData.category];

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Card>
        <CardHeader>
          <CardTitle className="text-2xl">Query Escalation Form</CardTitle>
          <CardDescription>
            Submit queries regarding transfer, leave, relocation, or other HR matters. 
            Your query will be automatically routed to the appropriate department.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            
            {/* Employee Information */}
            <div className="space-y-4 p-4 border rounded-lg">
              <h3 className="font-semibold text-lg">Your Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="name">Full Name *</Label>
                  <Input
                    id="name"
                    required
                    value={formData.employee_name}
                    onChange={(e) => setFormData({...formData, employee_name: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="emp_id">Employee ID *</Label>
                  <Input
                    id="emp_id"
                    required
                    value={formData.employee_id}
                    onChange={(e) => setFormData({...formData, employee_id: e.target.value})}
                  />
                </div>
                <div>
                  <Label htmlFor="email">Email *</Label>
                  <Input
                    id="email"
                    type="email"
                    required
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

            {/* Query Details */}
            <div className="space-y-4">
              <div>
                <Label htmlFor="category">Issue Category *</Label>
                <Select
                  value={formData.category}
                  onValueChange={(value) => setFormData({...formData, category: value})}
                  required
                >
                  <SelectTrigger id="category">
                    <SelectValue placeholder="Select issue type" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="transfer">Transfer Request</SelectItem>
                    <SelectItem value="leave">Leave / Maternity / CCL</SelectItem>
                    <SelectItem value="relocation">Relocation / Accommodation</SelectItem>
                    <SelectItem value="promotion">Promotion / Career Progression</SelectItem>
                    <SelectItem value="benefits">Benefits / Reimbursements</SelectItem>
                    <SelectItem value="governance">Policy / Governance Query</SelectItem>
                    <SelectItem value="other">Other</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Routing Information */}
              {currentRoute && (
                <div className="flex items-start gap-3 p-4 bg-blue-50 rounded-lg">
                  <Info className="w-5 h-5 text-blue-600 mt-0.5" />
                  <div className="text-sm">
                    <p className="font-medium text-blue-900">This query will be routed to:</p>
                    <p className="text-blue-700"><strong>Department:</strong> {currentRoute.department}</p>
                    <p className="text-blue-700"><strong>Cell:</strong> {currentRoute.cell}</p>
                  </div>
                </div>
              )}

              <div>
                <Label htmlFor="subject">Subject *</Label>
                <Input
                  id="subject"
                  required
                  placeholder="Brief subject line for your query"
                  value={formData.subject}
                  onChange={(e) => setFormData({...formData, subject: e.target.value})}
                />
              </div>

              <div>
                <Label htmlFor="description">Detailed Description *</Label>
                <Textarea
                  id="description"
                  required
                  rows={8}
                  placeholder="Provide detailed information about your query, including relevant dates, reference numbers, and any previous correspondence..."
                  value={formData.description}
                  onChange={(e) => setFormData({...formData, description: e.target.value})}
                />
              </div>

              <div>
                <Label htmlFor="priority">Priority</Label>
                <Select
                  value={formData.priority}
                  onValueChange={(value) => setFormData({...formData, priority: value})}
                >
                  <SelectTrigger id="priority">
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="normal">Normal</SelectItem>
                    <SelectItem value="high">High</SelectItem>
                    <SelectItem value="urgent">Urgent</SelectItem>
                  </SelectContent>
                </Select>
              </div>
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
              className="w-full"
              size="lg"
            >
              {submitting ? (
                <span>Submitting...</span>
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Submit Query
                </>
              )}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
