import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_pages(url):
    result = requests.get(url)
    soup = BeautifulSoup(result.text, "html.parser")

    searchCountPages = soup.find("div", {"id":"searchCountPages"})

    searchCountPages_lst = searchCountPages.string.strip().split(" ")

    for i in range(len(searchCountPages_lst)):
        idx = 0
        for j in range(len(searchCountPages_lst[i])):
            j -= idx
            if(searchCountPages_lst[i][j] < "0" or searchCountPages_lst[i][j] > "9"):
                searchCountPages_lst[i] = searchCountPages_lst[i].replace(searchCountPages_lst[i][j], "")
                idx += 1

    totalPages = int(searchCountPages_lst[len(searchCountPages_lst) - 1])

    max_page = int(totalPages / LIMIT)
    return max_page

def extract_job(html):
    title = html.find("h2", {"class":"title"}).find("a")["title"]
    company = html.find("span", {"class":"company"})
    if company:
        company_anchor = company.find("a")
        if company_anchor is not None:
            company = company_anchor.string
        else:
            company = company.string
        company = company.strip()
    else:
        company = None
    location = html.find("div", {"class":"recJobLoc"})["data-rc-loc"]
    job_id = html["data-jk"]
    return {
        "title": title, 
        "company": company, 
        "location": location, 
        "link": f"https://kr.indeed.com/viewjob?jk={job_id}"
    }

def extract_jobs(last_pages, url):
    jobs = []
    for page in range(last_pages):
        print(f"Scrapping indeed: Page: {page}")
        result = requests.get(f"{url}&start={page * LIMIT}")
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all("div", {"class":"jobsearch-SerpJobCard"})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"https://kr.indeed.com/jobs?q={word}&limit={LIMIT}"
    last_pages = get_last_pages(url)
    jobs = extract_jobs(last_pages, url)
    return jobs