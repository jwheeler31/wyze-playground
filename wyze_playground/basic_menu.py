import json
import pathlib
import re
import sys

from json import JSONDecodeError
from requests.exceptions import HTTPError
from wyze_sdk import Client
from wyze_sdk.models.devices import Bulb


class WyzeAPI:
    _EMAIL_DICT_KEY: str = "WYZE_EMAIL"
    _PASS_DICT_KEY: str = "WYZE_PASSWORD"
    _PARENT_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent
    _CREDENTIALS_PATH: pathlib.Path = _PARENT_DIR.joinpath("credentials.json")

    def __init__(self):
        self._credentials: dict[str, str] | None = None
        self._client: Client | None = None
        self._bulbs: dict[str, Bulb] | None = None

    def login(self, redo_login: bool = False) -> bool:
        if self.is_logged_in() and not redo_login:
            return True

        try:
            if self._credentials is None:
                self._load_credentials()
            self._client = Client(email=self._credentials[WyzeAPI._EMAIL_DICT_KEY],
                                  password=self._credentials[WyzeAPI._PASS_DICT_KEY])
            return True
        except HTTPError as e:
            print("Login failed.")
            print(f"Error: {e}")
            self._credentials = None
            self._client = None
            return False

    def is_logged_in(self) -> bool:
        return self._client is not None

    def get_all_bulbs(self, refresh: bool = False) -> dict[str, Bulb]:
        if refresh is True or self._bulbs is None or len(self._bulbs) == 0:
            self._init_bulbs_dict()
        return self._bulbs

    def get_bulb_from_name(self, name: str) -> Bulb | None:
        all_bulbs: dict[str, Bulb] = self.get_all_bulbs()
        if name not in all_bulbs.keys():
            print(f"Invalid bulb name: {name}", file=sys.stderr)
            return None
        return all_bulbs[name]

    def bulb_turn_on(self, name: str) -> bool:
        return self._bulb_power(name, True)

    def bulb_turn_off(self, name: str) -> bool:
        return self._bulb_power(name, False)

    def set_bulb_color(self, name: str, hex_color: str) -> bool:
        bulb: Bulb = self.get_bulb_from_name(name)
        if bulb is None:
            return False
        if not re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', hex_color):
            print(f"Invalid hex color: {hex_color}", file=sys.stderr)
            return False
        self._client.bulbs.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color=hex_color)
        return True

    def _load_credentials(self) -> None:
        """
        Loads the credentials into an internal data member.
        :return: None
        """
        if not self._CREDENTIALS_PATH.is_file():
            print(f"File 'credentials.json' is required at location: {str(WyzeAPI._CREDENTIALS_PATH)}")
            sys.exit()
        with open(self._CREDENTIALS_PATH) as f:
            try:
                self._credentials = json.loads(f.read())
            except JSONDecodeError as e:
                print("Failed to decode json from credentials file.", file=sys.stderr)
                print(f"Error: {e}", file=sys.stderr)
                sys.exit()

        has_err: bool = False
        if WyzeAPI._EMAIL_DICT_KEY not in self._credentials:
            has_err = True
            print(f"Expected entry {self._EMAIL_DICT_KEY} in credentials file", file=sys.stderr)
        if WyzeAPI._PASS_DICT_KEY not in self._credentials:
            has_err = True
            print(f"Expected entry {self._PASS_DICT_KEY} in credentials file", file=sys.stderr)

        if has_err:
            sys.exit()

    def _get_client(self) -> Client | None:
        if self._client is None:
            if self.login() is False:
                return None
        return self._client

    def _init_bulbs_dict(self):
        self._bulbs = {}
        for bulb in self._client.bulbs.list():
            self._bulbs[bulb.nickname] = bulb

    def _bulb_power(self, name: str, on: bool) -> bool:
        bulb: Bulb = self.get_bulb_from_name(name)
        if bulb is None:
            print(f"Failed to turn {'on' if on is True else 'off'} bulb: {name}", file=sys.stderr)
            return False
        if on:
            self._client.bulbs.turn_on(device_mac=bulb.mac, device_model=bulb.product.model)
        else:
            self._client.bulbs.turn_off(device_mac=bulb.mac, device_model=bulb.product.model)
        return True


def main() -> None:
    user_input: str
    api: WyzeAPI | None = None

    while True:
        print("Wyze Bulb Operations:")
        print("  1) turn on bulb")
        print("  2) turn off bulb")
        print("  3) list all bulbs")
        print("  4) set bulb color")
        print("  q) quit")
        user_input = input("> ")

        if api is None:
            api = WyzeAPI()
            if not api.login():
                api = None
                continue

        match user_input:
            case "1":
                bulb_nickname: [str] = input("Enter bulb name: ")
                api.bulb_turn_on(bulb_nickname)
            case "2":
                bulb_nickname: [str] = input("Enter bulb name: ")
                api.bulb_turn_off(bulb_nickname)
            case "3":
                names: [str] = api.get_all_bulbs().keys()
                pretty_string: str = str(list(names)).replace('[', '').replace(']', '')
                print(pretty_string)
            case "4":
                bulb_nickname: [str] = input("Enter bulb name: ")
                color: str = input("Enter hex color (excluding hash): ")
                api.set_bulb_color(bulb_nickname, color)
            case "q":
                sys.exit()
            case _:
                print(f"Unrecognized input '{user_input}'\n")
        print()


# ---
# Application entry point
# ---
main()
