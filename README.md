# crowsnest-connector-udp-nmea

A crowsnest microservice for connecting to NMEA UDP stream

### How it works

For now, this microservice jsut does the basics.

- Connects to UPD
- Listens on the continuous stream
- Transform these 0183 or 2000 NMEA senteces
- Wraps into a brefv message and outputs over MQTT

### Typical setup (docker-compose)

```yaml
version: "3"
services:
  ouster-lidar:
    image: ghcr.io/mo-rise/crowsnest-connector-lidar-ouster:latest
    restart: unless-stopped
    network_mode: "host"
    environment:
      - MQTT_BROKER_HOST=localhost
      - MQTT_BROKER_PORT=1883
      - MQTT_TOPIC_POINTCLOUD=CROWSNEST/<platform>/LIDAR/<device_id>/POINTCLOUD
      - OUSTER_HOSTNAME=<IP of sensor>
      - OUSTER_ATTITUDE=90,45,180
      - POINTCLOUD_FREQUENCY=2
```

## Development setup

To setup the development environment:

    python3 -m venv venv
    source ven/bin/activate

Install everything thats needed for development:

    pip install -r requirements_dev.txt

To run the linters:

    black main.py tests
    pylint main.py

To run the tests:

    no automatic tests yet...

Add breaf as submodule:

```basch

git submodule add <url>


# Once the project is added to your repo, you have to init and update it.

git submodule init
git submodule update

```

## License

Apache 2.0, see [LICENSE](./LICENSE)
