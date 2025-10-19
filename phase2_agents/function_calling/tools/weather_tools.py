"""
Weather Tools
Functions for getting weather information

These are the actual Python functions that will be executed when
the agent decides it needs weather information. Notice how each
function has clear documentation - this helps both humans reading
the code and the AI understanding when to use each function.
"""
import random
from typing import Dict

def get_current_weather(location: str, unit: str = "celsius") -> Dict:
    """
    Get the current weather for a location.
    
    This is a mock function that simulates calling a weather API.
    In a real application, this would make an actual API call to
    a service like OpenWeatherMap. For learning purposes, we are
    generating realistic-looking fake data.
    
    Args:
        location: The city and country, e.g., "London, UK"
        unit: Temperature unit - either "celsius" or "fahrenheit"
    
    Returns:
        Dictionary containing weather information with these keys:
        - location: The location that was queried
        - temperature: Current temperature in the specified unit
        - unit: The unit used for temperature
        - conditions: Description of current conditions
        - humidity: Humidity percentage
        - wind_speed: Wind speed in km/h or mph
    """
    # Generate realistic-looking fake weather data
    # In reality, you would call an API here
    temperature = random.randint(10, 30) if unit == "celsius" else random.randint(50, 86)
    
    conditions = random.choice([
        "Sunny",
        "Partly Cloudy", 
        "Cloudy",
        "Light Rain",
        "Rainy"
    ])
    
    return {
        "location": location,
        "temperature": temperature,
        "unit": unit,
        "conditions": conditions,
        "humidity": random.randint(40, 90),
        "wind_speed": random.randint(5, 25)
    }

def get_weather_forecast(location: str, days: int = 3) -> Dict:
    """
    Get the weather forecast for a location.
    
    This provides a multi-day forecast. Again, this is simulated data,
    but it demonstrates how you would structure a forecast function.
    
    Args:
        location: The city and country, e.g., "Paris, France"
        days: Number of days to forecast (1-7)
    
    Returns:
        Dictionary containing:
        - location: The location queried
        - forecast: List of daily forecasts, each containing:
          - day: Day name or date
          - high: High temperature
          - low: Low temperature  
          - conditions: Expected conditions
    """
    # Ensure days is within reasonable bounds
    days = max(1, min(days, 7))
    
    day_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    forecast = []
    for i in range(days):
        forecast.append({
            "day": day_names[i % 7],
            "high": random.randint(15, 28),
            "low": random.randint(8, 15),
            "conditions": random.choice(["Sunny", "Partly Cloudy", "Rainy", "Cloudy"])
        })
    
    return {
        "location": location,
        "forecast": forecast
    }


# This is the critical part - the function schemas
# These are JSON descriptions that tell the language model about our functions
WEATHER_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather conditions for a specific location. Use this when the user asks about current weather, temperature, or conditions right now.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country, for example: 'London, UK' or 'Tokyo, Japan'"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "The temperature unit to use. Defaults to celsius."
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather_forecast",
            "description": "Get the weather forecast for upcoming days. Use this when the user asks about future weather, what it will be like tomorrow, or planning for upcoming days.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and country"
                    },
                    "days": {
                        "type": "integer",
                        "description": "Number of days to forecast (1-7). Defaults to 3."
                    }
                },
                "required": ["location"]
            }
        }
    }
]