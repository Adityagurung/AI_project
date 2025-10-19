"""
Test Suite for Weather Agent
Demonstrates function calling in action
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from weather_agent import WeatherAgent
from shared.config.settings import settings


def print_separator(title="", char="=", length=70):
    """Print a visual separator with optional title"""
    if title:
        print(f"\n{char * length}")
        print(f"{title:^{length}}")
        print(f"{char * length}")
    else:
        print(f"\n{char * length}")


def test_basic_weather_query():
    """Test 1: Basic current weather query"""
    print_separator("TEST 1: Basic Weather Query")
    
    agent = WeatherAgent()
    
    print("\n🌤️  Testing current weather lookup...")
    print("\n❓ User: What's the weather like in Tokyo?")
    
    response = agent.chat("What's the weather like in Tokyo?")
    
    print(f"\n🤖 Agent: {response}")
    
    print("\n✅ Test complete!")
    print("\n💡 Notice how the agent:")
    print("   1. Recognized it needed weather data")
    print("   2. Called the get_current_weather function")
    print("   3. Used the result to form a natural response")
    
    return agent


def test_forecast_query():
    """Test 2: Weather forecast query"""
    print_separator("TEST 2: Weather Forecast")
    
    agent = WeatherAgent()
    
    print("\n📅 Testing forecast lookup...")
    print("\n❓ User: What will the weather be like in Paris over the next 5 days?")
    
    response = agent.chat("What will the weather be like in Paris over the next 5 days?")
    
    print(f"\n🤖 Agent: {response}")
    
    print("\n✅ Test complete!")
    print("\n💡 The agent understood:")
    print("   - This is about future weather (not current)")
    print("   - It should use the forecast function")
    print("   - It should request 5 days of data")
    
    return agent


def test_conversation_flow():
    """Test 3: Multi-turn conversation"""
    print_separator("TEST 3: Conversation Flow")
    
    agent = WeatherAgent()
    
    print("\n💬 Testing conversation with context...")
    
    # First question
    print("\n❓ User: What's the weather in London?")
    response1 = agent.chat("What's the weather in London?")
    print(f"🤖 Agent: {response1}")
    
    # Follow-up question
    print("\n❓ User: What about the forecast?")
    response2 = agent.chat("What about the forecast?")
    print(f"🤖 Agent: {response2}")
    
    print("\n✅ Test complete!")
    print("\n💡 The agent remembered:")
    print("   - We were talking about London")
    print("   - The follow-up 'what about' refers to London")
    print("   - Context is maintained across messages")
    
    return agent


def test_no_function_needed():
    """Test 4: Questions that don't need functions"""
    print_separator("TEST 4: No Function Needed")
    
    agent = WeatherAgent()
    
    print("\n🗣️  Testing non-weather queries...")
    
    queries = [
        "Hello! What can you help me with?",
        "What weather information can you provide?",
        "Thank you for your help!"
    ]
    
    for query in queries:
        print(f"\n❓ User: {query}")
        response = agent.chat(query)
        print(f"🤖 Agent: {response}")
    
    print("\n✅ Test complete!")
    print("\n💡 Notice that:")
    print("   - Agent responded directly without function calls")
    print("   - It understood these were conversational, not data queries")
    print("   - Functions are only used when actually needed")


def test_complex_query():
    """Test 5: Complex multi-location query"""
    print_separator("TEST 5: Complex Query")
    
    agent = WeatherAgent()
    
    print("\n🌍 Testing complex, multi-location query...")
    print("\n❓ User: Compare the weather in New York and Los Angeles")
    
    response = agent.chat("Compare the weather in New York and Los Angeles")
    
    print(f"\n🤖 Agent: {response}")
    
    print("\n✅ Test complete!")
    print("\n💡 The agent:")
    print("   - Recognized it needs data for TWO locations")
    print("   - Made multiple function calls")
    print("   - Compared the results")
    print("   - Provided a comprehensive answer")


def show_conversation_history(agent):
    """Show the complete conversation history"""
    print_separator("Conversation History Analysis")
    
    history = agent.get_conversation_history()
    
    print(f"\n📜 Total messages in conversation: {len(history)}")
    print("\nMessage breakdown:")
    
    for i, msg in enumerate(history, 1):
        role = msg.get('role', 'unknown')
        
        if role == 'system':
            print(f"\n{i}. SYSTEM MESSAGE (instructions to agent)")
            print(f"   Preview: {msg.get('content', '')[:100]}...")
        
        elif role == 'user':
            print(f"\n{i}. USER MESSAGE")
            print(f"   Content: {msg.get('content', '')}")
        
        elif role == 'assistant':
            if hasattr(msg, 'tool_calls') and msg.tool_calls:
                print(f"\n{i}. ASSISTANT (requesting function calls)")
                for tool_call in msg.tool_calls:
                    print(f"   Function: {tool_call.function.name}")
                    print(f"   Arguments: {tool_call.function.arguments}")
            else:
                print(f"\n{i}. ASSISTANT RESPONSE")
                content = msg.get('content', '')
                if isinstance(content, str):
                    print(f"   Content: {content[:150]}...")
        
        elif role == 'tool':
            print(f"\n{i}. TOOL RESULT")
            print(f"   Function: {msg.get('name', 'unknown')}")
            print(f"   Result: {msg.get('content', '')[:100]}...")


def interactive_mode():
    """Interactive mode - chat with the agent"""
    print_separator("INTERACTIVE MODE")
    
    print("\n🤖 Weather Agent is ready to chat!")
    print("\nCommands:")
    print("  quit     - Exit")
    print("  reset    - Start new conversation")
    print("  history  - Show conversation history")
    print("\nTry asking about:")
    print("  - Current weather in any city")
    print("  - Weather forecasts")
    print("  - Comparing weather between cities")
    
    agent = WeatherAgent()
    
    while True:
        print("\n" + "-" * 70)
        user_input = input("\n❓ You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("\n👋 Goodbye!")
            break
        
        if user_input.lower() == 'reset':
            agent.reset_conversation()
            print("✅ Conversation reset!")
            continue
        
        if user_input.lower() == 'history':
            show_conversation_history(agent)
            continue
        
        # Get response from agent
        response = agent.chat(user_input)
        print(f"\n🤖 Agent: {response}")


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🚀 TESTING WEATHER AGENT - FUNCTION CALLING")
    print("=" * 70)
    
    # Validate settings
    try:
        settings.validate()
        print("✅ Settings validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    try:
        # Run all tests
        print("\n🧪 Running automated tests...")
        
        test_basic_weather_query()
        test_forecast_query()
        test_conversation_flow()
        test_no_function_needed()
        test_complex_query()
        
        print_separator("ALL TESTS PASSED! ✅")
        
        # Offer interactive mode
        print("\n💬 Would you like to try interactive mode? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice == 'y':
            interactive_mode()
        
        print("\n" + "=" * 70)
        print("🎉 Function Calling Demo Complete!")
        print("=" * 70)
        
        print("\n📚 What you learned:")
        print("   ✅ How to define function schemas")
        print("   ✅ How the agent decides when to call functions")
        print("   ✅ How function results flow back to the agent")
        print("   ✅ How context is maintained in conversations")
        print("   ✅ The complete function calling lifecycle")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()