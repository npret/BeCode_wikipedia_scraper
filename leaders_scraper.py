import requests
from bs4 import BeautifulSoup
import string

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

def get_first_paragraph(wikipedia_url):
    leader_first_name = None

    for country_code, leaders in leaders_per_country.items():
        for leader in leaders:
            if leader['wikipedia_url'] == wikipedia_url:
                leader_first_name = leader['first_name']
                break
        if leader_first_name:
                break
        
    if not leader_first_name:
         print("Leader not found for this URL.")
         return None

    print(wikipedia_url)

    req_leader_wiki_url = requests.get(wikipedia_url)
    soup = BeautifulSoup(req_leader_wiki_url.content, 'html.parser')

    paragraphs = [p.text for p in soup.find_all("p")]

    for first_paragraph in paragraphs:
        if first_paragraph.strip():
            first_word = first_paragraph.lstrip().split()[0].strip(string.punctuation).lower()
            if first_word == leader_first_name.lower():
                return first_paragraph
            
    return None

# print(get_first_paragraph('https://fr.wikipedia.org/wiki/Emmanuel_Macron'))
