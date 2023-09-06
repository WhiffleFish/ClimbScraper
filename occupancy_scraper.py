from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time

opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode

browser = Firefox(options=opts, executable_path=r'/Users/tyler/code/random/climbing/geckodriver')
# browser.get('https://thespotgym.com/gym-occupancy')
browser.get(r'https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=1038')
print('Page Loaded')
time.sleep(5.0)
soup = BeautifulSoup(browser.page_source, features="html.parser")
print('Checking for count...')
elements = soup.find_all("div", id="facility-count")
count = elements[0].find_all("span", id="count")[0].text
browser.close()

print('Number of occupants:', count)
