import os
import re
import requests
from bs4 import BeautifulSoup



def fetch_page(url):
    """Fetch the content of a web page."""
    response = requests.get(url)
    response.raise_for_status()  # Raise an error for bad responses
    return response.text

def get_domain_from_url(url):
    """Extract the domain from a given URL."""
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_trailing_path(url):
    """Extract the trailing path from a given URL."""
    from urllib.parse import urlparse
    parsed_url = urlparse(url)
    return parsed_url.path

def path_to_filename(path):
    """Convert a URL path to a safe filename."""
    import re
    # Replace non-alphanumeric characters with underscores
    safe_filename = re.sub(r'[^a-zA-Z0-9]', '_', path)
    return safe_filename.strip('_') + '.html'


def retrieve_page(url, lang="es-ES"):    
    """Retrieve a single page and save its content."""
    # content
    page_content = fetch_page(url)
    soup = BeautifulSoup(page_content, 'html.parser')
    relevant_content = soup.find('div', class_=re.compile("^ChapterContent_reader"))

    filename = path_to_filename(get_trailing_path(url))
    data_filename = os.path.join(data_dir, filename)

    # Save the content to a file
    with open(data_filename, 'w', encoding='utf-8') as file:
        file.write(relevant_content.prettify())

    print(iter, f"Saved content from {next_link} to {data_filename}")

    # Find the next link
    next_link = soup.find_all('div', class_='[pointer-events:all]')[1].find('a')['href'].strip()
    #check if empty
    if not next_link:
        print("No more links found. Exiting.")
        return None

    next_link = schema + domain + next_link
    return next_link

def scrap_site(starting_url, lang="es-ES"):
    """Scrape the site starting from the given URL."""
    schema = 'https://'
    domain = get_domain_from_url(starting_url)

    data_dir = os.path.join("data", lang)


    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    next_link = starting_url
    iter = 0
    while next_link:
        iter += 1

        # content
        page_content = fetch_page(next_link)
        soup = BeautifulSoup(page_content, 'html.parser')
        relevant_content = soup.find('div', class_=re.compile("^ChapterContent_reader"))

        filename = path_to_filename(get_trailing_path(next_link))
        data_filename = os.path.join(data_dir, filename)

        # Save the content to a file
        with open(data_filename, 'w', encoding='utf-8') as file:
            file.write(relevant_content.prettify())

        print(iter, f"Saved content from {next_link} to {data_filename}")

        # Find the next link
        next_link = soup.find_all('div', class_='[pointer-events:all]')[1].find('a')['href'].strip()
        #check if empty
        if not next_link:
            print("No more links found. Exiting.")
            break

        next_link = schema + domain + next_link        



if __name__ == "__main__":
    
    #url = "https://www.bible.com/es-ES/bible/574/GEN.1.L%25C3%2591LE13" # TOBA

    url = "https://www.bible.com/es-ES/bible/222/GEN.1.BHTI" # BHTI
    url = "https://www.bible.com/es-ES/bible/222/SIR.8.BHTI"

    scrap_site(url, 'BHTI_es')