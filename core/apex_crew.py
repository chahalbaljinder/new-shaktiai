"""
APEX AI Crew - Agentic RAG System for Policy Queries
Specialized agents: Athena (Legal/Policy), Asha (Wellness), Scribe (Documentation)
"""

import os
import sys
from typing import List, Dict, Optional
from pathlib import Path

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from core.llm import get_llm

# Try to import knowledge base components
try:
    from knowledge_base.retriever import KnowledgeRetriever
    KB_AVAILABLE = True
    print("✅ Knowledge base retriever available")
except ImportError as e:
    KB_AVAILABLE = False
    print(f"⚠️ Knowledge base not available: {e}")
except Exception as e:
    KB_AVAILABLE = False
    print(f"⚠️ Knowledge base error: {e}")


class Apex:
    """APEX implementation with specialized agents and knowledge base support."""
    
    def __init__(self):
        """Initialize APEX with agents and knowledge base."""
        print("🚀 Initializing APEX system...")
        
        try:
            self.llm = get_llm()
            print("✅ LLM initialized")
        except Exception as e:
            print(f"❌ LLM initialization failed: {e}")
            raise
        
        # Agent definitions
        self.agent_info = {
            "athena": {
                "name": "Athena",
                "role": "Legal & Policy Expert",
                "expertise": "DRDO policies, POSH Act, legal rights, and government regulations",
                "specialties": ["POSH Act", "maternity leave", "transfer policies", "CCL", "legal rights", "government regulations"]
            },
            "asha": {
                "name": "Asha",
                "role": "Wellness & Support Counselor",
                "expertise": "mental wellness, work-life balance, and stress management",
                "specialties": ["mental wellness", "stress management", "work-life balance", "burnout", "career counseling"]
            },
            "scribe": {
                "name": "Scribe",
                "role": "Documentation Specialist",
                "expertise": "application preparation, form filling, and official correspondence",
                "specialties": ["application writing", "official letters", "documentation", "form filling", "correspondence"]
            }
        }
        
        # Initialize knowledge base retriever
        self.retriever = None
        if KB_AVAILABLE:
            try:
                self.retriever = KnowledgeRetriever()
                print("✅ APEX Knowledge base loaded successfully")
            except Exception as e:
                print(f"⚠️ Could not load knowledge base: {e}")
                self.retriever = None
        else:
            print("ℹ️ APEX running without knowledge base (RAG disabled)")
        
        print("✅ APEX initialization complete")
    
    def get_relevant_knowledge(self, agent_type: str, query: str) -> tuple[str, List[Dict]]:
        """
        Retrieve relevant knowledge from the agent's knowledge base.
        
        Args:
            agent_type: Type of agent (athena, asha, scribe)
            query: User query
            
        Returns:
            Tuple of (context_string, detailed_source_citations)
        """
        if not self.retriever:
            return "", []
        
        try:
            # Retrieve relevant chunks
            chunks = self.retriever.retrieve_for_agent(agent_type, query, top_k=3)
            
            if not chunks:
                return "", []
            
            # Format context
            context = self.retriever.format_context(chunks)
            
            # Extract source information
            sources = []
            for chunk in chunks:
                sources.append({
                    'document': chunk.get('document', 'Unknown'),
                    'page_reference': chunk.get('page_reference', 'Unknown'),
                    'similarity': chunk.get('similarity', 0),
                    'text': chunk.get('text', '')[:200]  # First 200 chars for preview
                })
            
            return context, sources
            
        except Exception as e:
            print(f"Error retrieving knowledge: {e}")
            return "", []
    
    def get_agent_response(self, agent_type: str, query: str, context: str = None) -> Dict:
        """Get a response from a specific agent with knowledge base integration."""
        agent_info = self.agent_info[agent_type]
        
        # Get relevant knowledge from knowledge base
        knowledge_context, sources = self.get_relevant_knowledge(agent_type, query)
        
        # Build prompt
        prompt = f"""
You are {agent_info['name']}, a {agent_info['role']} specializing in {agent_info['expertise']}.
Your mission is to help DRDO employees and women scientists with accurate, trustworthy, and professional information.

A user has asked:
"{query}"

Your response guidelines:
1️⃣ Be professional yet empathetic - use clear language and a supportive tone.
2️⃣ Provide specific, actionable information based on official policies and guidelines.
3️⃣ When using information from the knowledge base, integrate it naturally - don't just copy-paste.
4️⃣ If providing legal or policy information, cite the relevant acts, rules, or guidelines.
5️⃣ End with a helpful sign-off, reminding them they can ask for clarification.

"""
        
        if knowledge_context:
            prompt += f"""
Below is relevant information from your knowledge base.
Use this to provide accurate, policy-compliant information:

---
{knowledge_context}
---

"""
        
        prompt += """
Your answer must be:
✅ Accurate and based on official policies
✅ Clear and actionable
✅ Professional yet empathetic
✅ Well-structured with proper formatting

If the question is outside your scope, say so politely and suggest which expert might be better suited.

📚 "Source references are provided for transparency."

Provide your response now:
"""
        
        # Get LLM response
        try:
            response = self.llm._call(prompt)
        except Exception as e:
            response = f"I apologize, but I encountered an error processing your request: {str(e)}"
        
        return {
            'agent_name': agent_info['name'],
            'agent_role': agent_info['role'],
            'response': response,
            'sources': sources,
            'has_knowledge_base': len(sources) > 0
        }
    
    def process_query(self, query: str, agent_types: Optional[List[str]] = None, context: str = None) -> str:
        """
        Process a query through one or more APEX agents.
        
        Args:
            query: User's question
            agent_types: List of agent types to use. If None, auto-detect or use Athena
            context: Additional context (optional)
            
        Returns:
            Formatted response string
        """
        # Auto-detect relevant agent if not specified
        if not agent_types or len(agent_types) == 0:
            agent_types = self._detect_relevant_agents(query)
        
        # Get responses from selected agents
        responses = []
        all_sources = []
        
        for agent_type in agent_types:
            if agent_type in self.agent_info:
                agent_response = self.get_agent_response(agent_type, query, context)
                responses.append(agent_response)
                all_sources.extend(agent_response["sources"])
        
        # Format response
        if len(responses) == 1:
            # Single agent response
            agent_resp = responses[0]
            formatted_response = f"## {agent_resp['agent_name']}'s Response\n\n{agent_resp['response']}"
            
            # Add sources
            if agent_resp['sources']:
                formatted_response += "\n\n### 📚 Sources Referenced\n"
                for i, src in enumerate(agent_resp['sources'], 1):
                    formatted_response += f"{i}. {src['document']} ({src['page_reference']})\n"
        
        else:
            # Multiple agents - synthesize
            formatted_response = "# 🧬 APEX Expert Guidance\n\n"
            
            # Add individual responses
            for agent_resp in responses:
                kb_indicator = "📚" if agent_resp["has_knowledge_base"] else "🧠"
                formatted_response += f"## {kb_indicator} {agent_resp['agent_name']} - {agent_resp['agent_role']}\n\n"
                formatted_response += f"{agent_resp['response']}\n\n"
            
            # Add consolidated sources
            if all_sources:
                formatted_response += "\n## 📚 Sources Referenced\n"
                seen_docs = set()
                for src in all_sources:
                    doc_id = f"{src['document']}_{src['page_reference']}"
                    if doc_id not in seen_docs:
                        formatted_response += f"— {src['document']} ({src['page_reference']})\n"
                        seen_docs.add(doc_id)
        
        return formatted_response
    
    def _detect_relevant_agents(self, query: str) -> List[str]:
        """Auto-detect which agents are most relevant for a query."""
        query_lower = query.lower()
        
        # Keywords for each agent
        agent_keywords = {
            'athena': ['policy', 'posh', 'legal', 'act', 'leave', 'maternity', 'transfer', 'ccl', 'rights', 'regulation', 'guideline'],
            'asha': ['stress', 'wellness', 'mental', 'burnout', 'balance', 'support', 'counseling', 'anxiety', 'depression'],
            'scribe': ['application', 'form', 'letter', 'document', 'write', 'prepare', 'draft', 'submit']
        }
        
        # Score each agent
        scores = {}
        for agent, keywords in agent_keywords.items():
            score = sum(1 for keyword in keywords if keyword in query_lower)
            if score > 0:
                scores[agent] = score
        
        # Return agents with scores, or default to Athena
        if scores:
            relevant_agents = [agent for agent, _ in sorted(scores.items(), key=lambda x: x[1], reverse=True)]
            return relevant_agents[:2]  # Max 2 agents
        else:
            return ['athena']  # Default to Athena for policy questions
    
    def generate_application(self, application_type: str, details: str) -> str:
        """
        Generate a formatted application using Scribe agent.
        
        Args:
            application_type: Type of application (maternity-leave, ccl, etc.)
            details: User-provided details for the application
            
        Returns:
            Formatted application text
        """
        prompt = f"""
You are Scribe, a Documentation Specialist for DRDO.
Generate a professional application for: {application_type}

User details:
{details}

Format the application properly with:
1. Date and subject line
2. Proper salutation
3. Well-structured body with all necessary details
4. Professional closing
5. Follow official government correspondence format

Generate the complete application now:
"""
        
        try:
            response = self.llm._call(prompt)
            return response
        except Exception as e:
            return f"Error generating application: {str(e)}"


def ask_apex(query: str, agent_types: List[str] = None, context: str = None) -> str:
    """
    Process a query through APEX agents with knowledge base integration.
    
    Args:
        query: The user's question or issue
        agent_types: Optional list of agent types to use. If None, auto-detect.
                    Options: "athena", "asha", "scribe"
        context: Additional context (optional)
    """
    # Use cached global instance to avoid reloading knowledge base
    global apex_instance
    if apex_instance is None:
        apex_instance = Apex()
    
    return apex_instance.process_query(query, agent_types, context)


def generate_application(application_type: str, details: str) -> str:
    """Generate an application using APEX Scribe agent."""
    global apex_instance
    if apex_instance is None:
        apex_instance = Apex()
    
    return apex_instance.generate_application(application_type, details)


# Global cached instance - loaded once when module is imported
apex_instance = None
