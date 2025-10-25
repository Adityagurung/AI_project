"""
Customer Service Multi-Agent System
Built with OpenAI Swarm Framework

This demonstrates the power of multi-agent coordination. Instead of one
agent trying to handle everything, we have specialized agents that each
excel at their specific domain. They collaborate by handing off 
conversations to each other when appropriate.

The system includes:
- Triage Agent: Routes conversations to the right specialist
- Sales Agent: Handles product questions and sales
- Support Agent: Helps with technical issues
- Refund Agent: Processes returns and refunds

Watch how naturally these agents work together, just like a real
customer service team.
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from swarm import Swarm, Agent
from shared.config.settings import settings

# Initialize Swarm client
client = Swarm()


# ============================================================================
# TOOL FUNCTIONS - These are the actions agents can take
# ============================================================================

def get_product_info(product_name: str) -> str:
    """
    Look up information about a product.
    
    In a real system, this would query a product database.
    For demonstration, we return mock data.
    """
    products = {
        "laptop": {
            "name": "Pro Laptop 15",
            "price": "$1299.99",
            "description": "High-performance laptop with 16GB RAM, 512GB SSD",
            "in_stock": True
        },
        "mouse": {
            "name": "Wireless Mouse Pro",
            "price": "$29.99",
            "description": "Ergonomic wireless mouse with precision tracking",
            "in_stock": True
        },
        "keyboard": {
            "name": "Mechanical Keyboard",
            "price": "$79.99",
            "description": "Mechanical keyboard with RGB lighting",
            "in_stock": False
        }
    }
    
    product_name = product_name.lower()
    
    if product_name in products:
        p = products[product_name]
        stock_status = "In stock" if p["in_stock"] else "Currently out of stock"
        return f"{p['name']}: {p['description']}. Price: {p['price']}. {stock_status}"
    else:
        return f"Sorry, I couldn't find information about '{product_name}'. Available products: laptop, mouse, keyboard"


def check_order_status(order_id: str) -> str:
    """
    Check the status of an order.
    
    In production, this would query your order management system.
    """
    # Mock order data
    if order_id == "12345":
        return "Order #12345: Shipped on Oct 15. Expected delivery: Oct 22. Tracking: TRK789456123"
    elif order_id == "67890":
        return "Order #67890: Processing. Expected to ship within 24 hours."
    else:
        return f"I couldn't find order #{order_id}. Please verify the order number."


def process_refund(order_id: str, reason: str) -> str:
    """
    Initiate a refund for an order.
    
    This demonstrates how different agents might have access to
    different tools. Only the Refund Agent can call this function.
    """
    return f"Refund initiated for order #{order_id}. Reason: {reason}. You'll receive an email confirmation within 24 hours. Funds will be returned to your original payment method in 5-7 business days."


def escalate_to_human(issue_description: str) -> str:
    """
    Escalate a complex issue to a human agent.
    
    Some situations require human judgment or intervention.
    """
    return f"I've escalated your issue to our human support team. Issue: {issue_description}. A team member will contact you within 2 hours during business hours."


# ============================================================================
# HANDOFF FUNCTIONS - These enable agent-to-agent transfers
# ============================================================================

def transfer_to_sales() -> Agent:
    """Transfer conversation to the Sales Agent"""
    return sales_agent


def transfer_to_support() -> Agent:
    """Transfer conversation to the Support Agent"""
    return support_agent


def transfer_to_refunds() -> Agent:
    """Transfer conversation to the Refund Agent"""
    return refund_agent


def transfer_to_triage() -> Agent:
    """Transfer back to the Triage Agent"""
    return triage_agent


# ============================================================================
# AGENT DEFINITIONS
# ============================================================================

# TRIAGE AGENT - The entry point that routes conversations
triage_agent = Agent(
    name="Triage Agent",
    instructions="""You are a helpful customer service triage agent. Your role is to:

1. Greet customers warmly
2. Understand what they need help with
3. Route them to the appropriate specialist agent:
   - Sales Agent: For product questions, purchases, availability
   - Support Agent: For technical issues, how-to questions, troubleshooting
   - Refund Agent: For returns, refunds, cancellations

Be friendly but efficient. Ask clarifying questions if you're not sure which agent
would be best, but don't keep customers waiting unnecessarily. Once you understand
their needs, transfer them to the right specialist.

You don't handle the actual issues yourself - you're like a receptionist who
directs people to the right department.""",
    functions=[transfer_to_sales, transfer_to_support, transfer_to_refunds]
)

# SALES AGENT - Handles product and sales questions
sales_agent = Agent(
    name="Sales Agent",
    instructions="""You are a knowledgeable sales agent. Your role is to:

1. Answer questions about products (features, pricing, availability)
2. Help customers find the right product for their needs
3. Provide accurate product information
4. Be enthusiastic but honest about products

You have access to product information through the get_product_info function.
Available products: laptop, mouse, keyboard

If a customer has a technical issue or wants a refund, transfer them to the
appropriate agent. For complex sales questions you can't answer, escalate to
a human agent.

Be helpful and sales-oriented, but never pushy or dishonest.""",
    functions=[get_product_info, transfer_to_support, transfer_to_refunds, 
               transfer_to_triage, escalate_to_human]
)

# SUPPORT AGENT - Handles technical issues
support_agent = Agent(
    name="Support Agent",
    instructions="""You are a technical support specialist. Your role is to:

1. Help customers troubleshoot technical issues
2. Provide how-to guidance and instructions
3. Check order status when customers have concerns
4. Offer solutions to common problems

You can check order status using the check_order_status function.

Common issues you can help with:
- Product setup and configuration
- Connectivity problems
- Software issues
- Usage questions

If the issue requires a refund or return, transfer to the Refund Agent.
If you need product information for sales purposes, transfer to Sales Agent.
For issues beyond your capability, escalate to a human agent.

Be patient, clear, and methodical in your explanations.""",
    functions=[check_order_status, transfer_to_sales, transfer_to_refunds,
               transfer_to_triage, escalate_to_human]
)

# REFUND AGENT - Handles returns and refunds
refund_agent = Agent(
    name="Refund Agent",
    instructions="""You are a refund and returns specialist. Your role is to:

1. Process refund requests professionally
2. Understand the reason for the return
3. Initiate refunds through the proper process
4. Set proper expectations about timing

You can process refunds using the process_refund function.

Company refund policy:
- 30-day return window for most products
- Item must be in original condition
- Refunds take 5-7 business days
- Original shipping is non-refundable

Be empathetic to customer concerns while following company policy.
If they have technical issues, consider transferring to Support to see
if the issue can be resolved before processing a refund.

For policy exceptions or complex cases, escalate to a human agent.""",
    functions=[process_refund, check_order_status, transfer_to_support,
               transfer_to_triage, escalate_to_human]
)


# ============================================================================
# CONVERSATION HANDLER
# ============================================================================

def run_customer_service_demo():
    """
    Run an interactive demo of the customer service system.
    
    This lets you experience how the multi-agent system feels from
    a user perspective. Notice how seamlessly agents hand off to
    each other and how each agent stays within their domain of expertise.
    """
    print("="*70)
    print("🤖 MULTI-AGENT CUSTOMER SERVICE SYSTEM")
    print("="*70)
    
    print("\nWelcome to our customer service! Type your questions and watch")
    print("how different specialized agents handle different types of requests.")
    print("\nTry asking about:")
    print("  • Product information (triggers Sales Agent)")
    print("  • Technical issues (triggers Support Agent)")
    print("  • Refunds or returns (triggers Refund Agent)")
    print("  • Order status (Support or Refund Agent)")
    
    print("\nCommands:")
    print("  'quit' - Exit the demo")
    print("  'reset' - Start a new conversation")
    print("\n" + "="*70 + "\n")
    
    # Start with triage agent
    current_agent = triage_agent
    messages = []
    context_variables = {}
    
    while True:
        user_input = input("You: ").strip()
        
        if not user_input:
            continue
        
        if user_input.lower() == 'quit':
            print("\n👋 Thank you for contacting customer service!")
            break
        
        if user_input.lower() == 'reset':
            print("\n🔄 Starting new conversation...\n")
            current_agent = triage_agent
            messages = []
            context_variables = {}
            continue
        
        # Add user message
        messages.append({"role": "user", "content": user_input})
        
        # Run the swarm with current agent
        response = client.run(
            agent=current_agent,
            messages=messages,
            context_variables=context_variables
        )
        
        # Update for next iteration
        current_agent = response.agent
        messages = response.messages
        context_variables = response.context_variables
        
        # Print the agent's response
        last_message = messages[-1]
        agent_name = current_agent.name
        
        print(f"\n{agent_name}: {last_message['content']}\n")
        
        # Show when agent handoffs occur
        if len(messages) > 2:
            # Check if the agent changed from previous iteration
            prev_messages_len = len(messages) - 2
            if prev_messages_len >= 0:
                # Agent switch is indicated by function calls in message history
                for msg in messages:
                    if msg.get('role') == 'assistant' and msg.get('tool_calls'):
                        for tool_call in msg['tool_calls']:
                            if 'transfer' in tool_call['function']['name']:
                                print(f"   🔄 [Transferred to {agent_name}]\n")
                                break


def test_specific_scenarios():
    """
    Test specific scenarios to demonstrate agent coordination.
    
    This runs through predefined scenarios so you can see exactly
    how the system handles different types of requests.
    """
    print("="*70)
    print("📋 SCENARIO TESTING")
    print("="*70)
    
    scenarios = [
        {
            "name": "Product Inquiry",
            "messages": ["Hi, I'm interested in buying a laptop"],
            "expected": "Should route to Sales Agent"
        },
        {
            "name": "Technical Issue",
            "messages": ["My mouse isn't connecting to my computer"],
            "expected": "Should route to Support Agent"
        },
        {
            "name": "Refund Request",
            "messages": ["I need to return my order #12345"],
            "expected": "Should route to Refund Agent"
        },
        {
            "name": "Multi-Step Interaction",
            "messages": [
                "I want to buy a keyboard",
                "Actually, I have a technical question about setup",
                "Never mind, I just want to return it"
            ],
            "expected": "Should transfer between multiple agents"
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{'='*70}")
        print(f"Scenario {i}: {scenario['name']}")
        print(f"Expected: {scenario['expected']}")
        print(f"{'='*70}\n")
        
        current_agent = triage_agent
        messages = []
        
        for message in scenario['messages']:
            print(f"User: {message}")
            messages.append({"role": "user", "content": message})
            
            response = client.run(
                agent=current_agent,
                messages=messages
            )
            
            current_agent = response.agent
            messages = response.messages
            
            last_message = messages[-1]
            print(f"{current_agent.name}: {last_message['content']}\n")
        
        input("Press Enter to continue to next scenario...")


def main():
    """Main entry point"""
    print("\n🌟 OpenAI Swarm - Multi-Agent Customer Service System\n")
    
    print("This demonstration shows how multiple specialized agents")
    print("can work together to handle complex customer service scenarios.")
    print("\nEach agent has:")
    print("  • Specific expertise and instructions")
    print("  • Their own set of tools")
    print("  • Ability to hand off to other agents")
    print("\nYou'll see agents coordinate seamlessly, just like a real team!\n")
    
    print("Choose an option:")
    print("  1. Interactive demo (chat with the agents)")
    print("  2. Scenario testing (watch predefined scenarios)")
    print("  3. Both")
    
    choice = input("\nYour choice (1/2/3): ").strip()
    
    if choice == "1":
        run_customer_service_demo()
    elif choice == "2":
        test_specific_scenarios()
    elif choice == "3":
        test_specific_scenarios()
        print("\n" + "="*70)
        print("Now try the interactive demo!")
        print("="*70 + "\n")
        run_customer_service_demo()
    else:
        print("Invalid choice. Running interactive demo...")
        run_customer_service_demo()


if __name__ == "__main__":
    main()