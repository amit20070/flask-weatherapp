from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

# Replace with your actual API key
API_KEY = '97d33ec8d1c9460b86a63735253007'
BASE_URL = 'http://api.weatherapi.com/v1/current.json'

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        units = request.form.get('units', 'metric')
        
        # Make API request
        url = f"{BASE_URL}?key={API_KEY}&q={city}&aqi=no"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            weather_data = {
                'city': data['location']['name'],
                'country': data['location']['country'],
                'temperature': round(data['current']['temp_c'] if units == 'metric' else data['current']['temp_f']),
                'description': data['current']['condition']['text'],
                'icon': data['current']['condition']['icon'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        else:
            error = "City not found. Please try again."
    
    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    app.run(debug=True)
