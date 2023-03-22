import json
from typing import List

import pytest
from assertpy import assert_that
from wyze_sdk import Client
from wyze_sdk.api.devices import BulbsClient
from wyze_sdk.models.devices import Bulb


@pytest.fixture(scope='session')
def client() -> Client:
    with open("../credentials.json") as f:
        raw_credentials = f.read()
        decoded_credentials: dict[str, str] = json.loads(raw_credentials)
        if 'WYZE_TOTP_KEY' in decoded_credentials.keys():
            return Client(
                email=decoded_credentials['WYZE_EMAIL'],
                password=decoded_credentials['WYZE_PASSWORD'],
                totp_key=decoded_credentials['WYZE_TOTP_KEY'])
        else:
            return Client(
                email=decoded_credentials['WYZE_EMAIL'],
                password=decoded_credentials['WYZE_PASSWORD'])


@pytest.fixture(scope='session')
def bulbs_client(client: Client) -> BulbsClient:
    return client.bulbs


def test_get_all_bulbs(bulbs_client: BulbsClient) -> None:
    bulbs: List[Bulb] = list(bulbs_client.list())
    nicknames: List[str] = list(map(lambda bulb: bulb.nickname, bulbs))
    assert_that(nicknames).contains_only('Bedroom Color Bulb', 'Dining Table Bulb', 'Living Room Corner')


def test_turn_off_bedroom_bulb(bulbs_client: BulbsClient) -> None:
    bulb: Bulb = get_bedroom_bulb(bulbs_client)
    bulbs_client.turn_off(device_mac=bulb.mac, device_model=bulb.product.model)


def test_turn_on_bedroom_bulb(bulbs_client: BulbsClient) -> None:
    bulb: Bulb = get_bedroom_bulb(bulbs_client)
    bulbs_client.turn_on(device_mac=bulb.mac, device_model=bulb.product.model)


def test_set_sun_match_off_bedroom_bulb(bulbs_client: BulbsClient) -> None:
    bulb: Bulb = get_bedroom_bulb(bulbs_client)
    bulbs_client.set_sun_match(device_mac=bulb.mac, device_model=bulb.product.model, sun_match=False)


def test_set_sun_match_on_bedroom_bulb(bulbs_client: BulbsClient) -> None:
    bulb: Bulb = get_bedroom_bulb(bulbs_client)
    bulbs_client.set_sun_match(device_mac=bulb.mac, device_model=bulb.product.model, sun_match=True)


def test_set_bedroom_bulb_to_2700k(bulbs_client: BulbsClient) -> None:
    bulb: Bulb = get_bedroom_bulb(bulbs_client)
    bulbs_client.set_color(device_mac=bulb.mac, device_model=bulb.product.model, color='FDF4DC')


def get_bedroom_bulb(bulbs_client: BulbsClient) -> Bulb:
    bulbs: List[Bulb] = list(filter(lambda bulb: bulb.nickname == 'Bedroom Color Bulb', bulbs_client.list()))
    assert_that(bulbs).is_length(1)
    return bulbs[0]
