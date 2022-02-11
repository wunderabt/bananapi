#!/usr/bin/env python3

import datetime
import netrc
from typing import Tuple, List
from fritzconnection import FritzConnection
from fritzconnection.lib.fritzhomeauto import FritzHomeAutomation

from influxdb import InfluxDBClient

FRITZ_ADDRESS = "fritz.box"


def get_credentials(hostname: str) -> Tuple[str, str, str]:
    return netrc.netrc().authenticators(hostname)


def get_fritz_connection(credentials: Tuple[str, str, str]) -> FritzConnection:
    return FritzConnection(address=FRITZ_ADDRESS, password=credentials[2])


def get_thermostat_readings(fritzconn: FritzConnection) -> List[Tuple[str, float, float]]:
    """
    returns a list of 3-tuples with (device_name, current_temperature, set_temperature)
    """
    fh = FritzHomeAutomation(fritzconn)
    infos = [(x["NewDeviceName"], float(x["NewTemperatureCelsius"]/10), float(x["NewHkrSetTemperature"]/10)) for x in fh.device_information()
             if x["NewProductName"] == "FRITZ!DECT 301" and x["NewTemperatureIsValid"] == "VALID"]
    return infos


def push_to_influx(thermostat_infos: List[Tuple[str, float]]) -> None:
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


if __name__ == "__main__":
    fc = get_fritz_connection(get_credentials(FRITZ_ADDRESS))
    ti = get_thermostat_readings(fc)
    #print(ti)
    push_to_influx(ti)

