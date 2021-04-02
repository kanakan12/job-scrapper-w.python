import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f"https://kr.indeed.com/jobs?q=python&limit={LIMIT}"

def extract_indeed_pages():
    result = requests.get(URL)
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

def extract_indeed_jobs(last_pages):
    for page in range(last_pages):
        result = requests.get(f"{URL}&start={page * LIMIT}")
        print(result.status_code)