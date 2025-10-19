"""
Weather Agent - Function Calling Implementation

This is your first complete agent. It demonstrates the fundamental pattern
of all AI agents: receive input, decide what to do, execute actions, and
provide results.

The flow works like this:
1. User asks a question
2. Agent analyzes if it needs to use tools
3. If yes, agent requests function calls
4. We execute those functions
5. We send results back to agent
6. Agent formulates final answer
"""
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional

# Add project root so we can import from shared
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from openai import OpenAI
from shared.config.settings import settings
from shared.utils.logger import logger

# Import our weather tools
from tools.weather_tools import (
    get_current_weather,
    get_weather_forecast,
    WEATHER_TOOLS
)


class WeatherAgent:
    """
    A simple weather agent that uses function calling.
    
    This agent can answer weather-related questions by calling
    appropriate weather functions. It demonstrates the core
    pattern of function calling in a clear, understandable way.
    """
    
    def __init__(self):
        """
        Initialize the weather agent.
        
        We set up the OpenAI client and define which functions
        are available. We also keep a conversation history so
        the agent can maintain context across multiple exchanges.
        """
        logger.info("Initializing Weather Agent...")
        
        # Create OpenAI client
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        
        # Store available tools
        self.tools = WEATHER_TOOLS
        
        # Map function names to actual Python functions
        # This is how we know which function to execute when
        # the model requests a function call
        self.available_functions = {
            "get_current_weather": get_current_weather,
            "get_weather_forecast": get_weather_forecast
        }
        
        # Initialize conversation history
        # We keep the entire conversation so the model has context
        self.messages = [
            {
                "role": "system",
                "content": """You are a helpful weather assistant. You can provide current weather 
information and forecasts for any location. When users ask about weather, use the available 
functions to get accurate, up-to-date information. Be friendly and conversational in your 
responses. If a user asks about weather without specifying a location, politely ask them 
which location they are interested in."""
            }
        ]
        
        logger.info("Weather Agent initialized successfully")
    
    def _execute_function_call(self, function_name: str, function_args: Dict) -> str:
        """
        Execute a function call and return the result.
        
        This is where the actual function execution happens. The language
        model has told us which function to call and with what arguments.
        We execute it and return the results as a string.
        
        Args:
            function_name: Name of the function to call
            function_args: Dictionary of arguments for the function
        
        Returns:
            JSON string containing the function results
        """
        logger.info(f"Executing function: {function_name}")
        logger.info(f"With arguments: {function_args}")
        
        # Look up the actual Python function
        if function_name not in self.available_functions:
            error_msg = f"Function {function_name} not found"
            logger.error(error_msg)
            return json.dumps({"error": error_msg})
        
        function_to_call = self.available_functions[function_name]
        
        try:
            # Call the function with the provided arguments
            # The ** unpacks the dictionary into keyword arguments
            result = function_to_call(**function_args)
            
            logger.info(f"Function result: {result}")
            
            # Return result as JSON string
            return json.dumps(result)
            
        except Exception as e:
            error_msg = f"Error executing function: {str(e)}"
            logger.error(error_msg)
            return json.dumps({"error": error_msg})
    
    def chat(self, user_message: str) -> str:
        """
        Process a user message and return a response.
        
        This is the heart of the agent. Here is where the complete
        function calling loop happens. Let me walk you through each
        step so you understand exactly what is happening.
        
        Args:
            user_message: The user's question or request
        
        Returns:
            The agent's response as a string
        """
        logger.info(f"User message: {user_message}")
        
        # Step 1: Add user message to conversation history
        self.messages.append({
            "role": "user",
            "content": user_message
        })
        
        # Step 2: Make initial API call with available tools
        # We tell the model what functions are available and let it decide
        # whether it needs to call any of them
        logger.info("Making initial API call...")
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4 for better function calling
            messages=self.messages,
            tools=self.tools,  # This is where we provide the function definitions
            tool_choice="auto"  # Let the model decide if it needs to call functions
        )
        
        # Get the assistant's response
        response_message = response.choices[0].message
        
        # Step 3: Check if the model wants to call any functions
        # This is the key decision point - did the model decide it needs tools?
        tool_calls = response_message.tool_calls
        
        if not tool_calls:
            # No function calls needed - model can answer directly
            logger.info("No function calls needed, returning direct response")
            assistant_response = response_message.content
            
            # Add assistant response to history
            self.messages.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            return assistant_response
        
        # Step 4: Function calls were requested
        # The model has decided it needs to use tools to answer the question
        logger.info(f"Model requested {len(tool_calls)} function call(s)")
        
        # Add the assistant's message (with function calls) to history
        self.messages.append(response_message)
        
        # Step 5: Execute each requested function call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            logger.info(f"Processing function call: {function_name}")
            
            # Execute the function
            function_response = self._execute_function_call(
                function_name,
                function_args
            )
            
            # Step 6: Add function result to conversation
            # We tell the model "here are the results of the function you called"
            self.messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": function_response
            })
        
        # Step 7: Make second API call with function results
        # Now the model has the actual data and can formulate its final response
        logger.info("Making second API call with function results...")
        
        second_response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=self.messages
        )
        
        # Get final response
        final_message = second_response.choices[0].message
        final_response = final_message.content
        
        # Add to history
        self.messages.append({
            "role": "assistant",
            "content": final_response
        })
        
        logger.info(f"Final response: {final_response}")
        
        return final_response
    
    def reset_conversation(self):
        """
        Reset the conversation history.
        
        This clears everything except the system message, giving you
        a fresh start. Useful when you want to begin a new conversation.
        """
        logger.info("Resetting conversation")
        
        # Keep only the system message
        self.messages = [self.messages[0]]
    
    def get_conversation_history(self) -> List[Dict]:
        """
        Get the complete conversation history.
        
        This is useful for debugging or understanding what the agent
        has been discussing. You can see every message, including
        function calls and their results.
        
        Returns:
            List of message dictionaries
        """
        return self.messages