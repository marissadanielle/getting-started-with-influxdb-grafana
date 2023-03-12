from flask import Flask
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import random

app = Flask(__name__)

org = 'test'
bucket = 'test'
token = '74nk_oba0aQ44sevrbHBaK1mwC-3Saz3OdO5zbxCthI-xedAidr0S4pEuKGadvBO9nS92iF4vsKHhH8KytDspA=='

# store url of influxDB instance
url = 'http://influxdb:8086'

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org,
    debug=True
)


write_api = client.write_api(write_options=SYNCHRONOUS)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

# route to add a datapoint
@app.route('/influx', methods=["POST"])
def add_data():
    """Accept point measurements and inserts them to influxdb."""
    p = influxdb_client.Point("measurement").tag("location", "test")\
        .field("temperature", random.randint(0, 100))\
        .field("humidity", random.randint(0, 100))\
        .field("wind", random.randint(-10, 10))\
    
    write_api.write(bucket=bucket, org=org, record=p)
    return "ok"


@app.route('/data', methods=['GET'])
def query():
    query_api = client.query_api()
    query = 'from(bucket:"test")\
        |> range(start: -10)\
        |> filter(fn:(r) => r._measurement == "measurement")\
        |> filter(fn:(r) => r.location == "test")\
        |> filter(fn:(r) => r._field == "temperature")'
    result = query_api.query(org=org, query=query)
    results = []
    print("hello")
    for table in result:
        for record in table.records:
            results.append((record.get_field(), record.get_value()))

    print(results)
    return results

# TODO process to read data from LORA sensor periodically

# TODO write data to influx db
# https://github.com/influxdata/influxdb-client-python

# Restructure raw sensor data -> influx data

# Work on static data


if __name__ == "__main__":
    app.run(debug=True, port=8080)
