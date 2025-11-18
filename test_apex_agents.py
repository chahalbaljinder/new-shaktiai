"""
APEX Agents Testing Script
Tests Athena, Asha, and Scribe with specific queries from user requirements.
"""

import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_athena_queries():
    """Test Athena with policy and research funding queries."""
    print("🏛️  TESTING ATHENA (Policy & Research Agent)")
    print("=" * 60)
    
    athena_queries = [
        {
            "query": "I am a woman scientist looking to return to research after a 2-year break. What specific provisions or schemes does the DST Women Scientist Scheme-B (WOS-B) offer for re-entry, and what is the upper age limit?",
            "expected_topics": ["women scientist scheme", "re-entry", "age limit", "DST"]
        },
        {
            "query": "I need to submit a proposal for the 'Apex' project. Based on the ER & IPR 'Grant-in-Aid' formats, structure a project summary that includes the 'Objectives', 'Methodology', and 'Budgetary Breakdown' sections.",
            "expected_topics": ["grant-in-aid", "project proposal", "objectives", "methodology", "budget"]
        },
        {
            "query": "We have developed a new AI multi-agent architecture. According to standard DRDO IPR guidelines, what is the first step to file a patent before publishing this in a conference paper?",
            "expected_topics": ["DRDO", "IPR", "patent", "filing", "publication"]
        },
        {
            "query": "Summarize the key differences between 'Extramural Research' and 'Contract Research' based on the DRDO funding guidelines.",
            "expected_topics": ["extramural research", "contract research", "DRDO", "funding"]
        }
    ]
    
    return test_agent_queries("athena", athena_queries)

def test_asha_queries():
    """Test Asha with wellness and support queries."""
    print("🧘 TESTING ASHA (Wellness & Support Agent)")  
    print("=" * 60)
    
    asha_queries = [
        {
            "query": "I am planning maternity leave. Can you list the exact duration of paid leave available under CCS (Leave) Rules, 1972, Rule 43, and explain how it differs from Child Care Leave (Rule 43-C)",
            "expected_topics": ["maternity leave", "CCS rules", "rule 43", "child care leave", "duration"]
        },
        {
            "query": "I feel overwhelmed by the 'publish or perish' pressure. Using the Centre for Good Governance Handbook on Stress Management, can you give me the '5-step framework' to handle role overload?",
            "expected_topics": ["stress management", "role overload", "5-step framework", "publish or perish"]
        },
        {
            "query": "I feel like I don't belong in this lab. Do you have any exercises from the 'Imposter Syndrome Workbook for Women in STEM' that can help me document my achievements?",
            "expected_topics": ["imposter syndrome", "women in STEM", "achievements", "exercises"]
        },
        {
            "query": "My senior is emailing me at 10 PM. Based on the Doan Lab Manual's mental health section, how should I politely set a boundary regarding after-hours communication?",
            "expected_topics": ["mental health", "boundaries", "after-hours", "communication", "Doan lab"]
        }
    ]
    
    return test_agent_queries("asha", asha_queries)

def test_scribe_queries():
    """Test Scribe with documentation and procedural queries."""
    print("📝 TESTING SCRIBE (Documentation & Procedures Agent)")
    print("=" * 60)
    
    scribe_queries = [
        {
            "query": "Draft a formal Office Memorandum (OM) to the Admin Department requesting a new laptop. Use the layout specified in the Central Secretariat Manual of Office Procedure (CSMOP) 2022, including the correct 'To' and 'Subject' alignment.",
            "expected_topics": ["office memorandum", "CSMOP", "format", "laptop request", "alignment"]
        },
        {
            "query": "I need to move this file for approval. Explain the difference between a 'Green Note' and a 'Yellow Note' based on the e-Office User Manual, and tell me which one is used for a final draft",
            "expected_topics": ["green note", "yellow note", "e-office", "file approval", "final draft"]
        },
        {
            "query": "I want to apply for a transfer to another department. Generate the 'Bio-Data Proforma' checklist based on the standard DoPT Deputation guidelines.",
            "expected_topics": ["bio-data proforma", "transfer", "DoPT", "deputation", "checklist"]
        }
    ]
    
    return test_agent_queries("scribe", scribe_queries)

def test_agent_queries(agent_name, queries):
    """Test specific queries for an agent."""
    try:
        from knowledge_base.retriever import KnowledgeRetriever
        retriever = KnowledgeRetriever()
        
        results_summary = {
            "agent": agent_name,
            "total_queries": len(queries),
            "successful_queries": 0,
            "failed_queries": 0,
            "details": []
        }
        
        for i, query_data in enumerate(queries, 1):
            query = query_data["query"]
            expected_topics = query_data["expected_topics"]
            
            print(f"\n🔍 QUERY {i}:")
            print(f"❓ {query}")
            print(f"📋 Expected Topics: {', '.join(expected_topics)}")
            print("-" * 50)
            
            try:
                # Get retrieval results
                results = retriever.retrieve_for_agent(agent_name, query, top_k=3)
                
                if results:
                    print(f"✅ Found {len(results)} relevant chunks")
                    
                    # Analyze quality of results
                    best_similarity = max([r.get('similarity', 0) for r in results])
                    avg_similarity = sum([r.get('similarity', 0) for r in results]) / len(results)
                    
                    print(f"📊 Best Similarity: {best_similarity:.3f}")
                    print(f"📊 Average Similarity: {avg_similarity:.3f}")
                    
                    # Show top result
                    top_result = results[0]
                    source = top_result.get('metadata', {}).get('source', 'Unknown')
                    text_preview = top_result['text'][:300] + "..." if len(top_result['text']) > 300 else top_result['text']
                    
                    print(f"📄 Source: {source}")
                    print(f"📜 Preview: {text_preview}")
                    
                    # Check if expected topics are covered
                    combined_text = " ".join([r['text'].lower() for r in results])
                    topics_found = [topic for topic in expected_topics if any(keyword in combined_text for keyword in topic.split())]
                    
                    print(f"🎯 Topics Covered: {len(topics_found)}/{len(expected_topics)} - {topics_found}")
                    
                    # Determine success based on similarity and topic coverage
                    if best_similarity > 0.3 and len(topics_found) > 0:
                        print("✅ QUERY SUCCESS")
                        results_summary["successful_queries"] += 1
                        success = True
                    else:
                        print("⚠️  QUERY PARTIAL SUCCESS")
                        results_summary["successful_queries"] += 0.5
                        success = False
                else:
                    print("❌ No results found")
                    results_summary["failed_queries"] += 1
                    success = False
                
                # Store details
                results_summary["details"].append({
                    "query": query[:100] + "..." if len(query) > 100 else query,
                    "success": success,
                    "similarity": best_similarity if results else 0,
                    "topics_found": len(topics_found) if results else 0,
                    "total_topics": len(expected_topics)
                })
                
            except Exception as e:
                print(f"❌ Query failed with error: {e}")
                results_summary["failed_queries"] += 1
                results_summary["details"].append({
                    "query": query[:100] + "..." if len(query) > 100 else query,
                    "success": False,
                    "error": str(e)
                })
        
        return results_summary
        
    except Exception as e:
        print(f"❌ Agent {agent_name} test failed: {e}")
        return None

def test_core_integration():
    """Test the ask_apex core function."""
    print("\n🔗 TESTING CORE INTEGRATION")
    print("=" * 60)
    
    try:
        from core.crew import ask_apex
        
        test_query = "What is the sexual harassment policy?"
        print(f"🧪 Testing ask_apex with: '{test_query}'")
        
        response = ask_apex(test_query, ["policy-guide"])
        
        if response and len(response) > 50:
            print("✅ ask_apex working correctly")
            print(f"📝 Response length: {len(response)} characters")
            print(f"📜 Sample response: {response[:200]}...")
            return True
        else:
            print("⚠️  ask_apex returned short/empty response")
            print(f"Response: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Core integration test failed: {e}")
        return False

def main():
    """Run comprehensive testing of all APEX agents."""
    print("🚀 APEX AGENTS COMPREHENSIVE TESTING")
    print("=" * 80)
    print("Testing Athena, Asha, and Scribe with specific user queries...")
    print()
    
    # Test each agent
    athena_results = test_athena_queries()
    asha_results = test_asha_queries()  
    scribe_results = test_scribe_queries()
    core_works = test_core_integration()
    
    # Generate final report
    print("\n" + "=" * 80)
    print("📊 FINAL TESTING REPORT")
    print("=" * 80)
    
    all_results = [r for r in [athena_results, asha_results, scribe_results] if r]
    
    if all_results:
        total_queries = sum([r["total_queries"] for r in all_results])
        total_successful = sum([r["successful_queries"] for r in all_results])
        
        print(f"📈 Overall Success Rate: {total_successful}/{total_queries} ({(total_successful/total_queries)*100:.1f}%)")
        
        for result in all_results:
            agent = result["agent"].title()
            success_rate = (result["successful_queries"] / result["total_queries"]) * 100
            print(f"  🤖 {agent}: {result['successful_queries']}/{result['total_queries']} ({success_rate:.1f}%)")
        
        print(f"\n🔗 Core Integration: {'✅ Working' if core_works else '❌ Failed'}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if total_successful / total_queries > 0.8:
            print("🎉 Excellent! Your RAG pipeline is performing very well!")
            print("✅ Ready for production use")
        elif total_successful / total_queries > 0.6:
            print("👍 Good performance! Some fine-tuning recommended:")
            print("  - Consider adding more relevant documents") 
            print("  - Review chunk size and overlap settings")
        else:
            print("⚠️  Performance needs improvement:")
            print("  - Check if PDFs were processed correctly")
            print("  - Verify vector store creation")
            print("  - Consider document preprocessing")
        
        # Agent-specific recommendations
        for result in all_results:
            agent = result["agent"]
            if result["successful_queries"] / result["total_queries"] < 0.7:
                print(f"  📚 {agent.title()}: Add more relevant documents or improve preprocessing")
    
    else:
        print("❌ Testing failed - check your knowledge base setup")
        print("🔧 Run create_apex_rag.py to rebuild the knowledge base")

if __name__ == "__main__":
    main()