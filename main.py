import asyncio
from bs4 import BeautifulSoup
import aiohttp
from fake_useragent import UserAgent
from redisServices import write_dict_to_redis, get_all_date_from_redis


async def get_data():
    async with aiohttp.ClientSession() as session:
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/'
                      'apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user_agent': UserAgent()['google_chrome']
        }
        async with session.get(url='https://ua1xbet.com/us/live/football', headers=headers) as response:
            response_text = await response.text()

        soup = BeautifulSoup(response_text, 'html.parser')

        types = list()
        for type_name in soup.find('div', class_='c-bets').find_all('div'):
            types.append(type_name.text)

        all_info = list()
        for i in soup.find_all('div', class_='c-events__item c-events__item_game c-events-scoreboard__wrap'):
            team = i.find('span', class_='c-events__teams')
            time = i.find('div', class_='c-events__time')
            score = i.find('div', class_='c-events-scoreboard__lines')
            finally_scope = score.text.split()[0], ':', score.text.split()[1]

            info = {
                "away": team.text.split('\n')[3],
                "home": team.text.split('\n')[2],
                "time": time.text.split('\n')[1:3],
                "currentScore": ''.join(finally_scope),
                'markets': {
                    'title': None,
                    'outcomes': []
                }
            }

            bets = i.find_all('span', class_='c-bets__inner')
            for p, bet in enumerate(bets):
                info['markets']['outcomes'].append({
                    "active": False if bet.text == '-' else True,
                    "odd": bet.text,
                    "type": types[p],
                })

            all_info.append(info)

        await write_dict_to_redis(all_info)


async def get_database():
    await get_data()

    finally_data = await get_all_date_from_redis()

    return finally_data


async def main_test():
    await get_data()


if __name__ == '__main__':
    asyncio.run(main_test())