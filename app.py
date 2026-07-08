from flask import Flask, render_template, jsonify
import sqlite3
import requests

app = Flask(__name__)

DATABASE = "quotes.db"


def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS quotes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            quote TEXT NOT NULL,
            author TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_quote")
def get_quote():

    try:

        response = requests.get(
            "https://dummyjson.com/quotes/random",
            timeout=10
        )

        data = response.json()

        quote = data["quote"]
        author = data["author"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO quotes (quote, author) VALUES (?, ?)",
            (quote, author)
        )

        conn.commit()
        conn.close()

        return jsonify({
            "quote": quote,
            "author": author
        })

    except Exception as e:

        return jsonify({
            "quote": "Failed to fetch quote.",
            "author": str(e)
        }), 500


@app.route("/history")
def history():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT quote, author FROM quotes ORDER BY id DESC"
    )

    rows = cursor.fetchall()

    conn.close()

    history = []

    for row in rows:

        history.append({
            "quote": row["quote"],
            "author": row["author"]
        })

    return jsonify(history)


if __name__ == "__main__":
    app.run(debug=True)