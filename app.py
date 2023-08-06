import pandas as pd
import sqlite3
from flask import Flask, send_file

app = Flask(__name__)

# Determines if user wants profile information in Excel File
@app.route('/toExcel')
def toExcel():
    condition = input("Do you want to download a Excel File: Yes or No")
    if (condition == 'no') or (condition == 'No'):
        exit()
    connection = sqlite3.connect('Recruiter_Information.db')
    query = 'SELECT * FROM employees'
    df = pd.read_sql_query(query, connection)
    connection.close()

    excel_file_path = 'employees_data.xlsx'
    df.to_excel(excel_file_path, index=False)
    return send_file(excel_file_path, as_attachment=True)