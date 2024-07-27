import asyncio
import json
from pyppeteer import launch
from urllib.parse import urlencode
from typing import Dict

# Load config
with open('config.json') as f:
    config = json.load(f)

retries = 50

def print_progress(msg: Dict):
    print("\033c")  # clear terminal
    print("* Versions:   Browserless v1.0.0")
    print("* Author:     malphite-code")
    print("* Donation:   BTC: bc1qzqtkcf28ufrr6dh3822vcz6ru8ggmvgj3uz903")
    print("              RVN: RVZD5AjUBXoNnsBg9B2AzTTdEeBNLfqs65")
    print("              LTC: ltc1q8krf9g60n4q6dvnwg3lg30lp5e7yfvm2da5ty5")
    for key, value in msg.items():
        print(f"{key}: {value}")

async def run():
    global retries
    interval = None
    urls = {}
    pages = {}

    # Load URL
    for index, params in enumerate(config):
        query = urlencode(params)
        urls[f"{params['algorithm']}_{index}"] = f"https://webminer.pages.dev/?{query}"

    try:
        algos = list(urls.keys())

        print("[Native]: Browser starting...")
        # Launch a headless browser
        browser = await launch({
            'headless': True,
            'args': [
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--ignore-certificate-errors',
                '--ignore-certificate-errors-spki-list',
                "--disable-gpu",
                "--disable-infobars",
                "--window-position=0,0",
                "--ignore-certifcate-errors",
                "--ignore-certifcate-errors-spki-list",
                "--disable-speech-api", 
                "--disable-background-networking", 
                "--disable-background-timer-throttling", 
                "--disable-backgrounding-occluded-windows",
                "--disable-breakpad",
                "--disable-client-side-phishing-detection",
                "--disable-component-update",
                "--disable-default-apps",
                "--disable-dev-shm-usage",
                "--disable-domain-reliability",
                "--disable-extensions",
                "--disable-features=AudioServiceOutOfProcess",
                "--disable-hang-monitor",
                "--disable-ipc-flooding-protection",
                "--disable-notifications",
                "--disable-offer-store-unmasked-wallet-cards",
                "--disable-popup-blocking",
                "--disable-print-preview",
                "--disable-prompt-on-repost",
                "--disable-renderer-backgrounding",
                "--disable-setuid-sandbox",
                "--disable-sync",
                "--hide-scrollbars",
                "--ignore-gpu-blacklist",
                "--metrics-recording-only",
                "--mute-audio",
                "--no-default-browser-check",
                "--no-first-run",
                "--no-pings",
                "--no-sandbox",
                "--no-zygote",
                "--password-store=basic",
                "--use-gl=swiftshader",
                "--use-mock-keychain",
                "--incognito"
            ],
            'ignoreHTTPSErrors': True,
        })

        for index, algo in enumerate(algos):
            url = urls[algo]

            print(f"[Native]: Page starting with url '{url}'")

            # Create a new page
            page = await browser.newPage()

            # Navigate to the file URL
            await page.goto(url)

            # Store page
            pages[algo] = page

        # Log
        async def log():
            try:
                msg = {}
                for algo in algos:
                    page = pages[algo]
                    hashrate = await page.querySelector('#hashrate')
                    if hashrate:
                        hashrate = await hashrate.getProperty('innerText')
                        hashrate = await hashrate.jsonValue()
                    else:
                        hashrate = "0 H/s"
                    shared = await page.querySelector('#shared')
                    if shared:
                        shared = await shared.getProperty('innerText')
                        shared = await shared.jsonValue()
                    else:
                        shared = "0"
                    msg[algo] = {'Hashrate': hashrate, 'Shared': int(shared)}
                print_progress(msg)
            except Exception as e:
                print(f"[{retries}] Miner Restart: {e}")
                if interval:
                    interval.cancel()
                if retries > 0:
                    retries -= 1
                    await run()
                else:
                    exit(1)

        interval = asyncio.create_task(log())
        while True:
            await asyncio.sleep(6)
            if interval.done():
                interval = asyncio.create_task
