"""
Debug the knowledge retrieval system
"""

from knowledge_base.retriever import KnowledgeRetriever

def debug_retrieval():
    print("🔍 Debugging Knowledge Retrieval System")
    print("=" * 50)
    
    retriever = KnowledgeRetriever()
    
    print(f"Available agents: {retriever.get_available_agents()}")
    
    # Test retrieval for each agent
    test_queries = [
        ("maaya", "pregnancy nutrition"),
        ("gynika", "menstrual bleeding"),
        ("meher", "domestic violence"),
        ("nyaya", "patient rights"),
        ("vaanya", "menopause nutrition")
    ]
    
    for agent, query in test_queries:
        print(f"\n📋 Testing {agent} with query: '{query}'")
        try:
            results = retriever.retrieve_for_agent(agent, query, top_k=2, min_similarity=0.1)
            print(f"   Found {len(results)} results")
            
            for i, result in enumerate(results):
                doc_title = result.get('doc_title', 'Unknown')
                similarity = result.get('similarity', 0)
                text_preview = result.get('text', '')[:100] + "..."
                print(f"   {i+1}. {doc_title} (similarity: {similarity:.3f})")
                print(f"      Preview: {text_preview}")
                
        except Exception as e:
            print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    debug_retrieval()
