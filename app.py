from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# โหลดข้อมูลจาก CSV
DATA_FILE = 'data.csv'
LOG_FILE = 'checkin_log.csv'
data = pd.read_csv(DATA_FILE)

# =========================
# หน้าแรก: input ชื่อผู้เข้าร่วม
@app.route('/')
def index():
    return render_template('index.html')

# =========================
# เช็คอินและแสดงที่นั่ง
@app.route("/check", methods=["GET", "POST"])
def check():
    if request.method == "GET":
        return redirect(url_for("index"))  # หรือ render_template("checkin_form.html")
    name = request.form.get('name')

    # ค้นหาชื่อใน data.csv
    result = data[data['name'].str.contains(name, na=False)]

    if not result.empty:
        person = result.iloc[0]
        label = person['label']
        checkin_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, 'w', encoding='utf-8') as f:
                f.write('name,label,table,seat,time\n')

        log_df = pd.read_csv(LOG_FILE)

        if name in log_df['name'].values:
            prev_time = log_df.loc[log_df['name'] == name, 'time'].values[0]
            return render_template('check.html',
                                   name=name,
                                   table=person['table'],
                                   seat=person['seat'],
                                   label=label,
                                   already=True,
                                   prev_time=prev_time)

        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(f"{name},{label},{person['table']},{person['seat']},{checkin_time}\n")

        return render_template('check.html',
                               name=name,
                               table=person['table'],
                               seat=person['seat'],
                               label=label,
                               already=False,
                               time=checkin_time)
    else:
        return render_template('check.html', error='ไม่พบชื่อในระบบ กรุณาติดต่อเจ้าหน้าที่')

# =========================
# หน้าผู้ดูแลดูเช็คอินทั้งหมด
@app.route('/admin')
def admin():
    if os.path.exists(LOG_FILE):
        log_df = pd.read_csv(LOG_FILE)
    else:
        log_df = pd.DataFrame(columns=['name', 'label', 'table', 'seat', 'time'])
    return render_template('admin.html', log=log_df.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
