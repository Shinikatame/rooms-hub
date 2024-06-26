from httpx import AsyncClient
from bs4 import BeautifulSoup
from asyncio import gather, create_task

class Vimm:
    url_base = 'https://vimm.net'
    data = []

    client = AsyncClient(timeout = None)


    async def runner(self, search: str):
        await self.__worker(search)

        return self.data


    async def __worker(self, search: str):
        url = f'{self.url_base}/vault/?p=list&q={search}'

        while True:
            response = await self.client.get(url)

            soup = BeautifulSoup(response.text, 'html.parser')

            container = soup.find('main', class_ = 'mainContent')
            if not container: break

            paginator = container.find_all('div', recursive = False)[-3].find_all('a')[-1]
            if not paginator: break

            next_page_path = paginator.get('href')
            if next_page_path == '#': break

            url = f'{self.url_base}/{next_page_path}'
            await self.__scrapper(soup)
            

    async def __scrapper(self, soup: BeautifulSoup):
        table = soup.find('table', class_= 'rounded centered cellpadding1 hovertable striped')
        
        rows = table.find_all('tr')[1:]

        tasks = []

        for row in rows:
            task = create_task(self.__get_infos(row))
            tasks.append(task)
            # break

        await gather(*tasks)

    
    async def __get_infos(self, row: BeautifulSoup):
        row_data = row.find_all('td')

        payload = {}

        payload['console'] = row_data[0].text
        payload['title'] = row_data[1].text
        payload['url'] = self.url_base + row_data[1].find('a').get('href')

        payload['region'] = row_data[2].find('img').get('title')
        payload['version'] = row_data[3].text
        payload['languages'] = row_data[4].text

        response = await self.client.get(payload['url'])
        soup = BeautifulSoup(response.text, 'html.parser')

        payload['download'] = bool(soup.find('div', class_ = 'innerMain').find('form').find('button'))

        self.data.append(payload)