"""Stiga API Client."""
import requests

class StigaApiClient:
    def __init__(self, firebase_token):
        self.firebase_token = firebase_token
        self.base_url = "https://connectivity-production.stiga.com/api/"

    def get_devices(self):
        headers = {"Authorization": f"Bearer {self.firebase_token}"}
        response = requests.get(self.base_url + "garage/integration", headers=headers)
        return response.json()

    def start_session(self, uuid, zone_id=None):
        headers = {"Authorization": f"Bearer {self.firebase_token}"}
        params = {"uuid": uuid}
        data = {"data": {"zone_id": zone_id} if zone_id else {}}
        response = requests.post(self.base_url + f"devices/{uuid}/command/startsession", params=params, json=data, headers=headers)
        return response.json()

    def end_session(self, uuid):
        headers = {"Authorization": f"Bearer {self.firebase_token}"}
        params = {"uuid": uuid}
        response = requests.post(self.base_url + f"devices/{uuid}/command/endsession", params=params, headers=headers)
        return response.json()
