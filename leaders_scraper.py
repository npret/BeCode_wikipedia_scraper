import requests
from bs4 import BeautifulSoup
import re

def get_leaders():

    root_url = "https://country-leaders.onrender.com/"

    status_url = "status"
    countries_url = "/countries"
    leaders_url = "/leaders"
    cookie_url = "/cookie"

    #Get cookies
    req_cookies = requests.get(f"{root_url}/{cookie_url}")
    cookie = req_cookies.cookies
    print(req_cookies.status_code, cookie)

    # Get countries list: ['us', 'be', 'ma', 'ru', 'fr']
    req_countries = requests.get(f"{root_url}/{countries_url}", cookies=cookie)
    countries = req_countries.json()
    print(req_countries.status_code, countries)

    # Get leaders from each country and add them to dictionary.
    leaders_per_country = {}

    for country_code in countries:

        params = {'country': country_code}

        req_leaders = requests.get(f"{root_url}/{leaders_url}", params=params, cookies=cookie)

        if req_leaders.status_code == 200:
            leaders_per_country[country_code] = req_leaders.json()
        else:
            print(req_leaders.status_code, f"Failed to retrieve leaders from: {country_code}")

    return leaders_per_country

leaders_per_country = get_leaders()
# print(leaders_per_country)

def is_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

def get_first_paragraph(wikipedia_url):
    req_leader_wiki_url = requests.get(wikipedia_url)
    soup = BeautifulSoup(req_leader_wiki_url.content, 'html.parser')
    paragraphs = soup.find_all("p")

    for p in paragraphs:
        if p.find("b"):
            first_paragraph = p.text.strip()
            # Removes citations e.g. [4]
            first_paragraph_cleaned = re.sub(r'\[\d+]', '', first_paragraph).strip()
            
            #checks if arabic script and flips the paragraph around.
            if is_arabic(first_paragraph_cleaned):
                first_paragraph_cleaned = first_paragraph_cleaned[::-1]

            return first_paragraph_cleaned
    
    return None
