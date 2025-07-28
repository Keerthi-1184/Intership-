from flask import Flask, render_template, request
import numpy as np
import pickle
import pandas  as pd

app = Flask(__name__)

# Load model
with open('model/house_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try: 
        sqft = float(request.form['sqft'])
        beds = int(request.form['beds'])
        bath = int(request.form['bath'])
        year_built = int(request.form['year_built'])
        zip = int(request.form['zip'])
        lot_size = float(request.form['lot_size'])
        floor_count = float(request.form['floor_count'])
        material = request.form['construction_material']
        neighborhood = request.form['neightborhood']
        distance_to_school = float(request.form['distance_to_school'])
        distance_to_transport = float(request.form['distance_to_transport'])
        local_income_avg = float(request.form['local_income_avg'])
        property_tax = float(request.form['property_tax'])
        mortgage_rate = float(request.form['mortgage_rate'])
        listed_month= request.form['listed_month']
        days_on_market = int(request.form['days_on_market'])

        input_data = np.array([[sqft, beds, bath, year_built, zip, lot_size, floor_count, material, neighborhood, distance_to_school, distance_to_transport, local_income_avg, property_tax, mortgage_rate, listed_month, days_on_market ]])
        
        price = model.predict(input_data)[0]
        return render_template('index.html', price=price)
    except Exception as e:
        return render_template('index.html', error="Error: " + str(e))


if __name__ == '__main__':
    app.run(debug=True)