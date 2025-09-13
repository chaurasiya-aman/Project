from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3 as sql

app = Flask(__name__)
app.secret_key = 'your_secret_key_here' 
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
 
        try:
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                            (username, email, password))
                con.commit()
                flash("Registration successful! Please login.", "success")
                return redirect(url_for('login'))
        except Exception as e:
            flash("User already exists or database error.", "danger")
            print("Error:", e)
            return render_template('register.html')
    return render_template('register.html')


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            user = cur.fetchone()

            if user:
                session['user_id'] = user[0]
                session['username'] = user[1]
                flash("Logged in successfully!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in to access the dashboard.", "warning")
        return redirect(url_for('login'))

    
    internships = [
        {
            "title": "Web Development Intern",
            "company": "TechSoft Solutions",
            "location": "Remote",
            "description": "Build and maintain web applications using Flask and React."
        },
        {
            "title": "Data Science Intern",
            "company": "DataMinds AI",
            "location": "Bangalore, India",
            "description": "Work with big data, machine learning, and analytics tools."
        },
        {
            "title": "UI/UX Design Intern",
            "company": "DesignHub",
            "location": "Remote",
            "description": "Help create beautiful and intuitive user experiences."
        }
    ]

    return render_template('dashboard.html', username=session['username'], internships=internships)

@app.route('/applicant')
def applicant():
    return render_template('applicant.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
