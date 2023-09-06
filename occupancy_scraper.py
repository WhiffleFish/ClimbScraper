from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os

delay = 5 # seconds

opts = Options()
opts.headless = True

browser = Firefox(options=opts, executable_path=os.path.join(os.path.dirname(__file__), 'geckodriver'))
# browser.get(r'https://thespotgym.com/gym-occupancy')
browser.get(r'https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=1038')

try:
    elem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'facility-count')))
    time.sleep(1.0)
    print(elem.text)
except TimeoutException:
    print("Loading took too much time!")

browser.close()
