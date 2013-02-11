from flask import Flask, render_template
import datetime

import sqlite3 as lite

app = Flask(__name__)

@app.route("/")
def current():
    con = lite.connect('sensordb')
    with con:
        con.row_factory = lite.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM readings WHERE ID = (SELECT MAX(ID) FROM readings)")

        row = cur.fetchone()

        templateData = {
           'date': row["date"],
           'time': row["time"],
           'outside': row["Outside"],
           'masterbr': row["MasterBR"],
           'waterhtr': row["WaterHtr"],
           'basement': row["Basement"],
           'humidity': row["Humidity"],
           'furn_out': row["Furn_Out"],
           'furn_in' : row["Furn_In"],
           'onboard' : row["Onboard"]
           }
    
    return render_template('main.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=False)

