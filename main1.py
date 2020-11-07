from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import pickle
import random
from bs4 import BeautifulSoup as bsoup
import requests

class InstaMediaDownload:
    def __init__(self):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15")

        self.driver = webdriver.Firefox(profile, executable_path='./geckodriver')
        self.driver.get('https://www.instagram.com/')
        input('\n\nEnter After getting on profile...')
    def main(self):
        Post_links = []
        Download_links = []
        self.scroll_to_end()
        Html = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[3]/article').get_attribute('innerHTML')
        Soup = bsoup(Html)

        all_post = Soup.find_all('a')
        for tag in all_post:
            Post_links.append(f'https://www.instagram.com{tag.get("href")}')


        for url in Post_links:
            self.driver.get(url)
            sleep(2)
            Article = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div[1]/article/div[2]')
            Article_html = Article.get_attribute('innerHTML')
            Article_soup = bsoup(Article_html)
            try:
                image = Article_soup.find('img').get('src')
                Download_links.append(image)
                r = requests.get(image)
                file_name = (f'post{Download_links.index(image)+1}')
                with open(f'media/{file_name}.png', 'wb') as f:
                    f.write(r.content)
            except:
                video = Article_soup.find('video').get('src')
                Download_links.append(video)
                r = requests.get(video)
                file_name = (f'post{Download_links.index(video)+1}')
                with open(f'media/{file_name}.mp4', 'wb') as f:
                    f.write(r.content)


    def scroll_to_end(self):
        posts_number = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/header/section/ul/li[1]/span/span').get_attribute('innerHTML')
        result_num = int(''.join([i for i in posts_number if  i.isdigit()]))
        print(result_num)
        main = result_num//3
        for _ in range(main):
            sleep(0.7)
            self.driver.execute_script(f"window.scrollBy(0, 300);")
            
Bot = InstaMediaDownload()
Bot.main()
