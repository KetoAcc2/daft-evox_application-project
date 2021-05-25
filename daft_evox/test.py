import json
import random
import re
import pytest
import requests

api_key = {"access_token": "apikey123abc"}


def test_endpoints():
    message_text = """
    {
        "message_text": "testMessage123"
    }
    """
    json_message = json.loads(message_text)
    json_message['message_text'] += str(random.randint(1, 10))

    # sending message
    url = 'http://127.0.0.1:8000/messages'
    response = requests.post(url, json=json_message, headers=api_key)

    assert response.status_code == 201

    regex_id = "\\d+"
    message_id = re.search(regex_id, response.text).group()

    # retrieving message by id we received in response for post method
    url = f'http://127.0.0.1:8000/messages/{message_id}'
    response = requests.get(url, headers=api_key)

    assert response.status_code == 200
    assert response.json()['message_text'] == json_message['message_text']

    message_counter = response.json()['view_counter']

    # checking if view_counter works as well
    response = requests.get(url, headers=api_key)

    assert response.status_code == 200
    assert response.json()['view_counter'] == (message_counter + 1)

    # updating text message

    message_updated = """
    {
        "message_text": "updatedMessage123"
    }
    """

    json_message = json.loads(message_updated)
    json_message['message_text'] += str(random.randint(1, 10))

    url = f'http://127.0.0.1:8000/messages/{message_id}'
    response = requests.put(url, json=json_message, headers=api_key)

    assert response.status_code == 204

    # checking if text is updated and counter is reset
    url = f'http://127.0.0.1:8000/messages/{message_id}'
    response = requests.get(url, headers=api_key)

    COUNTER_AFTER_UPDATE = 1

    assert response.status_code == 200
    assert response.json()['message_text'] == json_message['message_text']
    assert response.json()['view_counter'] == COUNTER_AFTER_UPDATE

    # deleting the message
    url = f'http://127.0.0.1:8000/messages/{message_id}'
    response = requests.delete(url, json=json_message, headers=api_key)

    assert response.status_code == 204

    # checking if message is deleted
    url = f'http://127.0.0.1:8000/messages/{message_id}'
    response = requests.get(url, headers=api_key)

    assert response.status_code == 404
