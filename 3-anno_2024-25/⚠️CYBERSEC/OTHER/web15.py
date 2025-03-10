from bs4 import BeautifulSoup
import requests
import re

html = requests.get("http://web-16.challs.olicyber.it/").text
soup = BeautifulSoup(html, "html.parser")
external_resources = []
links = []
for a in soup.find_all('a', href=True):
    external_resources.append(a['href'])
    links.append(("http://web-16.challs.olicyber.it" + a['href']))
print(external_resources)
print(links)

for link in links:
    html = requests.get(link).text
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all(string= re.compile("flag")):
        print(a)
        break

    for a in soup.find_all('a', href=True):
        if a['href'] not in external_resources:
            external_resources.append(a['href'])
            links.append(("http://web-16.challs.olicyber.it" + a['href']))

