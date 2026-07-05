from flask import Flask,render_template,redirect
import sqlite3
import random
from datetime import datetime

app=Flask(__name__)


def init_db():

    conn=sqlite3.connect(
    "honeypot.db"
    )

    cursor=conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS logs(

    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ip TEXT,
    activity TEXT,
    time TEXT

    )

    """)

    conn.commit()
    conn.close()


init_db()


@app.route("/")
def home():

    conn=sqlite3.connect(
    "honeypot.db"
    )

    cursor=conn.cursor()

    cursor.execute(
    "SELECT * FROM logs ORDER BY id DESC LIMIT 10"
    )

    logs=cursor.fetchall()

    cursor.execute(
    "SELECT COUNT(*) FROM logs"
    )

    total=cursor.fetchone()[0]

    cursor.execute(
    "SELECT COUNT(DISTINCT ip) FROM logs"
    )

    unique_ips=cursor.fetchone()[0]

    cursor.execute("""

    SELECT ip,COUNT(*)

    FROM logs

    GROUP BY ip

    HAVING COUNT(*)>2

    """)

    suspicious=cursor.fetchall()

    conn.close()

    return render_template(
    "index.html",
    logs=logs,
    total=total,
    unique=unique_ips,
    suspicious=suspicious
    )


@app.route("/generate")
def generate():

    ips=[

    "192.168.1.2",
    "192.168.1.4",
    "10.0.0.5",
    "172.16.1.10"

    ]

    activities=[

    "SSH Login Attempt",
    "HTTP Request",
    "FTP Login Attempt",
    "Admin Access Request",
    "Failed Authentication"

    ]

    conn=sqlite3.connect(
    "honeypot.db"
    )

    cursor=conn.cursor()

    for i in range(15):

        cursor.execute(
        """
        INSERT INTO logs(
        ip,
        activity,
        time
        )

        VALUES(?,?,?)
        """,
        (
        random.choice(ips),
        random.choice(activities),
        datetime.now().strftime(
        "%d-%m-%Y %I:%M:%S %p"
        )
        )
        )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/clear")
def clear():

    conn=sqlite3.connect(
    "honeypot.db"
    )

    cursor=conn.cursor()

    cursor.execute(
    "DELETE FROM logs"
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__=="__main__":
    app.run(debug=True)