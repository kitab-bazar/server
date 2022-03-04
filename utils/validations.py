from django.conf import settings
import requests


class MissingCaptchaException(Exception):
    pass


def validate_hcaptcha(captcha, site_key):
    CAPTCHA_VERIFY_URL = 'https://hcaptcha.com/siteverify'
    SECRET_KEY = settings.HCAPTCHA_SECRET

    data = {'secret': SECRET_KEY, 'response': captcha, 'sitekey': site_key}
    response = requests.post(url=CAPTCHA_VERIFY_URL, data=data)

    response_json = response.json()
    return response_json['success']
