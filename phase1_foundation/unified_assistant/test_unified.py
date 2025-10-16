"""
Test Suite for Unified Assistant
Comprehensive testing with interactive demo
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from assistant_manager import UnifiedAssistantManager
from shared.config.settings import settings

def print_separator(char="=", length=70):
    """Print a visual separator"""
    print("\n" + char * length)

def test_initialization():
    """Test 1: Initialize the manager"""
    print_separator()
    print("TEST 1: Initialization")
    print_separator()
    
    print("\n🚀 Initializing Unified Assistant Manager...")
    manager = UnifiedAssistantManager()
    
    print("\n✅ Manager initialized!")
    
    # Check status
    status = manager.get_status()
    print("\n📊 Assistant Status:")
    for name, info in status.items():
        if isinstance(info, dict):
            available = "✅" if info.get('available', False) else "❌"
            print(f"   {available} {name}: {info.get('status', 'unknown')}")
    
    return manager

def test_faq_assistant(manager):
    """Test 2: FAQ Assistant functionality"""
    print_separator()
    print("TEST 2: FAQ Assistant")
    print_separator()
    
    questions = [
        "What are the prerequisites for this course?",
        "How long does the course take?",
        "Do I need a GPU?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 70)
        
        response = manager.ask_faq(question)
        
        print(f"\n💡 Answer:\n{response['answer'][:300]}...")
        
        if response.get('sources'):
            print(f"\n📚 Used {response.get('num_sources', 0)} FAQ sources")
    
    print("\n✅ FAQ Assistant test complete!")

def test_docs_assistant(manager):
    """Test 3: Docs Assistant functionality"""
    print_separator()
    print("TEST 3: Docs Assistant")
    print_separator()
    
    # List documents
    print("\n📄 Available documents:")
    docs = manager.list_available_documents()
    for i, doc in enumerate(docs, 1):
        print(f"   {i}. {doc['filename']} ({doc['type']})")
    
    # Search documents
    print("\n🔍 Searching documents...")
    queries = [
        "What is RAG?",
        "What are Python best practices?",
        "How many phases are in the project?"
    ]
    
    for query in queries:
        print(f"\n❓ Query: {query}")
        response = manager.search_documents(query, top_k=2)
        print(f"💡 Answer: {response['answer'][:200]}...")
        
        if response.get('sources'):
            sources = [s['filename'] for s in response['sources']]
            print(f"📚 Sources: {', '.join(sources)}")
    
    print("\n✅ Docs Assistant test complete!")

def test_youtube_summarizer(manager):
    """Test 4: YouTube Summarizer functionality"""
    print_separator()
    print("TEST 4: YouTube Summarizer")
    print_separator()
    
    # List available videos
    print("\n📹 Available videos:")
    manager.list_available_videos()
    
    # Summarize a video
    print("\n📊 Summarizing 'procrastination' video...")
    result = manager.summarize_video('procrastination', 'brief')
    
    if not result.get('error'):
        print(f"\n📹 Title: {result.get('title', 'Unknown')}")
        print(f"⏱️  Duration: {result.get('duration', 0)} seconds")
        print(f"\n📄 Summary:\n{result['summary'][:400]}...")
        
        # Ask a question about the video
        print("\n❓ Asking about the video...")
        question = "What is the main topic?"
        answer = manager.ask_about_video(question)
        print(f"Question: {question}")
        print(f"💡 Answer: {answer['answer'][:200]}...")
    
    print("\n✅ YouTube Summarizer test complete!")

def test_auto_routing(manager):
    """Test 5: Auto-routing functionality"""
    print_separator()
    print("TEST 5: Auto-Routing")
    print_separator()
    
    test_queries = [
        "What are the course prerequisites?",  # Should route to FAQ
        "Tell me about RAG",                    # Should route to Docs
        "What are Python best practices?"       # Should route to Docs
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        response = manager.auto_route(query)
        
        assistant_type = response.get('assistant_type', 'unknown')
        print(f"   Routed to: {assistant_type}")
        print(f"   Answer: {response.get('answer', '')[:150]}...")
    
    print("\n✅ Auto-routing test complete!")

def test_statistics(manager):
    """Test 6: Get combined statistics"""
    print_separator()
    print("TEST 6: Statistics")
    print_separator()
    
    stats = manager.get_combined_stats()
    
    print("\n📊 Manager Stats:")
    if 'manager' in stats:
        print(f"   Assistants available: {stats['manager']['assistants_available']}/3")
    
    print("\n📈 FAQ Stats:")
    if 'faq' in stats:
        conv_stats = stats['faq'].get('conversation_stats', {})
        print(f"   Conversation turns: {conv_stats.get('total_turns', 0)}")
    
    print("\n📚 Docs Stats:")
    if 'docs' in stats:
        print(f"   Documents loaded: {stats['docs'].get('documents_loaded', 0)}")
    
    print("\n✅ Statistics test complete!")

def interactive_demo(manager):
    """Interactive demo mode"""
    print_separator()
    print("INTERACTIVE DEMO MODE")
    print_separator()
    
    print("\n🤖 Unified AI Assistant Ready!")
    print("\n" + manager.help())
    
    print("\nType 'help' to see commands again")
    print("Type 'quit' to exit")
    
    while True:
        print("\n" + "-"*70)
        user_input = input("\n💬 You: ").strip()
        
        if not user_input:
            continue
        
        cmd_lower = user_input.lower()
        
        # Command handling
        if cmd_lower == 'quit':
            print("\n👋 Goodbye!")
            break
        
        if cmd_lower == 'help':
            print(manager.help())
            continue
        
        if cmd_lower == 'status':
            status = manager.get_status()
            print("\n📊 Status:")
            for name, info in status.items():
                if isinstance(info, dict):
                    print(f"   {name}: {info}")
            continue
        
        if cmd_lower == 'stats':
            stats = manager.get_combined_stats()
            print("\n📈 Statistics:")
            for key, value in stats.items():
                print(f"   {key}: {value}")
            continue
        
        if cmd_lower.startswith('switch '):
            assistant_type = cmd_lower[7:].strip()
            result = manager.switch_assistant(assistant_type)
            print(f"\n{result['message']}")
            continue
        
        if cmd_lower == 'list docs' or cmd_lower == 'list documents':
            docs = manager.list_available_documents()
            print("\n📄 Available documents:")
            for doc in docs:
                print(f"   - {doc['filename']}")
            continue
        
        if cmd_lower == 'list videos':
            manager.list_available_videos()
            continue
        
        if cmd_lower.startswith('summarize '):
            video_key = cmd_lower[10:].strip()
            print(f"\n⏳ Summarizing '{video_key}'...")
            result = manager.summarize_video(video_key)
            if not result.get('error'):
                print(f"\n📄 Summary:\n{result['summary']}")
            else:
                print(f"\n❌ {result['summary']}")
            continue
        
        # Default: use auto-routing
        print("\n⏳ Processing...")
        response = manager.auto_route(user_input)
        
        assistant = response.get('assistant_type', 'unknown')
        print(f"\n🤖 [{assistant.upper()}] Assistant:")
        print(response.get('answer', response.get('summary', 'No response')))
        
        if response.get('sources'):
            print(f"\n📚 Sources:")
            for source in response['sources'][:3]:
                print(f"   - {source.get('filename', 'Unknown')}")

def main():
    """Run all tests"""
    print("\n" + "="*70)
    print("🚀 TESTING UNIFIED AI ASSISTANT")
    print("="*70)
    
    # Validate settings
    try:
        settings.validate()
        print("✅ Settings validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    try:
        # Run all tests
        manager = test_initialization()
        test_faq_assistant(manager)
        test_docs_assistant(manager)
        test_youtube_summarizer(manager)
        test_auto_routing(manager)
        test_statistics(manager)
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        
        # Offer interactive mode
        print("\n🎮 Try interactive demo? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice == 'y':
            interactive_demo(manager)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()