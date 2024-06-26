from playwright.async_api import async_playwright
from asyncio import Queue

from utils.json import config_load

class _PlaywrightSingleton:
    max_tabs = config_load().max_tabs
    queue = Queue(max_tabs)

    isRunning = False

    _browser = None
    _context = None


    @classmethod
    async def _get_context(cls):
        if not cls._browser:
            playwright = await async_playwright().start()

            configs = config_load()
            cls._browser = await playwright.chromium.launch(headless = configs.headless)
            cls._context = await cls._browser.new_context()

        return cls._context


    async def _open_tabs(self):
        context = await self._get_context()
        for _ in range(self.max_tabs):
            page = await context.new_page()
            await self.queue.put(page)


    async def start(self):
        if self.isRunning: return

        await self._open_tabs()
        
        self.isRunning = True


    async def get_tab(self):
        page = await self.queue.get()
        return page
    

    async def put_tab(self, page):
        await self.queue.put(page)

    
    async def restart(self):
        await self._browser.close()
        await self._restart()
        await self._open_tabs()

    
    @classmethod
    async def _restart(cls):
        configs = config_load()
        cls.max_tabs = configs.max_tabs
        cls.queue = Queue(configs.max_tabs)
        
        cls._browser = None
        cls._context = None


PlaywrightSingleton = _PlaywrightSingleton()