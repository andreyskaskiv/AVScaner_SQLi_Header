USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0',
]


CUSTOM_HEADERS = [
    {'User-Agent': ''},
    {'User-Agent': '', 'X-Custom-IP-Authorization': '127.0.0.1'},
    {'User-Agent': '', 'X-Forwarded-For': 'http://127.0.0.1'},
    {'User-Agent': '', 'X-Forwarded-For': '127.0.0.1:80'},
    {'User-Agent': '', 'X-Originally-Forwarded-For': '127.0.0.1'},
    {'User-Agent': '', 'X-Originating-': 'http://127.0.0.1'},
    {'User-Agent': '', 'X-Originating-IP': '127.0.0.1'},
    {'User-Agent': '', 'True-Client-IP': '127.0.0.1'},
    {'User-Agent': '', 'X-WAP-Profile': '127.0.0.1'},
    {'User-Agent': '', 'X-Arbitrary': 'http://127.0.0.1'},
    {'User-Agent': '', 'X-HTTP-DestinationURL': 'http://127.0.0.1'},
    {'User-Agent': '', 'X-Forwarded-Proto': 'http://127.0.0.1'},
    {'User-Agent': '', 'Destination': '127.0.0.1'},
    {'User-Agent': '', 'X-Remote-IP': '127.0.0.1'},
    {'User-Agent': '', 'X-Client-IP': 'http://127.0.0.1'},
    {'User-Agent': '', 'X-Host': 'http://127.0.0.1'},
    {'User-Agent': '', 'X-Forwarded-Host': 'http://127.0.0.1'},
    {'User-Agent': '', 'X-Forwarded-Port': '4443'},
    {'User-Agent': '', 'X-Forwarded-Port': '80'},
    {'User-Agent': '', 'X-Forwarded-Port': '8080'},
    {'User-Agent': '', 'X-Forwarded-Port': '8443'},
    {'User-Agent': '', 'X-ProxyUser-Ip': '127.0.0.1'},
    {'User-Agent': '', 'Client-IP': '127.0.0.1'}

]