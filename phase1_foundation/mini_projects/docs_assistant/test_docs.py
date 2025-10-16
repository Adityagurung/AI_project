"""
Test Suite for Docs Assistant
Comprehensive testing with interactive mode
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from docs_assistant import DocsAssistant
from shared.config.settings import settings

def print_separator(char="=", length=60):
    """Print a visual separator"""
    print("\n" + char * length)

def test_document_loading():
    """Test 1: Load documents"""
    print_separator()
    print("TEST 1: Document Loading")
    print_separator()
    
    print("\n📚 Initializing Docs Assistant...")
    assistant = DocsAssistant()
    
    print("\n📂 Loading documents...")
    result = assistant.load_documents()
    
    print(f"\n✅ Loaded: {result['loaded']} documents")
    print(f"   Failed: {result['failed']}")
    print(f"\n📊 Summary:")
    for key, value in result['summary'].items():
        print(f"   {key}: {value}")
    
    print("\n✅ Document loading test complete!")
    return assistant

def test_list_documents(assistant):
    """Test 2: List all documents"""
    print_separator()
    print("TEST 2: List Documents")
    print_separator()
    
    docs = assistant.list_documents()
    
    print(f"\n📄 Found {len(docs)} documents:")
    for i, doc in enumerate(docs, 1):
        print(f"\n   {i}. {doc['filename']}")
        print(f"      Type: {doc['type']}")
        print(f"      Size: {doc['size_bytes']} bytes")
    
    print("\n✅ List documents test complete!")

def test_basic_questions(assistant):
    """Test 3: Ask basic questions"""
    print_separator()
    print("TEST 3: Basic Questions")
    print_separator()
    
    questions = [
        "What is this project about?",
        "How many phases are in the project?",
        "What is RAG and how does it work?",
        "What are some Python best practices?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 60)
        
        response = assistant.ask(question, top_k=3)
        
        print(f"\n💡 Answer:\n{response['answer']}")
        
        if response['sources']:
            print(f"\n📚 Sources ({response['num_sources']}):")
            for source in response['sources']:
                print(f"   - {source['filename']}")
    
    print("\n✅ Basic questions test complete!")

def test_document_filtering(assistant):
    """Test 4: Search with filtering"""
    print_separator()
    print("TEST 4: Document Type Filtering")
    print_separator()
    
    print("\n🔍 Searching only in text files...")
    results = assistant.search("RAG", top_k=3, doc_type='text')
    
    print(f"\n   Found {len(results)} results")
    for i, result in enumerate(results, 1):
        source = result.get('metadata', {}).get('source', 'Unknown')
        print(f"   {i}. From: {source}")
    
    print("\n✅ Filtering test complete!")

def test_document_summary(assistant):
    """Test 5: Summarize specific documents"""
    print_separator()
    print("TEST 5: Document Summarization")
    print_separator()
    
    # Get list of documents
    docs = assistant.list_documents()
    
    if docs:
        # Summarize first document
        first_doc = docs[0]['filename']
        print(f"\n📄 Summarizing: {first_doc}")
        print("-" * 60)
        
        result = assistant.summarize_document(first_doc)
        
        if result['success']:
            print(f"\n📝 Summary:\n{result['summary']}")
        else:
            print(f"\n❌ {result['summary']}")
    
    print("\n✅ Summarization test complete!")

def test_statistics(assistant):
    """Test 6: Get statistics"""
    print_separator()
    print("TEST 6: Statistics")
    print_separator()
    
    stats = assistant.get_stats()
    
    print(f"\n📊 Documents loaded: {stats['documents_loaded']}")
    print(f"\n📈 Document summary:")
    for key, value in stats['document_summary'].items():
        print(f"   {key}: {value}")
    
    print(f"\n📚 Available documents:")
    for doc in stats['available_documents']:
        print(f"   - {doc}")
    
    print("\n✅ Statistics test complete!")

def interactive_mode(assistant):
    """Interactive Q&A mode"""
    print_separator()
    print("INTERACTIVE MODE")
    print_separator()
    
    print("\n🤖 Docs Assistant ready! (Type 'quit' to exit)")
    print("\nCommands:")
    print("  quit      - Exit interactive mode")
    print("  list      - Show all documents")
    print("  summary <filename> - Summarize a document")
    print("  stats     - Show statistics")
    print("\nOr just ask a question about your documents!")
    
    while True:
        print("\n" + "-"*60)
        user_input = input("\n❓ You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("\n👋 Goodbye!")
            break
        
        if user_input.lower() == 'list':
            docs = assistant.list_documents()
            print("\n📄 Available documents:")
            for i, doc in enumerate(docs, 1):
                print(f"   {i}. {doc['filename']} ({doc['type']})")
            continue
        
        if user_input.lower().startswith('summary '):
            filename = user_input[8:].strip()
            print(f"\n📝 Generating summary for: {filename}")
            result = assistant.summarize_document(filename)
            print(f"\n{result['summary']}")
            continue
        
        if user_input.lower() == 'stats':
            stats = assistant.get_stats()
            print(f"\n📊 Statistics:")
            print(f"   Documents: {stats['documents_loaded']}")
            print(f"   Total size: {stats['document_summary']['total_size_mb']} MB")
            continue
        
        # Regular question
        response = assistant.ask(user_input)
        print(f"\n🤖 Assistant:\n{response['answer']}")
        
        if response['sources']:
            print(f"\n📚 Sources:")
            for source in response['sources']:
                print(f"   - {source['filename']}")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 TESTING DOCS ASSISTANT")
    print("="*60)
    
    # Validate settings
    try:
        settings.validate()
        print("✅ Settings validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    try:
        # Run all tests
        assistant = test_document_loading()
        test_list_documents(assistant)
        test_basic_questions(assistant)
        test_document_filtering(assistant)
        test_document_summary(assistant)
        test_statistics(assistant)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        
        # Ask if user wants interactive mode
        print("\n💬 Try interactive mode? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice == 'y':
            interactive_mode(assistant)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()