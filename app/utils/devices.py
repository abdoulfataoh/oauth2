# coding: utf-8

from user_agents import parse  # type: ignore


def parse_device(user_agent: str) -> dict:

    ua = parse(user_agent)

    if ua.is_mobile:
        device_type = 'mobile'
    elif ua.is_tablet:
        device_type = 'tablet'
    else:
        device_type = 'desktop'

    return {
        'device_type': device_type,
        'device_name': f'{ua.browser.family} on {ua.os.family}',
        'browser': ua.browser.family,
        'os': ua.os.family,
    }
