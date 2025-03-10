from bs4 import BeautifulSoup
from bs4 import Comment

with open("index.html") as f:
    soup = BeautifulSoup(f, "html.parser")

comments = soup.find_all(string=lambda text: isinstance(text, Comment))
for c in comments:
    print(c)
    print("===========")
    c.extract()