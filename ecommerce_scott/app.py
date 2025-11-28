from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"

users = {
    "admin": {
        "password": generate_password_hash("admin123"),
        "role": "admin"
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and check_password_hash(users[username]["password"], password):
            session['user'] = username
            session['role'] = users[username]["role"]
            return redirect(url_for("admin_dashboard")) if session['role']=="admin" else redirect(url_for("customer_dashboard"))

        return "Invalid login details"
    return render_template("login.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users:
            return "User already exists"

        users[username] = {
            "password": generate_password_hash(password),
            "role": "customer"
        }
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/customer_dashboard')
def customer_dashboard():
    if "user" not in session: return redirect(url_for('login'))
    return render_template("customer_dashboard.html", user=session['user'])

@app.route('/admin_dashboard')
def admin_dashboard():
    if "user" not in session or session["role"] != "admin":
        return redirect(url_for('login'))
    return render_template("admin_dashboard.html", users=users)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
