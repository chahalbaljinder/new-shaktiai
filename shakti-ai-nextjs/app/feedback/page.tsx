"use client";

import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  MessageSquare, 
  AlertTriangle, 
  FileText, 
  HelpCircle,
  ArrowRight,
  Shield,
  Clock,
  CheckCircle,
  ArrowLeft,
  Home
} from 'lucide-react';
import Link from 'next/link';
import FeedbackForm from '@/components/FeedbackForm';
import QueryForm from '@/components/QueryForm';
import ComplaintForm from '@/components/ComplaintForm';

type ViewType = 'menu' | 'feedback' | 'query' | 'complaint';

export default function FeedbackSystemPage() {
  const [currentView, setCurrentView] = useState<ViewType>('menu');

  const renderContent = () => {
    switch (currentView) {
      case 'feedback':
        return <FeedbackForm />;
      case 'query':
        return <QueryForm />;
      case 'complaint':
        return <ComplaintForm />;
      default:
        return <MenuView onSelectView={setCurrentView} />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      <div className="container mx-auto py-8 px-4">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-4 mb-4">
            <Link href="/">
              <Button 
                variant="outline" 
                size="sm"
                className="gap-2"
              >
                <Home className="w-4 h-4" />
                Back to Dashboard
              </Button>
            </Link>
            {currentView !== 'menu' && (
              <Button 
                variant="outline"
                size="sm"
                onClick={() => setCurrentView('menu')}
                className="gap-2"
              >
                <ArrowLeft className="w-4 h-4" />
                Back to Menu
              </Button>
            )}
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Feedback, Queries & Complaints
          </h1>
          <p className="text-lg text-gray-600">
            Your voice matters. We're here to listen and support you.
          </p>
        </div>

        {/* Content */}
        {renderContent()}
      </div>
    </div>
  );
}

function MenuView({ onSelectView }: { onSelectView: (view: ViewType) => void }) {
  return (
    <div className="max-w-6xl mx-auto">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Annual Feedback */}
        <Card className="hover:shadow-lg transition-shadow cursor-pointer border-t-4 border-t-blue-500">
          <CardHeader>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-3 bg-blue-100 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
              <CardTitle className="text-xl">Annual Feedback</CardTitle>
            </div>
            <CardDescription>
              Share your thoughts on workplace environment, leadership, and culture
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2 text-gray-600">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span>Anonymous or identified submission</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span>Structured feedback sections</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span>Confidential aggregation</span>
              </div>
            </div>
            <Button 
              onClick={() => onSelectView('feedback')}
              className="w-full"
            >
              Fill Feedback Form <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </CardContent>
        </Card>

        {/* Query Escalation */}
        <Card className="hover:shadow-lg transition-shadow cursor-pointer border-t-4 border-t-green-500">
          <CardHeader>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-3 bg-green-100 rounded-lg">
                <HelpCircle className="w-6 h-6 text-green-600" />
              </div>
              <CardTitle className="text-xl">Query Escalation</CardTitle>
            </div>
            <CardDescription>
              Get help with transfer, leave, benefits, and policy questions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2 text-gray-600">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span>Auto-routed to correct department</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <CheckCircle className="w-4 h-4 text-green-600" />
                <span>Status tracking available</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <Clock className="w-4 h-4 text-gray-500" />
                <span>Response within 15-30 days</span>
              </div>
            </div>
            <Button 
              onClick={() => onSelectView('query')}
              className="w-full bg-green-600 hover:bg-green-700"
            >
              Submit Query <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </CardContent>
        </Card>

        {/* Complaints & Grievances */}
        <Card className="hover:shadow-lg transition-shadow cursor-pointer border-t-4 border-t-red-500">
          <CardHeader>
            <div className="flex items-center gap-3 mb-2">
              <div className="p-3 bg-red-100 rounded-lg">
                <AlertTriangle className="w-6 h-6 text-red-600" />
              </div>
              <CardTitle className="text-xl">Complaints & Grievances</CardTitle>
            </div>
            <CardDescription>
              Report harassment, discrimination, or serious workplace issues
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-2 text-gray-600">
                <Shield className="w-4 h-4 text-red-600" />
                <span>Strict confidentiality maintained</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <Shield className="w-4 h-4 text-red-600" />
                <span>ICC notification for harassment</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <Shield className="w-4 h-4 text-red-600" />
                <span>Anonymous submission option</span>
              </div>
            </div>
            <Button 
              onClick={() => onSelectView('complaint')}
              className="w-full bg-red-600 hover:bg-red-700"
            >
              File Complaint <ArrowRight className="w-4 h-4 ml-2" />
            </Button>
          </CardContent>
        </Card>
      </div>

      {/* Info Section */}
      <Card className="mt-8 bg-blue-50 border-blue-200">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-blue-600" />
            How It Works
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-semibold text-blue-900 mb-2">📋 Annual Feedback</h4>
              <p className="text-sm text-gray-700">
                Collected annually to understand employee sentiment and improve workplace policies. 
                Results are aggregated and used for organizational development.
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-green-900 mb-2">🎯 Query Escalation</h4>
              <p className="text-sm text-gray-700">
                Automatically routes your query to: <br/>
                • Local HR (transfer, leave, relocation) <br/>
                • Women Welfare Cell (support issues) <br/>
                • Benefits Cell (reimbursements)
              </p>
            </div>
            <div>
              <h4 className="font-semibold text-red-900 mb-2">⚖️ Complaints</h4>
              <p className="text-sm text-gray-700">
                For serious issues: <br/>
                • Harassment → ICC immediately notified <br/>
                • Discrimination → Women Welfare Cell <br/>
                • Unresolved → RTI/Legal forums available
              </p>
            </div>
          </div>
          <div className="pt-4 border-t border-blue-300">
            <p className="text-sm text-gray-700">
              <strong>Confidentiality Guarantee:</strong> All submissions are handled with strict confidentiality. 
              Your personal data is protected per organizational policy and relevant data protection laws.
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
