from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  
import os
from langchain.llms import Cohere 

app = Flask(__name__, template_folder=os.path.abspath("templates"))
CORS(app)  # Allow CORS

# Set Cohere API Key directly
os.environ["COHERE_API_KEY"] = "skYltvJTYK2lpYBwKwwwBlbd68XppoE5l5u5t3l3"

# Initialize Cohere LLM
cohere_client = Cohere(cohere_api_key=os.environ["COHERE_API_KEY"], model="command-r-plus")

# Initialize conversation history
conversation_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_query = request.json.get("question")

    if not user_query:
        return jsonify({"error": "No question provided"}), 400

    
    conversation_history.append(f"User: {user_query}")
    context = "\n".join(conversation_history[-10:])  # Keep last 10 exchanges

    prompt = f"Context: {context}\nUser: {user_query}\nBot:"

    try:
        # Generate response
        response_text = cohere_client.predict(prompt).strip()  
        formatted_sources = ["No sources available"]  

        # Add bot response to conversation history
        conversation_history.append(f"Bot: {response_text}")

        return jsonify({"answer": response_text, "sources": formatted_sources})
    
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
