import requests as requests
from bs4 import BeautifulSoup

title = ""
paragraphs = []

def parse_job(url):
    # Parse job html and collect links, adding them to list in the job dict
    
    html = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(html.text, 'html.parser')

    title = soup.find_all('h1')
    text = soup.find_all('p')

    uls = soup.find_all('ul')
    responsibilities_1 = uls[4]
    responsibilities_2 = uls[5]
    requirements_1 = uls[6]

    for paragraph in text:
        paragraphs.append(paragraph.text)

    print(title[0].text)
    print("")
    for para in paragraphs[4:-9]:
        print(para)
    print("\nResponsibilities")
    for ul in responsibilities_1:
        print(ul.text)
    print("\nResponsibilities")
    for ul in responsibilities_2:
        print(ul.text)
    print("\nRequirements")
    for ul in requirements_1:
        print(ul.text)
    print("")


if __name__ == '__main__':

    
    parse_job("https://resources.workable.com/senior-auditor-job-description")
