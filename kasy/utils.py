import json
import re
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings


class SmsApiError(Exception):
    """Błąd wysyłki wiadomości przez SMSAPI."""


def normalize_phone_number(phone_number):
    number = re.sub(r'\D', '', phone_number or '')
    if len(number) == 9:
        number = '48' + number
    if len(number) < 10 or len(number) > 15:
        raise SmsApiError('Nieprawidłowy numer telefonu odbiorcy.')
    return number


def send_sms(phone_number, message):
    token = settings.SMSAPI_ACCESS_TOKEN
    if not token:
        raise SmsApiError('Brak konfiguracji SMSAPI_ACCESS_TOKEN.')

    payload = {
        'to': normalize_phone_number(phone_number),
        'message': message,
        'format': 'json',
        'encoding': 'utf-8',
    }
    if settings.SMSAPI_SENDER:
        payload['from'] = settings.SMSAPI_SENDER

    request = Request(
        'https://api.smsapi.pl/sms.do',
        data=urlencode(payload).encode('utf-8'),
        headers={'Authorization': 'Bearer {}'.format(token)},
        method='POST',
    )

    try:
        with urlopen(request, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
    except HTTPError as exc:
        try:
            details = exc.read().decode('utf-8')
        except Exception:
            details = str(exc)
        raise SmsApiError('SMSAPI odrzuciło wiadomość: {}'.format(details))
    except (URLError, ValueError) as exc:
        raise SmsApiError('Nie udało się połączyć z SMSAPI: {}'.format(exc))

    if result.get('error'):
        raise SmsApiError(
            'SMSAPI: {}'.format(result.get('message') or result['error'])
        )
    return result
