from flask import Flask, render_template, request
import pandas as pd
import os
from datetime import datetime
from flask import send_file

app = Flask(__name__)
data = pd.read_csv('data.csv')
log_file = 'checkin_log.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    name = request.form.get('name')

    # ค้นจากชื่อใน data.csv
    result = data[data['name'].str.contains(name, na=False)]

    if not result.empty:
        person = result.iloc[0]
        label = person['label']
        checkin_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # ถ้า log ยังไม่มี ให้สร้าง header
        if not os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write('name,label,table,seat,time\n')

        # อ่าน log เดิม
        log_df = pd.read_csv(log_file)

        # เช็คว่าชื่อนี้เช็คอินไปแล้วหรือยัง
        if name in log_df['name'].values:
            prev_time = log_df.loc[log_df['name'] == name, 'time'].values[0]
            return render_template('result.html',
                                   name=name,
                                   table=person['table'],
                                   seat=person['seat'],
                                   label=label,
                                   already=True,
                                   prev_time=prev_time)

        # บันทึก log ใหม่
        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(f"{name},{label},{person['table']},{person['seat']},{checkin_time}\n")

        return render_template('result.html',
                               name=name,
                               table=person['table'],
                               seat=person['seat'],
                               label=label,
                               already=False,
                               time=checkin_time)

    else:
        return render_template('result.html', error='ไม่พบชื่อในระบบ กรุณาติดต่อเจ้าหน้าที่')
    
@app.route('/admin')
def admin():
    if not os.path.exists(log_file):
        return render_template('admin.html', data=[])
    log_df = pd.read_csv(log_file)
    return render_template('admin.html', data=log_df.to_dict(orient='records'))

@app.route('/download')
def download():
    if os.path.exists(log_file):
        return send_file(log_file, as_attachment=True)
    else:
        return "ยังไม่มีข้อมูล Check-in"
    
if __name__ == '__main__':
    app.run(debug=True)
