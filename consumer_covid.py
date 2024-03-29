import json
from kafka import KafkaConsumer
from matplotlib import pyplot as plt
import matplotlib.animation as animation
from matplotlib.axis import Axis
from datetime import datetime
from matplotlib.dates import DateFormatter


consumer = KafkaConsumer(
    'covid_1',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

dates = []
dailyconfirmed = []
dailydeceased = []
dailyrecovered = []

# Initialize plot
fig, ax = plt.subplots()

lines = []
legend_added = False

ax.set_xlabel('Date')
ax.set_ylabel('Count')
ax.set_title('Live COVID Data')

def update(frame):
    for message in consumer:
        data = message.value
        # print("Data ************", data)
        date_time = datetime.strptime(data['date'], '%d %B %Y %H:%M:%S')
        # print("date time ?????? ", date_time)
        dates.append(date_time)
        if data['dailyconfirmed']:
            dailyconfirmed.append(int(data['dailyconfirmed']))
        else :
            dailyconfirmed.append(0)
        if data['dailydeceased']:
            dailydeceased.append(int(data['dailydeceased']))
        else :
            dailydeceased.append(0)
        if data['dailyrecovered']:
            dailyrecovered.append(int(data['dailyrecovered']))
        else :
            dailyrecovered.append(0)
        break  

    confirmed_line, = ax.plot(dates, dailyconfirmed, label='Daily Confirmed', color='blue', linestyle='-')
    deceased_line, = ax.plot(dates, dailydeceased, label='Daily Deceased', color='red', linestyle='--')
    recovered_line, = ax.plot(dates, dailyrecovered, label='Daily Recovered', color='green', linestyle='-.')
    
    # Add the lines to the list
    lines.extend([confirmed_line, deceased_line, recovered_line])

    ax.relim()
    ax.autoscale_view()
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %H:%M:%S'))
    global legend_added
    if not legend_added:
        ax.legend(loc='upper left')
        legend_added = True
    fig.autofmt_xdate()  
    return lines

ani = animation.FuncAnimation(fig, update, frames=None, blit=True, interval=1000)
 
def press(event):
    if event.key == 'q':
        ani.event_source.stop()
        fig.savefig("plot.png")
        print("Plot saved")

cid = fig.canvas.mpl_connect('key_press_event', press)

plt.show()


# from kafka import KafkaConsumer
# import dash
# from dash import dcc, html
# from dash.dependencies import Input, Output
# import plotly.graph_objs as go
# from datetime import datetime
# import json

# # Kafka consumer configuration
# consumer = KafkaConsumer(
#     'covid_new_data.',
#     bootstrap_servers='localhost:9092',
#     auto_offset_reset='earliest',
#     enable_auto_commit=False,
#     group_id='my-group',
#     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# )

# # Initialize the Dash app
# app = dash.Dash(__name__)

# # Initialize Kafka consumer (replace 'bootstrap_servers' and 'topic' with your Kafka server and topic)
# consumer = KafkaConsumer('covid', bootstrap_servers=['localhost:9092'])

# # Define layout of the dashboard
# app.layout = html.Div([
#     dcc.Graph(id='covid-graph'),
#     dcc.Interval(
#         id='interval-component',
#         interval=5000,  # in milliseconds, update every hour
#         n_intervals=0
#     )
# ])

# # Function to fetch and update data from Kafka
# def fetch_data():
#     # Fetch new data
#     for message in consumer:
#         new_data = message.value
#         # Parse the data if it's in JSON format, adjust this based on your actual data format
#         new_data = json.loads(new_data)
#     return new_data

# # Callback to update the graph
# @app.callback(Output('covid-graph', 'figure'),
#               [Input('interval-component', 'n_intervals')])
# def update_graph(n):
#     try:
#         # Fetch data
#         new_data = fetch_data()
        
#         print("Fetched data:", new_data)  # Print fetched data for debugging
        
#         if not new_data:
#             print("No data fetched")
#             return {'data': [], 'layout': {}}

#         # Prepare data for plotting
#         dates = [datetime.strptime(new_data['dateymd'], '%Y-%m-%d')]
#         dailyconfirmed = [int(new_data['dailyconfirmed'])]
#         dailydeceased = [int(new_data['dailydeceased'])]
#         dailyrecovered = [int(new_data['dailyrecovered'])]

#         # Create traces
#         confirmed_trace = go.Scatter(x=dates, y=dailyconfirmed, mode='lines', name='Daily Confirmed Cases')
#         deceased_trace = go.Scatter(x=dates, y=dailydeceased, mode='lines', name='Daily Deceased Cases')
#         recovered_trace = go.Scatter(x=dates, y=dailyrecovered, mode='lines', name='Daily Recovered Cases')

#         # Update layout
#         layout = go.Layout(title='COVID-19 Daily Cases',
#                            xaxis=dict(title='Date'),
#                            yaxis=dict(title='Number of Cases'))

#         # Create figure
#         fig = go.Figure(data=[confirmed_trace, deceased_trace, recovered_trace], layout=layout)

#         return fig

#     except Exception as e:
#         print("Error:", str(e))
#         return {'data': [], 'layout': {}}

# if __name__ == '__main__':
#     app.run_server(debug=True)

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# def animate(i):
#     xar = []
#     yar = []
#     for message in consumer:
#         data = message.value
#         print("Data ****** ", data['dailyconfirmed'], data['date'] )
#         xar.append(data['dailyconfirmed'])
#         yar.append(data['date'])
#     ax1.clear()
#     ax1.plot(xar,yar)

# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()