import requests
from bs4 import BeautifulSoup
import re
import json
import os

def get_leaders():

    root_url = "https://country-leaders.onrender.com/"
    countries_url = "/countries"
    leaders_url = "/leaders"
    cookie_url = "/cookie"

    leaders_per_country = {}

    with requests.Session() as session:
        session.get(f"{root_url}/{cookie_url}")

        # Get countries list: ['us', 'be', 'ma', 'ru', 'fr']
        req_countries = session.get(f"{root_url}/{countries_url}")
        countries = req_countries.json()

        # Get leaders from each country and add them to dictionary.

        for country_code in countries:

            params = {'country': country_code}
        
            try:

                req_leaders = session.get(f"{root_url}/{leaders_url}", params=params)
            
                if req_leaders.status_code == 403:
                    session.get(f"{root_url}/{cookie_url}")
                    req_leaders = session.get(f"{root_url}/{leaders_url}", params=params)

                if req_leaders.status_code == 200:
                    leaders = req_leaders.json()
                    updated_leaders = []

                    for leader in leaders:
                        wikipedia_url = leader.get("wikipedia_url")
                        if wikipedia_url:
                            first_paragraph = get_first_paragraph(session, wikipedia_url)
                            if first_paragraph:
                                #print(f"{first_paragraph}")
                                leader["first_paragraph"] = first_paragraph
                            else:
                                leader["first_paragraph"] = None
                        updated_leaders.append(leader)      
                            
                    leaders_per_country[country_code] = updated_leaders

                else:
                    print(req_leaders.status_code, f"Failed to retrieve leaders from: {country_code}")

            except requests.RequestException as e:
                print(f"Could not retreive leaders for {country_code}: {e}")
    
    return leaders_per_country

def is_arabic(text):
    return bool(re.search(r'[\u0600-\u06FF]', text))

def get_first_paragraph(session, wikipedia_url):
    req_leader_wiki_url = session.get(wikipedia_url)
    soup = BeautifulSoup(req_leader_wiki_url.content, 'html.parser')
    paragraphs = soup.find_all("p")

    for p in paragraphs:
        if p.find("b"):
            first_paragraph = p.text.strip()
            # Removes citations e.g. [4], symbols and phonetic guides
            first_paragraph_cleaned = re.sub(r'\[\d+\]|\[.*?\]|/.*?/|[ɪˈˌːθðʃʒŋʊəɛɔɑɒʔʲʷ̃ɡʧʤ]|[ⓝⓘⓒⓗⓖⓞⓟⓑⓘⓛⓢ]|;|\b[a-z]+-[A-Z]+\b|\b[A-Z]+-[a-z]+\b', '', first_paragraph).strip()

            #checks if arabic script and flips the paragraph around.
            if is_arabic(first_paragraph_cleaned):
                first_paragraph_cleaned = first_paragraph_cleaned[::-1]

            return first_paragraph_cleaned
    
    return None

leaders_per_country = get_leaders()

def save(leaders_per_country):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(script_dir, "leaders.json")
    
    try: 
        with open(file_path, "w") as file:
            json.dump(leaders_per_country, file, indent=4)
        print(f"Saved to {file_path}")
        
        with open(file_path, "r") as file:
            loaded_leaders = json.load(file)

    except Exception as e:
        print(f"Error saving file: {e}")


save(leaders_per_country)
