"""
Direct approach for SHAKTI-AI system with PDF knowledge base integration.
"""

from typing import Dict, List, Optional
from core.llm import GeminiLLM
from knowledge_base.retriever import KnowledgeRetriever

class Apex:
    """APEX implementation with PDF knowledge base support."""
    
    def __init__(self):
        self.llm = GeminiLLM()
        
        # Initialize knowledge retriever
        try:
            self.retriever = KnowledgeRetriever()
            print(f"📚 Knowledge base loaded for agents: {', '.join(self.retriever.get_available_agents())}")
        except Exception as e:
            print(f"⚠️ Knowledge base not available: {e}")
            self.retriever = None
        
        self.agent_info = {
            "legal-guide": {
                "name": "Athena",
                "role": "Policy & Procedure Agent",
                "expertise": "government HR policies, legal regulations, and official procedures for women scientists in Indian government organizations",
                "specialties": [
                    # Leave Policies
                    "maternity leave", "child care leave", "CCL", "paternity leave", 
                    "medical leave", "study leave", "earned leave", "casual leave",
                    
                    # Transfer & Posting Policies  
                    "transfer guidelines", "spouse ground transfer", "hardship posting",
                    "family station transfer", "compassionate transfer", "mutual transfer",
                    
                    # Legal Rights & Protection
                    "POSH Act", "sexual harassment", "workplace harassment", 
                    "gender discrimination", "equal opportunity", "women's rights at workplace",
                    
                    # Career & Promotion
                    "promotion policies", "career progression", "performance appraisal",
                    "project allocation", "research opportunities", "leadership positions",
                    
                    # Grievance & Redressal
                    "grievance filing", "complaint procedures", "appeals process", 
                    "disciplinary action", "vigilance matters", "administrative redressal"
                ]
            },
            "wellness": {
                "name": "Asha",
                "role": "Wellness & Support Agent",
                "expertise": "mental wellness, work-life balance, and confidential emotional support for women scientists in government organizations",
                "specialties": [
                    # Mental Wellness & Stress Management
                    "stress management", "anxiety", "burnout prevention", "emotional support",
                    "mental health resources", "counseling referrals", "crisis intervention",
                    
                    # Work-Life Integration
                    "work-life balance", "time management", "career-family balance",
                    "dual career couples", "childcare support", "eldercare responsibilities",
                    
                    # Workplace Wellness
                    "workplace stress", "professional isolation", "imposter syndrome",
                    "confidence building", "peer support networks", "mentorship guidance",
                    
                    # Safety & Confidential Support
                    "workplace harassment support", "emotional trauma", "safety planning",
                    "anonymous reporting", "confidential counseling", "victim support",
                    
                    # Empowerment & Motivation  
                    "self-advocacy", "assertiveness training", "communication skills",
                    "boundary setting", "resilience building", "motivational support",
                    
                    # Specialized Support for Scientists
                    "research stress", "publication pressure", "conference anxiety",
                    "presentation skills", "networking challenges", "career transitions"
                ]
            },
            "documentation": {
                "name": "Scribe", 
                "role": "Documentation & Workflow Agent",
                "expertise": "automated document generation, form assistance, and procedural guidance for women scientists in government organizations",
                "specialties": [
                    # Document Generation & Forms
                    "leave applications", "transfer requests", "grievance forms", "appeal letters",
                    "maternity leave forms", "CCL applications", "medical leave documentation",
                    "official correspondence", "policy interpretation documents", "legal notices",
                    
                    # Workflow & Process Guidance
                    "step-by-step procedures", "submission guidelines", "approval workflows",
                    "document checklists", "required attachments", "filing deadlines",
                    "follow-up procedures", "status tracking", "escalation protocols",
                    
                    # Administrative Navigation
                    "office procedures", "bureaucratic processes", "authority identification",
                    "submission channels", "reference number tracking", "timeline management",
                    "reminder systems", "progress monitoring", "case documentation",
                    
                    # Specialized Government Forms
                    "POSH complaint forms", "vigilance matter reports", "transfer applications",
                    "promotion documentation", "performance appraisal submissions", 
                    "research proposal formats", "project allocation requests",
                    
                    # Compliance & Legal Documentation
                    "policy compliance forms", "statutory requirements", "legal documentation",
                    "evidence compilation", "witness statements", "incident reports",
                    "safety documentation", "confidentiality agreements",
                    
                    # Communication & Correspondence
                    "official email templates", "letter formatting", "petition drafting",
                    "meeting minutes", "formal requests", "acknowledgment receipts",
                    "status inquiry letters", "clarification requests"
                ]
            }
        }
    
    def get_relevant_knowledge(self, agent_type: str, query: str) -> tuple[str, List[Dict]]:
        """
        Retrieve relevant knowledge from the agent's knowledge base.
        
        Args:
            agent_type: Type of agent
            query: User query
            
        Returns:
            Tuple of (context_string, detailed_source_citations)
        """
        # Map agent types to knowledge base names
        agent_mapping = {
            "legal-guide": "athena",
            "wellness": "asha", 
            "documentation": "scribe"
        }
        
        kb_agent_name = agent_mapping.get(agent_type)
        
        if not self.retriever or not kb_agent_name or kb_agent_name not in self.retriever.get_available_agents():
            return "", []
        
        try:
            # Retrieve relevant chunks
            retrieved_chunks = self.retriever.retrieve_for_agent(kb_agent_name, query, top_k=4, min_similarity=0.2)
            
            if not retrieved_chunks:
                return "", []
            
            # Format context with more detailed information
            context_parts = []
            for i, chunk in enumerate(retrieved_chunks):
                doc_title = chunk.get('doc_title', 'Unknown')
                chunk_text = chunk.get('text', '')
                relevance = chunk.get('similarity', 0)
                
                context_part = f"[Reference {i+1} from '{doc_title}' (Relevance: {relevance:.2f})]:\n{chunk_text}"
                context_parts.append(context_part)
            
            context = "\n\n---\n\n".join(context_parts)
            
            # Get detailed source citations with enhanced metadata
            sources = self.retriever.get_enhanced_source_citations(retrieved_chunks)
            
            return context, sources
            
        except Exception as e:
            print(f"Error retrieving knowledge for {agent_type}: {e}")
            return "", []
    
    def get_agent_response(self, agent_type: str, query: str, age: Optional[int] = None) -> Dict[str, any]:
        """Get a response from a specific agent with knowledge base integration."""
        agent_info = self.agent_info[agent_type]
        
        # Get relevant knowledge from knowledge base
        knowledge_context, sources = self.get_relevant_knowledge(agent_type, query)
        
        
        # Add knowledge base context if available
        
        prompt = f"""
            You are {agent_info['name']}, a {agent_info['role']} who specializes in {agent_info['expertise'].replace(", ", ", and")}.
            Your mission is to empower women scientists in Indian government organizations (DRDO, ISRO, CSIR) by providing accurate, trustworthy, and confidential support — helping them navigate complex policies, procedures, and workplace challenges with confidence.

            A user has asked:
            "{query}"

            Your style guide:
            1️⃣ Your reply must feel professional yet supportive — use clear, confident language while maintaining warmth and empathy.
            2️⃣ Add **micro-questions** or reflection prompts when it helps the user clarify their situation or next steps.
            3️⃣ Include **practical examples** or **step-by-step guidance** when relevant (like specific procedures, templates, or scripts they could use).
            4️⃣ If you use information from the knowledge base, integrate it naturally — provide context and explain relevance rather than just listing facts.
            5️⃣ End with a **empowering sign-off**: reassure them of confidentiality, encourage follow-up questions, or remind them of available support.
            6️⃣ Provide specific policy details, legal rights, or procedural information when clearly relevant — be thorough but organized, don't overwhelm.
            7️⃣ Consider the unique challenges faced by women in scientific government roles: work-life balance, career progression, systemic barriers, and safety concerns.
            8️⃣ Maintain complete confidentiality and remind users of anonymous reporting options when discussing sensitive matters.

            Context: You are part of Project Apex, designed specifically for women scientists in Indian government organizations who may face cultural barriers, policy complexity, and workplace challenges unique to these environments.

            """

        if age:
            prompt += f"\nAdapt your tone and examples for a {age}-year-old."

        if knowledge_context:
            prompt += f"""
        Below is relevant information from your knowledge base.
        Paraphrase it into your own words — do not just copy-paste.

        ---
        {knowledge_context}
        ---
        """

        prompt += """
        Your answer must be:
        ✅ Clear and practical.
        ✅ Emotionally validating.
        ✅ Culturally sensitive for India.
        ✅ 100% respectful and non-judgmental.
        ✅ End with a line reminding them they can check your references.

        If the question is outside your scope, say so politely and suggest where they can go next.

        When you are done, add a short note:
        📚 "Full source references are provided for transparency."

        Start your response directly — no preamble about being an AI.
        """


        
        
        
        # Get response from LLM
        response_text = self.llm._call(prompt)
        
        # Return structured response
        return {
            "agent_name": agent_info["name"],
            "agent_role": agent_info["role"],
            "response": response_text,
            "sources": sources,
            "has_knowledge_base": bool(knowledge_context)
        }
    
    def process_query(self, query: str, agent_types: Optional[List[str]] = None, age: Optional[int] = None) -> str:
        """Process a query through one or more agents."""
        # Use all agents if none specified
        if not agent_types or len(agent_types) == 0:
            agent_types = list(self.agent_info.keys())
            
        # Get responses from each selected agent
        responses = []
        all_sources = []
        
        for agent_type in agent_types:
            if agent_type in self.agent_info:
                agent_response = self.get_agent_response(agent_type, query, age)
                responses.append(agent_response)
                all_sources.extend(agent_response["sources"])
        
        # If only one agent, return its response directly
        if len(responses) == 1:
            agent_resp = responses[0]
            formatted_response = f"## {agent_resp['agent_name']}'s Response\n\n{agent_resp['response']}"
            
            # Add detailed sources if available
            # Add sources if available
            if all_sources:
                formatted_response += f"\n\n## 📚 Sources Used\n"

                # Group all pages per document
                grouped = {}
                for src in all_sources:
                    doc = src['document'].strip()
                    page_ref = src.get('page_reference', 'Unknown')

                    # Extract page numbers only
                    nums = []
                    for p in page_ref.replace('Pages', '').replace('Page', '').split(','):
                        p = p.strip()
                        if p.isdigit():
                            nums.append(int(p))
                        elif '-' in p:
                            start, end = p.split('-')
                            if start.strip().isdigit() and end.strip().isdigit():
                                nums.extend(range(int(start.strip()), int(end.strip()) + 1))

                    if doc not in grouped:
                        grouped[doc] = set()
                    grouped[doc].update(nums)

                # Collapse consecutive numbers nicely
                def collapse(nums):
                    nums = sorted(nums)
                    if not nums:
                        return ''
                    ranges = []
                    start = prev = nums[0]
                    for n in nums[1:]:
                        if n == prev + 1:
                            prev = n
                        else:
                            if start == prev:
                                ranges.append(f"{start}")
                            else:
                                ranges.append(f"{start}–{prev}")
                            start = prev = n
                    if start == prev:
                        ranges.append(f"{start}")
                    else:
                        ranges.append(f"{start}–{prev}")
                    return "pp. " + ', '.join(ranges)

                for doc, nums in grouped.items():
                    if nums:
                        page_str = collapse(nums)
                    else:
                        page_str = "(Page Unknown)"
                    formatted_response += f"— {doc}, {page_str}\n"


            
        # Otherwise, synthesize the responses
        synthesis_prompt = f"""The following experts have provided responses to this query:
        
Query: {query}

"""
        
        expert_responses = []
        for agent_resp in responses:
            expert_responses.append(f"**{agent_resp['agent_name']} ({agent_resp['agent_role']}):**\n{agent_resp['response']}")
        
        synthesis_prompt += "\n\n".join(expert_responses)
        
        synthesis_prompt += """\n\nPlease synthesize these expert opinions into a comprehensive, coherent response.
Highlight the areas of consensus and note any different perspectives. Maintain a helpful, empathetic tone
and ensure the response is culturally sensitive and appropriate. Structure the response clearly."""
        
        synthesis = self.llm._call(synthesis_prompt)
        
        # Format final response
        formatted_response = "# 🧬 APEX Expert Guidance\n\n"
        formatted_response += synthesis
        
        # Add sources if available (group by document and merge page numbers)
        if all_sources:
            formatted_response += f"\n\n## 📚 Sources Referenced\n"
            # Group by document
            doc_pages = {}
            for src in all_sources:
                doc = src['document'].strip()
                page_ref = src.get('page_reference', 'Unknown')
                # Extract page numbers
                nums = []
                for p in page_ref.replace('Pages', '').replace('Page', '').split(','):
                    p = p.strip()
                    if p.isdigit():
                        nums.append(int(p))
                    elif '-' in p:
                        parts = p.split('-')
                        if len(parts) == 2 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
                            nums.extend(range(int(parts[0].strip()), int(parts[1].strip()) + 1))
                if doc not in doc_pages:
                    doc_pages[doc] = set()
                doc_pages[doc].update(nums)
            # Collapse consecutive numbers into ranges
            def collapse(nums):
                nums = sorted(nums)
                if not nums:
                    return ''
                ranges = []
                start = prev = nums[0]
                for n in nums[1:]:
                    if n == prev + 1:
                        prev = n
                    else:
                        if start == prev:
                            ranges.append(f"{start}")
                        else:
                            ranges.append(f"{start}-{prev}")
                        start = prev = n
                if start == prev:
                    ranges.append(f"{start}")
                else:
                    ranges.append(f"{start}-{prev}")
                return ', '.join(ranges)
            for i, (doc, nums) in enumerate(doc_pages.items(), 1):
                if nums:
                    page_str = collapse(nums)
                    if ',' in page_str or '-' in page_str:
                        page_label = f"Pages {page_str}"
                    else:
                        page_label = f"Page {page_str}"
                else:
                    page_label = "Page Unknown"
                formatted_response += f"{i}. {doc} ({page_label})\n"
        
        # Add individual expert responses section
        formatted_response += "\n\n---\n\n## 👥 Individual Expert Responses\n\n"
        
        for agent_resp in responses:
            kb_indicator = "📚" if agent_resp["has_knowledge_base"] else "🧠"
            formatted_response += f"### {kb_indicator} {agent_resp['agent_name']} - {agent_resp['agent_role']}\n\n"
            formatted_response += f"{agent_resp['response']}\n\n"
            
        return formatted_response

def ask_apex(query: str, agent_types: List[str] = None, age: Optional[int] = None) -> str:
    """
    Process a query through APEX agents with knowledge base integration.
    
    Args:
        query: The user's question or issue
        agent_types: Optional list of agent types to use. If None, all agents will be used.
                    Options: "legal-guide", "wellness", "documentation"
    """
    # Use cached global instance to avoid reloading knowledge base
    global apex_instance
    if apex_instance is None:
        apex_instance = Apex()
    
    return apex_instance.process_query(query, agent_types, age)

# Global cached instance - loaded once when module is imported
apex_instance = None
