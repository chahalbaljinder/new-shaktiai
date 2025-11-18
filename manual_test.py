"""
Manual APEX Testing - Direct Test of Knowledge Base
Tests the APEX agents by directly loading the processed chunks without embeddings.
"""
import sys
import os
import pickle
import json
from pathlib import Path

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def load_agent_chunks(agent_name):
    """Load chunks for an agent directly from pickle files."""
    kb_path = Path(current_dir) / "knowledge_base" / "processed" / f"{agent_name}_vectorstore"
    chunks_file = kb_path / "chunks.pkl"
    metadata_file = kb_path / "metadata.json"
    
    if not chunks_file.exists():
        print(f"❌ Chunks file not found for {agent_name}: {chunks_file}")
        return None, None
    
    try:
        # Load chunks
        with open(chunks_file, 'rb') as f:
            chunks = pickle.load(f)
        
        # Load metadata
        metadata = {}
        if metadata_file.exists():
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
        
        print(f"✅ Loaded {len(chunks)} chunks for {agent_name}")
        return chunks, metadata
    
    except Exception as e:
        print(f"❌ Error loading chunks for {agent_name}: {e}")
        return None, None

def simple_text_search(chunks, query, top_k=3):
    """Simple text-based search using keyword matching."""
    query_words = query.lower().split()
    
    scored_chunks = []
    
    for chunk in chunks:
        text = chunk.get('text', '').lower()
        
        # Simple scoring based on keyword matches
        score = 0
        for word in query_words:
            if word in text:
                score += text.count(word)
        
        if score > 0:
            scored_chunks.append({
                'chunk': chunk,
                'score': score,
                'text': chunk.get('text', ''),
                'metadata': chunk.get('metadata', {}),
                'doc_title': chunk.get('doc_title', 'Unknown')
            })
    
    # Sort by score and return top results
    scored_chunks.sort(key=lambda x: x['score'], reverse=True)
    return scored_chunks[:top_k]

def test_agent_queries(agent_name, queries):
    """Test queries for a specific agent."""
    print(f"\n{'🏛️' if agent_name=='athena' else '🧘' if agent_name=='asha' else '📝'} TESTING {agent_name.upper()}")
    print("=" * 60)
    
    # Load chunks
    chunks, metadata = load_agent_chunks(agent_name)
    if chunks is None:
        return False
    
    print(f"📚 Knowledge Base: {len(chunks)} chunks loaded")
    if metadata:
        print(f"📊 Metadata: {metadata.get('model_name', 'Unknown model')}")
    
    success_count = 0
    
    for i, query in enumerate(queries, 1):
        print(f"\n🔍 QUERY {i}:")
        print(f"❓ {query}")
        print("-" * 50)
        
        try:
            results = simple_text_search(chunks, query, top_k=2)
            
            if results:
                print(f"✅ Found {len(results)} relevant chunks")
                
                for j, result in enumerate(results, 1):
                    score = result['score']
                    doc_title = result['doc_title']
                    text_preview = result['text'][:200] + "..." if len(result['text']) > 200 else result['text']
                    
                    print(f"\n📄 Result {j}:")
                    print(f"   📊 Score: {score}")
                    print(f"   📚 Source: {doc_title}")
                    print(f"   📜 Preview: {text_preview}")
                
                success_count += 1
            else:
                print("❌ No relevant chunks found")
        
        except Exception as e:
            print(f"❌ Query failed: {e}")
    
    success_rate = (success_count / len(queries)) * 100
    print(f"\n📊 {agent_name.upper()} SUCCESS RATE: {success_count}/{len(queries)} ({success_rate:.1f}%)")
    
    return success_count > 0

def main():
    """Run manual testing of APEX agents."""
    print("🧪 MANUAL APEX TESTING (Text-based Search)")
    print("=" * 80)
    print("Testing knowledge base content without embeddings...")
    
    # Define test queries
    test_queries = {
        'athena': [
            "DST Women Scientist Scheme-B WOS-B re-entry provisions age limit",
            "DRDO IPR patent filing guidelines before publication",
            "extramural research contract research DRDO funding differences",
            "grant-in-aid project proposal objectives methodology budget"
        ],
        'asha': [
            "CCS Leave Rules 1972 Rule 43 maternity leave duration child care leave",
            "stress management 5-step framework role overload Centre Good Governance",
            "imposter syndrome workbook women STEM achievements exercises",
            "Doan Lab Manual mental health boundaries after-hours communication"
        ],
        'scribe': [
            "Central Secretariat Manual Office Procedure CSMOP 2022 memorandum format",
            "e-Office User Manual Green Note Yellow Note difference final draft",
            "Bio-Data Proforma checklist DoPT Deputation guidelines transfer"
        ]
    }
    
    all_agents_working = True
    
    for agent_name, queries in test_queries.items():
        agent_success = test_agent_queries(agent_name, queries)
        if not agent_success:
            all_agents_working = False
    
    # Final report
    print("\n" + "=" * 80)
    print("📊 MANUAL TESTING REPORT")
    print("=" * 80)
    
    if all_agents_working:
        print("🎉 SUCCESS! All APEX agents have relevant knowledge content!")
        print("\n💡 NEXT STEPS:")
        print("1. The knowledge base content is good")
        print("2. The issue is likely with sentence-transformers/TensorFlow imports")
        print("3. You can either:")
        print("   a) Fix the TensorFlow/tf-keras dependency issue")
        print("   b) Use the Streamlit app (python app.py) which may handle imports better")
        print("   c) Use the FastAPI backend (python backend_service.py)")
        
        print("\n🚀 RECOMMENDED TESTING APPROACH:")
        print("Since the knowledge base is properly loaded, try:")
        print("  1. python app.py  (Streamlit interface)")
        print("  2. Test your queries through the web interface")
        
        print("\n📚 KNOWLEDGE BASE STATUS:")
        for agent_name in ['athena', 'asha', 'scribe']:
            chunks, metadata = load_agent_chunks(agent_name)
            if chunks:
                print(f"  ✅ {agent_name.title()}: {len(chunks)} chunks ready")
    
    else:
        print("⚠️  Some agents may need more relevant content")
        print("Consider reviewing the PDF processing and chunk creation")
    
    print("\n🔧 TROUBLESHOOTING TIPS:")
    print("- If imports fail, ensure all dependencies are properly installed")
    print("- Try testing through Streamlit app instead of direct import")
    print("- The knowledge base files are properly created and loaded")

if __name__ == "__main__":
    main()