# -*- coding: utf-8 -*-
import asyncio
import re
from asyncio import TimeoutError

import aiohttp
from aiohttp import Timeout, ClientOSError, ClientResponseError
from aiohttp.http_exceptions import HttpProcessingError

BEGINS_WITH_DIGIT = re.compile(r'\s+\d+')


class TaskException(Exception):
    pass


async def download(url: str) -> bytes:
    try:
        with Timeout(10):
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.read()

    except (
            TimeoutError,
            ClientOSError,
            ClientResponseError,
            HttpProcessingError
    ) as e:
        msg = "Couldn't download file {}: {}".format(url, e)
        raise TaskException(msg)


def parse_int(str_digit: str) -> int:
    return int(''.join(filter(lambda x: x.isdigit(), str_digit)))


async def minimum_spread(data: str) -> int:
    try:
        data_content = [
            i.rstrip().split() for i in data.split('\n')
            if BEGINS_WITH_DIGIT.match(i)
        ]
        spread = [parse_int(i[1]) - parse_int(i[2]) for i in data_content]
        return spread.index(min(spread)) + 1
    except (TypeError, IndexError) as e:
        msg = 'Error in {}:{}'.format('minimum_spread', e)
        raise TaskException(msg)


async def smallest_goal_difference(data: str) -> str:
    try:
        data_content = [
            i.rstrip().split() for i in data.split('\n')
            if BEGINS_WITH_DIGIT.match(i)
        ]
        goal_difference = [(int(i[6]) - int(i[8])) for i in data_content]
        return data_content[goal_difference.index(min(goal_difference))][1]

    except (TypeError, IndexError) as e:
        msg = 'Error in {}:{}'.format('smallest_goal_difference', e)
        raise TaskException(msg)


async def main():
    # http://codekata.com/data/04/weather.dat

    print("""In weather.dat you’ll find daily weather data for Morristown,
    NJ for June 2002. Your program downloads this text file then outputs the
    day number (column one) with the smallest temperature spread (the maximum
    temperature is the second column, the minimum the third column)\n""")
    weather_data = await download('http://codekata.com/data/04/weather.dat')
    print(weather_data.decode("utf-8"))
    result = await minimum_spread(weather_data.decode("utf-8"))
    print("\nSmallest temperature spread day:", result)

    # http://codekata.com/data/04/football.dat

    print("""\nThe file football.dat contains the results from the English
    Premier League for 2001/2. The columns labeled ‘F’ and ‘A’ contain the
    total number of goals scored for and against each team in that season
    (so Arsenal scored 79 goals against opponents, and had 36 goals scored
    against them). Your program should download the file and print the name of
    the team with the smallest difference in ‘for’ and ‘against’ goals.\n""")
    football_data = await download('http://codekata.com/data/04/football.dat')
    print(football_data.decode('utf-8'))
    result = await smallest_goal_difference(football_data.decode('utf-8'))
    print("Team with smallest goals difference:", result)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


def run():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
