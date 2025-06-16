from flask import Flask, render_template, request, redirect, session, url_for, flash
import database

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Replace with a secure key

@app.route('/')
def index():
    if 'user_id' in session:
        tasks = database.get_tasks_by_user(session['user_id'])
        return render_template('tasks.html', tasks=tasks)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if database.register_user(username, email, password):
            flash("Registration successful. Please login.")
            return redirect(url_for('login'))
        else:
            flash("Username or email already exists.")
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = database.validate_login(username, password)
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash("Invalid credentials.")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/add', methods=['POST'])
def add_task():
    if 'user_id' in session:
        task = request.form['task']
        database.add_task(session['user_id'], task)
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    if 'user_id' in session:
        database.delete_task(session['user_id'], task_id)
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['POST'])
def edit_task(task_id):
    if 'user_id' in session:
        new_text = request.form['task']
        database.edit_task(session['user_id'], task_id, new_text)
    return redirect(url_for('index'))

if __name__ == '__main__':
    database.init_db()
    app.run(debug=True)
