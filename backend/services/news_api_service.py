import requests
import os

class NewsAPIService:
    BASE_URL = 'https://newsapi.org/v2'
    API_KEY = '1e642381fe9d49ae8a5554db83d01aa1'

    @staticmethod
    def get_top_headlines(country='us', category=None, q=None, page_size=20, page=1):
        params = {
            'apiKey': NewsAPIService.API_KEY,
            'country': country,
            'pageSize': page_size,
            'page': page
        }
        if category:
            params['category'] = category
        if q:
            params['q'] = q

        response = requests.get(f'{NewsAPIService.BASE_URL}/top-headlines', params=params)
        response.raise_for_status()
        return response.json()

    @staticmethod
    def get_everything(q, page_size=20, page=1):
        params = {
            'apiKey': NewsAPIService.API_KEY,
            'q': q,
            'pageSize': page_size,
            'page': page,
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
    
    @staticmethod
    def get_indian_news(category=None, page_size=20):
        try:
            from datetime import datetime, timedelta
            
            # Get date for last 24 hours
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            # Search from all major Indian news publishers
            params = {
                'apiKey': NewsAPIService.API_KEY,
                'q': 'India OR Indian OR Delhi OR Mumbai OR Modi OR BJP OR Congress OR Bangalore OR Chennai OR Kolkata OR Hyderabad',
                'domains': 'timesofindia.indiatimes.com,thehindu.com,indianexpress.com,hindustantimes.com,ndtv.com,news18.com,indiatoday.in,thequint.com,scroll.in,firstpost.com,livemint.com,business-standard.com,economictimes.indiatimes.com',
                'from': yesterday,
                'pageSize': page_size,
                'sortBy': 'publishedAt'
            }
            
            response = requests.get(f'{NewsAPIService.BASE_URL}/everything', params=params)
            response.raise_for_status()
            return response.json()
        except:
            # Final fallback to general India search
            return NewsAPIService.get_everything('India', page_size)