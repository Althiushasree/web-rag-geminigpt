from flask import Flask, request, jsonify, render_template
from retriever import retrieve_context
from generator import generate_answer

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/query", methods=["POST"])
def query():
    data = request.get_json()
    if not data or "query" not in data:
        return jsonify({"error": "Missing 'query' field in request body"}), 400

    user_query = data["query"].strip()
    if not user_query:
        return jsonify({"error": "Query cannot be empty"}), 400

    try:
        context_chunks, sources = retrieve_context(user_query)
        answer = generate_answer(user_query, context_chunks)

        return jsonify({
            "query": user_query,
            "answer": answer,
            "sources": sources,
            "context_chunks": context_chunks,
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
