from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('vertretungsplan.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect('vertretungsplan.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS vertretungen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datum TEXT NOT NULL,
            klasse TEXT NOT NULL,
            fach TEXT NOT NULL,
            lehrer TEXT NOT NULL,
            raum TEXT NOT NULL,
            urspruenglicher_lehrer TEXT,
            kommentare TEXT
        );
    ''')
    conn.commit()
    conn.close()

# Datenbank initialisieren
init_db()

@app.route("/")
def index():
    conn = get_db_connection()
    vertretungen = conn.execute('SELECT * FROM vertretungen').fetchall()
    conn.close()
    return render_template('plan.html', vertretungen=vertretungen)

@app.route("/add", methods=["POST"])
def add_entry():
    datum = request.form['datum']
    klasse = request.form['klasse']
    fach = request.form['fach']
    lehrer = request.form['lehrer']
    raum = request.form['raum']
    urspruenglicher_lehrer = request.form.get('urspruenglicher_lehrer', '')
    kommentare = request.form.get('kommentare', '')
    
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO vertretungen (datum, klasse, fach, lehrer, raum, urspruenglicher_lehrer, kommentare)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (datum, klasse, fach, lehrer, raum, urspruenglicher_lehrer, kommentare))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/update/<int:id>", methods=["POST"])
def update_entry(id):
    datum = request.form['datum']
    klasse = request.form['klasse']
    fach = request.form['fach']
    lehrer = request.form['lehrer']
    raum = request.form['raum']
    urspruenglicher_lehrer = request.form.get('urspruenglicher_lehrer', '')
    kommentare = request.form.get('kommentare', '')
    
    conn = get_db_connection()
    conn.execute('''
        UPDATE vertretungen 
        SET datum = ?, klasse = ?, fach = ?, lehrer = ?, raum = ?, urspruenglicher_lehrer = ?, kommentare = ?
        WHERE id = ?
    ''', (datum, klasse, fach, lehrer, raum, urspruenglicher_lehrer, kommentare, id))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete_entry(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM vertretungen WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
