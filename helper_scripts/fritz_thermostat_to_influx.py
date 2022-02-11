#!/usr/bin/env python3

import datetime
import netrc
from typing import Tuple, List, Dict
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation
from fritzconnection.lib.fritzstatus import FritzStatus

from influxdb import InfluxDBClient

FRITZ_ADDRESS = "fritz.box"


def get_credentials(hostname: str) -> Tuple[str, str, str]:
    return netrc.netrc().authenticators(hostname)


def get_fritz_connection(credentials: Tuple[str, str, str]) -> FritzConnection:
    return FritzConnection(address=FRITZ_ADDRESS, user=credentials[0], password=credentials[2])


def get_thermostat_readings(fritzconn: FritzConnection) -> List[Tuple[str, float, float]]:
    """
    returns a list of 3-tuples with (device_name, current_temperature, set_temperature)
    """
    fh = FritzHomeAutomation(fritzconn)
    infos = [(x["NewDeviceName"], float(x["NewTemperatureCelsius"]/10), float(x["NewHkrSetTemperature"]/10)) for x in fh.device_information()
             if x["NewProductName"] == "FRITZ!DECT 301" and x["NewTemperatureIsValid"] == "VALID"]
    return infos


def get_status_info(fritzconn: FritzConnection):
    fs = FritzStatus(fritzconn)
    info = {
        "modelname": fs.modelname,
        "data" : {
            "data_transfer": {
                "bytes_received": fs.bytes_received,
                "bytes_sent": fs.bytes_sent,
            },
            "uptime": {
                "connection_uptime": fs.connection_uptime,
                "device_uptime": fs.device_uptime,
            }
        }
    }
    return info

def push_to_influx(thermostat_infos: List[Tuple[str, float]], fritz_status_info: Dict) -> None:
    timestamp = datetime.datetime.now()
    client = InfluxDBClient("troi", 8086, "influxdb", "influxdb", "heating")
    points = [
        {
            "measurement": "temperature",
            "tags": {"device": x[0]},
            "fields": {"C": x[1], "target_C": x[2]},
            "time": timestamp.isoformat()
        } for x in thermostat_infos
    ]
    client.write_points(points)

    client = InfluxDBClient("troi", 8086, "influxdb", "influxdb", "fritzstatus")
    points = []
    for topkey, subdict in fritz_status_info["data"].items():
        points.append(
            {
                "measurement": topkey,
                "tags": {"device": fritz_status_info["modelname"]},
                "fields": subdict,
                "time": timestamp.isoformat()
            }
        )
    client.write_points(points)


if __name__ == "__main__":
    fc = get_fritz_connection(get_credentials(FRITZ_ADDRESS))
    ti = get_thermostat_readings(fc)
    si = get_status_info(fc)
    #print(ti)
    push_to_influx(ti, si)

