"""
Test script for FAQ Assistant
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from phase1_foundation.mini_projects.faq_assistant.faq_assistant import FAQAssistant
from shared.config.settings import settings


def print_separator():
    """Print a visual separator"""
    print("\n" + "="*60)

def test_basic_questions():
    """Test 1: Basic FAQ questions"""
    print_separator()
    print("TEST 1: Basic FAQ Questions")
    print_separator()
    
    # Initialize assistant
    print("\n📚 Initializing FAQ Assistant...")
    assistant = FAQAssistant()
    
    # Test questions
    questions = [
        "What are the prerequisites for the AI course?",
        "How long does the course take?",
        "Do I need a GPU?"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n❓ Question {i}: {question}")
        print("-" * 60)
        
        response = assistant.ask(question)
        
        print(f"\n💡 Answer:\n{response['answer']}")
        
        if response.get('sources'):
            print(f"\n📚 Sources used: {response['num_sources']}")
    
    print("\n✅ Basic questions test complete!")

def test_conversation_memory():
    """Test 2: Conversation with context"""
    print_separator()
    print("TEST 2: Conversation Memory")
    print_separator()
    
    assistant = FAQAssistant()
    
    # Series of related questions
    conversation = [
        "What projects will I build in this course?",
        "Which one is the most advanced?",
        "How much time does that one take?"
    ]
    
    print("\n🗣️ Testing conversation flow with context...")
    
    for i, question in enumerate(conversation, 1):
        print(f"\n❓ Turn {i}: {question}")
        print("-" * 60)
        
        response = assistant.ask(question, include_sources=False)
        print(f"\n💡 Answer:\n{response['answer'][:300]}...")
    
    # Show conversation history
    print("\n📜 Conversation History:")
    history = assistant.get_conversation_history()
    print(f"   Total turns: {len(history)}")
    
    print("\n✅ Conversation memory test complete!")

def test_follow_up_questions():
    """Test 3: Follow-up questions"""
    print_separator()
    print("TEST 3: Follow-up Questions")
    print_separator()
    
    assistant = FAQAssistant()
    
    # Initial question and follow-ups
    print("\n❓ Initial: Tell me about the certification")
    response1 = assistant.ask("Tell me about the certification")
    print(f"\n💡 Answer:\n{response1['answer']}")
    
    print("\n❓ Follow-up: What do I need to complete to get it?")
    response2 = assistant.ask("What do I need to complete to get it?")
    print(f"\n💡 Answer:\n{response2['answer']}")
    
    print("\n✅ Follow-up questions test complete!")

def test_unknown_questions():
    """Test 4: Questions without FAQ answers"""
    print_separator()
    print("TEST 4: Unknown Questions")
    print_separator()
    
    assistant = FAQAssistant()
    
    unknown_questions = [
        "What's the weather like today?",
        "Who won the world cup?"
    ]
    
    for question in unknown_questions:
        print(f"\n❓ Question: {question}")
        response = assistant.ask(question, include_sources=False)
        print(f"\n💡 Answer:\n{response['answer']}")
    
    print("\n✅ Unknown questions test complete!")

def interactive_mode():
    """Interactive chat mode"""
    print_separator()
    print("INTERACTIVE MODE")
    print_separator()
    
    assistant = FAQAssistant()
    
    print("\n🤖 FAQ Assistant is ready! (Type 'quit' to exit, 'reset' to clear history)")
    print("\nTry asking:")
    print("  - What are the prerequisites?")
    print("  - How much does it cost?")
    print("  - What tools do I need?")
    
    while True:
        print("\n" + "-"*60)
        user_input = input("\n❓ You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("\n👋 Goodbye!")
            break
        
        if user_input.lower() == 'reset':
            assistant.reset_conversation()
            print("✅ Conversation history cleared!")
            continue
        
        if user_input.lower() == 'stats':
            stats = assistant.get_stats()
            print("\n📊 Statistics:")
            print(f"   Conversation turns: {stats['conversation_stats']['total_turns']}")
            print(f"   FAQs in database: {stats['rag_stats'].get('points_count', 'N/A')}")
            continue
        
        response = assistant.ask(user_input)
        print(f"\n🤖 Assistant:\n{response['answer']}")
        
        if response.get('sources'):
            print(f"\n📚 (Used {response['num_sources']} FAQ sources)")

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("🚀 TESTING FAQ ASSISTANT")
    print("="*60)
    
    # Validate settings
    try:
        settings.validate()
        print("✅ Settings validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    try:
        # Run automated tests
        test_basic_questions()
        test_conversation_memory()
        test_follow_up_questions()
        test_unknown_questions()
        
        print("\n" + "="*60)
        print("✅ ALL AUTOMATED TESTS PASSED!")
        print("="*60)
        
        # Ask if user wants interactive mode
        print("\n💬 Would you like to try interactive mode? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice == 'y':
            interactive_mode()
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()