from aiohttp.http_exceptions import HttpProcessingError
from aioresponses import aioresponses
from asynctest.case import TestCase
from ddt import ddt, unpack, data

from tasks.main import parse_int, download, TaskException, minimum_spread, \
    smallest_goal_difference
from tasks.tests import WEATHER_DATA, FOOTBAL_DATA


@ddt
class MainTestCase(TestCase):
    use_default_loop = False

    def setUp(self):
        self.url = 'http://dummy.testcase'

    @unpack
    @data(
        ('33*', 33),
        ('2x2x2', 222),
        ('x22', 22)
    )
    def test_parse_int(self, to_parse, expected):
        parsed = parse_int(to_parse)
        self.assertEqual(parsed, expected)

    @aioresponses(param="aiomock")
    async def test_download(self, aiomock):
        aiomock.get(self.url, body=b'test_response', status=200)
        result = await download(self.url)
        self.assertEqual(result, b'test_response')

    async def test_download_with_error(self):
        with aioresponses() as m:
            m.get(
                self.url,
                status=500,
                exception=HttpProcessingError(message='test error')
            )
            with self.assertRaises(TaskException) as exc:
                await download(self.url)

            self.assertTrue(
                "http://dummy.testcase" in str(exc.exception)
            )

    async def test_minimum_spread(self):
        result = await minimum_spread(WEATHER_DATA.decode('utf-8'))
        self.assertEqual(result, 7)

    async def test_smallest_goal_difference(self):
        result = await smallest_goal_difference(FOOTBAL_DATA.decode('utf-8'))
        self.assertEqual(result, 'TestTeam_1')
