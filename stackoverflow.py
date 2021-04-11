import requests
from bs4 import BeautifulSoup

URL = "https://stackoverflow.com"

def get_last_page(url):
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")
    pages = soup.find("div", {"class":"s-pagination"})
    if pages:
        pages = pages.find_all("a")
    else:
        return -1
    last_pages = pages[-3].get_text(strip=True)
    return int(last_pages)

def extract_job(html):
    title = html.find("h2", {"class":"fs-body3"}).find("a").text
    company, location = html.find("h3", {"class":"fs-body1"}).find_all("span", recursive = False)
    company = company.get_text(strip=True).strip(" \r")
    location = location.get_text(strip=True)
    job_id = html["data-jobid"]
    return {
        "title": title, 
        "company":company, 
        "location":location, 
        "link":f"{URL}/jobs/{job_id}"
    }

def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping SO: Page: {page}")
        result = requests.get(f"{url}&pg={page+1}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"-job"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"{URL}/jobs?r=true&q={word}"
    last_pages = get_last_page(url)
    if last_pages == -1:
        return
    jobs = extract_jobs(last_pages, url)
    return jobs