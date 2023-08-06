import requests
from lxml import html
from spiderlib import DrupalPipeline

#
resp = requests.get("http://www.ala.org/news/press-releases")
if resp.status_code==200:
  links = html.etree.HTML(resp.text).xpath("//span[@class='field-content']//@href")
  links = ["http://www.ala.org"+x for x in links]

  for link in links:
    resp = requests.get(link)
    if resp.status_code==200:
      root = html.etree.HTML(resp.text)
      title = root.xpath("//h1[@class='page-header']//text()")
      title = "".join(title)
      content = root.xpath("//div[@class='field-items']//text()")
      content = "<p>".join(content)
      content = "来源地址 "+link+"<p>"+content




# d8 = DrupalPipeline(host="192.250.197.186:8887", user="developer", password="webadmin-password-123")
# values = []
# values.append(["我是标题", "我是内容"])
# d8.save(values)

