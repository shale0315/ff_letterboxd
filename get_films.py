import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def get_films():
    load_dotenv()
    url=os.getenv("FILMS_LIST_URL")
    directory=os.getenv("DIRECTORY")
    r=requests.get(url)
    soup=BeautifulSoup(r.content, "html.parser")

    # print(soup.prettify())

    # print(soup.find("div"))
    # print(soup.find_all("div"))

    # divs=soup.find("div")
    # # print(divs.find_next("div"))
    # divs2=divs.find_next("div")
    # # print(divs2.find_next("div"))
    # divs3=divs2.find_next("div")
    # print(divs3.find_next("div"))

    # print(soup.div["data-target-link"])
    # print(soup.find("li", {'class':'"posteritem'},["data-details-endpoint"]))

    # print(soup.find("ul", {'class':'js-list-entries poster-list -p125 -grid'}))
    movies=soup.find("ul", {'class':'js-list-entries poster-list -p125 -grid'})
    # print(movies)
    # i=0
    # filtered_movies=[]
    url_sub_list = []
    title_list = []
    for item in movies:
        if item != "\n":
            # print(f"Item {i}: {item.div['data-target-link']}")
            url_sub_list.append(item.div['data-target-link'])
            with open(f"{directory}letterboxd_url_subs.txt", "a") as f:
                f.write(f"{item.div['data-target-link']}\n")
            with open(f"{directory}letterboxd_titles.txt", "a") as f:
                f.write(f"{item.div['data-item-name']}\n")
            title_list.append(item.div['data-item-name'])
            # i+=1
    return url_sub_list, title_list