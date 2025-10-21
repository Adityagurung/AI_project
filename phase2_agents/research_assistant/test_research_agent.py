"""
Test Suite for Research Assistant Agent
Comprehensive testing of database query capabilities

This test suite demonstrates progressively more sophisticated agent behaviors:
1. Simple single-query questions
2. Questions requiring data interpretation
3. Questions requiring multiple queries
4. Complex analytical questions requiring reasoning

Each test is designed to show you a different aspect of how the agent
thinks about and analyzes business data.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from research_agent import ResearchAgent
from shared.config.settings import settings


def print_separator(title="", char="=", length=70):
    """Print a visual separator with optional title"""
    if title:
        print(f"\n{char * length}")
        print(f"{title:^{length}}")
        print(f"{char * length}")
    else:
        print(f"\n{char * length}")


def test_simple_customer_lookup():
    """
    Test 1: Simple customer lookup by email
    
    This is the simplest type of query - a direct lookup of a specific
    record. The agent needs to recognize that it should use the
    get_customer_by_email function and pass the email address.
    """
    print_separator("TEST 1: Simple Customer Lookup")
    
    agent = ResearchAgent()
    
    print("\n📧 Testing customer lookup by email...")
    print("\n❓ Question: What can you tell me about customer alice@email.com?")
    
    response = agent.ask("What can you tell me about customer alice@email.com?")
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent recognized this requires customer data")
    print("   - Called get_customer_by_email with the email address")
    print("   - Interpreted the results in a conversational way")
    
    return agent


def test_top_customers_analysis():
    """
    Test 2: Top customers analysis
    
    This requires the agent to understand that "best customers" or
    "top customers" means ranking by total spending. It also needs
    to interpret the results meaningfully - not just list numbers
    but provide business context.
    """
    print_separator("TEST 2: Top Customers Analysis")
    
    agent = ResearchAgent()
    
    print("\n🏆 Testing top customers analysis...")
    print("\n❓ Question: Who are our top 3 customers and how much have they spent?")
    
    response = agent.ask("Who are our top 3 customers and how much have they spent?")
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent understood 'top customers' means highest spending")
    print("   - Called get_top_customers with limit=3")
    print("   - Presented data in a clear, ranked format")
    
    return agent


def test_inventory_concern():
    """
    Test 3: Inventory status check
    
    This tests whether the agent can assess a business concern. When
    asked about inventory risks, the agent needs to query low stock
    items and then interpret whether those levels are actually concerning.
    """
    print_separator("TEST 3: Inventory Concern Analysis")
    
    agent = ResearchAgent()
    
    print("\n📦 Testing inventory risk assessment...")
    print("\n❓ Question: Are we at risk of running out of any products?")
    
    response = agent.ask("Are we at risk of running out of any products?")
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent recognized this is about inventory levels")
    print("   - Called get_low_stock_products to check inventory")
    print("   - Interpreted the results as potential business risks")
    print("   - Provided actionable insights, not just raw data")
    
    return agent


def test_revenue_analysis():
    """
    Test 4: Revenue and performance analysis
    
    Financial questions require the agent to understand business metrics
    like revenue, order count, and average order value. The agent should
    provide context about what these numbers mean.
    """
    print_separator("TEST 4: Revenue Analysis")
    
    agent = ResearchAgent()
    
    print("\n💰 Testing revenue analysis...")
    print("\n❓ Question: How much revenue have we generated in the last 30 days?")
    
    response = agent.ask("How much revenue have we generated in the last 30 days?")
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent understood this requires revenue calculation")
    print("   - Called get_total_revenue with appropriate time filter")
    print("   - Presented financial metrics with business context")
    
    return agent


def test_multi_query_analysis():
    """
    Test 5: Question requiring multiple queries
    
    This is where the agent's reasoning really shines. Some questions
    cannot be answered with a single query. The agent needs to recognize
    this and chain multiple queries together, using information from
    one query to inform the next.
    """
    print_separator("TEST 5: Multi-Query Analysis")
    
    agent = ResearchAgent()
    
    print("\n🔗 Testing multi-step reasoning...")
    print("\n❓ Question: What has alice@email.com ordered and what was her total spending?")
    
    response = agent.ask("What has alice@email.com ordered and what was her total spending?")
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent needed both customer info and order history")
    print("   - Made multiple database queries")
    print("   - Synthesized information from different sources")
    print("   - Provided comprehensive answer combining all data")
    
    return agent


def test_category_analysis():
    """
    Test 6: Product category analysis
    
    This tests the agent's ability to work with categorical data and
    provide insights about specific product segments.
    """
    print_separator("TEST 6: Category Analysis")
    
    agent = ResearchAgent()
    
    print("\n📱 Testing category-based queries...")
    print("\n❓ Question: Show me all our Electronics products and their prices")
    
    response = agent.ask("Show me all our Electronics products and their prices")
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent recognized this requires filtering by category")
    print("   - Called get_products_by_category")
    print("   - Organized results in a useful format")
    
    return agent


def test_recent_activity():
    """
    Test 7: Recent activity analysis
    
    Time-based queries require the agent to understand temporal
    concepts and filter data appropriately.
    """
    print_separator("TEST 7: Recent Activity")
    
    agent = ResearchAgent()
    
    print("\n📅 Testing time-based analysis...")
    print("\n❓ Question: What orders have we received in the last week?")
    
    response = agent.ask("What orders have we received in the last week?")
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent understood 'last week' as a time filter")
    print("   - Called get_recent_orders with appropriate days parameter")
    print("   - Presented recent transaction activity")
    
    return agent


def test_complex_business_question():
    """
    Test 8: Complex analytical question
    
    This is the most sophisticated test. The agent needs to understand
    a complex, open-ended business question and figure out what data
    would be relevant to answer it comprehensively. It may need to
    make multiple queries and reason about the relationships between
    different data points.
    """
    print_separator("TEST 8: Complex Business Analysis")
    
    agent = ResearchAgent()
    
    print("\n🎯 Testing complex analytical reasoning...")
    print("\n❓ Question: Give me an overview of business performance - revenue, ")
    print("   top customers, and any inventory concerns I should know about")
    
    response = agent.ask(
        "Give me an overview of business performance - revenue, top customers, "
        "and any inventory concerns I should know about"
    )
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent broke down complex question into components")
    print("   - Made multiple strategic queries (revenue, customers, inventory)")
    print("   - Synthesized data from different sources")
    print("   - Provided comprehensive business insights")
    print("   - Highlighted important patterns or concerns")
    
    return agent


def test_conversation_context():
    """
    Test 9: Conversation with context
    
    This tests whether the agent maintains context across multiple
    questions in a conversation. Follow-up questions should work
    naturally without repeating all the context.
    """
    print_separator("TEST 9: Conversational Context")
    
    agent = ResearchAgent()
    
    print("\n💬 Testing conversation with context...")
    
    # First question
    print("\n❓ Question 1: Who is our top customer?")
    response1 = agent.ask("Who is our top customer?")
    print(f"\n🤖 Agent: {response1}")
    
    # Follow-up question that relies on context
    print("\n❓ Question 2: What have they ordered?")
    response2 = agent.ask("What have they ordered?")
    print(f"\n🤖 Agent: {response2}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Agent remembered the top customer from first question")
    print("   - Understood 'they' refers to that customer")
    print("   - Retrieved order history for the right customer")
    print("   - Context maintained across conversation turns")
    
    return agent


def test_business_health_method():
    """
    Test 10: Using the convenience method
    
    This demonstrates the specialized analyze_business_health method
    which encapsulates a common comprehensive analysis request.
    """
    print_separator("TEST 10: Business Health Analysis Method")
    
    agent = ResearchAgent()
    
    print("\n🏥 Testing business health analysis convenience method...")
    print("\n📊 Calling: agent.analyze_business_health()")
    
    response = agent.analyze_business_health()
    
    print(f"\n🤖 Agent Response:\n{response}")
    
    print("\n✅ Test complete!")
    print("\n💡 What happened:")
    print("   - Used high-level convenience method")
    print("   - Agent performed comprehensive multi-query analysis")
    print("   - Provided complete business health overview")
    print("   - Demonstrated value of abstraction for common tasks")


def interactive_mode():
    """
    Interactive mode - ask your own questions to the research agent
    
    This lets you experiment freely with the agent and see how it
    handles different types of business questions. Try to think of
    questions that would require different query strategies and see
    how the agent reasons through them.
    """
    print_separator("INTERACTIVE MODE")
    
    print("\n🤖 Research Assistant is ready!")
    print("\nYou can ask questions about:")
    print("  • Customers (who are they, what have they bought)")
    print("  • Products (what do we sell, inventory levels, categories)")
    print("  • Orders (recent activity, order history)")
    print("  • Revenue (financial performance, trends)")
    print("  • Business health (comprehensive overviews)")
    
    print("\nCommands:")
    print("  quit     - Exit interactive mode")
    print("  reset    - Start new conversation")
    print("  health   - Run business health analysis")
    
    print("\nTry asking complex questions that require multiple queries!")
    print("For example:")
    print("  - Which Electronics products are low in stock?")
    print("  - How much revenue did we make last month?")
    print("  - What is the order history for bob@email.com?")
    print("  - Are any of our top customers inactive?")
    
    agent = ResearchAgent()
    
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
            print("\n✅ Conversation reset! Starting fresh.")
            continue
        
        if user_input.lower() == 'health':
            print("\n⏳ Analyzing business health...")
            response = agent.analyze_business_health()
            print(f"\n🤖 Agent:\n{response}")
            continue
        
        # Regular question
        print("\n⏳ Analyzing your question...")
        response = agent.ask(user_input)
        print(f"\n🤖 Agent:\n{response}")


def main():
    """
    Run all tests in sequence
    
    This test suite is designed to be educational. Each test builds on
    the previous ones, showing you progressively more sophisticated
    agent capabilities. Watch how the agent reasons through different
    types of business questions.
    """
    print("\n" + "="*70)
    print("🚀 TESTING RESEARCH ASSISTANT AGENT")
    print("="*70)
    
    # Validate settings
    try:
        settings.validate()
        print("✅ Settings validated")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    print("\n📚 This test suite demonstrates:")
    print("   • Simple database lookups")
    print("   • Data interpretation and analysis")
    print("   • Multi-query reasoning")
    print("   • Complex business analysis")
    print("   • Conversational context")
    
    try:
        # Run all automated tests
        print("\n🧪 Running automated tests...\n")
        
        test_simple_customer_lookup()
        input("\nPress Enter to continue to next test...")
        
        test_top_customers_analysis()
        input("\nPress Enter to continue to next test...")
        
        test_inventory_concern()
        input("\nPress Enter to continue to next test...")
        
        test_revenue_analysis()
        input("\nPress Enter to continue to next test...")
        
        test_multi_query_analysis()
        input("\nPress Enter to continue to next test...")
        
        test_category_analysis()
        input("\nPress Enter to continue to next test...")
        
        test_recent_activity()
        input("\nPress Enter to continue to next test...")
        
        test_complex_business_question()
        input("\nPress Enter to continue to next test...")
        
        test_conversation_context()
        input("\nPress Enter to continue to next test...")
        
        test_business_health_method()
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        
        print("\n📊 What you learned:")
        print("   ✅ How agents query structured databases")
        print("   ✅ How agents reason about business questions")
        print("   ✅ How agents chain multiple queries together")
        print("   ✅ How agents interpret data in business context")
        print("   ✅ How agents maintain conversational context")
        
        # Offer interactive mode
        print("\n💬 Would you like to try interactive mode? (y/n): ", end="")
        choice = input().strip().lower()
        
        if choice == 'y':
            interactive_mode()
        
        print("\n" + "="*70)
        print("🎉 Research Agent Testing Complete!")
        print("="*70)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()