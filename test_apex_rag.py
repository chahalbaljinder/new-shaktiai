"""
APEX RAG Pipeline Tester
This script tests the APEX knowledge base and retrieval system.
"""

import sys
import os

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def test_apex_rag():
    """Test the APEX RAG pipeline."""
    try:
        print("🧪 Testing APEX RAG Pipeline")
        print("=" * 40)
        
        from knowledge_base.retriever import KnowledgeRetriever
        
        # Initialize retriever
        print("📋 Initializing Knowledge Retriever...")
        retriever = KnowledgeRetriever()
        
        # Check available agents
        available_agents = retriever.get_available_agents()
        print(f"✅ Available agents: {available_agents}")
        
        if not available_agents:
            print("❌ No agents available! Run create_apex_rag.py first.")
            return False
        
        # Get knowledge base statistics
        print(f"\n📊 Knowledge Base Statistics:")
        stats = retriever.get_knowledge_stats()
        for agent_name, agent_stats in stats.items():
            print(f"  📚 {agent_name.title()}: {agent_stats.get('total_chunks', 0)} chunks")
        
        # Test queries for each agent
        test_queries = {
            'athena': [
                "What is the POSH Act?",
                "Maternity leave policy",
                "Sexual harassment guidelines"
            ],
            'asha': [
                "Stress management techniques",
                "Work life balance",
                "Mental health support"
            ],
            'scribe': [
                "Leave application form",
                "Grievance filing procedure",
                "Office documentation"
            ]
        }
        
        print(f"\n🔍 Testing Retrieval for Each Agent:")
        print("-" * 40)
        
        all_tests_passed = True
        
        for agent_name in ['athena', 'asha', 'scribe']:
            if agent_name in available_agents:
                print(f"\n🤖 Testing {agent_name.title()}:")
                
                queries = test_queries.get(agent_name, ["test query"])
                
                for query in queries:
                    print(f"  🔎 Query: '{query}'")
                    
                    try:
                        results = retriever.retrieve_for_agent(agent_name, query, top_k=2)
                        
                        if results:
                            print(f"    ✅ Found {len(results)} relevant chunks")
                            
                            # Show first result preview
                            first_result = results[0]
                            text_preview = first_result['text'][:100] + "..." if len(first_result['text']) > 100 else first_result['text']
                            similarity = first_result.get('similarity', 0)
                            print(f"    📄 Preview: {text_preview}")
                            print(f"    📊 Similarity: {similarity:.3f}")
                        else:
                            print(f"    ⚠️  No results found")
                            all_tests_passed = False
                            
                    except Exception as e:
                        print(f"    ❌ Query failed: {e}")
                        all_tests_passed = False
            else:
                print(f"\n⚠️  {agent_name.title()}: Not available")
                all_tests_passed = False
        
        # Test the core integration
        print(f"\n🔗 Testing Core Integration:")
        try:
            from core.crew import ask_apex
            print("✅ Core integration available")
            
            # Test a simple query
            print("🧪 Testing ask_apex function...")
            response = ask_apex("What is sexual harassment policy?", ["legal-guide"])
            
            if response and len(response) > 50:
                print("✅ ask_apex working correctly")
                print(f"📝 Sample response: {response[:200]}...")
            else:
                print("⚠️  ask_apex returned short/empty response")
                print(f"Response: {response}")
                
        except Exception as e:
            print(f"❌ Core integration test failed: {e}")
            all_tests_passed = False
        
        # Final results
        print(f"\n" + "=" * 40)
        if all_tests_passed:
            print("🎉 ALL TESTS PASSED!")
            print("✅ Your APEX RAG pipeline is working correctly!")
            print("\n🚀 Ready to use:")
            print("  - Streamlit app: python app.py")
            print("  - FastAPI backend: python backend_service.py")
            print("  - Next.js frontend: cd shakti-ai-nextjs && npm run dev")
        else:
            print("⚠️  SOME TESTS FAILED!")
            print("Check the error messages above and ensure:")
            print("  - PDFs were processed correctly")
            print("  - Vector stores were created")
            print("  - All dependencies are installed")
        
        return all_tests_passed
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Run create_apex_rag.py first to create the knowledge base")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def quick_query_test(agent_name, query):
    """Quick test of a single query."""
    try:
        from knowledge_base.retriever import KnowledgeRetriever
        retriever = KnowledgeRetriever()
        
        print(f"Testing {agent_name}: '{query}'")
        results = retriever.retrieve_for_agent(agent_name, query, top_k=1)
        
        if results:
            result = results[0]
            preview = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
            print(f"✅ Found: {preview}")
            print(f"📊 Similarity: {result.get('similarity', 0):.3f}")
        else:
            print("❌ No results found")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 2:
        # Quick query mode: python test_apex_rag.py athena "POSH Act"
        agent_name = sys.argv[1]
        query = sys.argv[2]
        quick_query_test(agent_name, query)
    else:
        # Full test mode
        test_apex_rag()