import requests

def get_leaders():

    root_url = "https://country-leaders.onrender.com/"

    status_url = "status"
    countries_url = "/countries"
    leaders_url = "/leaders"
    cookie_url = "/cookie"

<<<<<<< Updated upstream
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
=======
    with requests.Session() as session:
        session.get(f"{root_url}/{cookie_url}")

        #Get cookies
        #req_cookies = requests.get(f"{root_url}/{cookie_url}")
        #cookie = req_cookies.cookies

        # Get countries list: ['us', 'be', 'ma', 'ru', 'fr']
        req_countries = session.get(f"{root_url}/{countries_url}")
        countries = req_countries.json()

        # Get leaders from each country and add them to dictionary.
        leaders_per_country = {}
>>>>>>> Stashed changes

    for country_code in countries:

        params = {'country': country_code}

<<<<<<< Updated upstream
        req_leaders = requests.get(f"{root_url}/{leaders_url}", params=params, cookies=cookie)
=======
                req_leaders = session.get(f"{root_url}/{leaders_url}", params=params)
            
                if req_leaders.status_code == 403:
                    session.get(f"{root_url}/{cookie_url}")
                    req_leaders = session.get(f"{root_url}/{leaders_url}", params=params)
>>>>>>> Stashed changes

        if req_leaders.status_code == 200:
            leaders_per_country[country_code] = req_leaders.json()
        else:
            print(req_leaders.status_code, f"Failed to retrieve leaders from: {country_code}")

<<<<<<< Updated upstream
    return leaders_per_country
=======
                    for leader in leaders_per_country[country_code]:
                        wikipedia_url = leader.get("wikipedia_url")
                        if wikipedia_url:
                            first_paragraph = get_first_paragraph(session, wikipedia_url)
                            if first_paragraph:
                                print(f"{first_paragraph}")

                else:
                    print(req_leaders.status_code, f"Failed to retrieve leaders from: {country_code}")

            except requests.RequestException as e:
                print(f"Could not retreive leaders for {country_code}: {e}")

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

get_leaders()
>>>>>>> Stashed changes
