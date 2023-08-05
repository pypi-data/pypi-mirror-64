"""Contains the NextcloudMonitor class"""

import requests


class NextcloudPollError(Exception):
    """Failed to fetch nextcloud monitor data."""

    pass


class NextcloudMonitor:
    """An object containing a dictionary representation of dat returned by
    Nextcloud's monitoring api

    Attributes:
        nextcloud_url (str): Full https url to a nextcloud instance
        user (str): Username of the Nextcloud user with access to the monitor api
        app_password (str): App password generated from Nextcloud security settings page
    """

    def __init__(self, nextcloud_url, user, app_password):
        self.data = dict()
        self.api_url = (
            f"{nextcloud_url}/ocs/v2.php/apps/serverinfo/api/v1/info?format=json"
        )
        self.user = user
        self.password = app_password
        self.update()

    def update(self):
        response = requests.get(self.api_url, auth=(self.user, self.password))
        try:
            self.data = response.json()["ocs"]["data"]
        except:
            raise NextcloudPollError(
                "Connection to Nextcloud API failed. Check your url, username and password and try again"
            )
