"""
Quick APEX Test Script
Test individual queries for debugging
"""
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

def quick_test(agent, query):
    """Test a single query quickly."""
    try:
        from knowledge_base.retriever import KnowledgeRetriever
        
        print(f"Testing {agent.upper()}: {query[:50]}...")
        
        retriever = KnowledgeRetriever()
        results = retriever.retrieve_for_agent(agent, query, top_k=2)
        
        if results:
            top_result = results[0]
            similarity = top_result.get('similarity', 0)
            source = top_result.get('metadata', {}).get('source', 'Unknown')
            text = top_result['text'][:200] + "..." if len(top_result['text']) > 200 else top_result['text']
            
            print(f"✅ Similarity: {similarity:.3f}")
            print(f"📄 Source: {source}")
            print(f"📜 Text: {text}")
            print("=" * 50)
            
            return True
        else:
            print("❌ No results found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

# Test key queries
print("🧪 QUICK APEX TESTING")
print("=" * 30)

# Athena tests
quick_test("athena", "DST Women Scientist Scheme-B WOS-B re-entry provisions age limit")
quick_test("athena", "DRDO IPR patent filing guidelines before publication")

# Asha tests  
quick_test("asha", "CCS Leave Rules 1972 Rule 43 maternity leave duration")
quick_test("asha", "stress management 5-step framework role overload")

# Scribe tests
quick_test("scribe", "Central Secretariat Manual Office Procedure CSMOP 2022 memorandum format")
quick_test("scribe", "e-Office User Manual Green Note Yellow Note difference")

print("Done!")