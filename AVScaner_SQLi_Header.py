import asyncio
import os
import random
import time
from asyncio import Queue

import aiohttp
from aiohttp import ClientConnectorCertificateError, ClientSSLError
from aiohttp import ClientSession

from handlers.DTO import UrlHeader
from handlers.file_handler import read_file_to_queue, read_file_to_list, write_to_file
from handlers.parse_arguments import parse_arguments
from handlers.utils import C, timer_decorator, limit_rate_decorator
from handlers.various_headers import USER_AGENTS, CUSTOM_HEADERS

PARSE_ARGS = parse_arguments()

INPUT = PARSE_ARGS.input
OUTPUT = PARSE_ARGS.output
PAYLOADS = PARSE_ARGS.payloads
BYPASS_PAYLOADS = PARSE_ARGS.bypass
CALL_LIMIT_PER_SECOND = PARSE_ARGS.concurrency
TIMEOUT = PARSE_ARGS.timeout
BYPASS_ONLY_FALSE_POSITIVE = PARSE_ARGS.bypass_only_false_positive
BYPASS_ALL = PARSE_ARGS.bypass_all
PROXY = PARSE_ARGS.proxy


async def generate_payload_headers(payload_patterns: list[str], set_timeout: str):
    modified_header_list = []

    for header in CUSTOM_HEADERS:
        user_agent = random.choice(USER_AGENTS)
        header['User-Agent'] = user_agent

        for header_item in header.keys():

            for payload in payload_patterns:
                modified_payload = payload.replace("%__TIME_OUT__%", set_timeout)
                modified_header = {**header, header_item: header[header_item] + modified_payload}
                modified_header_list.append(modified_header)

    return modified_header_list


@limit_rate_decorator(calls_limit=CALL_LIMIT_PER_SECOND, timeout=1)
async def make_request(url: str, header: dict, session: ClientSession) -> (
        tuple[str, int, dict, float] | tuple[str, None, None]):
    proxy_url = PROXY if PROXY else None
    scheme = url.replace('https://', 'http://')

    try:
        start_time = time.perf_counter()
        async with session.get(scheme, headers=header, proxy=proxy_url, ssl=False) as response:
            elapsed_time = time.perf_counter() - start_time
            return url, response.status, header, elapsed_time

    except (ClientConnectorCertificateError, ClientSSLError) as ssl_error:
        print(f'{C.red}[!] SSL Error in make_request for {url}: {ssl_error}{C.norm}')
        return url, None, None

    except aiohttp.ClientError as e:
        print(f'{C.red}[!] HTTP Client Error in make_request for {url}: {e}{C.norm}')
        return url, None, None

    except Exception as e:
        print(f'{C.red}[!] Unexpected Error in make_request for {url} {e}{C.norm}')
        return url, None, None


@limit_rate_decorator(calls_limit=CALL_LIMIT_PER_SECOND, timeout=1)
async def process_bypass_waf(req: UrlHeader, bypass_patterns: list[str]):
    tasks = []
    for payload_bypass in bypass_patterns:
        modified_url = req.url + payload_bypass
        tasks.append(make_request(url=modified_url, header=req.header, session=req.session))

    for i, as_completed in enumerate(asyncio.as_completed(tasks)):

        try:
            url, response_status, header, response_time = await as_completed
            color = C.white
            if response_status == 200 and response_time >= int(req.timeout):
                color = C.bold_green

                output_folder = 'output_report'
                output_file = f'{output_folder}/vulnerable_headers.txt'
                await write_to_file(f'URL: {url} | Status: {response_status} | '
                                    f'Response time: {response_time:.2f} sec | Header: {header}',
                                    output_file)

            elif response_status == 403 and response_time > int(req.timeout):
                color = C.yellow
            elif response_status == 403 and response_time < int(req.timeout):
                color = C.red
            print(f"{C.magenta}        [{i + 1}] {C.white}"
                  f"Bypass URL: {url} | Status: {color}{response_status} | "
                  f"Response time: {response_time:.2f} sec | Header: {C.blue}{header}{C.norm}")

        except Exception as e:
            print(f"{C.red}[!] Error in bypass task: {e}{C.norm}")


async def get_link_bypass_queue(bypass_patterns: list[str], link_bypass_queue: Queue):
    while True:
        request = await link_bypass_queue.get()

        try:
            await process_bypass_waf(request, bypass_patterns)
        except Exception as e:
            print(f'{C.red}[!] Error in get_link_bypass_queue: {e}{C.norm}')
        finally:
            link_bypass_queue.task_done()


async def analyze_response(url_number: int, url: str,
                           response_status: int, header: dict,
                           response_time: float, timeout: int, link_bypass_queue: Queue, session: ClientSession) -> None:
    output_folder = OUTPUT
    os.makedirs(output_folder, exist_ok=True)

    color = C.bold_white
    color_status = C.bold_white
    if response_status == 200 and response_time >= timeout:
        color = C.bold_green

        output_file = f'{output_folder}/vulnerable_headers.txt'
        await write_to_file(f'URL: {url} | Status: {response_status} | '
                            f'Response time: {response_time:.2f} sec | Header: {header}',
                            output_file)

    elif response_status == 403 and response_time > timeout:
        color = C.bold_magenta

        if BYPASS_ONLY_FALSE_POSITIVE:
            url_header = UrlHeader(url, header, timeout, session)
            await link_bypass_queue.put(url_header)

        output_file = f'{output_folder}/vulnerable_headers_403.txt'
        await write_to_file(f'URL: {url} | Status: {response_status} | '
                            f'Response time: {response_time:.2f} sec | Header: {header}',
                            output_file)

    elif response_status == 403 and response_time < timeout:
        color = C.white
        color_status = C.red

        if BYPASS_ALL:
            url_header = UrlHeader(url, header, timeout, session)
            await link_bypass_queue.put(url_header)

        # output_file = f'{output_folder}/vulnerable_headers_403_without_timeout.txt'
        # await write_to_file(f'URL: {url} | Status: {response_status} | '
        #                     f'Response time: {response_time:.2f} sec | Header: {header}',
        #                     output_file)

    print(f"{C.bold_cyan}[{url_number + 1}] {color}"
          f"URL: {url} | Status: {color_status}{response_status}{color} | "
          f"Response time: {response_time:.2f} sec | Header: {C.blue}{header}{C.norm}")


@limit_rate_decorator(calls_limit=CALL_LIMIT_PER_SECOND, timeout=1)
async def process_link(link: str, link_bypass_queue, payload_patterns: list[str], session: ClientSession):
    timeout_10s = '10'
    user_agent = random.choice(USER_AGENTS)
    normal_header = {'User-Agent': user_agent}

    headers_with_payload = await generate_payload_headers(payload_patterns, timeout_10s)

    url, response_status, header, normal_response_time = await make_request(link, normal_header, session)
    print(f"\n{C.bold_white}Test URL: {url} | Status: {response_status} | "
          f"Normal response time: {normal_response_time:.2f}sec{C.norm}")

    tasks = [
        make_request(url=url, header=header, session=session)
        for header in headers_with_payload
    ]

    print(f'{C.yellow}[*] Total number of payload options per link including header:'
          f' {C.bold_yellow}{len(tasks)}\n{C.norm}')

    timeout_10s_int = int(timeout_10s)
    for url_number, as_completed in enumerate(asyncio.as_completed(tasks)):
        try:
            url, response_status, header, response_time = await as_completed
            await analyze_response(url_number, url, response_status, header, response_time, timeout_10s_int,
                                   link_bypass_queue, session)

        except Exception as e:
            print(f"{C.red}[!] Error in process_link task: {e}{C.norm}")


async def handle_queue(link_queue: Queue, link_bypass_queue: Queue, payload_patterns: list[str], session: ClientSession):
    while True:
        link = await link_queue.get()

        try:
            await process_link(link, link_bypass_queue, payload_patterns, session)
        except Exception as e:
            print(f'{C.red}[!] Error in handle_queue: {e}{C.norm}')
        finally:
            link_queue.task_done()


async def cancel_tasks(tasks: list[asyncio.Task]):
    for task in tasks:
        if not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


@timer_decorator
async def main():
    link_queue = asyncio.Queue(maxsize=100)
    link_bypass_queue = asyncio.Queue(maxsize=1)

    payload_patterns = await read_file_to_list(PAYLOADS)
    bypass_patterns = await read_file_to_list(BYPASS_PAYLOADS)

    producer = asyncio.create_task(read_file_to_queue(INPUT, link_queue))

    timeout_for_all_requests = aiohttp.ClientTimeout(total=TIMEOUT)
    async with (aiohttp.ClientSession(
            connector=aiohttp.TCPConnector(limit=100, ssl=False, keepalive_timeout=45),
            timeout=timeout_for_all_requests) as session):

        consumers = [asyncio.create_task(handle_queue(link_queue=link_queue,
                                                      link_bypass_queue=link_bypass_queue,
                                                      payload_patterns=payload_patterns,
                                                      session=session)) for _ in range(20)]

        consumers_bypass = [asyncio.create_task(get_link_bypass_queue(link_bypass_queue=link_bypass_queue,
                                                                      bypass_patterns=bypass_patterns,
                                                                      )) for _ in range(20)]

        await asyncio.gather(producer)
        await link_queue.join()

        await cancel_tasks(consumers)
        await asyncio.gather(*consumers, return_exceptions=True)

        await link_bypass_queue.join()
        await cancel_tasks(consumers_bypass)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{C.red} [!] Program interrupted by user. Exiting...{C.norm}")
    except Exception as e:
        print(f"{C.red}[!] Unexpected error: {e}{C.norm}")
