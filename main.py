from copy import error
import logging
from typing import Any
import warnings
import threading
import socket
import struct
import pynmea2

from datetime import datetime, timezone
from streamz import Stream
from environs import Env
from paho.mqtt.client import Client as MQTT

from brefv_spec.envelope import Envelope
from brefv_spec.messages.position import Position 

# Reading config from environment variables
env = Env()
MQTT_BROKER_HOST: str = env("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT: int = env.int("MQTT_BROKER_PORT", 1883)
MQTT_CLIENT_ID: str = env("MQTT_CLIENT_ID", None)
MQTT_TRANSPORT: str = env("MQTT_TRANSPORT", "tcp")
MQTT_TLS: bool = env.bool("MQTT_TLS", False)
MQTT_USER: str = env("MQTT_USER", None)
MQTT_PASSWORD: str = env("MQTT_PASSWORD", None)
MQTT_TOPIC_RAW: str = env("MQTT_TOPIC_RAW", "CROWSNEST/PLATFORM/SENSOR/ID/RAW")
MQTT_TOPIC_JSON: str = env("MQTT_TOPIC_JSON", "CROWSNEST/PLATFORM/SENSOR/ID/JSON")

MCAST_GRP: str = env("MCAST_GRP", "239.192.0.3")
MCAST_PORT: int = env.int("MCAST_PORT", 60003)


# Setup logger
LOG_LEVEL = env.log_level("LOG_LEVEL", logging.INFO)
logging.basicConfig(level=LOG_LEVEL)
logging.captureWarnings(True)
warnings.filterwarnings("once")
LOGGER = logging.getLogger("crowsnest-connector-upd-nmea")


# Create mqtt client and configure it according to configuration
mq = MQTT(client_id=MQTT_CLIENT_ID, transport=MQTT_TRANSPORT)
mq.username_pw_set(MQTT_USER, MQTT_PASSWORD)

if MQTT_TLS:
    mq.tls_set()

mq.enable_logger(LOGGER)


def to_brefv_raw(in_msg):
    """Raw in message to brefv envelope"""

    envelope = Envelope(
        sent_at=datetime.now(timezone.utc).isoformat(),
        message=in_msg,
    )
    LOGGER.debug("Assembled into brefv envelope: %s", envelope)
    return envelope.json()




def to_mqtt(payload: Any, topic: str):
    """Publish a payload to a mqtt topic"""

    LOGGER.debug("Publishing on %s with payload: %s", topic, payload)
    try:
        mq.publish(
            topic,
            payload,
        )
    except Exception:  # pylint: disable=broad-except
        LOGGER.exception("Failed publishing to broker!")


def listen_multicast_nmea_0183(source):
    """Multicast input"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        source.emit(sock.recv(10240))
        LOGGER.info(sock.recv(10240))


def pars_nmea(nmea_msg_bytes):
    """Parsing ANavS NMEA sentences"""

    nmea_parameters = {
        "timestamp": None,
        "lat": None,
        "lat_dir": None,
        "lon": None,
        "lon_dir": None,
        "sog": None,
        "cog": None,
        "rot": None,
        "heading": None,
        "altitude": None,
        "gps_quality": None,
        "num_satellites": None,
    }

    nmea_msg = nmea_msg_bytes.decode("utf-8")
    LOGGER.info(nmea_msg)
    nmea_list = nmea_msg.split("\r")

    for nmea_str in nmea_list:
        nmea_str = "$" + nmea_str.split("$")[-1]

        try:
            nmea_type_msg = nmea_str.split(",")[0].replace("$", "")

            if nmea_type_msg == "PASHR":
                PASHR_items = nmea_str.split(",")
                PASHR = {
                    "heading": float(PASHR_items[2]),
                    "roll": float(PASHR_items[4]),
                    "pitch": float(PASHR_items[5]),
                    "roll_accuracy": float(PASHR_items[7]),
                    "heading_accuracy": float(PASHR_items[9]),
                }
                nmea_parameters.update(PASHR)

            msg = pynmea2.parse(nmea_str)

            if msg.sentence_type == "GGA":
                GGA = {
                    "timestamp": msg.timestamp.isoformat(),
                    "longitude": float(msg.lon) /100,
                    "longitude_dir": msg.lon_dir,
                    "latitude": float(msg.lat) /100,
                    "latitude_dir": msg.lat_dir,
                    "altitude": msg.altitude,
                    "num_satellites": int(msg.num_sats),
                    "gps_quality": msg.gps_qual,
                }
                nmea_parameters.update(GGA)

            elif msg.sentence_type == "RMC":
                RMC = {
                    "datestamp": msg.datestamp.isoformat(),
                }
                nmea_parameters.update(RMC)

            elif msg.sentence_type == "VTG":
                VTG = {
                    "sog": msg.spd_over_grnd_kts,
                    "cog": msg.true_track,
                }
                nmea_parameters.update(VTG)

            elif msg.sentence_type == "ROT":
                ROT = {
                    "rot": msg.rate_of_turn,
                }
                nmea_parameters.update(ROT)

            elif msg.sentence_type == "GST":
                GST = {
                    "std_dev_altitude": msg.std_dev_altitude,
                    "std_dev_longitude": msg.std_dev_longitude,
                    "std_dev_latitude": msg.std_dev_latitude,
                }
                nmea_parameters.update(GST)

        except Exception as e:
            LOGGER.info(e)
            pass
    LOGGER.info(nmea_parameters)

    return nmea_parameters


def to_brefv_nmea(GNSS_parameters):
    """NMEA in message to brefv envelope"""

    # TODO: Create brefv format 

    envelope = Envelope(
        sent_at=datetime.now(timezone.utc).isoformat(),
        message=GNSS_parameters,
    )
    LOGGER.debug("Assembled into brefv envelope: %s", envelope)
    return envelope.json()



if __name__ == "__main__":

    # Build pipeline
    LOGGER.info("Building pipeline...")
    LOGGER.info("Connecting to multicast...")

    source = Stream()

    # RAW MQTT stream
    pipe_to_brefv_raw = source.map(to_brefv_raw).sink(to_mqtt, topic=MQTT_TOPIC_RAW)

    # JSON MQTT stream
    pipe_to_brefv_json = source.map(pars_nmea).map(to_brefv_raw).sink(to_mqtt, topic=MQTT_TOPIC_JSON)

    LOGGER.info("Connecting to MQTT broker...")
    mq.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

    # Socket Multicast runs in the foreground so we put the MQTT stuff in a separate thread
    threading.Thread(target=mq.loop_forever, daemon=True).start()

    # MAIN listener
    listen_multicast_nmea_0183(source)
