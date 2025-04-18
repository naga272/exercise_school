from flask import Flask, render_template
import sqlite3
import os 


app = Flask(__name__, template_folder='templates')
filename_db = os.path.join(".", "flussi", "db.sqlite3")
flag = False



def get_db_connection():
    conn = sqlite3.connect(filename_db)
    conn.row_factory = sqlite3.Row 
    return conn


def init_db():
    if not os.path.exists("flussi"):
        os.makedirs("flussi")
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS utenti (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    
    cur.execute('INSERT OR IGNORE INTO utenti (nome, email) VALUES (?, ?)', ('Mario Rossi', 'mario@example.com'))

    conn.commit()
    conn.close()


@app.route("/")
def homepage():
    conn = get_db_connection()
    utenti = conn.execute("SELECT * FROM utenti").fetchall()
    conn.close()
    return render_template("index.html", utenti = utenti)


if __name__ == "__main__":
    if flag == False:
        init_db()
        flag = True 

    app.run(debug=True)

