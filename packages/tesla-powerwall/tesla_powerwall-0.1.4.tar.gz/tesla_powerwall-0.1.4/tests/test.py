import unittest
from responses import add, Response

from powerwall import PowerWall

ENDPOINT = "https://1.1.1.1"

add(
    Response(
        method='GET',
        url=f'{ENDPOINT}/system_status/soe',
        json={'percentage': 53.16394658753709}
    )
)


class TestPowerWall(unittest.TestCase):
    def setUp(self):
        self.powerwall = PowerWall(ENDPOINT)

    def test_endpoint_setup(self):
        test_endpoint_1 = "1.1.1.1"
        pw = PowerWall(test_endpoint_1)
        self.assertEqual(pw._endpoint, f"https://{test_endpoint_1}")

        test_endpoint_2 = "http://1.1.1.1"
        pw = PowerWall(test_endpoint_2)
        self.assertEqual(pw._endpoint, f"https://1.1.1.1")

        test_endpoint_3 = "https://1.1.1.1/"
        pw = PowerWall(test_endpoint_3)
        self.assertEqual(pw._endpoint, test_endpoint_3)
