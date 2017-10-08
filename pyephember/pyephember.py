"""
PyEphEmber interface implementation for https://ember.ephcontrols.com/
"""


import logging
import json
import datetime
import requests

_LOGGER = logging.getLogger(__name__)


class EphEmber:
    """Interacts with a EphEmber thermostat via API.
    Example usage: t = EphEmber('me@somewhere.com', 'mypasswd')
                   t.getZoneTemperature('myzone') # Get temperature
    """

    # pylint: disable=too-many-instance-attributes

    def _requires_refresh_token(self):
        """
        Check if a refresh of the token is needed
        """
        expires_on = datetime.datetime.strptime(
            self.login_data['token']['expiresOn'], '%Y-%m-%dT%H:%M:%SZ')
        refresh = datetime.datetime.utcnow() + datetime.timedelta(seconds=30)
        return expires_on < refresh

    def _request_token(self, force=False):
        """
        Request a new auth token
        """
        if self.login_data is None:
            raise RuntimeError("Don't have a token to refresh")

        if not force:
            if not self._requires_refresh_token():
                # no need to refresh as token is valid
                return True

        headers = {
            "Accept": "application/json",
            'Authorization':
                'Bearer ' + self.login_data['token']['accessToken']
        }

        url = self.api_base_url + "account/RefreshToken"

        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        refresh_data = response.json()

        if 'token' not in refresh_data:
            return False

        self.login_data['token']['accessToken'] = refresh_data['accessToken']
        self.login_data['token']['issuedOn'] = refresh_data['issuedOn']
        self.login_data['token']['expiresOn'] = refresh_data['expiresOn']

        return True

    def _login(self):
        """
        Login using username / password and get the first auth token
        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }

        url = self.api_base_url + "account/directlogin"

        data = {'Email': self.username,
                'Password': self.password,
                'RememberMe': 'True'}

        response = requests.post(url, data=data, headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        self.login_data = response.json()
        if not self.login_data['isSuccess']:
            self.login_data = None
            return False

        if ('token' in self.login_data
                and 'accessToken' in self.login_data['token']):
            self.home_id = self.login_data['token']['currentHomeId']
            self.user_id = self.login_data['token']['userId']
            return True

        self.login_data = None
        return False

    def _do_auth(self):
        """
        Do authentication to the system (if required)
        """
        if self.login_data is None:
            return self._login()

        return self._request_token()

    # Public interface
    def get_home(self, home_id=None):
        """
        Get the data about a home
        """
        now = datetime.datetime.utcnow()
        if self.home and now < self.home_refresh_at:
            return self.home

        if not self._do_auth():
            raise RuntimeError("Unable to login")

        if home_id is None:
            home_id = self.home_id

        url = self.api_base_url + "Home/GetHomeById"

        params = {
            "homeId": home_id
        }

        headers = {
            "Accept": "application/json",
            'Authorization':
                'bearer ' + self.login_data['token']['accessToken']
        }

        response = requests.get(
            url, params=params, headers=headers, timeout=10)

        if response.status_code != 200:
            raise RuntimeError(
                "{} response code when getting home".format(
                    response.status_code))

        home = response.json()

        if self.cache_home:
            self.home = home
            self.home_refresh_at = (datetime.datetime.utcnow()
                                    + datetime.timedelta(minutes=5))

        return home

    def get_zones(self):
        """
        Get all zones
        """
        home_data = self.get_home()
        if not home_data['isSuccess']:
            return []

        zones = []

        for receiver in home_data['data']['receivers']:
            for zone in receiver['zones']:
                zones.append(zone)

        return zones

    def get_zone_names(self):
        """
        Get the name of all zones
        """
        zone_names = []
        for zone in self.get_zones():
            zone_names.append(zone['name'])

        return zone_names

    def get_zone(self, zone_name):
        """
        Get the information about a particular zone
        """
        for zone in self.get_zones():
            if zone_name == zone['name']:
                return zone

        raise RuntimeError("Unknown zone")

    def is_zone_active(self, zone_name):
        """
        Check if a zone is active
        """
        zone = self.get_zone(zone_name)
        if zone is None:
            raise RuntimeError("Unable to get zone")

        return zone['isCurrentlyActive']

    def get_zone_temperature(self, zone_name):
        """
        Get the temperature for a zone
        """
        zone = self.get_zone(zone_name)

        if zone is None:
            raise RuntimeError("Unknown zone")

        return zone['currentTemperature']

    def is_boost_active(self, zone_name):
        """
        Check if a zone is active
        """
        zone = self.get_zone(zone_name)

        if zone is None:
            raise RuntimeError("Unknown zone")

        return zone['isBoostActive']

    def is_target_temperature_reached(self, zone_name):
        """
        Check if a zone is active
        """
        zone = self.get_zone(zone_name)

        if zone is None:
            raise RuntimeError("Unknown zone")

        return zone['isTargetTemperatureReached']

    def set_target_temperature_by_id(self, zone_id, target_temperature):
        """
        Set the target temperature for a zone by id
        """
        if not self._do_auth():
            raise RuntimeError("Unable to login")

        data = {
            "ZoneId": zone_id,
            "TargetTemperature": target_temperature
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Authorization':
                'Bearer ' + self.login_data['token']['accessToken']
        }

        url = self.api_base_url + "Home/ZoneTargetTemperature"

        response = requests.post(url, data=json.dumps(
            data), headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        zone_change_data = response.json()

        return zone_change_data.get("isSuccess", False)

    def set_target_temperture_by_name(self, zone_name, target_temperature):
        """
        Set the target temperature for a zone by name
        """
        zone = self.get_zone(zone_name)

        if zone is None:
            raise RuntimeError("Unknown zone")

        return self.set_target_temperature_by_id(zone["zoneId"],
                                                 target_temperature)

    def activate_boost_by_id(self, zone_id, target_temperature, num_hours=1):
        """
        Activate boost for a zone based on the numeric id
        """
        if not self._do_auth():
            raise RuntimeError("Unable to login")

        zones = [zone_id]
        data = {
            "ZoneIds": zones,
            "NumberOfHours": num_hours,
            "TargetTemperature": target_temperature
        }

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Authorization':
                'Bearer ' + self.login_data['token']['accessToken']
        }

        url = self.api_base_url + "Home/ActivateZoneBoost"

        response = requests.post(url, data=json.dumps(
            data), headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        boost_data = response.json()

        return boost_data.get("isSuccess", False)

    def activatae_boost_by_name(self,
                                zone_name,
                                target_temperature,
                                num_hours=1):
        """
        Activate boost by the name of the zone
        """

        zone = self.get_zone(zone_name)
        if zone is None:
            raise RuntimeError("Unknown zone")

        return self.activate_boost_by_id(zone["zoneId"],
                                         target_temperature, num_hours)

    def deactivate_boost_by_id(self, zone_id):
        """
        Deactivate boost for a zone based on the numeric id
        """
        if not self._do_auth():
            raise RuntimeError("Unable to login")

        zones = [zone_id]
        data = zones

        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            'Authorization':
                'Bearer ' + self.login_data['token']['accessToken']
        }

        url = self.api_base_url + "Home/DeActivateZoneBoost"
        response = requests.post(url, data=json.dumps(
            data), headers=headers, timeout=10)

        if response.status_code != 200:
            return False

        boost_data = response.json()

        return boost_data.get("isSuccess", False)

    def deactivate_boost_by_name(self, zone_name):
        """
        Deactivate boost by the name of the zone
        """

        zone = self.get_zone(zone_name)
        if zone is None:
            raise RuntimeError("Unknown zone")

        return self.deactivate_boost_by_id(zone["zoneId"])

    # Ctor
    def __init__(self, username, password, cache_home=False):
        """Performs login and save session cookie."""
        # HTTPS Interface

        self.home_id = None
        self.user_id = None
        self.login_data = None
        self.username = username
        self.password = password
        self.cache_home = cache_home
        self.home = None
        self.home_refresh_at = None
        self.api_base_url = 'https://ember.ephcontrols.com/api/'

        if not self._login():
            raise RuntimeError("Unable to login")
