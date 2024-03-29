import json
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
bootstrap_servers='localhost:9092', 
value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

# url = 'https://api.covid19india.org/data.json' # Specify the URL for the COVID-19 data source

# # One time data Covid
# response = requests.get(url) # Send a GET request to the URL
# data = response.json() # Get the JSON response
# message = data['cases_time_series']
# print("data <<<<<<<<<<<<< ", data['cases_time_series'])
# for data_dict in message:
#     producer.send('covid', value=data_dict)
# producer.flush()

# # Print the message
# print(f"Sent message: {data_dict}")

def get_user_input():
    try:
        daily_confirmed = input("Enter daily confirmed cases: ")
        daily_deceased = input("Enter daily deceased cases: ")
        daily_recovered = input("Enter daily recovered cases: ")
        total_confirmed = input("Enter total confirmed cases: ")
        total_deceased = input("Enter total deceased cases: ")
        total_recovered = input("Enter total recovered cases: ")

        current_date = datetime.now().strftime("%d %B %Y %H:%M:%S")
        current_date_ymd = datetime.now().strftime("%Y-%m-%d")

        data = {
            "dailyconfirmed": daily_confirmed,
            "dailydeceased": daily_deceased,
            "dailyrecovered": daily_recovered,
            "date": current_date,
            "dateymd": current_date_ymd,
            "totalconfirmed": total_confirmed,
            "totaldeceased": total_deceased,
            "totalrecovered": total_recovered
        }

        return data
    except Exception as e:
        print(f"Error occurred: {e}")
        return None
    
while True :
    message = get_user_input()

    # Send the message to the topic
    producer.send('covid_1', value=message)
    producer.flush()

    # Print the message
    print(f"Sent message: {message}")