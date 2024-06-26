from asyncio import run

from utils.json import json_dump

from crawlers.vimm import Vimm

async def main():
    data = await Vimm().runner('god of war') 

    json_dump('data2.json', data)

run(main())