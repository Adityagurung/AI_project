"""
Test script for the RAG pipeline.
Run this to verify everything is working correctly.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from rag_pipeline.retriever import RAGRetriever
from shared.config.settings import settings
from shared.utils.logger import logger

def test_basic_ingestion():
    """Test 1: Ingest sample documents"""
    print("\n" + "="*50)
    print("TEST 1: Document Ingestion")
    print("="*50)
    
    # Sample documents about AI
    sample_docs = [
        {
            'text': """Artificial Intelligence (AI) is the simulation of human intelligence by machines. 
            It involves creating systems that can perform tasks that typically require human intelligence, 
            such as visual perception, speech recognition, decision-making, and language translation. 
            AI can be categorized into narrow AI, which is designed for specific tasks, and general AI, 
            which would have human-like cognitive abilities.""",
            'metadata': {'source': 'AI Basics', 'topic': 'Introduction'}
        },
        {
            'text': """Machine Learning is a subset of AI that enables systems to learn and improve from 
            experience without being explicitly programmed. It focuses on the development of computer programs 
            that can access data and use it to learn for themselves. The process includes training a model 
            on a dataset and then using that model to make predictions or decisions.""",
            'metadata': {'source': 'ML Guide', 'topic': 'Machine Learning'}
        },
        {
            'text': """Retrieval-Augmented Generation (RAG) is a technique that combines retrieval-based 
            approaches with generative AI models. It works by first retrieving relevant documents from a 
            knowledge base, then using those documents as context for a language model to generate responses. 
            This approach helps reduce hallucinations and provides more accurate, grounded answers.""",
            'metadata': {'source': 'RAG Tutorial', 'topic': 'RAG'}
        }
    ]
    
    # Initialize RAG system
    rag = RAGRetriever()
    
    # Ingest documents
    texts = [doc['text'] for doc in sample_docs]
    metadata = [doc['metadata'] for doc in sample_docs]
    
    rag.ingest_documents(texts=texts, metadata=metadata)
    
    # Check stats
    stats = rag.get_stats()
    print(f"\n✅ Ingestion complete!")
    print(f"   - Points in collection: {stats.get('points_count', 0)}")
    print(f"   - Collection status: {stats.get('status', 'unknown')}")
    
    return rag

def test_retrieval(rag):
    """Test 2: Retrieve relevant documents"""
    print("\n" + "="*50)
    print("TEST 2: Document Retrieval")
    print("="*50)
    
    query = "What is machine learning?"
    print(f"\nQuery: '{query}'")
    
    results = rag.retrieve(query, top_k=2)
    
    print(f"\n✅ Retrieved {len(results)} documents:")
    for i, result in enumerate(results, 1):
        print(f"\n   Document {i} (Score: {result['score']:.3f}):")
        print(f"   {result['text'][:100]}...")
        print(f"   Source: {result['metadata'].get('source', 'Unknown')}")

def test_rag_query(rag):
    """Test 3: Complete RAG query"""
    print("\n" + "="*50)
    print("TEST 3: Complete RAG Query")
    print("="*50)
    
    questions = [
        "What is Retrieval-Augmented Generation?",
        "Explain the difference between narrow AI and general AI",
        "How does machine learning work?"
    ]
    
    for question in questions:
        print(f"\n📝 Question: {question}")
        print("-" * 50)
        
        result = rag.query(question, top_k=3)
        
        print(f"\n💡 Answer:\n{result['answer']}")
        print(f"\n📚 Used {result['num_sources']} sources")

def test_metadata_filtering(rag):
    """Test 4: Metadata filtering"""
    print("\n" + "="*50)
    print("TEST 4: Metadata Filtering")
    print("="*50)
    
    query = "Tell me about AI"
    metadata_filter = {'topic': 'Machine Learning'}
    
    print(f"\nQuery: '{query}'")
    print(f"Filter: {metadata_filter}")
    
    results = rag.retrieve(query, top_k=2, metadata_filter=metadata_filter)
    
    print(f"\n✅ Retrieved {len(results)} documents with filter:")
    for i, result in enumerate(results, 1):
        print(f"\n   Document {i}:")
        print(f"   Topic: {result['metadata'].get('topic', 'Unknown')}")
        print(f"   {result['text'][:80]}...")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 TESTING RAG PIPELINE")
    print("="*60)
    
    # Validate settings
    try:
        settings.validate()
        print("✅ Settings validated successfully")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\n⚠️  Please check your .env file and set OPENAI_API_KEY")
        return
    
    try:
        # Run tests
        rag = test_basic_ingestion()
        test_retrieval(rag)
        test_rag_query(rag)
        test_metadata_filtering(rag)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\n🎉 Your RAG pipeline is working correctly!")
        print("📝 Next steps:")
        print("   1. Try adding your own documents")
        print("   2. Experiment with different queries")
        print("   3. Move on to Day 2: Building mini-projects")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {str(e)}")
        logger.exception("Test failed")

if __name__ == "__main__":
    main()