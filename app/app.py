from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from requests import get

app = Flask(__name__)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlite3.db"
db.init_app(app)

class USD_rate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    rate = db.Column(db.Float, nullable=False)
    change_rate = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

url_archive = 'https://www.cbr-xml-daily.ru/daily_json.js'

@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        if request.form['button'] == 'Check':
            response = get(url_archive)
            data = response.json()
            
            data_now = data.get('Date')
            value_now = float(data.get('Valute').get('USD').get('Value'))
            value_previous = float(data.get('Valute').get('USD').get('Previous'))
            delta_value = round(value_now - value_previous, 4)
            
            rate = USD_rate(
                date = data_now,
                rate = value_now,
                change_rate = delta_value)
            db.session.add(rate)
            db.session.commit()
            return render_template('index.html', 
                           value_now = value_now,
                           value_previous = value_previous,
                           delta_value = delta_value)
        elif request.form['button'] == 'Show table':
            return redirect('/db.html')
    else:
        return render_template('index.html', 
                           value_now = 'Нет данных',
                           value_previous = 'Нет данных',
                           delta_value = 0)

@app.route('/db.html')
def db_page():
    result = db.session.execute('SELECT * FROM USD_rate')
    result_list = []
    for row in result:
        result_list.append(row)
    return render_template('db.html', rate = result_list)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')