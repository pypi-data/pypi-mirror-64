from aiohttp import web

from secure_aiohttp.settings import DEFAULT_CSP_REPORT_URI, logger


def _csp_builder(csp_dict: dict) -> str:
    """Builds CSP string from dictionary

    Parameters:
        csp_dict(dict): csp parameters

    Returns:
        str: string built from csp_dict dictionary

    """

    if 'report-uri' not in csp_dict:
        csp_dict.update({'report-uri': DEFAULT_CSP_REPORT_URI})

    return_str = ''
    for key, value in csp_dict.items():
        key = key.strip()

        if not key:
            raise AttributeError(f'CSP dictionary configured incorrectly. Not valid key specified.')

        value = _validate_value(value)
        return_str += key
        if isinstance(value, str):
            return_str += ' ' + value.strip()
        elif isinstance(value, list) or isinstance(value, tuple):
            return_str += ' ' + ' '.join(value)
        elif value is None:
            # when value not needed, for example: `block-all-mixed-content;`
            pass
        else:
            raise AttributeError(f'{key} should be either string, list, tuple or None.')

        return_str += '; '

    return return_str[:-2]  # removing '; ' from end of string


def _validate_value(value):
    """
    Adds `'` to self and none parameters.
    """
    update_values = ['self', 'none']

    if isinstance(value, str):
        if value in update_values:
            return f'\'{value}\''

    if isinstance(value, list) or isinstance(value, tuple):
        return_list = list()
        for item in value:
            if item in update_values:
                item = f'\'{item}\''
            return_list.append(value)
        return return_list

    return value


async def csp_report_handler(request):
    """
    WIP: Gathers logs for CSP reports
    """

    csp_report = (await request.json())['csp-report']
    logger.warning(csp_report)

    return web.Response(status=200)
