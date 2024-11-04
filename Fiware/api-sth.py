import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import requests
from datetime import datetime
import pytz

# Constants for IP and port
IP_ADDRESS = "20.201.112.53"
PORT_STH = 8666
DASH_HOST = "0.0.0.0"  # Set this to "0.0.0.0" to allow access from any IP

# Function to get luminosity data from the API
def get_luminosity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Lamp/id/urn:ngsi-ld:Lamp:03x/attributes/luminosity?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error: {e}")
            return []
    else:
        print(f"Error accessing {url}: {response.status_code}")
        return []
    
def get_humidity_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Humi/id/urn:ngsi-ld:Humi:03x/attributes/humidity?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error: {e}")
            return []
    else:
        print(f"Error accessing {url}: {response.status_code}")
        return []
    
def get_temperature_data(lastN):
    url = f"http://{IP_ADDRESS}:{PORT_STH}/STH/v1/contextEntities/type/Temp/id/urn:ngsi-ld:Temp:03x/attributes/temperature?lastN={lastN}"
    headers = {
        'fiware-service': 'smart',
        'fiware-servicepath': '/'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        try:
            values = data['contextResponses'][0]['contextElement']['attributes'][0]['values']
            return values
        except KeyError as e:
            print(f"Key error: {e}")
            return []
    else:
        print(f"Error accessing {url}: {response.status_code}")
        return []

# Set lastN value
lastN = 10  # Get 10 most recent points at each interval

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('LumiTemp Data Viewer'),
    dcc.Graph(id='lumitemp-graph'),
    # Store to hold historical data
    dcc.Store(id='data-store', data={'timestamps': [], 'luminosity_values': [], 'humidity_values': [], 'temperature_values': []}),
    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds (10 seconds)
        n_intervals=0
    )
])

@app.callback(
    Output('data-store', 'data'),
    Input('interval-component', 'n_intervals'),
    State('data-store', 'data')
)
def update_data_store(n, stored_data):
    # Ensure all required keys exist
    stored_data.setdefault('timestamps', [])
    stored_data.setdefault('luminosity_values', [])
    stored_data.setdefault('humidity_values', [])
    stored_data.setdefault('temperature_values', [])

    # Get luminosity, humidity, and temperature data
    data_luminosity = get_luminosity_data(lastN)
    data_humidity = get_humidity_data(lastN)
    data_temperature = get_temperature_data(lastN)

    if data_luminosity:
        luminosity_values = [float(entry['attrValue']) for entry in data_luminosity]
        timestamps = [entry['recvTime'] for entry in data_luminosity]

        stored_data['timestamps'].extend(timestamps)
        stored_data['luminosity_values'].extend(luminosity_values)

    if data_humidity:
        humidity_values = [float(entry['attrValue']) for entry in data_humidity]
        timestamps = [entry['recvTime'] for entry in data_humidity]

        stored_data['timestamps'].extend(timestamps)
        stored_data['humidity_values'].extend(humidity_values)

    if data_temperature:
        temperature_values = [float(entry['attrValue']) for entry in data_temperature]
        timestamps = [entry['recvTime'] for entry in data_temperature]

        stored_data['timestamps'].extend(timestamps)
        stored_data['temperature_values'].extend(temperature_values)

    return stored_data

@app.callback(
    Output('lumitemp-graph', 'figure'),
    Input('data-store', 'data')
)

def update_graph(stored_data):
    if (stored_data['timestamps']) and (stored_data['luminosity_values'] or stored_data['humidity_values'] or stored_data['temperature_values']):
        # Calculate mean luminosity
        mean_luminosity = sum(stored_data['luminosity_values']) / len(stored_data['luminosity_values']) if stored_data['luminosity_values'] else 0
        mean_humidity = sum(stored_data['humidity_values']) / len(stored_data['humidity_values']) if stored_data['humidity_values'] else 0
        mean_temperature = sum(stored_data['temperature_values']) / len(stored_data['temperature_values']) if stored_data['temperature_values'] else 0

        # Create traces for the plot
        trace_luminosity = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['temperature_values'],
            mode='lines+markers',
            name='Luminosity',
            line=dict(color='orange')
        )
        
        trace_mean_luminosity = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_luminosity, mean_luminosity],
            mode='lines',
            name='Mean Luminosity',
            line=dict(color='orange', dash='dash')
        )
        
        trace_humidity = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['humidity_values'],
            mode='lines+markers',
            name='Humidity',
            line=dict(color='blue')
        )
        
        trace_mean_humidity = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_humidity, mean_humidity],
            mode='lines',
            name='Mean Humidity',
            line=dict(color='blue', dash='dash')
        )
        
        trace_temperature = go.Scatter(
            x=stored_data['timestamps'],
            y=stored_data['temperature_values'],
            mode='lines+markers',
            name='Temperature',
            line=dict(color='red')
        )
        
        trace_mean_temperature = go.Scatter(
            x=[stored_data['timestamps'][0], stored_data['timestamps'][-1]],
            y=[mean_temperature, mean_temperature],
            mode='lines',
            name='Mean Humidity',
            line=dict(color='red', dash='dash')
        )

        # Create figure
        fig = go.Figure(data=[trace_luminosity, trace_mean_luminosity, trace_humidity, trace_mean_humidity, trace_temperature, trace_mean_temperature])

        # Update layout
        fig.update_layout(
            title='Luminosity and Humidity Over Time',
            xaxis_title='Timestamp',
            yaxis_title='Values',
            hovermode='closest'
        )

        return fig

    return {}

if __name__ == '__main__':
    app.run_server(debug=True, host=DASH_HOST, port=8050)