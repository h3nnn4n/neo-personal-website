from django.conf import settings
from influxdb import InfluxDBClient
from memoize import memoize


def _influxdb():
    return InfluxDBClient(
        settings.INFLUXDB_HOST,
        settings.INFLUXDB_PORT,
        settings.INFLUXDB_USER,
        settings.INFLUXDB_PASSWORD,
        settings.INFLUXDB_DATABASE,
        timeout=settings.INFLUXDB_TIMEOUT,
        ssl=getattr(settings, "INFLUXDB_SSL", False),
        verify_ssl=getattr(settings, "INFLUXDB_VERIFY_SSL", False),
    )


def influxdb_query(query: str):
    client = _influxdb()
    return client.query(query)


@memoize(timeout=10, unless=settings.DEBUG)
def get_setpoint():
    query = """
    SELECT median("value") FROM "pid_state" WHERE ("key" = 'setpoint') AND time >= now() - 30m and time <= now() GROUP BY time(10s), "key" fill(null)
    """
    result = influxdb_query(query)
    return tuple(result.raw["series"][0]["values"][-1])


@memoize(timeout=10, unless=settings.DEBUG)
def get_temperature():
    query = """
    SELECT median("value") FROM "pid_state" WHERE ("key" = 'input') AND time >= now() - 30m and time <= now() GROUP BY time(10s), "key" fill(null)
    """
    result = influxdb_query(query)
    return tuple(result.raw["series"][0]["values"][-1])
