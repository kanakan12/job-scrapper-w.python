import requests
from bs4 import BeautifulSoup

URL = f"https://stackoverflow.com/jobs?q=python"

def get_last_page():
    request = requests.get(URL)
    soup = BeautifulSoup(request.text, "html.parser")
    pages = soup.find("div", {"class":"s-pagination"}).find_all("a")
    print(pages)

def get_jobs():
    last_pages = get_last_page()
    return []