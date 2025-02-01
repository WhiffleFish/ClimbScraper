import requests
import re
import datetime

URL = 'https://portal.rockgympro.com/portal/public/415a34a23151c6546419c1415d122b61/occupancy?&iframeid=occupancyCounter&fId=1038'

def get_occupancy():
    page = requests.get(URL)
    content = page.content.decode()
    s = r"'BLD'.* \n\s*'capacity'.*\n\s*'count' : \d{1,3}"
    re_match = re.search(s, content)
    if re_match:
        count_match = re.search(
            r"(?<='count' : )\d{1,3}",
            re_match.group(0)
        )
        return int(count_match.group(0))
    else:
        return float('nan')

def write_to_file(count, file='occupancy.csv'):
    with open(file, 'a') as file:
        file.write(', '.join([str(datetime.datetime.now()), str(count)])+'\n')

if __name__ == '__main__':
    occ = get_occupancy()
    write_to_file(occ)
