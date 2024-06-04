import requests
# import pandas as pd
from bs4 import BeautifulSoup

state_names = ["Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", "California", "Colorado", "Connecticut", "District ", "of Columbia", "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]
state_lower = [state.lower() for state in state_names]

def mall_outlet(inp):
    # user_input = input("Are you searching for a mall or an outlet? (m [mall]/o [outlet]): ")

    while inp != 'm' and inp != 'o':
        inp = input(f'Please type either "m" for mall or "o" for outlets. Try again: ')
    
    if inp == 'm':
        return "malls"
    else:
        return "outlets"

def singular(str):
    return str[:-1]

def fetch_and_parse_url(url):
    """
    Fetches the content of the given URL and parses it using BeautifulSoup.
    
    Parameters:
    url (str): The URL of the webpage to fetch.
    
    Returns:
    BeautifulSoup: A BeautifulSoup object containing the parsed HTML content.
    """
    # Send a GET request to the specified URL
    page = requests.get(url)
    
    # Raise an exception if the request was unsuccessful
    page.raise_for_status()
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(page.text, 'html.parser')
    
    # Return the BeautifulSoup object
    return soup


# ~~~~~~~~~~~~~~~~~~~~~~~ MALLS ~~~~~~~~~~~~~~~~~~~~~~~ #


def find_mall_index(mall_names, target_mall):
    mall_names_lower = [mall.lower() for mall in mall_names]
    if target_mall.lower() in mall_names_lower:
        return mall_names_lower.index(target_mall)
    else:
        # print("Check to make sure the name is entered right")
        return None

def get_mall_info(soup):
    """
    """
    mall_urls = []
    mall_names = []

    mall_info_html = soup.find_all('div', class_ = 'info')
    mall_info = [mall.text.strip() for mall in mall_info_html]
    
    for mall in mall_info_html:
        mall_tag = mall.find('a').get('href')
        mall_urls.append(mall_tag)

    for mall in mall_info:
        extracted_name = mall.split("\n")[0]
        mall_names.append(extracted_name)

    return mall_names, mall_urls
    

# ~~~~~~~~~~~~~~~~~~~~~~~ STORES ~~~~~~~~~~~~~~~~~~~~~~~ #


def find_store_index(store_names, target_store):
    if target_store in store_names:
        return store_names.index(target_store)
    # else:
    #     print("Check to make sure the name is entered right")
    #     return None

def generate_mall_directory(mall_url):
    mall_soup = fetch_and_parse_url(mall_url)
    directory = mall_soup.find_all('ul', class_ = 'table1_flex')[1]
    unfiltered_store_info = [store.text.strip() for store in directory]
    
    store_names = [store for store in unfiltered_store_info if store !=""]
    store_sites = directory.find_all('a')
    store_links = [link.get('href') for link in store_sites]
    return store_names, store_links

def get_store_info(store_url):
    info_soup = fetch_and_parse_url(store_url)
    info_table = info_soup.find('table', class_ = 'table_info')

    brand_link = info_table.find_all('a')[0]
    brand_url = brand_link.get('href')
    return brand_url

def get_brand_site(brand_url):
    brand_soup = fetch_and_parse_url(brand_url)
    brand_table = brand_soup.find('table', class_='table_info')
    brand_site = brand_table.find_all('a')[-1].get('href')
    return brand_site

#####################################################################################################

def main():
    state = input("Enter the state you wish to view malls from (e.g., Alabama): ")
    if state.lower() not in state_lower:
        print(f"The State you entered could not be found. Please try again.")
        return

    is_mall = input(f'Are you searching for a mall or an outlet? (m [mall]/o [outlet]): ')
    mall_or_outlet = mall_outlet(is_mall)

    url = f'https://www.mallscenters.com/{mall_or_outlet}/{state}'
    soup = fetch_and_parse_url(url)


    mall_names, mall_urls = get_mall_info(soup)
    mall_names_lower = [mall.lower() for mall in mall_names]

    while True:
        target_mall = input("Enter the target %s name: " % singular(mall_or_outlet))
        if target_mall.lower() in mall_names_lower:
            break
        else:
            print("The %s you are looking for couldn't be found. Please try again." % singular(mall_or_outlet))

    mall_index = find_mall_index(mall_names, target_mall)

    if mall_index is not None:
        mall_url = mall_urls[mall_index]
        store_names, store_links = generate_mall_directory(mall_url)
        store_names_lower = [name.lower() for name in store_names]
        while True:
            target_store = input("Enter the target store name: ")
            store_index = find_store_index(store_names_lower, target_store.lower())
            if store_index is None:
                print("The store you are looking for couldn't be found. Please try again.")
            else:
                break
    
        store_url = store_links[store_index]
        brand_url = get_store_info(store_url)
        brand_site = get_brand_site(brand_url)
        print(f"The website for {store_names[store_index]} at {mall_names[mall_index]} is: {brand_site}")
        # elif store_index is None:
        #     target_store = input("Store couldn't be found. Check spelling or try again: ")
        #     store_index = find_store_index(store_names_lower, target_store.lower())

if __name__ == "__main__":
    main()