from flask import Flask, render_template, make_response
import requests
import pdfkit
import re
from datetime import datetime

app = Flask(__name__)


@app.route("/")
def home():
    r= requests.get("http://localhost:5002/api/patients")
    data = r.json()
    ids = [(item["id"], item["First"], item["Surname"]) for item in data["patients"]]
    return render_template("index.html", ids = ids)

@app.route("/patient/<id>")
def patient_data(id):

    r = requests.get("http://localhost:5002/api/patient/"+id)
    r2= requests.get("http://localhost:5002/api/observation/"+id)
    observations = r2.json()
    datas = r.json()

    view= [(date, next(iter(values)), values.get(next(iter(values)))) for date, values in observations.items()]


    return render_template("test1.html", name=[datas,view,id])

@app.route("/patient/<id>/<date>")
def full_observations(id, date):

    r2= requests.get("http://localhost:5002/api/observation/"+id)
    observations = r2.json()
    #
    full_view = [(num,values) for num, values in observations.items() if num in date]

    return render_template("observations_full.html", data=full_view)


@app.route('/patient/<id>/<date>/pdf')
def generate_pdf(id,date):

    r = requests.get("http://localhost:5002/api/patient/"+id+"/full-name")
    data = r.json()
    full_name = data["Full name"]
    r3 = requests.get("http://localhost:5002/api/patient/"+id)
    get_add=  r3.json()
    address = get_add["Address"]
    address_split = re.split(";|,", address)

    r2= requests.get("http://localhost:5002/api/observation/"+id)
    observations = r2.json()

    full_view = [(num,values) for num, values in observations.items() if num in date]

    check_scores ={}
    dates = full_view[0][0]

    today = datetime.today()
    today = today.strftime('%d-%B-%Y')
    today_date = str(today)


    for item in full_view:
        for key, value in item[1].items():
            number = re.split('\D', value)
            number  = number[0]

            if 'Diastolic Blood Pressure' in key:
                if int(number) > 80:
                    check_scores['Diastolic Blood Pressure']= True

            if 'Systolic Blood Pressure' in key:
                if int(number) > 120:
                    check_scores['Systolic Blood Pressure']= True
            if 'Heart rate' in key:
                if int(number) > 100:
                    check_scores['Heart rate']= True

            if 'Respiratory rate' in key:
                if int(number) > 20:
                    check_scores['Respiratory rate']= True

            if 'Body Mass Index' in key:
                if int(number) > 25:
                    check_scores['Body Mass Index']= True

            if 'Total Cholesterol ' in key:
                if int(number) > 240:
                    check_scores['Total Cholesterol']= True
            if 'Body Temperature ' in key:
                if int(number) > 39:
                    check_scores["Body temperature"] = True


    rendered= render_template('pdf_letter.html', today= today_date, address= address_split , full_name = full_name, dates=dates,  data=full_view, check= check_scores)
    css= ['static/css/style.css']
    pdf = pdfkit.from_string(rendered, False, css=css)


    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition']= 'attachment; filename=output.pdf'

    return response


if __name__ == "__main__":
    app.run(debug= True, port=5003)



