from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

BUDGET = 10000
SAVINGS_GOAL = 5000

# Create database table
def init_db():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute('''
CREATE TABLE IF NOT EXISTS expenses(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item TEXT NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL
)
''')

    conn.commit()
    conn.close()

init_db()


@app.route('/')
def home():

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        total = 0

    remaining = BUDGET - total

    warning = ""

    if total > BUDGET:
        warning = "⚠ WARNING! Budget Exceeded"

    elif total > (BUDGET * 0.8):
        warning = "⚠ ALERT! 80% Budget Used"

    if remaining >= SAVINGS_GOAL:
        savings_msg = "🎉 Savings Goal Achieved!"
    else:
        savings_msg = "💰 Keep Saving!"

    return render_template(
        'index.html',
        expenses=expenses,
        total=total,
        budget=BUDGET,
        remaining=remaining,
        warning=warning,
        savings_msg=savings_msg
    )

@app.route('/add', methods=['POST'])
def add():

    item = request.form['item']
    amount = float(request.form['amount'])
    category = request.form['category']

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO expenses(item,amount,category) VALUES(?,?,?)",
        (item, amount, category)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


@app.route('/report')
def report():

    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    cursor.execute("SELECT SUM(amount) FROM expenses")
    total = cursor.fetchone()[0]

    conn.close()

    if total is None:
        total = 0

    return render_template(
        'report.html',
        expenses=expenses,
        total=total
    )


if __name__ == '__main__':
    app.run(debug=True)