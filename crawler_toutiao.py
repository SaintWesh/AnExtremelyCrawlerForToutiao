import json
import sys
from urllib import request, parse
from collections import namedtuple

NEWS_FIELDS = 'title abstract article_url'.split()

class TouTiaoCrawler:
  
  News = namedtuple('News', NEWS_FIELDS)
  MAX_OFFSET = 600  
  URL_PATTERN = "http://www.toutiao.com/search_content/?offset=%d&format=json&keyword=%s&autoload=true&count=20&cur_tab=1"
  
  def __init__(self):
    self._news_dict = {}

  def crawl(self, keyword):
    keyword = keyword.strip()    
    if not keyword:
      return
    if keyword not in self._news_dict:
      self._news_dict[keyword] = []
    news_list = self._news_dict[keyword]

    offset = 0
    while offset <= self.MAX_OFFSET:
      url = self.URL_PATTERN % (offset, parse.quote_plus(keyword))
      print("########" + url)
      offset_news = self._json_to_news(self._url_to_json(url))
      #如果爬完所有关键词，则停止
      if not offset_news:
        return    
      news_list.extend(offset_news)
      offset = offset + 20
    
  #从url获取json格式的信息
  def _url_to_json(self, url):
    if not url:
      return None
    
    with request.urlopen(url) as res:
      return json.loads(res.read().decode())['data']
  
  #返回获取的新闻
  def _json_to_news(self, json_data):
    if not json_data:
      print(json_data)
      return None
    
    print(len(json_data))
    news_from_json = []
    for news_data in json_data:
      if 'title' in news_data:
        print(news_data['title'])
        news_from_json.append(self.News._make(news_data[field] for field in NEWS_FIELDS))
    return news_from_json

if __name__ == '__main__':

  keyword = "Elon Musk"
  crawler = TouTiaoCrawler()
  crawler.crawl(keyword)
  

