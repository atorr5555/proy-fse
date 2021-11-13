from selenium import webdriver
from selenium.webdriver.chrome.options import Options
#from scrapy.selector import Selector
from parsel import Selector
import webbrowser

opts = Options()
opts.add_argument("--headless")

def youtube(cancion):
    i = cancion
    song = i.replace(" ", "+")
    base_url = "https://www.youtube.com"

    url = 'https://www.youtube.com/results?search_query=' + song

    driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=opts)
    driver.get(url)

    sel = Selector(driver.page_source)
    primer_resultado = sel.xpath('//div/h3/a[@class="yt-simple-endpoint style-scope ytd-video-renderer"]/@href').extract_first()
    link_primer_resultado = base_url + primer_resultado
    print(link_primer_resultado)
    driver.close()
    return link_primer_resultado
