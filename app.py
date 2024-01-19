import os
import openai
from main import qa,memory,get_chunks
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)

@app.route("/chat")
def chat():
   query = request.json["query"] 
   response = qa.invoke(query)
   return jsonify({"response": response})

if __name__ == "__main__":
   app.run()
   
