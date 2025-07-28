from flask import Flask, render_template
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
 
app = Flask(__name__)
 
@app.route('/')
def index():
    # Data Simulation
    np.random.seed(0)  # For reproducibility
    dates = pd.date_range(start='2025-01-01', periods=10)
    sales = np.random.randint(1000, 5000, size=10)
    profit = np.random.randint(100, 1000, size=10)
 
    # Create DataFrame
    df = pd.DataFrame({
        'Sales': sales,
        'Profit': profit
    }, index=dates)
 
    # Data Analysis
    average_sales = df['Sales'].mean()
    total_profit = df['Profit'].sum()
    max_profit = df['Profit'].max()
 
    # Visualization: Generate plot
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df.index, df['Sales'], label='Sales', marker='o')
    ax.plot(df.index, df['Profit'], label='Profit', marker='x', linestyle='--')
    ax.set_title('Sales and Profit Over Time')
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount')
    ax.grid(True)
    ax.legend()
 
    # Save plot to a BytesIO object and encode as base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf-8')
    plt.close()  # Close the plot to free memory
 
    # Render the template with data
    return render_template('index.html',
                           table=df.to_html(classes='table'),
                           average_sales=average_sales,
                           total_profit=total_profit,
                           max_profit=max_profit,
                           plot_url=plot_url)
 
if __name__ == '__main__':
    app.run(debug=True)