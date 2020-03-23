from flask import Flask, jsonify
from flask_restful import Resource, Api
from fhir_parser.fhir import FHIR

app = Flask(__name__)
api = Api(app)

class AllNames(Resource):


    def __init__(self):
        super(AllNames, self).__init__()

    def get(self):
        fhir_parser = FHIR(endpoint="https://localhost:5001/api/", verify_ssl=False)
        patients = fhir_parser.get_all_patients()
        lst_json = []
        for patient in patients:


            names = {}
            names["id"] = patient.uuid
            names["First"] = patient.name.given
            names["Surname"] = patient.name.family
            lst_json.append(names)

        main_json = {}
        main_json["patients"] = lst_json

        return jsonify(main_json)


#
class User(Resource):

    def __init__(self):
        super(User, self).__init__()

    def get(self, id):
        fhir_parser = FHIR(endpoint="https://localhost:5001/api/", verify_ssl=False)
        patients = fhir_parser.get_all_patients()

        patient_ids  = [patient.uuid for patient in patients]
        if id in patient_ids:
            patient= fhir_parser.get_patient(id)
            names = {}
            names["ID"] = patient.uuid
            names["First name"]= patient.name.given
            names["Surname"]  =patient.name.family
            address=""
            for a in patient.addresses:
                address= str(a).replace('\n', ';')
            names['Address'] = address
            numbers = patient.telecoms

            for number in numbers:
                values = str(number).split(":", 1)

                names[values[0]] = values[1]

            names["Martial Status"]= patient.marital_status.__str__()
            names["Birth date"] = str(patient.birth_date)
            names["Gender"]= patient.gender

            return names, 200
        else:
            return "error, not found",400

class Patient_Observation(Resource):

    def get(seld, id):
        fhir_parser = FHIR(endpoint="https://localhost:5001/api/", verify_ssl=False)
        observations = fhir_parser.get_patient_observations(id)

        dates = set()
        x = {dates.add(str(observation.effective_datetime.date())) for observation in observations if str(observation.effective_datetime.date()) not in dates}

        test2_ = {}
        for date in dates:
            test_ = {}
            for observation in observations:
                if date in str(observation.effective_datetime.date()):
                    for component in observation.components:
                        if component.value is None:
                            continue
                        else:
                            test_[component.display] = str(component.value) + str(component.unit)



            test2_[date] = test_

        return jsonify(test2_)

class Patient_Full_Name(Resource):

    def get(self, id):
        fhir_parser = FHIR(endpoint="https://localhost:5001/api/", verify_ssl=False)
        patient = fhir_parser.get_patient(id)
        full_name = patient.full_name()

        json_ = {}
        json_['Full name']  = full_name

        return jsonify(json_)



api.add_resource(AllNames, "/api/patients", endpoint="patients")
api.add_resource(User, "/api/patient/<id>", endpoint="patient")
api.add_resource(Patient_Observation, "/api/observation/<id>", endpoint="observation")
api.add_resource(Patient_Full_Name, "/api/patient/<id>/full-name", endpoint="full_name")

if __name__ == "__main__":

    app.run(debug=True, port=5002)
