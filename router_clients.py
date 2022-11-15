import requests

# Do away with annoying error; sure we should check the cert but...
requests.packages.urllib3.disable_warnings()


class UnifiAuthorizationError(Exception):
    pass


class UnifiInstantiationError(Exception):
    pass


class UnifiActionError(Exception):
    pass


class UnifiClient:
    def __init__(self, network_controller, username, password):
        self.controller = network_controller
        auth_endpoint = f"https://{self.controller}:443/api/auth/login"
        self.session = requests.Session()
        login_payload = {"username": username, "password": password}
        login = self.session.post(auth_endpoint, json=login_payload)
        if login.status_code != 200:
            raise UnifiAuthorizationError("Problem logging in to the network controller")

        try:
            cookie = login.headers.get("Set-Cookie").split(";")[0]
        except AttributeError:
            raise UnifiInstantiationError("Set-Cookie token not found in login response")
        except SyntaxError:
            raise UnifiInstantiationError("Set-Cookie token value found is not a string")

        csrf_token = login.headers.get("x-csrf-token")
        if csrf_token is None:
            raise UnifiInstantiationError("CSRF token not found in login response")

        self.session.headers.update({"Cookie": cookie, "x-csrf-token": csrf_token})

    def change_wifi_password(self, network_id, new_password):
        network_url = f"https://{self.controller}:443/proxy/network/api/s/default/rest/wlanconf/{network_id}"
        network_payload = {"x_passphrase": new_password}

        response = self.session.put(network_url, json=network_payload)

        if response.status_code != 200:
            raise UnifiActionError(f"Network '{network_id}' password update failed")
