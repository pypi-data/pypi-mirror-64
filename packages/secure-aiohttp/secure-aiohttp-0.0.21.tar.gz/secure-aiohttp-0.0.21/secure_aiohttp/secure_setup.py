from secure_aiohttp.settings import CSP_DEFAULT, DEFAULT_CSP_REPORT_URI
from secure_aiohttp.utils import _csp_builder, csp_report_handler

__all__ = ['SecureAiohttp', ]


class SecureAiohttp:
    """Class for setting up secure_aiohttp lib

    Parameters:
        csp(string|dict): used for building Content-Security-Policy header
        hsts(bool): True for enabling, False for disabling
        hsts_max_age(int): The time, in seconds, that the browser should
                           remember that a site is only to be accessed
                           using HTTPS. Default is one year.
        hsts_inclue_subdomains(bool): If this optional parameter is
                                      specified, this rule applies to all
                                      of the site's subdomains as well.
                                      Default is True.
        preload(bool): Preloading Strict Transport Security enabling.
                       Default is True.

    """
    def __init__(self, app,
                 csp=None,
                 csp_testing=False,
                 scp_report_uri=DEFAULT_CSP_REPORT_URI,
                 hsts=True,
                 hsts_max_age=31536000,
                 hsts_inclue_subdomains=True,
                 hsts_preload=True):
        self.app = app
        # csp:
        self.csp = csp
        self.csp_testing = csp_testing
        self.scp_report_uri = scp_report_uri
        # hsts:
        self.hsts = hsts
        self.hsts_max_age = hsts_max_age
        self.hsts_inclue_subdomains = hsts_inclue_subdomains
        self.hsts_preload = hsts_preload

        self.__setup()

    def __setup(self, ):
        if self.csp:
            dict_report_uri = self.csp.get('report_uri')
            if isinstance(self.scp_report_uri, dict) and dict_report_uri:
                self.scp_report_uri = dict_report_uri

            self.app.router.add_post(self.scp_report_uri.strip(), csp_report_handler)
            self.app.on_response_prepare.append(self._csp_prepare)
        if self.hsts:
            self.app.on_response_prepare.append(self._hsts_prepare)

    async def _csp_prepare(self, request, response):
        """
        If csp - string -> looking in predifined data.
        If csp - dict -> builder makes CSP string out of it.
        If csp - not specified or None -> ignores it.
        """
        csp_dict = CSP_DEFAULT.get(str(self.csp)) or self.csp
        csp_string = _csp_builder(csp_dict)
        if self.csp_testing:
            response.headers['Content-Security-Policy-Report-Only'] = csp_string
        else:
            response.headers['Content-Security-Policy'] = csp_string

    async def _hsts_prepare(self, request, response):
        if not isinstance(self.hsts_max_age, int):
            raise AttributeError('hsts_max_age should be int.')

        hsts_str = f'max-age={self.hsts_max_age}'
        if self.hsts_inclue_subdomains:
            hsts_str += '; includeSubDomains'
        if self.hsts_preload:
            hsts_str += '; preload'
        response.headers['Strict-Transport-Security'] = hsts_str
