## google sheet
import geopy.distance as ps
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
client = gspread.authorize(creds)
sheet = client.open("Data name").sheet1
data = sheet.get_all_records()


### web service
from flask import Flask , jsonify, request
app = Flask(__name__)

def manageEmployee(name):
    listdata = pd.DataFrame(data)
    employee = listdata[ listdata['Name'] == name ]
    print(employee)
    return employee


@app.route('/getEmployee' , methods=['GET'])
def home():
    try:
        name = request.args.get('name')
        res = manageEmployee(name)
        msg = ''
        for i in range(len(res)):
            show = res.iloc[i]
            msg = msg + "เบอร์คุณ "+show['Name']+" เบอร์โทร "+ str(show['tel']) + "\n"
        if msg == '':
            msg = "ไม่มีคนที่คุณค้นหา"

        return jsonify({'message' : msg })
    except Exception as e:
        print(e)
        return jsonify({'message' : 'error นะดูใหม่อีกที'})





if __name__ == '__main__':
    app.run(debug=True)

#get_worksheet(0)

# def loadData():
#     list_of_hashes = sheet.get_all_records()
#     return list_of_hashes

# def insert():
#     row = ["คุณบอม" , "30" , "PM" , "ดูงานอย่างเดียว"]
#     index = 2
#     sheet.insert_row(row, index)

# def update():
#     sheet.update_cell(2, 1, "บิ๊ก")

# def delete():
#     sheet.delete_row(2)