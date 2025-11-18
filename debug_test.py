"""
Simple APEX test - debug version
"""
import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("🔍 Debugging APEX components...")

# Test 1: Check if knowledge base directories exist
print("\n1. Checking knowledge base structure...")
kb_path = os.path.join(current_dir, "knowledge_base", "processed")
if os.path.exists(kb_path):
    agents = ['athena', 'asha', 'scribe']
    for agent in agents:
        agent_path = os.path.join(kb_path, f"{agent}_vectorstore")
        if os.path.exists(agent_path):
            print(f"✅ {agent.title()} vectorstore found")
            # Check files
            required_files = ['index.faiss', 'chunks.pkl', 'metadata.json']
            for file in required_files:
                file_path = os.path.join(agent_path, file)
                if os.path.exists(file_path):
                    print(f"  ✅ {file}")
                else:
                    print(f"  ❌ {file} missing")
        else:
            print(f"❌ {agent.title()} vectorstore not found")
else:
    print(f"❌ Knowledge base processed directory not found: {kb_path}")

# Test 2: Try importing required modules
print("\n2. Testing imports...")
try:
    from sentence_transformers import SentenceTransformer
    print("✅ sentence-transformers")
except ImportError as e:
    print(f"❌ sentence-transformers: {e}")

try:
    import faiss
    print("✅ faiss")
except ImportError as e:
    print(f"❌ faiss: {e}")

try:
    from knowledge_base.vector_store import VectorStore
    print("✅ VectorStore")
except ImportError as e:
    print(f"❌ VectorStore: {e}")

try:
    from knowledge_base.retriever import KnowledgeRetriever
    print("✅ KnowledgeRetriever")
except ImportError as e:
    print(f"❌ KnowledgeRetriever: {e}")

# Test 3: Try initializing retriever
print("\n3. Testing retriever initialization...")
try:
    from knowledge_base.retriever import KnowledgeRetriever
    
    # Change to the correct path
    kb_base_path = os.path.join(current_dir, "knowledge_base", "processed")
    retriever = KnowledgeRetriever(kb_base_path)
    
    available_agents = retriever.get_available_agents()
    print(f"✅ Available agents: {available_agents}")
    
    if available_agents:
        stats = retriever.get_knowledge_stats()
        for agent, stat in stats.items():
            chunk_count = stat.get('total_chunks', 0)
            print(f"  📚 {agent.title()}: {chunk_count} chunks")
        
        # Test a simple query
        print("\n4. Testing simple queries...")
        test_queries = {
            'athena': 'sexual harassment policy',
            'asha': 'maternity leave',
            'scribe': 'office memorandum'
        }
        
        for agent in available_agents:
            if agent in test_queries:
                query = test_queries[agent]
                print(f"\n🔍 Testing {agent.title()}: '{query}'")
                
                try:
                    results = retriever.retrieve_for_agent(agent, query, top_k=1)
                    if results:
                        result = results[0]
                        similarity = result.get('similarity', 0)
                        text_preview = result['text'][:150] + "..." if len(result['text']) > 150 else result['text']
                        print(f"✅ Found result (similarity: {similarity:.3f})")
                        print(f"📜 Preview: {text_preview}")
                    else:
                        print("❌ No results found")
                except Exception as e:
                    print(f"❌ Query failed: {e}")
    else:
        print("❌ No agents loaded")
        
except Exception as e:
    print(f"❌ Retriever initialization failed: {e}")
    import traceback
    traceback.print_exc()

print("\n🏁 Debug test complete!")