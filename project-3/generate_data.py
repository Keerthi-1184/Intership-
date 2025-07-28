import pandas as pd
import random
import numpy as np

def generate_data(num_samples=1000):
    data = {
        'sqft': np.random.randint(800, 5000, size=num_samples),
        'beds': np.random.randint(1, 6, size=num_samples),
        'bath': np.random.randint(1, 5, size=num_samples),
        'year_built': np.random.randint(1900, 2023, size=num_samples),
        'zip': np.random.randint(10000, 99999, size=num_samples),
        'price': np.random.randint(100000, 1000000, size=num_samples),
        'lot_size': np.random.randint(1000, 10000, size=num_samples),
        'floor_count': np.random.randint(1, 4, size=num_samples),
        'construction_material' : random.choices(['Brick', 'Wood', 'Concrete'], k=num_samples),
        'neightborhood' : random.choice(['Downtown', 'Suburb', 'Uptown'], k=num_samples),
        'distance_to_school' : np.random.uniform(0.1, 10.0, size=num_samples),
        'distance_to_transport' : np.random.uniform(0.1, 5.0, size=num_samples),
        'local_income_avg' : np.random.randint(30000, 150000, size=num_samples),
        'property_tax' : np.random.uniform(0.5, 3.0, size=num_samples),
        'mortgage_rate' : np.random.uniform(2.5, 7.5, size=num_samples),
        'listed_month' : random.choice(['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'], k=num_samples),
        'days_on_market': np.random.randint(1, 180, size=num_samples)
    }

    df = pd.DataFrame(data)

    print(df.head())

    df.to_csv('data/synthetic_house_prices.csv', index=False)
    print("Data saved to 'data/synthetic_house_prices.csv'")

if __name__== "__main__":
    generate_data()