import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pickle
from sklearn.preprocessing import StandardScaler
import os

# Load dataset
df = pd.read_csv('data/synthetic_house_prices.csv')

# Features and target
features=[col for col in ['sqft', 'beds', 'bath', 'year_built', 'zip', 'lot_size', 'floor_count', 'construction_material', 'neighborhood', 'distance_to_school', 'distance_to_transport', 'local_income_avg', 'property_tax', 'mortgage_rate', 'listed_month', 'days_on_market']if col in df.columns]
x = df[features]
categoricals = [col for col in ['construction_material', 'neighborhood', 'listed_month'] if col in df.columns]
if categoricals:
    x = pd.concat([x,pd.get_dummies(df[categoricals], drop_first=True)], axis=1)
y = df['price']

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_text_scaled = scaler.transform(X_test)
# Train model
model = LinearRegression()
model.fit(X_train_scaled, y_train)

os.makedirs("model", exist_ok=True)

# Save model
with open('model/house_model.pkl', 'wb') as f:
    pickle.dump(model, f)

with open('model/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

