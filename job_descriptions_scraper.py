from bs4 import BeautifulSoup
import requests
import json
import os

source_link = "https://resources.workable.com/job-descriptions/"

jobs = {}
url_links = []

def scrape(source_link):
    # Parse letter folders and get links to jobs
    html = requests.get(source_link)

    soup = BeautifulSoup(html.text, 'html.parser')

    sections = soup.find_all('section')

    links = soup.find_all('a')

    for link in links:
        if link.get('title'):
            if "job description" in link.get('title'):
                #print(link, "\n")
                try:
                    jobs[link.get('title')]['href'] = link.get('href')
                except KeyError:
                    jobs[link.get('title')] = {}
                    jobs[link.get('title')]['href'] = link.get('href')
                    jobs[link.get('title')]['title'] = ""
                    jobs[link.get('title')]['links'] = []
                    jobs[link.get('title')]['link_count'] = 0
                url_links.append(link.get('href'))

def parse_job(url):
    # Parse job html and collect links, adding them to list in the job dict
    job = url[len(source_link):]
    html = requests.get(source_link)
    soup = BeautifulSoup(html.text, 'html.parser')

    titles = soup.find_all('h4')
    links = soup.find_all('a')

    for link in links:
        if source_link in link.get('href'):
            if 'Act' in link.text or 'Code' in link.text:
                try:
                    jobs[job]['links'].append(link.text)
                except KeyError:
                    jobs[job] = {}
                    jobs[job]['href'] = link.get('href')
                    jobs[job]['title'] = ""
                    jobs[job]['links'] = []
                    jobs[job]['link_count'] = 0
                try:
                    jobs[str(link.get('href'))[len(source_link):]]['title'] = link.text
                except KeyError:
                    job_key = str(link.get('href'))[len(source_link):]

                    jobs[job_key] = {}
                    jobs[job_key]['href'] = link.get('href')
                    jobs[job_key]['title'] = link.text
                    jobs[job_key]['links'] = []
                    jobs[job_key]['link_count'] = 0


if __name__ == '__main__':

    scrape(source_link)

    for link in url_links:
        parse_job(link)

    print(jobs)

    with open('test.json', 'w+') as f:
        f.write(json.dumps(jobs))
