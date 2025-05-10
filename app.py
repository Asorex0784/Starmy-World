from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def init_db():
    with sqlite3.connect('kullanicilar.db') as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE, password TEXT)')
        conn.commit()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    try:
        with sqlite3.connect('kullanicilar.db') as conn:
            conn.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        return "Kayıt başarılı!"
    except:
        return "Kullanıcı zaten var."

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    with sqlite3.connect('kullanicilar.db') as conn:
        user = conn.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password)).fetchone()
    if user:
        return f"Hoş geldin, {username}!"
    return "Giriş başarısız!"

if __name__ == '__main__':
    init_db()
    app.run()
