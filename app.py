# สมาชิกในกลุ่ม 1.พงษ์ศักดิ์ เมฆอรุณ  013
# สมาชิกในกลุ่ม 2.ญาณิศา เคลือบกลิ่น 006
# สมาชิกในกลุ่ม 3.ศุภกร เมฆวัน 018

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)
app.secret_key = 'jengR99'

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'atm_db'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        username = request.form['username']
        balance = float(request.form['balance'])

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE account_number = %s', [account_number])
        account = cursor.fetchone()

        if account:
            flash('Account number already exists!', 'danger')
        else:
            cursor.execute('INSERT INTO accounts (account_number, username, balance) VALUES (%s, %s, %s)', (account_number, username, balance))
            mysql.connection.commit()
            flash('Account created successfully!', 'success')
        cursor.close()
        return redirect(url_for('index'))
    return render_template('create_account.html')


@app.route('/view_balance', methods=['GET', 'POST'])
def view_balance():
    if request.method == 'POST':
        account_number = request.form['account_number']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE account_number = %s', [account_number])
        account = cursor.fetchone()
        cursor.close()
        if account:
            return render_template('view_balance.html', account=account)
        flash('Account not found', 'danger')
    return render_template('view_balance.html')

@app.route('/deposit', methods=['GET', 'POST'])
def deposit():
    if request.method == 'POST':
        account_number = request.form['account_number']

        if not account_number:
            flash('Account number is required', 'danger')
            return redirect(url_for('index'))

        try:
            amount = float(request.form['amount'])
            if amount <= 0:
                flash('Deposit amount must be positive', 'danger')
                return redirect(url_for('index'))
        except ValueError:
            flash('Invalid amount', 'danger')
            return redirect(url_for('index'))

        cursor = mysql.connection.cursor()
        try:
            # Check if the account exists
            cursor.execute('SELECT * FROM accounts WHERE account_number = %s', [account_number])
            account = cursor.fetchone()

            if account:
                cursor.execute('UPDATE accounts SET balance = balance + %s WHERE account_number = %s', (amount, account_number))
                mysql.connection.commit()
                flash('Deposit successful!', 'success')
            else:
                flash('Account not found', 'danger')
        finally:
            cursor.close()

        return redirect(url_for('index'))

    return render_template('deposit.html')


@app.route('/withdraw', methods=['GET', 'POST'])
def withdraw():
    if request.method == 'POST':
        account_number = request.form['account_number']
        
        if not account_number:
            flash('Account number is required', 'danger')
            return redirect(url_for('index'))
        
        try:
            amount = float(request.form['amount'])
        except ValueError:
            flash('Invalid amount', 'danger')
            return redirect(url_for('index'))

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute('SELECT balance FROM accounts WHERE account_number = %s', [account_number])
            account = cursor.fetchone()

            if account:
                if amount <= 0:
                    flash('Withdrawal amount must be positive', 'danger')
                elif account['balance'] < amount:
                    flash('Insufficient funds', 'danger')
                else:
                    cursor.execute('UPDATE accounts SET balance = balance - %s WHERE account_number = %s', (amount, account_number))
                    mysql.connection.commit()
                    flash('Withdrawal successful!', 'success')
            else:
                flash('Account not found', 'danger')

        finally:
            cursor.close()

        return redirect(url_for('index'))
    
    return render_template('withdraw.html')



@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        account_number = request.form['account_number']
        cursor = mysql.connection.cursor()
        cursor.execute('DELETE FROM accounts WHERE account_number = %s', [account_number])
        mysql.connection.commit()
        cursor.close()
        flash('Account deleted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('delete_account.html')

if __name__ == '__main__':
    app.run(debug=True)
