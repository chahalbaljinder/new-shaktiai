"""
Test script to demonstrate enhanced PDF references in SHAKTI-AI
"""

from crew import ShaktiAI

def test_enhanced_references():
    """Test the enhanced reference system with sample queries."""
    
    print("🧬 Testing SHAKTI-AI Enhanced Reference System")
    print("=" * 60)
    
    shakti = ShaktiAI()
    
    # Test queries for different agents
    test_queries = [
        {
            "agent": "maternal",
            "query": "What are the WHO recommendations for antenatal care during pregnancy?",
            "description": "Testing maternal health knowledge with WHO guidelines"
        },
        {
            "agent": "reproductive", 
            "query": "How can adolescents manage heavy menstrual bleeding?",
            "description": "Testing reproductive health knowledge"
        },
        {
            "agent": "mental",
            "query": "What legal protections exist for women facing domestic violence?",
            "description": "Testing mental health and legal knowledge"
        },
        {
            "agent": "legal",
            "query": "What are the patient rights according to NHRC 2019?",
            "description": "Testing legal knowledge base"
        },
        {
            "agent": "feminist",
            "query": "What nutritional recommendations are important during menopause?",
            "description": "Testing feminist health knowledge"
        }
    ]
    
    for i, test_case in enumerate(test_queries, 1):
        print(f"\n🔍 Test Case {i}: {test_case['description']}")
        print(f"Agent: {test_case['agent'].title()}")
        print(f"Query: {test_case['query']}")
        print("-" * 60)
        
        try:
            response = shakti.get_agent_response(test_case['agent'], test_case['query'])
            
            print(f"\n👤 {response['agent_name']} ({response['agent_role']}):")
            print(f"📚 Knowledge Base Available: {response['has_knowledge_base']}")
            
            if response['sources']:
                print(f"\n📖 References Found: {len(response['sources'])}")
                
                for j, source in enumerate(response['sources'][:2], 1):  # Show first 2 sources
                    print(f"\n  📄 Reference {j}:")
                    print(f"    Document: {source['document']}")
                    print(f"    Page: {source.get('page_reference', 'Unknown')}")
                    print(f"    Relevance: {source['relevance_score']:.3f} ({source['confidence']})")
                    print(f"    Preview: {source['preview'][:100]}...")
                    
                    if source['relevance_score'] > 0.4:
                        print(f"    Extract: {source['extract'][:150]}...")
            else:
                print("⚠️ No knowledge base references found")
                
            print(f"\n💬 Response Preview:")
            print(f"    {response['response'][:200]}...")
            
        except Exception as e:
            print(f"❌ Error testing {test_case['agent']}: {e}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_enhanced_references()
