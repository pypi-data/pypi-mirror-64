import logging

DEFAULT_CSP_REPORT_URI = '/secureaiohttp-csp-report-uri'

CSP_DEFAULT = {
    'default': {
        'connect-src': 'self',
        'default-src': 'none',
        'img-src': 'self',
        'script-src': 'self',
        'style-src': 'self',
        'report-uri': DEFAULT_CSP_REPORT_URI,
    },
    'same-origin': {
        'default-src': 'self',
    },
    'google-analitycs': {
        'script-src': ['self', 'www.google-analytics.com', 'ajax.googleapis.com']
    }
}

logging.basicConfig(
    level=logging.WARNING,
    format='[%(levelname)s] - [%(asctime)s] - %(message)s',
)
logger = logging.getLogger('secure_aiohttp')
