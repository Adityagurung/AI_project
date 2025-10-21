"""
Research Assistant Agent
Multi-tool agent for business data analysis

This agent demonstrates a more sophisticated use of function calling where
the agent needs to understand business context, interpret data, and potentially
chain multiple queries together to answer complex questions.

Unlike the weather agent which had straightforward tool usage, this agent
needs to think about:
- What information is needed to answer a business question
- Which database queries will provide that information
- How to interpret the results in a business context
- Whether multiple queries need to be combined

This represents the next level of agent sophistication where reasoning
about tool selection and result interpretation becomes crucial.
"""
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from openai import OpenAI
from shared.config.settings import settings
from shared.utils.logger import logger

# Import database tools
from tools.database_tools import (
    get_customer_by_email,
    get_top_customers,
    get_products_by_category,
    get_low_stock_products,
    get_recent_orders,
    get_total_revenue,
    get_customer_orders,
    DATABASE_TOOLS
)


class ResearchAgent:
    """
    A research assistant that can query business data to answer questions.
    
    This agent has access to a database containing customer, product, and
    order information. It can answer questions about business performance,
    customer behavior, inventory status, and more.
    
    The key difference from simpler agents is that this one needs to
    understand business context and interpret data meaningfully. When
    someone asks "how is business going?", the agent needs to figure out
    what metrics matter and how to present them in a useful way.
    """
    
    def __init__(self):
        """
        Initialize the research assistant agent.
        
        We set up access to the database tools and establish the agent's
        persona as a business analyst who can help answer data-driven
        questions about company performance.
        """
        logger.info("Initializing Research Agent...")
        
        # Create OpenAI client
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Store available tools
        self.tools = DATABASE_TOOLS
        
        # Map function names to actual Python functions
        # This is our dispatch table for executing the right function
        # when the agent requests it
        self.available_functions = {
            "get_customer_by_email": get_customer_by_email,
            "get_top_customers": get_top_customers,
            "get_products_by_category": get_products_by_category,
            "get_low_stock_products": get_low_stock_products,
            "get_recent_orders": get_recent_orders,
            "get_total_revenue": get_total_revenue,
            "get_customer_orders": get_customer_orders
        }
        
        # Initialize conversation history
        # The system message establishes the agent's role and capabilities
        self.messages = [
            {
                "role": "system",
                "content": """You are a helpful business research assistant with access to company 
database information. You can query data about customers, products, orders, and revenue.

When answering questions:
1. Think about what data you need to answer the question fully
2. Use the available database functions to retrieve that data
3. Interpret the data in a business context
4. Provide clear, actionable insights based on the data

Available data categories:
- Customers: Information about customer accounts, spending, and status
- Products: Product catalog with categories, prices, and inventory
- Orders: Transaction history with dates, quantities, and amounts
- Revenue: Financial metrics and trends

Be analytical but conversational. If the data reveals interesting patterns or 
concerns (like low inventory or inactive customers), point them out proactively.
If you need to make multiple queries to fully answer a question, do so.
Always cite specific numbers from the data to support your answers."""
            }
        ]
        
        logger.info("Research Agent initialized successfully")
    
    def _execute_function_call(self, function_name: str, function_args: Dict) -> str:
        """
        Execute a database query function and return the result.
        
        This is where the actual database queries happen. The language model
        has told us which query to run and with what parameters. We execute
        it and return the results as a JSON string that the model can then
        interpret and incorporate into its response.
        
        Args:
            function_name: Name of the database function to call
            function_args: Dictionary of arguments for the function
        
        Returns:
            JSON string containing the query results
        """
        logger.info(f"Executing database query: {function_name}")
        logger.info(f"With arguments: {function_args}")
        
        # Look up the actual Python function
        if function_name not in self.available_functions:
            error_msg = f"Function {function_name} not found"
            logger.error(error_msg)
            return json.dumps({"error": error_msg})
        
        function_to_call = self.available_functions[function_name]
        
        try:
            # Call the database query function
            result = function_to_call(**function_args)
            
            logger.info(f"Query returned: {len(str(result))} characters of data")
            
            # Return result as JSON string
            # The language model will receive this data and interpret it
            return json.dumps(result, default=str)
            
        except Exception as e:
            error_msg = f"Error executing query: {str(e)}"
            logger.error(error_msg)
            return json.dumps({"error": error_msg})
    
    def ask(self, question: str) -> str:
        """
        Ask the research assistant a question about business data.
        
        This is the main interface for interacting with the agent. You ask
        a question in natural language, and the agent figures out what data
        it needs, queries the database, and provides an analytical answer.
        
        The process works like this:
        1. Add the user's question to conversation history
        2. Call the language model with the question and available tools
        3. If the model wants to query the database, execute those queries
        4. Send the query results back to the model
        5. The model synthesizes everything into a final answer
        
        This might happen in one round (for simple questions) or multiple
        rounds (if the agent realizes it needs additional data after seeing
        initial results).
        
        Args:
            question: The user's question about business data
        
        Returns:
            The agent's analytical response
        """
        logger.info(f"User question: {question}")
        
        # Add user message to conversation history
        self.messages.append({
            "role": "user",
            "content": question
        })
        
        # We might need multiple rounds of tool calling for complex questions
        # For example, the agent might first query revenue, then based on
        # what it sees, decide it also needs to query top customers
        max_iterations = 5
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            logger.info(f"Agent reasoning iteration {iteration}")
            
            # Make API call with available tools
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            response_message = response.choices[0].message
            tool_calls = response_message.tool_calls
            
            # If no tool calls, we have our final answer
            if not tool_calls:
                logger.info("Agent provided final answer without additional tool calls")
                assistant_response = response_message.content
                
                self.messages.append({
                    "role": "assistant",
                    "content": assistant_response
                })
                
                return assistant_response
            
            # Tool calls were requested
            logger.info(f"Agent requested {len(tool_calls)} tool call(s)")
            
            # Add the assistant's message (with tool calls) to history
            self.messages.append(response_message)
            
            # Execute each requested tool call
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                logger.info(f"Executing: {function_name}({function_args})")
                
                # Execute the database query
                function_response = self._execute_function_call(
                    function_name,
                    function_args
                )
                
                # Add query result to conversation
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": function_response
                })
            
            # Continue the loop - the agent will now see the query results
            # and decide if it needs more data or can provide a final answer
        
        # If we hit max iterations, return what we have
        logger.warning(f"Reached maximum iterations ({max_iterations})")
        return "I apologize, but I needed to make too many queries to answer your question. Could you try rephrasing or breaking it into smaller questions?"
    
    def reset_conversation(self):
        """
        Reset the conversation history.
        
        This clears all previous questions and answers, giving you a fresh
        start. Useful when switching topics or starting a new analysis session.
        """
        logger.info("Resetting conversation")
        self.messages = [self.messages[0]]  # Keep only system message
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get the complete conversation history.
        
        This is useful for debugging or understanding the full context of
        the conversation, including all tool calls and results.
        
        Returns:
            List of message dictionaries
        """
        return self.messages
    
    def analyze_business_health(self) -> str:
        """
        Convenience method for a common analysis request.
        
        This demonstrates how you can build higher-level methods on top
        of the basic ask() functionality for common use cases.
        
        Returns:
            Comprehensive business health analysis
        """
        logger.info("Performing business health analysis")
        
        return self.ask(
            "Give me a comprehensive overview of business health. "
            "Include revenue trends, top customers, inventory status, "
            "and any concerns I should be aware of."
        )