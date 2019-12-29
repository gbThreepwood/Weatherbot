"""
Unit tests for the weatherbot
"""

import weatherbot

class TestWeatherbot:

    def test_openweathermap_url_builder(self):
        assert "http://api.openweathermap.org/data/2.5/forecast?q=Bergen,no&mode=json&units=metric&APPID=dummykey" == weatherbot.openweathermap_url_builder("Bergen", True, "dummykey", "metric")
