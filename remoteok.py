import requests
from bs4 import BeautifulSoup

URL = "https://remoteok.io"

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

def extract_job(html):
    title = html.find("h2", {"itemprop":"title"})
    if title:
        title = title.text
    else:
        return

    company = html.find("h3", {"itemprop":"name"})
    if company:
        company = company.text
    else:
        return

    location = html.find("div",{"class":"location"})
    if location:
        location = location.text
    else:
        location = ""

    link = html.find("a")["href"]
    return {
        "title": title, 
        "company":company, 
        "location":location, 
        "link":f"{URL}{link}"
    }

def extract_jobs(url):
    jobs = []
    print("Scrapping RE")
    result = requests.get(url, headers=headers)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find_all("td",{"class":"company_and_position"})
    for result in results:
        job = extract_job(result)
        jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"{URL}/remote-dev+{word}-jobs"
    jobs = extract_jobs(url)
    return jobs