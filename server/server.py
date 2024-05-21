from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

file_paths = {
    'produits': 'data/produits.csv',
    'ventes'  : 'data/ventes.csv'  ,
    'magasins': 'data/magasins.csv'
}

def load_data(file_type):
    return pd.read_csv(file_paths[file_type], sep=";")

@app.route('/data/<file_type>', methods=['GET'])
def get_data(file_type):
    if file_type in file_paths:
        data = load_data(file_type)
        return jsonify(data.to_dict(orient='records'))
    else:
        return jsonify({'error': 'Invalid file type'}), 404

if __name__ == '__main__':
    app.run()
    
#http://localhost:5000/data/ventes
