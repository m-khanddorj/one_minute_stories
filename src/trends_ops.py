from pytrends.request import TrendReq
import requests


# Function to get the top 5 trending topics in India using pytrends
def get_top_trending_topics_in_india(n):
    pytrends = TrendReq(hl='en-US', tz=360)
    trending_searches_df = pytrends.trending_searches(pn='india')
    top_5_trending_topics = trending_searches_df.head(n)[0].tolist()
    return top_5_trending_topics

# Function to get a related news article for each trending topic using News API
def get_related_news_articles(topics, news_api_key):
    news_articles = []
    for topic in topics:
        url = f"https://newsapi.org/v2/everything?q={topic}&apiKey={news_api_key}&pageSize=1"
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get('articles')
            if articles:
                news_articles.append({
                    'topic': topic,
                    'title': articles[0]['title'],
                    'description': articles[0]['description'],
                    'url': articles[0]['url']
                })
            else:
                news_articles.append({
                    'topic': topic,
                    'title': 'No article found',
                    'description': 'No description available',
                    'url': ''
                })
        else:
            news_articles.append({
                'topic': topic,
                'title': 'Error retrieving article',
                'description': f'Status code: {response.status_code}',
                'url': ''
            })
    return news_articles


def get_related_news_articles_bing(topics: list, subscription_key: str, count: int = 1) -> list:
    search_url = "https://api.bing.microsoft.com/v7.0/news/search"
    
    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    news_articles = []
    
    for topic in topics:

        params = {"q": topic, "mkt": "en-US", "count": count}
        try:
            response = requests.get(search_url, headers=headers, params=params)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return []

        search_results = response.json()
        news_items = search_results.get("value", [])
        
        if not news_items:
            print("No news items found.")
            return []
        
        for item in news_items:
            news_articles.append({
                'topic': topic,
                'title': item['name'],
                'description': item['description'],
                'url': item['url']
            })
    
    return news_articles


