import datetime
import json
import os

import requests


def remote_address(request):
    """
    Get IP from a request by user

    :param value: request
    :return: IP
    """

    ip = ""
    # https://stackoverflow.com/a/48223489/645458
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
        print(f"x={ip}")
    else:
        ip = request.META.get("REMOTE_ADDR")
        print(f"r={ip}")
    return ip


def get_geo_data(ip):
    api_key = os.environ.get("ABSTRACT_GEOIP_KEY")
    url = f"https://ipgeolocation.abstractapi.com/v1/?api_key={api_key}&ip_address={ip}"
    response = requests.get(url)
    if response.ok:
        return json.loads(response.content)


def get_holiday_data(country_code):
    api_key = os.environ.get("ABSTRACT_HOLIDAY_KEY")
    now = datetime.now()
    url = f"https://holidays.abstractapi.com/v1/?api_key={api_key}&country={country_code}&year={now.year}&month={now.month}&day={now.day}"
    response = requests.get(url)
    if response.ok:
        return json.loads(response.content)
