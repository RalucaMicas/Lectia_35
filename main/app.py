from flask import Flask, request, jsonify

from datetime import datetime

import json

import os

app = Flask(__name__)

person_dir = 'persoane'

if not os.path.exists(person_dir):
    os.makedirs(person_dir)

timestamps_file_path = 'timestamps.txt'

def verificare_fisier_txt(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write('')

@app.route('/add-timestamp', methods=['POST'])
def add_timestamp():

    verificare_fisier_txt(timestamps_file_path)

    current_timestamp = datetime.now().isoformat()

    with open(timestamps_file_path, 'a') as file:
        file.write(current_timestamp + '\n')

    return jsonify({'message': 'Timestamp added', 'timestamp': current_timestamp}), 201

@app.route('/add-person', methods=['POST'])
def add_person():
    data = request.get_json()

    nume = data.get('nume')
    prenume = data.get('prenume')
    varsta = data.get('varsta')
    ocupatie = data.get('ocupatie')

    if not all([nume, prenume, varsta, ocupatie]):
        return jsonify({'message': 'Missing required fields'}), 400
    
    current_timestamp = datetime.now().isoformat()

    person_info = {
        'nume': nume,
        'prenume': prenume,
        'varsta': varsta,
        'ocupatie': ocupatie,
        'create_time': current_timestamp
    }

    filename = f'{nume}_{prenume}.json'
    file_path = os.path.join(person_dir, filename)

    try:
        with open(file_path, 'w') as json_file:
            json.dump(person_info, json_file, indent=4)

        return jsonify({'message': 'Info saved', 'fisier': filename}), 201
    
    except Exception as e:
        return jsonify({'message': 'Failed to save data', 'error': str(e)}), 500
    
@app.route('/persons', methods=['GET'])
def get_persons():
    filtru_varsta = request.args.get('varsta', type=int)

    persons = []
    for filename in os.listdir(person_dir):
        if filename.endswith('.json'):
            file_path = os.path.join(person_dir, filename)
            with open(file_path, 'r') as json_file:
                person_info = json.load(json_file)
                if filtru_varsta is None or person_info['varsta'] == filtru_varsta:
                    persons.append({
                        "nume": person_info['nume'],
                        "prenume": person_info['prenume']
                    })

    return jsonify(persons), 200

@app.route('/person/<nume>/<prenume>', methods=['GET'])
def get_persoana(nume, prenume):
    filename = f'{nume}_{prenume}.json'
    file_path = os.path.join(person_dir, filename)

    if not os.path.exists(file_path):
        return jsonify({'error': 'Person not found'}), 404
    
    with open(file_path, 'r') as json_file:
        person_info = json.load(json_file)

    return jsonify(person_info), 200

if __name__ == '__main__':
    app.run(debug=True)