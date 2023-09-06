from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

delay = 5 # seconds

opts = Options()
opts.headless = True
assert opts.headless  # Operating in headless mode

browser = Firefox(options=opts, executable_path=r'/Users/tyler/code/random/climbing/geckodriver')
# browser.get('https://thespotgym.com/gym-occupancy')
browser.get(r'https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=1038')

try:
    elem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'facility-count')))
    print(elem.text)
except TimeoutException:
    print("Loading took too much time!")

browser.close()
