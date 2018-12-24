from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import logging
import time

class InstagramBot():

  def __init__(self, username, password):
    self.username = username
    self.password = password
    self.driver = webdriver.Firefox()
  
  def close_browser(self):
    logging.basicConfig(filename=f'bot.log', level=logging.INFO)
    self.driver.close()
    logging.info(f'Closed session with {self.username}')

  def login(self):
    driver = self.driver
    driver.get("https://www.instagram.com/")
    time.sleep(2)
    # Login link
    login_link = driver.find_element_by_xpath('//a[@href="/accounts/login/?source=auth_switcher"]')
    login_link.click()

    time.sleep(2)
    username_input = driver.find_element_by_xpath('//input[@name="username"]')
    username_input.clear()
    username_input.send_keys(self.username)

    password_input = driver.find_element_by_xpath('//input[@name="password"]')
    password_input.clear()
    password_input.send_keys(self.password)
    password_input.send_keys(Keys.RETURN)

    time.sleep(2)
    try:
      not_now = driver.find_element_by_xpath('/html/body/div[3]/div/div/div/div[3]/button[2]')
    except:
      not_now = None
    if not_now:
      not_now.click()
    
  def like_pics(self, hashtags):
    logging.basicConfig(filename=f'bot.log', level=logging.INFO)
    logging.info('-------------- Starting New Session --------------')
    driver = self.driver
    for hashtag in hashtags:
      driver.get(f'https://www.instagram.com/explore/tags/{hashtag}/')
      time.sleep(2)
      for i in range(1, 3):
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(2)
      # Get picture link
      a_tags = driver.find_elements_by_tag_name('a')
      pics = [a.get_attribute('href') for a in a_tags]
      pics = [href for href in pics if '/p/' in href]
      logging.info(f'Starting picture liking on #{hashtag}')

      for pic in pics:
        driver.get(pic)
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        try:
          driver.find_element_by_xpath('//span[@aria-label="Unlike"]')
          logging.info(f'Skipped picture: {pic} in #{hashtag}')
          continue
        except Exception as e:
          try:
            driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
            logging.info(f'Liked picture: {pic} in #{hashtag}')
            time.sleep(2)
          except Exception as ex:
            time.sleep(1)

from settings import USERNAME, PASSWORD

bot = InstagramBot(USERNAME, PASSWORD)
bot.login()
# Put hashtags in the list below
bot.like_pics(['<hashtag>', '<hashtag>'])
bot.close_browser()