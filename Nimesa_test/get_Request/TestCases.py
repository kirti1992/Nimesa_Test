import data as data
import requests
import json
import jsonpath
import datetime
from datetime import timedelta
from datetime import date
from datetime import time
import unittest
import HtmlTestRunner


class Nimesa(unittest.TestCase):
    # API url
    url = "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us&appid=b6907d289e10d714a6e88b30761fae22"

    # Send Get Request
    response = requests.get(url)

    # pasrse response to json format
    json_response = response.json()
    data = json_response['list']

    new_dict = {}
    for element in data:
        date_text = element['dt_txt']
        if date_text not in new_dict:
            new_dict[date_text] = []

    # date_text_list consists of all dt_txt values
    date_text_list = list(new_dict)

    # splitting the date and time in dt_txt in different lists
    a, b = zip(*(s.split(" ") for s in date_text_list))
    dates_list = list(a)
    print(dates_list)
    times_list = list(b)
    print(times_list)

    # checking total number of hours is 96 and total number of days is 4
    def test_check_number_of_days(self):
        start = datetime.datetime.strptime(self.dates_list[0], "%Y-%m-%d")
        end = datetime.datetime.strptime(self.dates_list[-1], "%Y-%m-%d")
        number_of_days = end - start
        self.assertEqual(96, number_of_days.total_seconds() / 3600,
                         "total number of hours is not equal to 96. So data is not calculated hourly")
        self.assertEqual(4, number_of_days.days, "number of days is not equal to 4")

    # splitting the hours, minutes and seconds in differnt tuples
    # checking that each hour comes 4 times to validate that data is calculated hourly in each day
    #  and each of minutes and seconds have values as 00
    def test_cheking_hourly_interval(self):
        x, y, z = zip(*(s.split(":") for s in self.times_list))
        print(x)
        print(y)
        print(z)

        for element in x:
            self.assertEqual(4, x.count(element), "each hour appears 4 times for 4 days")
        for element in y:
            self.assertEqual('00', element, "each minutes value is equal to zero")
        for element in z:
            self.assertEqual('00', element, "each seconds value is equal to zero")

    # extractig values of temp, temp_min and temp_max in 3 separate lists
    # validating that temp<=temp_max
    # validating that temp>=temp_min
    def test_temperature_range(self):

        temp = []
        for item in self.data:
            temp.append(item['main']['temp'])
        print(temp)

        temp_min = []
        for item in self.data:
            temp_min.append(item['main']['temp_min'])
        print(temp_min)

        temp_max = []
        for item in self.data:
            temp_max.append(item['main']['temp_max'])
        print(temp_max)

        self.assertGreaterEqual(temp_max, temp)
        self.assertLessEqual(temp_min, temp)

    # extracting values of all id in one list
    # extracting values of all description in one list
    # creating a dictionary with id value and description values as key:value pairs
    # validating that for id value=800, corresponding description is clear sky
    # validating that for id value=500, corresponding description is light rain
    def test_weather_id_description(self):
        weather = []

        for item in self.data:
            weather.append(item['weather'])
        print(weather[0][0]['id'])

        all_values = []
        all_keys_id = []
        for list in weather:
            for inner_list in list:
                for key in inner_list:
                    if 'id' in inner_list:
                        value = inner_list['id']
            all_keys_id.append(value)
        print(all_keys_id)

        for list in weather:
            for inner_list in list:
                for key in inner_list:

                    if 'description' in inner_list:
                        desc_value = inner_list['description']
            all_values.append(desc_value)
        print(all_values)

        id_desc = dict(zip(all_keys_id, all_values))
        print(id_desc)
        for key in id_desc:
            if key == 800 in id_desc: self.assertTrue(id_desc[key] == 'clear sky')
            if key == 500 in id_desc: self.assertTrue(id_desc[key] == 'light rain')


if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(
        output="D:/Users/KKumar23/PycharmProjects/Nimesa_test/reports"))

