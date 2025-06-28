"""
Direct approach for SHAKTI-AI system with PDF knowledge base integration.
"""

from typing import Dict, List, Optional
from llm import GeminiLLM
from knowledge_base.retriever import KnowledgeRetriever

class ShaktiAI:
    """SHAKTI-AI implementation with PDF knowledge base support."""
    
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
            "maternal": {
                "name": "Maaya",
                "role": "Maternal Health Nurse",
                "expertise": "pregnancy, childbirth, and baby care",
                "specialties": ["pregnancy", "prenatal care", "childbirth", "postpartum", "breastfeeding", "infant care"]
            },
            "reproductive": {
                "name": "Gynika",
                "role": "Reproductive Health Advisor",
                "expertise": "menstruation, puberty, and contraception",
                "specialties": ["menstruation", "puberty", "contraception", "fertility", "reproductive health", "sexual health"]
            },
            "mental": {
                "name": "Meher",
                "role": "Mental Health Counselor",
                "expertise": "trauma, anxiety, and abuse recovery",
                "specialties": ["anxiety", "depression", "trauma", "PTSD", "domestic violence", "mental wellness"]
            },
            "legal": {
                "name": "Nyaya",
                "role": "Legal Rights Advisor",
                "expertise": "Indian laws related to women's rights",
                "specialties": ["women's rights", "family law", "workplace harassment", "domestic violence law", "property rights"]
            },
            "feminist": {
                "name": "Vaanya",
                "role": "Feminist Health Educator",
                "expertise": "menopause, hormonal health, and women's empowerment",
                "specialties": ["menopause", "hormonal health", "women's empowerment", "body autonomy", "health advocacy"]
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
            "maternal": "maaya",
            "reproductive": "gynika", 
            "mental": "meher",
            "legal": "nyaya",
            "feminist": "vaanya"
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
        
        prompt = f"""You are {agent_info['name']}, a {agent_info['role']} specializing in {agent_info['expertise'].replace(", ", ", and")}. 

        A user has asked the following question:
        {query}

        """

        if age:
            prompt += f"""The user is {age} years old. Adapt your tone, level of detail, and examples to be appropriate for this age."""

        if knowledge_context:
            prompt += f"""Based on the following information from your knowledge base:

        {knowledge_context}

        """

        prompt += f"""Please provide a helpful, informative, and compassionate response based on your expertise.
        Focus on providing accurate information while being culturally sensitive and respectful.
        If the question is outside your area of expertise, acknowledge this and provide general guidance.
        Keep your response clear, practical, and empathetic."""

        
        
        
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
            if agent_resp["sources"]:
                formatted_response += f"\n\n### 📚 Knowledge Base References\n"
                for i, source in enumerate(agent_resp["sources"], 1):
                    # Document header with confidence indicator
                    confidence_emoji = "🎯" if source['confidence'] == 'High' else "📊" if source['confidence'] == 'Medium' else "📋"
                    formatted_response += f"\n**{confidence_emoji} Reference {i}: {source['document']}**\n"
                    formatted_response += f"- **Location**: {source['page_reference']}\n"
                    formatted_response += f"- **Relevance**: {source['relevance_score']:.3f} ({source['confidence']} confidence)\n"
                    formatted_response += f"- **Content Preview**: {source['preview']}\n"
                    
                    # Show extract for high-relevance sources
                    if source['relevance_score'] > 0.4:
                        formatted_response += f"\n**📖 Key Extract**:\n"
                        formatted_response += f"*{source['extract']}*\n"
                    
                    # Add word count for context
                    formatted_response += f"- **Source Details**: {source['word_count']} words, {source['filename']}\n"
            
            return formatted_response
            
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
        formatted_response = "# 🧬 SHAKTI-AI Expert Guidance\n\n"
        formatted_response += synthesis
        
        # Add sources if available
        if all_sources:
            formatted_response += f"\n\n## 📚 Sources Referenced\n"
            unique_sources = {}
            for source in all_sources:
                doc_key = f"{source['document']}_{source.get('page_reference', 'Unknown')}"
                if doc_key not in unique_sources:
                    unique_sources[doc_key] = source
            
            for i, source in enumerate(unique_sources.values(), 1):
                formatted_response += f"{i}. {source['document']} ({source.get('page_reference', 'Page Unknown')})\n"
        
        # Add individual expert responses section
        formatted_response += "\n\n---\n\n## 👥 Individual Expert Responses\n\n"
        
        for agent_resp in responses:
            kb_indicator = "📚" if agent_resp["has_knowledge_base"] else "🧠"
            formatted_response += f"### {kb_indicator} {agent_resp['agent_name']} - {agent_resp['agent_role']}\n\n"
            formatted_response += f"{agent_resp['response']}\n\n"
            
        return formatted_response

def ask_shakti_ai(query: str, agent_types: List[str] = None, age: Optional[int] = None) -> str:
    """
    Process a query through SHAKTI-AI agents with knowledge base integration.
    
    Args:
        query: The user's question or issue
        agent_types: Optional list of agent types to use. If None, all agents will be used.
                    Options: "maternal", "reproductive", "mental", "legal", "feminist"
    """
    shakti = ShaktiAI()
    return shakti.process_query(query, agent_types, age)
