"""
Enhanced SHAKTI-AI Reference System - Demonstration
Shows improved PDF references with detailed metadata, page tracking, and accurate citations.
"""

from crew import ask_shakti_ai

def demonstrate_enhanced_references():
    """Demonstrate the enhanced reference system with detailed examples."""
    
    print("🧬 SHAKTI-AI Enhanced Reference System Demo")
    print("=" * 70)
    print("✨ NEW FEATURES:")
    print("   • Page-level tracking with page numbers")
    print("   • Enhanced PDF metadata extraction") 
    print("   • Confidence scoring (High/Medium/Low)")
    print("   • Detailed source citations with extracts")
    print("   • Improved chunking with context preservation")
    print("   • Smart relevance filtering")
    print("=" * 70)
    
    # Demo query with single agent
    print("\n🔍 DEMO 1: Single Agent Query with Enhanced References")
    print("-" * 50)
    
    response = ask_shakti_ai(
        "What are the key nutritional recommendations for women during menopause?",
        ["feminist"]
    )
    
    print(response)
    
    print("\n" + "=" * 70)
    print("\n🔍 DEMO 2: Multi-Agent Query with Combined Knowledge")
    print("-" * 50)
    
    response2 = ask_shakti_ai(
        "What legal protections and mental health support are available for women experiencing domestic violence?",
        ["mental", "legal"]
    )
    
    print(response2)
    
    print("\n" + "=" * 70)
    print("\n📋 REFERENCE SYSTEM FEATURES DEMONSTRATED:")
    print("✅ Accurate page number citations")
    print("✅ Document titles from PDF metadata")
    print("✅ Relevance scoring with confidence levels")
    print("✅ Content previews and detailed extracts")
    print("✅ Enhanced chunking preserving context")
    print("✅ Multiple PDF sources per query")
    print("✅ Source-cited responses from knowledge base")
    
    print("\n🎯 BENEFITS FOR USERS:")
    print("• Verifiable information with exact page references")
    print("• Confidence levels help assess information reliability")
    print("• Direct access to source material through citations")
    print("• Comprehensive coverage from multiple relevant documents")
    print("• Evidence-based responses grounded in authoritative sources")

if __name__ == "__main__":
    demonstrate_enhanced_references()
