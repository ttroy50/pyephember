"""
PyEphEmber interface implementation for https://ember.ephcontrols.com/
"""


import logging
import json
import datetime
from enum import Enum
import requests

_LOGGER = logging.getLogger(__name__)


class ZoneMode(Enum):
    """
    Modes that a zone can be set too
    """
    AUTO = 0
    ALL_DAY = 1
    ON = 2
    OFF = 3


def zone_is_active(zone):
    """
    Check if the zone is on.
    This is a bit of a hack as the new API doesn't have a currently
    active variable
    """
    if zone["prefix"]:
        if " off " in zone["prefix"]:
            return False
        if "active " in zone["prefix"]:
            return True
        if "ON mode" in zone["prefix"]:
            return True
    return zone["isboostactive"] or zone["isadvanceactive"]


def zone_name(zone):
    """
    Get zone name
    """
    return zone["name"]


def zone_is_hot_water(zone):
    """
    Is this a hot water zone
    """
    return zone["ishotwater"]


def zone_is_boost_active(zone):
    """
    Is the boost active for the zone
    """
    return zone["isboostactive"]


def zone_target_temperature(zone):
    """
    Get target temperature for this zone
    """
    return zone["targettemperature"]


def zone_current_temperature(zone):
    """
    Get current temperature for this zone
    """
    return zone["currenttemperature"]


def zone_mode(zone):
    """
    Get mode for this zone
    """
    return ZoneMode(zone['mode'])


class EphEmber:
    """
    Interacts with a EphEmber thermostat via API.
    Example usage: t = EphEmber('me@somewhere.com', 'mypasswd')
                   t.getZoneTemperature('myzone') # Get temperature
    """

    # pylint: disable=too-many-instance-attributes

    def _requires_refresh_token(self):
        """
        Check if a refresh of the token is needed
        """
        expires_on = self._login_data["last_refresh"] + \
            datetime.timedelta(seconds=self._refresh_token_validity_seconds)
        refresh = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        return expires_on < refresh

    def _request_token(self, force=False):
        """
        Request a new auth token
        """
        if self._login_data is None:
            raise RuntimeError("Don't have a token to refresh")

        if not force:
            if not self._requires_refresh_token():
                # no need to refresh as token is valid
                return True

        headers = {
            "Accept": "application/json",
            'Authorization': self._login_data['data']['refresh_token']
        }

        url = "{}{}".format(self.api_base_url, "appLogin/refreshAccessToken")

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            if response.status_code == 403:
                self._login_data = None
            return False

        refresh_data = response.json()

        if refresh_data.get('status', 9) != 0:
            if response.status_code == 403:
                self._login_data = None
            return False

        if 'token' not in refresh_data.get('data', {}):
            return False

        self._login_data['data'] = refresh_data['data']
        self._login_data['last_refresh'] = datetime.datetime.utcnow()

        return True

    def _login(self):
        """
        Login using username / password and get the first auth token
        """
        self._login_data = None
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        url = "{}{}".format(self.api_base_url, "appLogin/login")

        data = {'userName': self._username,
                'password': self._password}

        response = requests.post(url, data=json.dumps(
            data), headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        self._login_data = response.json()
        if self._login_data['status'] != 0:
            self._login_data = None
            return False
        self._login_data["last_refresh"] = datetime.datetime.utcnow()

        if ('data' in self._login_data
                and 'token' in self._login_data['data']):
            return True

        self._login_data = None
        return False

    def _do_auth(self):
        """
        Do authentication to the system (if required)
        """
        if self._login_data is None:
            return self._login()

        return self._request_token()

    def _get_first_gateway_id(self):
        """
        Get the first gatewayid associated with the account
        """
        if not self._homes:
            raise RuntimeError("Cannot get gateway id from list of homes.")
        return self._homes[0]['gatewayid']

    # Public interface
    def list_homes(self):
        """
        List the homes available for this user
        """
        if not self._do_auth():
            raise RuntimeError("Unable to login")

        url = "{}{}".format(self.api_base_url, "homes/list")
        headers = {
            "Accept": "application/json",
            'Authorization':
                self._login_data["data"]["token"]
        }

        response = requests.get(
            url, headers=headers, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(
                "{} response code when getting home".format(
                    response.status_code))

        homes = response.json()
        status = homes.get('status', 1)
        if status != 0:
            raise RuntimeError("Error getting home: {}".format(status))

        return homes.get("data", [])

    def get_home(self, gateway_id=None):
        """
        Get the data about a home.
        If not gateway_id is passed. A list_homes call is made and the
        first gateway from that is used.
        """
        now = datetime.datetime.utcnow()
        if self._home and now < self._home_refresh_at:
            return self._home

        if not self._do_auth():
            raise RuntimeError("Unable to login")

        if gateway_id is None:
            if not self._homes:
                self._homes = self.list_homes()
            gateway_id = self._get_first_gateway_id()

        url = "{}{}".format(self.api_base_url, "zones/polling")

        data = {
            "gateWayId": gateway_id
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Authorization':
                self._login_data["data"]["token"]
        }

        response = requests.post(
            url, data=json.dumps(
                data), headers=headers, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(
                "{} response code when getting home".format(
                    response.status_code))

        home = response.json()

        if self._cache_home:
            self._home = home
            self._home_refresh_at = (datetime.datetime.utcnow()
                                     + datetime.timedelta(minutes=5))

        status = home.get('status', 1)
        if status != 0:
            raise RuntimeError(
                "Error getting zones from home: {}".format(status))

        return home["data"]

    def get_zones(self):
        """
        Get all zones
        """
        home_data = self.get_home()
        if not home_data:
            return []

        return home_data

    def get_zone_names(self):
        """
        Get the name of all zones
        """
        zone_names = []
        for zone in self.get_zones():
            zone_names.append(zone['name'])

        return zone_names

    def get_zone(self, name):
        """
        Get the information about a particular zone
        """
        for zone in self.get_zones():
            if name == zone['name']:
                return zone

        raise RuntimeError("Unknown zone")

    def is_zone_active(self, name):
        """
        Check if a zone is active
        """
        zone = self.get_zone(name)
        if zone is None:
            raise RuntimeError("Unable to get zone")

        return zone_is_active(zone)

    def get_zone_temperature(self, name):
        """
        Get the temperature for a zone
        """
        zone = self.get_zone(name)

        if zone is None:
            raise RuntimeError("Unknown zone")

        return zone_current_temperature(zone)

    def is_boost_active(self, name):
        """
        Check if a zone is active
        """
        zone = self.get_zone(name)

        if zone is None:
            raise RuntimeError("Unknown zone")

        return zone_is_boost_active(zone)

    def is_target_temperature_reached(self, name):
        """
        Check if a zone is active
        """
        zone = self.get_zone(name)

        if zone is None:
            raise RuntimeError("Unknown zone")
        return zone_current_temperature(zone) >= zone_target_temperature(zone)

    def set_target_temperature_by_id(self, zone_id, target_temperature):
        """
        Set the target temperature for a zone by id
        """
        if not self._do_auth():
            raise RuntimeError("Unable to login")

        data = {
            "zoneid": zone_id,
            "temperature": target_temperature
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Authorization':
                self._login_data["data"]["token"]
        }

        url = "{}{}".format(self.api_base_url, "zones/setTargetTemperature")

        response = requests.post(url, data=json.dumps(
            data), headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        zone_change_data = response.json()

        return zone_change_data.get("status", 1) == 0

    def set_target_temperture_by_name(self, name, target_temperature):
        """
        Set the target temperature for a zone by name
        """
        zone = self.get_zone(name)

        if zone is None:
            raise RuntimeError("Unknown zone")

        return self.set_target_temperature_by_id(zone["zoneid"],
                                                 target_temperature)

    def activate_boost_by_id(self, zone_id, target_temperature, num_hours=1):
        """
        Activate boost for a zone based on the numeric id
        """
        if not self._do_auth():
            raise RuntimeError("Unable to login")

        data = {
            "zoneid": zone_id,
            "hours": num_hours,
            "temperature": target_temperature
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Authorization':
                self._login_data["data"]["token"]
        }

        url = "{}{}".format(self.api_base_url, "zones/boost")

        response = requests.post(url, data=json.dumps(
            data), headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        boost_data = response.json()

        return boost_data.get("status", 1) == 0

    def activate_boost_by_name(self,
                               name,
                               target_temperature,
                               num_hours=1):
        """
        Activate boost by the name of the zone
        """

        zone = self.get_zone(name)
        if zone is None:
            raise RuntimeError("Unknown zone")

        return self.activate_boost_by_id(zone["zoneid"],
                                         target_temperature, num_hours)

    def deactivate_boost_by_id(self, zone_id):
        """
        Deactivate boost for a zone based on the numeric id
        """
        if not self._do_auth():
            raise RuntimeError("Unable to login")

        data = {"zoneid": zone_id}

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Authorization':
                self._login_data["data"]["token"]
        }

        url = "{}{}".format(self.api_base_url, "zones/cancelBoost")
        response = requests.post(url, data=json.dumps(
            data), headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        boost_data = response.json()

        return boost_data.get("status", 1) == 0

    def deactivate_boost_by_name(self, name):
        """
        Deactivate boost by the name of the zone
        """

        zone = self.get_zone(name)
        if zone is None:
            raise RuntimeError("Unknown zone")

        return self.deactivate_boost_by_id(zone["zoneid"])

    def set_mode_by_id(self, zone_id, mode):
        """
        Set the mode by using the zone id
        Supported zones are available in the enum Mode
        """
        if not self._do_auth():
            raise RuntimeError("Unable to login")

        data = {
            "zoneid": zone_id,
            "model": mode.value
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Authorization':
                self._login_data["data"]["token"]
        }

        url = "{}{}".format(self.api_base_url, "zones/setModel")
        response = requests.post(url, data=json.dumps(
            data), headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        mode_data = response.json()

        return mode_data.get("status", 1) == 0

    def set_mode_by_name(self, name, mode):
        """
        Set the mode by using the name of the zone
        """
        zone = self.get_zone(name)
        if zone is None:
            raise RuntimeError("Unknown zone")

        return self.set_mode_by_id(zone["zoneid"], mode)

    def get_zone_mode(self, name):
        """
        Get the mode for a zone
        """
        zone = self.get_zone(name)

        if zone is None:
            raise RuntimeError("Unknown zone")

        return zone_mode(zone)

    def reset_login(self):
        """
        reset the login data to force a re-login
        """
        self._login_data = None

    # Ctor
    def __init__(self, username, password, cache_home=False):
        """Performs login and save session cookie."""

        self._login_data = None
        self._username = username
        self._password = password

        # This is the list of homes / gateways associated with the account.
        self._homes = None

        # This is the details of the home / zones for a single  home.
        self._cache_home = cache_home
        self._home_refresh_at = None
        self._home = None

        self.api_base_url = 'https://eu-https.topband-cloud.com/ember-back/'
        self._refresh_token_validity_seconds = 1800

        if not self._login():
            raise RuntimeError("Unable to login.")
