import asyncio
import aiohttp
import time
import os
import sys

BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'
CC_LIST = ('BE BG CZ DK DE EE IE ES FR HR IT CY LV LT LU HU MT NL AT PL PT RO SI SK FI SE GB').split()


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


def save_flag(img, filename):
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img)


async def get_flag(session, cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    async with session.get(url) as response:
        image = await response.read()
        return image


async def download_one(cc):
    async with aiohttp.ClientSession() as session:
        image = await get_flag(session, cc)
        show(cc)
        save_flag(image, cc.lower() + '.gif')
        return cc


async def download_many(cc_list):
    tasks = [asyncio.create_task(download_one(cc)) for cc in sorted(cc_list)]
    await asyncio.wait(tasks)


def main():
    t0 = time.time()
    asyncio.run(download_many(CC_LIST))
    elapsed = time.time() - t0
    msg = '\nflags downloaded in {:.2f}s'
    print(msg.format(elapsed))


if __name__ == '__main__':
    main()
