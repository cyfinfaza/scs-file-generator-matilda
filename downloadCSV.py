import asyncio
from pyppeteer import launch
from os.path import abspath


def downloadCSV(url):
    print("Loading page...")

    async def main():
        browser = await launch(options={"headless": True})
        page = await browser.newPage()
        await page.goto(url)
        print("Downloading...")
        await page._client.send(
            "Page.setDownloadBehavior",
            {"behavior": "allow", "downloadPath": abspath("./input/")},
        )
        await page.keyboard.down("Alt")
        await page.keyboard.press("KeyF")
        await page.keyboard.up("Alt")
        await asyncio.sleep(0.5)
        await page.keyboard.press("KeyD")
        await page.keyboard.press("KeyC")
        await asyncio.sleep(0.5)
        # await page.screenshot({"path": "example.png"})
        # await browser.close()

    asyncio.get_event_loop().run_until_complete(main())

    print("Downloaded")


if __name__ == "__main__":
    downloadCSV(
        "https://docs.google.com/spreadsheets/d/1VwNL2EPMhK5zRUr6NZi1qAGercA4MiS_ut-nJdugD_A/edit?usp=sharing"
    )
