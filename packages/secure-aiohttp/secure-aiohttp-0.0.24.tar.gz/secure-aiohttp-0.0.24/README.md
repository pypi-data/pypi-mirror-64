# secure-aiohttp
Library implements CSP and HSTS headers. In future CSRF token and maybe some other default security handlers will be added.

### HSTS(Strict-Transport-Security)
Way for web site to tell browsers that it should only be accessed using HTTPS, instead of using HTTP. Which is usually used for connection, even if web site enables HTTPS.
Helps to avoid man in the middle attack.([source](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security))
You can learn more here:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security

**Avaliable parameters:**
| Parameter              | Defenition                                                        | Default            |
|------------------------|-------------------------------------------------------------------|--------------------|
| hsts                   | should HSTS header be added                                       | True               |
| hsts_max_age           | for how long in seconds browser should redirect directly to HTTPS | 31536000(one year) |
| hsts_inclue_subdomains | should include subdomains                                         | True               |
| hsts_preload           | should use preload                                                | True               |

### CSP(Content-Security-Policy)
Content Security Policy (CSP) is an added layer of security that helps to detect and mitigate certain types of attacks, including Cross Site Scripting (XSS) and data injection attacks. These attacks are used for everything from data theft to site defacement to distribution of malware.([source](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP))
Basically it block all sources for front-end libraries/images/objects... that are not specified in whitelist to avoid downloading malicious code that can gather sensetive user data.
You can learn more here:
* https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
* https://content-security-policy.com/

**Avaliable parameters:**
| Parameter      | Defenition                                                        | Default                       |
|----------------|-------------------------------------------------------------------|-------------------------------|
| csp            | Should CSP header be added and if yes - what it should include                                        | None                          |
| csp_testing    | Enable CSP in report only mode, without actually blocking sources | False                         |
| scp_report_uri | Where browser should send CSP reports                             | /secureaiohttp-csp-report-uri |

`csp` parameter can be either:
* `None` to avoid using  CSP header at all
* `default|same-origin|google-analitycs` to use predifined CSP header
* `dict` with custom CSP parameters, example:
```

'myCSP': {
    'connect-src': 'self',
    'default-src': 'none',
    'img-src': 'self',
    'script-src': 'self',
    'style-src': 'self',
    'report-uri': '/my-csp-report-handler',
    'block-all-mixed-content': None
}


```
You need to pass `None` for parameters that require no values, like `block-all-mixed-content`.

Predifined CPS header variants are taken from https://content-security-policy.com/ and include:
* `default`: This policy allows images, scripts, AJAX, and CSS from the same origin, and does not allow any other resources to load (eg object, frame, media, etc). It is a good starting point for many sites.
* `google-analitycs`: Allow Google Analytics, Google AJAX CDN and Same Origin.
* `same-origin`: Only Allow Scripts from the same origin.

# Examples

You can see some simple examples in `example` folder.

# Contribution

Any contributions are welcome! Take action in securing your users! ;)

# License

`secure-aiohttp` is offered under the Apache 2 license.
