from bs4 import BeautifulSoup
import requests
import json
import os

git_link = "https://github.com"
root = "/JasonMWhite/gitlawca/tree/master/canada/eng/acts/"

alphabet = "a b c d e f g h i j k l m n o p q r s t u v w x y z".upper().split()

acts = {}
url_links = []

def scrape_law(root, letter):
    # Parse letter folders and get links to acts
    html = requests.get(root+letter)

    soup = BeautifulSoup(html.text, 'html.parser')
    links = soup.find_all('a')

    for link in links:
        if link.get('title'):
            if "md" in link.get('title'):
                #print(link, "\n")
                try:
                    acts[link.get('title')]['href'] = link.get('href')
                except KeyError:
                    acts[link.get('title')] = {}
                    acts[link.get('title')]['href'] = link.get('href')
                    acts[link.get('title')]['title'] = ""
                    acts[link.get('title')]['links'] = []
                    acts[link.get('title')]['link_count'] = 0
                url_links.append(link.get('href'))

def parse_act(url):
    # Parse act html and collect links, adding them to list in the act dict
    act = url[52:]
    html = requests.get(git_link+url)
    soup = BeautifulSoup(html.text, 'html.parser')

    titles = soup.find_all('h1')
    links = soup.find_all('a')

    for link in links:
        if '/JasonMWhite/gitlawca/blob/master/canada/eng/acts' in link.get('href'):
            if 'Act' in link.text or 'Code' in link.text:
                try:
                    acts[act]['links'].append(link.text)
                except KeyError:
                    acts[act] = {}
                    acts[act]['href'] = link.get('href')
                    acts[act]['title'] = ""
                    acts[act]['links'] = []
                    acts[act]['link_count'] = 0
                try:
                    acts[str(link.get('href'))[52:]]['title'] = link.text
                except KeyError:
                    act_key = str(link.get('href'))[52:]

                    acts[act_key] = {}
                    acts[act_key]['href'] = link.get('href')
                    acts[act_key]['title'] = link.text
                    acts[act_key]['links'] = []
                    acts[act_key]['link_count'] = 0


if __name__ == '__main__':

    for letter in alphabet:
        scrape_law(git_link + root, letter)

    for link in url_links:
        parse_act(link)

    print(acts)

    with open('test.json', 'w+') as f:
        f.write(json.dumps(acts))
