from kavenegar import *
from urllib.error import HTTPError


def verification(receptor, tokens: dict, template):
    try:
        api = KavenegarAPI('your_api_key')
        params = {
            'receptor': receptor,
            'template': template,
        }
        for k, v in tokens.items():
            params[k] = v
        response = api.verify_lookup(params)
        print(response)
        return True

    except APIException as e:
        print(e)
        return False

    except HTTPError as e:
        print(e)
        return False


def sms(receptor, message):
    try:
        api = KavenegarAPI('your_api_key')
        params = {
            'receptor': receptor,
            'message': message,
            'sender': 'your_phone_sender_in_kavenegar'
        }
        response = api.sms_send(params)
        print(response)

    except APIException as e:
        print(e)

    except HTTPError as e:
        print(e)
