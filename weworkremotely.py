import requests
from bs4 import BeautifulSoup

URL = "https://weworkremotely.com"

def extract_job(html):
    title = html.find("span", {"class":"title"})
    if title:
        title = title.text
    else:
        return

    company = html.find("span", {"class":"company"})
    if company:
        company = company.text
    else:
        return

    location = html.find("span", {"class":"region"})
    if location:
        location = location.text
    else:
        return

    link = html.find("a", recursive=False)["href"]
    return {
        "title": title, 
        "company":company, 
        "location":location, 
        "link":f"{URL}{link}"
    }

def extract_jobs(url):
    jobs = []
    print("Scrapping WR")
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")
    results = soup.find("section", {"class":"jobs"})
    if results:
        results = results.find_all("li")
    else:
        return
    for result in results:
        job = extract_job(result)
        if job is not None:
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"{URL}/remote-jobs/search?term={word}"
    jobs = extract_jobs(url)
    return jobs