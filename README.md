
How to run all containers (grafana, influx, flask-sensor-app...)
```
docker compose -f influx-grafana-chronograf-compose.yml up

# run in background (-d)
docker compose -f influx-grafana-chronograf-compose.yml up -d 

# to stop the containers
docker compose -f influx-grafana-chronograf-compose.yml stop

# stop containers / remove
docker compose -f influx-grafana-chronograf-compose.yml down
```
