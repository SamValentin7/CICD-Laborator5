from flask import Flask, request, render_template_string
import psycopg2

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host="db",
        database="mydb",
        user="user",
        password="password"
    )

@app.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == "POST":
        message = request.form["message"]
        cur.execute("INSERT INTO messages (text) VALUES (%s)", (message,))
        conn.commit()

    cur.execute("SELECT text FROM messages")
    messages = cur.fetchall()

    cur.close()
    conn.close()

    return render_template_string("""
        <h1>Messages</h1>
        <form method="POST">
            <input name="message">
            <button type="submit">Add</button>
        </form>
        <ul>
            {% for msg in messages %}
                <li>{{ msg[0] }}</li>
            {% endfor %}
        </ul>
    """, messages=messages)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)