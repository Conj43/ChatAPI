# imports
import logging
from flask import Flask, request, jsonify
from tools import create_tools
from flask_cors import CORS
from utils import call_agent
from heavyai import connect

# imports from other files
from db_config import HEAVY_USER, HEAVY_PROTOCOL, HEAVY_DBNAME, HEAVY_HOST, HEAVY_PASSWORD, HEAVY_PORT
from prompts import PROMPT

# App initialization
app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

# Helper function for connection management
def get_connection():
    try:
        return connect(
            user=HEAVY_USER,
            password=HEAVY_PASSWORD,
            host=HEAVY_HOST,
            port=HEAVY_PORT,
            dbname=HEAVY_DBNAME,
            protocol=HEAVY_PROTOCOL
        )
    except Exception as e:
        logging.error(f"Failed to establish connection: {e}")
        raise

# Routes
@app.route('/api', methods=['GET'])
def chat():
    user_input = request.args.get('user_input', '') 
    user_id = request.args.get('user_id', 'default_user') 
    conversation_id = request.args.get('conversation_id', 'default_conversation') 
    result = ''

    try:
        with get_connection() as con:
            tools = create_tools(con)  # Recreate tools for live connection
            if user_input:
                try:
                    result = call_agent(user_input, user_id, conversation_id, PROMPT, tools)
                    logging.info(f"Agent called successfully with input: {user_input}")
                except Exception as e:
                    logging.error(f"Error during agent call: {e}")
                    result = f"Error during agent call: {e}"
    except Exception as e:
        logging.error(f"Database connection error: {e}")
        result = f"Database connection error: {e}"

    logging.debug(f"User Input: {user_input}, Response: {result}")
    return jsonify({"user_input": user_input, "response": result})


@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Chatbot API!"})


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify database connection."""
    try:
        with get_connection() as con:
            return jsonify({"status": "healthy"})
    except Exception as e:
        logging.error(f"Health check failed: {e}")
        return jsonify({"status": "unhealthy", "error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
