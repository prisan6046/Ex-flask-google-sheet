## google sheet
import geopy.distance as ps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Data name").sheet1

### web service
from flask import Flask , jsonify, request
app = Flask(__name__)

def loadEmployee():
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    return listdata

def searchEmployee(name):
    data = sheet.get_all_records()
    listdata = pd.DataFrame(data)
    employee = listdata[ listdata['Name'] == name ]
    return employee

@app.route('/getEmployee' , methods=['GET'])
def getEmployee():
    try:
        name = request.args.get('name')
        res = searchEmployee(name)
        msg = ''
        for i in range(len(res)):
            show = res.iloc[i]
            msg = msg + "เบอร์คุณ "+show['Name']+" เบอร์โทร "+ str(show['tel']) + "\n"
        if msg == '':
            msg = "ไม่มีคนที่คุณค้นหา"

        return jsonify({'message' : msg })
    except Exception as e:
        return jsonify({'message' : 'error นะดูใหม่อีกที'})

@app.route('/insertEmployee' , methods=['GET'])
def InsertEmployee():
    try:
        name = request.args.get('name')
        age = request.args.get('age')
        position = request.args.get('position')
        detail = request.args.get('detail')
        tel = request.args.get('tel')
        res = loadEmployee()
        row = [ name , str(age) , position , detail , str(tel) ]
        index = int(len(res)+2)
        sheet.insert_row(row, index)
        return jsonify({'message' : "เพิ่มสำเร็จ" })
    except Exception as e:
        return jsonify({'message' : 'error นะดูใหม่อีกที'})


if __name__ == '__main__':
    app.run(debug=True)