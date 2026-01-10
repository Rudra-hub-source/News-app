import requests
import os

class NewsAPIService:
    BASE_URL = 'https://newsapi.org/v2'
    API_KEY = '1e642381fe9d49ae8a5554db83d01aa1'

    @staticmethod
    def get_top_headlines(country='us', category=None, q=None, page_size=20):
        params = {
            'apiKey': NewsAPIService.API_KEY,
            'country': country,
            'pageSize': page_size
        }
        if category:
            params['category'] = category
        if q:
            params['q'] = q

        response = requests.get(f'{NewsAPIService.BASE_URL}/top-headlines', params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_everything(q, page_size=20):
        params = {
            'apiKey': NewsAPIService.API_KEY,
            'q': q,
            'pageSize': page_size,
            'sortBy': 'publishedAt'
        }
        response = requests.get(f'{NewsAPIService.BASE_URL}/everything', params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_sources():
        params = {'apiKey': NewsAPIService.API_KEY}
        response = requests.get(f'{NewsAPIService.BASE_URL}/sources', params=params)
        response.raise_for_status()
        return response.json()