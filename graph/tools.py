import json

import requests
from langchain_core.tools import tool
from yarl import URL


def search_govuk(query: str) -> list[URL]:
    """Search GOV.UK for a query and return the top 3 items."""
    base_url = 'https://www.gov.uk/api'

    search_url = f'{base_url}/search.json'
    search_params = {'q': query, 'count': 3}

    search_response = requests.get(search_url, params=search_params)
    search_response.raise_for_status()

    search_results = search_response.json().get('results', [])

    urls: list[URL] = []

    for result in search_results:
        base_path = result.get('link', '').lstrip('/')
        if not base_path:
            continue

        urls.append(URL(f'{base_url}/content/{base_path}'))

    return urls


def get_govuk_content(url: URL) -> str:
    """Return a call to the GOV.UK content API as a string."""
    content_response = requests.get(url)
    content_response.raise_for_status()

    return json.dumps(content_response.json(), indent=4)


@tool
def search(query: str) -> str:
    """Search GOV.UK for the answer to a question."""
    results = search_govuk(query)

    result_string: str = ''

    for url in results:
        result_string += get_govuk_content(url)

    return result_string


TOOLS = [search]
