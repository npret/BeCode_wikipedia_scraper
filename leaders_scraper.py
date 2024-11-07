import requests

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
