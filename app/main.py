from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

#connect to PostgreSQL via .env
conn = psycopg2.connect(
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    dbname=os.getenv("DB_NAME"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD")
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS scents (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    mood TEXT,
    notes TEXT,
    occasion TEXT,
    description TEXT
);
""")
conn.commit()

cursor.execute("SELECT COUNT(*) FROM scents;")
if cursor.fetchone()[0] == 0:
    dummy_data = [
        ("Morning Bloom", "Fresh", "Jasmine, Green Tea", "Morning Walk", "Soft floral notes that awaken your senses"),
        ("Evening Ember", "Cozy", "Amber, Vanilla, Cedarwood", "Chilling at home", "Warm and comforting scent to unwind"),
        ("Ocean Drift", "Relaxed", "Sea breeze, Citrus", "Beach day", "Brings you back to a serene shoreline"),
        ("Midnight Muse", "Mysterious", "Oud, Blackcurrant", "Night out", "Bold, intriguing, and unforgettable"),
        ("Cherry Whisper", "Sweet", "Cherry blossom, Musk", "Picnic or Spring Date", "Soft sweetness with a romantic twist")
    ]

    for scent in dummy_data:
        cursor.execute("""
            INSERT INTO scents (name, mood, notes, occasion, description)
            VALUES (%s, %s, %s, %s, %s);
        """, scent)
    conn.commit()

@app.route("/")
def index():
    cursor.execute("SELECT * FROM scents;")
    scents = cursor.fetchall()
    return render_template("index.html", scents=scents)

@app.route("/table")
def view_table():
    cursor.execute("SELECT * FROM scents;")
    scents = cursor.fetchall()
    return render_template("table.html", scents=scents)


@app.route("/add", methods=["GET", "POST"])
def add_scent():
    if request.method == "POST":
        name = request.form["name"]
        mood = request.form["mood"]
        notes = request.form["notes"]
        occasion = request.form["occasion"]
        description = request.form["description"]
        cursor.execute("INSERT INTO scents (name, mood, notes, occasion, description) VALUES (%s, %s, %s, %s, %s);",
                       (name, mood, notes, occasion, description))
        conn.commit()
        return redirect("/")
    return render_template("add.html")

@app.route("/delete/<int:id>")
def delete_scent(id):
    cursor.execute("DELETE FROM scents WHERE id = %s;", (str(id),))
    conn.commit()
    return redirect("/")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_scent(id):
    if request.method == "POST":
        name = request.form["name"]
        mood = request.form["mood"]
        notes = request.form["notes"]
        occasion = request.form["occasion"]
        description = request.form["description"]
        cursor.execute("UPDATE scents SET name = %s, mood = %s, notes = %s, occasion = %s, description = %s WHERE id = %s;",
                       (name, mood, notes, occasion, description, str(id)))
        conn.commit()
        return redirect("/")
    else:
        cursor.execute("SELECT * FROM scents WHERE id = %s;", (str(id),))
        scent = cursor.fetchone()
        return render_template("edit.html", scent=scent)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
