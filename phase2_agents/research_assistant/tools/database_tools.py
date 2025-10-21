"""
Database Query Tools
Functions for querying structured data from a database

This module demonstrates how to give an AI agent access to your data.
In this example, we create a simple SQLite database with customer,
product, and order data. The agent can query this data to answer
business questions.

The key concepts you'll learn here:
1. Creating and managing a SQLite database
2. Writing safe SQL queries that prevent injection attacks
3. Returning structured data in a format the agent can understand
4. Handling database errors gracefully
5. Designing query functions that match natural language questions
"""
import sqlite3
from pathlib import Path
from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
import json


class DatabaseManager:
    """
    Manages the SQLite database for the research assistant.
    
    This class handles all database operations: creating tables,
    populating sample data, and executing queries. By centralizing
    database logic in a class, we make it easy to switch databases
    later or add connection pooling for production use.
    """
    
    def __init__(self, db_path: str = None):
        """
        Initialize the database manager.
        
        Args:
            db_path: Path to SQLite database file. If None, creates
                    a database in the research_assistant folder.
        """
        if db_path is None:
            # Create database in the research_assistant folder
            db_dir = Path(__file__).parent.parent
            db_path = db_dir / "business_data.db"
        
        self.db_path = db_path
        self.connection = None
        
        # Initialize database on creation
        self._initialize_database()
    
    def _get_connection(self):
        """
        Get a database connection.
        
        SQLite connections are not thread-safe, so we create a new
        connection for each operation. In production with multiple
        concurrent users, you would use a connection pool instead.
        """
        return sqlite3.connect(self.db_path)
    
    def _initialize_database(self):
        """
        Create tables and populate with sample data if they don't exist.
        
        This method sets up the entire database schema and fills it with
        realistic sample data. The data is designed to be interesting for
        queries - it has patterns, trends, and relationships that an agent
        can discover and analyze.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create customers table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                signup_date TEXT NOT NULL,
                status TEXT DEFAULT 'active',
                total_spent REAL DEFAULT 0.0
            )
        """)
        
        # Create products table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price REAL NOT NULL,
                stock_quantity INTEGER DEFAULT 0,
                description TEXT
            )
        """)
        
        # Create orders table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                order_date TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'completed',
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
                FOREIGN KEY (product_id) REFERENCES products (product_id)
            )
        """)
        
        # Check if we need to populate sample data
        cursor.execute("SELECT COUNT(*) FROM customers")
        if cursor.fetchone()[0] == 0:
            self._populate_sample_data(cursor)
        
        conn.commit()
        conn.close()
    
    def _populate_sample_data(self, cursor):
        """
        Populate the database with realistic sample data.
        
        This creates a miniature business dataset with customers,
        products, and orders. The data has realistic patterns:
        - Some customers buy more than others
        - Products have different price points and categories
        - Orders are distributed over time with some seasonality
        
        This makes it interesting for the agent to analyze.
        """
        # Insert sample customers
        customers = [
            ('Alice Johnson', 'alice@email.com', '2024-01-15', 'active'),
            ('Bob Smith', 'bob@email.com', '2024-02-20', 'active'),
            ('Carol Williams', 'carol@email.com', '2024-03-10', 'active'),
            ('David Brown', 'david@email.com', '2024-04-05', 'active'),
            ('Emma Davis', 'emma@email.com', '2024-05-12', 'active'),
            ('Frank Miller', 'frank@email.com', '2024-06-08', 'inactive'),
            ('Grace Wilson', 'grace@email.com', '2024-07-22', 'active'),
            ('Henry Moore', 'henry@email.com', '2024-08-14', 'active'),
        ]
        
        cursor.executemany(
            "INSERT INTO customers (name, email, signup_date, status) VALUES (?, ?, ?, ?)",
            customers
        )
        
        # Insert sample products
        products = [
            ('Laptop Pro 15', 'Electronics', 1299.99, 25, 'High-performance laptop'),
            ('Wireless Mouse', 'Electronics', 29.99, 150, 'Ergonomic wireless mouse'),
            ('USB-C Cable', 'Accessories', 12.99, 200, '6ft USB-C charging cable'),
            ('Desk Lamp', 'Office', 45.00, 80, 'LED desk lamp with adjustable brightness'),
            ('Office Chair', 'Furniture', 299.99, 40, 'Ergonomic office chair'),
            ('Notebook Set', 'Stationery', 15.99, 120, 'Set of 3 premium notebooks'),
            ('Headphones', 'Electronics', 89.99, 60, 'Noise-canceling headphones'),
            ('Monitor Stand', 'Accessories', 39.99, 90, 'Adjustable monitor stand'),
            ('Keyboard', 'Electronics', 79.99, 70, 'Mechanical keyboard'),
            ('Water Bottle', 'Office', 19.99, 100, 'Insulated stainless steel bottle'),
        ]
        
        cursor.executemany(
            "INSERT INTO products (name, category, price, stock_quantity, description) VALUES (?, ?, ?, ?, ?)",
            products
        )
        
        # Insert sample orders with realistic patterns
        # We'll create orders over the past few months
        base_date = datetime.now() - timedelta(days=90)
        
        orders = [
            # Alice - frequent buyer
            (1, 1, base_date + timedelta(days=5), 1, 1299.99, 'completed'),
            (1, 2, base_date + timedelta(days=5), 2, 59.98, 'completed'),
            (1, 7, base_date + timedelta(days=30), 1, 89.99, 'completed'),
            
            # Bob - moderate buyer
            (2, 5, base_date + timedelta(days=10), 1, 299.99, 'completed'),
            (2, 4, base_date + timedelta(days=10), 1, 45.00, 'completed'),
            
            # Carol - electronics enthusiast
            (3, 9, base_date + timedelta(days=15), 1, 79.99, 'completed'),
            (3, 7, base_date + timedelta(days=15), 1, 89.99, 'completed'),
            (3, 8, base_date + timedelta(days=40), 1, 39.99, 'completed'),
            
            # David - office setup
            (4, 5, base_date + timedelta(days=20), 1, 299.99, 'completed'),
            (4, 4, base_date + timedelta(days=20), 2, 90.00, 'completed'),
            (4, 6, base_date + timedelta(days=20), 3, 47.97, 'completed'),
            
            # Emma - budget conscious
            (5, 3, base_date + timedelta(days=25), 3, 38.97, 'completed'),
            (5, 6, base_date + timedelta(days=25), 2, 31.98, 'completed'),
            (5, 10, base_date + timedelta(days=50), 2, 39.98, 'completed'),
            
            # Frank - inactive customer, old order
            (6, 2, base_date + timedelta(days=2), 1, 29.99, 'completed'),
            
            # Grace - recent customer
            (7, 1, base_date + timedelta(days=70), 1, 1299.99, 'completed'),
            (7, 3, base_date + timedelta(days=70), 2, 25.98, 'completed'),
            
            # Henry - varied purchases
            (8, 7, base_date + timedelta(days=75), 1, 89.99, 'completed'),
            (8, 10, base_date + timedelta(days=75), 1, 19.99, 'completed'),
            (8, 8, base_date + timedelta(days=80), 1, 39.99, 'pending'),
        ]
        
        for customer_id, product_id, order_date, quantity, total, status in orders:
            cursor.execute(
                """INSERT INTO orders 
                (customer_id, product_id, order_date, quantity, total_amount, status) 
                VALUES (?, ?, ?, ?, ?, ?)""",
                (customer_id, product_id, order_date.strftime('%Y-%m-%d'), quantity, total, status)
            )
        
        # Update customer total_spent based on their orders
        cursor.execute("""
            UPDATE customers 
            SET total_spent = (
                SELECT COALESCE(SUM(total_amount), 0) 
                FROM orders 
                WHERE orders.customer_id = customers.customer_id
            )
        """)
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict]:
        """
        Execute a SQL query and return results as a list of dictionaries.
        
        This is the core method that actually runs queries. It converts
        SQL results from tuples to dictionaries with column names as keys,
        which makes the data much easier for the agent to work with.
        
        Args:
            query: SQL query string
            params: Optional tuple of parameters for parameterized queries
            
        Returns:
            List of dictionaries, one per row
        """
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row  # This makes rows accessible by column name
            cursor = conn.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            # Convert rows to dictionaries
            results = [dict(row) for row in cursor.fetchall()]
            
            conn.close()
            return results
            
        except sqlite3.Error as e:
            return [{"error": f"Database error: {str(e)}"}]


# Global database manager instance
db_manager = DatabaseManager()


# ============================================================================
# QUERY FUNCTIONS - These are the tools the agent will use
# ============================================================================

def get_customer_by_email(email: str) -> Dict:
    """
    Look up a customer by their email address.
    
    This demonstrates a simple lookup query. The agent might use this
    when someone asks "what do we know about customer alice@email.com?"
    
    Args:
        email: Customer's email address
        
    Returns:
        Dictionary with customer information or error
    """
    query = "SELECT * FROM customers WHERE email = ?"
    results = db_manager.execute_query(query, (email,))
    
    if not results:
        return {
            "found": False,
            "message": f"No customer found with email: {email}",
            "success": True
        }
    
    return {
        "found": True,
        "customer": results[0],
        "success": True
    }


def get_top_customers(limit: int = 5) -> Dict:
    """
    Get the top customers by total amount spent.
    
    This demonstrates an aggregate query with sorting and limiting.
    Useful for questions like "who are our best customers?"
    
    Args:
        limit: Number of top customers to return
        
    Returns:
        Dictionary with list of top customers
    """
    query = """
        SELECT name, email, total_spent, status
        FROM customers
        WHERE status = 'active'
        ORDER BY total_spent DESC
        LIMIT ?
    """
    
    results = db_manager.execute_query(query, (limit,))
    
    return {
        "count": len(results),
        "customers": results,
        "success": True
    }


def get_products_by_category(category: str) -> Dict:
    """
    Get all products in a specific category.
    
    Args:
        category: Product category (e.g., 'Electronics', 'Office')
        
    Returns:
        Dictionary with list of products
    """
    query = """
        SELECT name, price, stock_quantity, description
        FROM products
        WHERE category = ?
        ORDER BY price DESC
    """
    
    results = db_manager.execute_query(query, (category,))
    
    return {
        "category": category,
        "count": len(results),
        "products": results,
        "success": True
    }


def get_low_stock_products(threshold: int = 50) -> Dict:
    """
    Find products with stock below a threshold.
    
    This is useful for inventory management questions like
    "which products are running low?"
    
    Args:
        threshold: Stock quantity threshold
        
    Returns:
        Dictionary with list of low-stock products
    """
    query = """
        SELECT name, category, stock_quantity, price
        FROM products
        WHERE stock_quantity < ?
        ORDER BY stock_quantity ASC
    """
    
    results = db_manager.execute_query(query, (threshold,))
    
    return {
        "threshold": threshold,
        "count": len(results),
        "products": results,
        "success": True
    }


def get_recent_orders(days: int = 30) -> Dict:
    """
    Get orders from the last N days.
    
    This demonstrates date filtering and joining across tables.
    
    Args:
        days: Number of days to look back
        
    Returns:
        Dictionary with list of recent orders
    """
    cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    query = """
        SELECT 
            o.order_id,
            c.name as customer_name,
            p.name as product_name,
            o.order_date,
            o.quantity,
            o.total_amount,
            o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        WHERE o.order_date >= ?
        ORDER BY o.order_date DESC
    """
    
    results = db_manager.execute_query(query, (cutoff_date,))
    
    return {
        "days": days,
        "count": len(results),
        "orders": results,
        "success": True
    }


def get_total_revenue(days: int = None) -> Dict:
    """
    Calculate total revenue, optionally for a specific time period.
    
    This demonstrates aggregate functions (SUM).
    
    Args:
        days: Optional number of days to calculate revenue for.
              If None, calculates all-time revenue.
              
    Returns:
        Dictionary with revenue information
    """
    if days:
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        query = """
            SELECT 
                SUM(total_amount) as total_revenue,
                COUNT(*) as order_count,
                AVG(total_amount) as average_order_value
            FROM orders
            WHERE order_date >= ? AND status = 'completed'
        """
        results = db_manager.execute_query(query, (cutoff_date,))
        period = f"last {days} days"
    else:
        query = """
            SELECT 
                SUM(total_amount) as total_revenue,
                COUNT(*) as order_count,
                AVG(total_amount) as average_order_value
            FROM orders
            WHERE status = 'completed'
        """
        results = db_manager.execute_query(query)
        period = "all time"
    
    if results and results[0]['total_revenue'] is not None:
        return {
            "period": period,
            "total_revenue": round(results[0]['total_revenue'], 2),
            "order_count": results[0]['order_count'],
            "average_order_value": round(results[0]['average_order_value'], 2),
            "success": True
        }
    else:
        return {
            "period": period,
            "total_revenue": 0,
            "order_count": 0,
            "message": "No completed orders found for this period",
            "success": True
        }


def get_customer_orders(customer_email: str) -> Dict:
    """
    Get all orders for a specific customer.
    
    This demonstrates joining tables and filtering by customer.
    
    Args:
        customer_email: Customer's email address
        
    Returns:
        Dictionary with customer's order history
    """
    query = """
        SELECT 
            c.name as customer_name,
            p.name as product_name,
            o.order_date,
            o.quantity,
            o.total_amount,
            o.status
        FROM orders o
        JOIN customers c ON o.customer_id = c.customer_id
        JOIN products p ON o.product_id = p.product_id
        WHERE c.email = ?
        ORDER BY o.order_date DESC
    """
    
    results = db_manager.execute_query(query, (customer_email,))
    
    if not results:
        return {
            "found": False,
            "message": f"No orders found for customer: {customer_email}",
            "success": True
        }
    
    return {
        "found": True,
        "customer_email": customer_email,
        "order_count": len(results),
        "orders": results,
        "success": True
    }


# ============================================================================
# FUNCTION SCHEMAS FOR THE AGENT
# ============================================================================

DATABASE_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_by_email",
            "description": "Look up a customer's information by their email address. Returns customer details including name, status, and total amount spent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The customer's email address"
                    }
                },
                "required": ["email"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_top_customers",
            "description": "Get the top customers ranked by total amount spent. Only includes active customers. Use this to answer questions about best or most valuable customers.",
            "parameters": {
                "type": "object",
                "properties": {
                    "limit": {
                        "type": "integer",
                        "description": "Number of top customers to return (default: 5)",
                        "default": 5
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_products_by_category",
            "description": "Get all products in a specific category. Categories include: Electronics, Accessories, Office, Furniture, Stationery. Returns product names, prices, stock levels, and descriptions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "Product category to filter by"
                    }
                },
                "required": ["category"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_low_stock_products",
            "description": "Find products with stock quantity below a threshold. Use this for inventory management questions or to identify products that may need reordering.",
            "parameters": {
                "type": "object",
                "properties": {
                    "threshold": {
                        "type": "integer",
                        "description": "Stock quantity threshold (default: 50). Products with stock below this will be returned.",
                        "default": 50
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_recent_orders",
            "description": "Get orders from the last N days. Returns order details including customer name, product name, date, quantity, and amount. Use for recent activity analysis.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Number of days to look back (default: 30)",
                        "default": 30
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_total_revenue",
            "description": "Calculate total revenue, average order value, and order count. Can be filtered to a specific time period or show all-time statistics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "days": {
                        "type": "integer",
                        "description": "Optional: Number of days to calculate revenue for. If not provided, calculates all-time revenue."
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer_orders",
            "description": "Get all orders for a specific customer by their email. Returns complete order history with product details, dates, quantities, and amounts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_email": {
                        "type": "string",
                        "description": "Customer's email address"
                    }
                },
                "required": ["customer_email"]
            }
        }
    }
]