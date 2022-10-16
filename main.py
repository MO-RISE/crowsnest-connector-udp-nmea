import logging
from typing import Any
import warnings
import threading
import socket
import struct

from streamz import Stream
from environs import Env
from paho.mqtt.client import Client as MQTT

# from bresfv.envelope import Envelope


# Reading config from environment variables
env = Env()
MQTT_BROKER_HOST: str = env("MQTT_BROKER_HOST", "localhost")
MQTT_BROKER_PORT: int = env.int("MQTT_BROKER_PORT", 1883)
MQTT_CLIENT_ID: str = env("MQTT_CLIENT_ID", None)
MQTT_TRANSPORT: str = env("MQTT_TRANSPORT", "tcp")
MQTT_TLS: bool = env.bool("MQTT_TLS", False)
MQTT_USER: str = env("MQTT_USER", None)
MQTT_PASSWORD: str = env("MQTT_PASSWORD", None)
MQTT_TOPIC: str = env("MQTT_TOPIC", "SENSOR/TOPIC")
SENSOR_FREQUENCY: float = env.float("SENSOR_FREQUENCY", default=2)
MCAST_GRP: str = env("MCAST_GRP", "239.192.0.3")
MCAST_PORT: int = env.int("MCAST_PORT", 60003)


# Setup logger
LOG_LEVEL = env.log_level("LOG_LEVEL", logging.WARNING)
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


# def to_brefv(pcd: np.ndarray) -> Envelope:
#     """From point cloud to brefv envelope"""

#     envelope = Envelope(
#         sent_at=datetime.now(timezone.utc).isoformat(),
#         message=pcd.tolist(),
#     )

#     LOGGER.debug("Assembled into brefv envelope: %s", envelope)

#     return envelope.json()


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


def multicast_nmea_0183(source):
    """Multicast input"""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


    sock.bind((MCAST_GRP, MCAST_PORT))
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)

    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    while True:
        source.emit(sock.recv(10240))
        print(sock.recv(10240))




if __name__ == "__main__":

    # Build pipeline
    LOGGER.info("Building pipeline...")
    LOGGER.info("Connecting to multicast...")

    source = Stream()

    # # pipe_to_brefv = (
    # #     source.latest()
    # #     .rate_limit(1 / POINTCLOUD_FREQUENCY)
    # #     .map(partial(rotate_pcd, attitude=OUSTER_ATTITUDE))
    # #     .map(to_brefv)
    # # )

    # # pipe_to_brefv.sink(partial(to_mqtt, topic=MQTT_TOPIC_POINTCLOUD))

    # LOGGER.info("Connecting to MQTT broker...")
    # mq.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)

    # # Ouster SDK runs in the foreground so we put the MQTT stuff in a separate thread
    # threading.Thread(target=mq.loop_forever, daemon=True).start()

    multicast_nmea_0183(source)
