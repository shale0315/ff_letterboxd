from bs4 import BeautifulSoup

from get_films import get_films
# from rich import print
from time import sleep
from dotenv import load_dotenv
import os
import requests


movie_final = {}


def main():
    url_sub_list, url_titles = get_films()
    title_counter = 0
    load_dotenv()
    directory = os.getenv("DIRECTORY")
    vpn_switch = os.getenv("VPN_SWITCH")
    for item in url_sub_list:
        movie_data = {}
        print(f"Trying: {item}")
        url3= f"https://letterboxd.com{item}likes/"
        r = requests.get(url3)
        soup = BeautifulSoup(r.content, "html.parser")


        likes = soup.find(href=f"{item}likes/")
        watches = soup.find(href=f"{item}members/")


        if likes is None:
            print("Rate Limited -- Printing results to file")
            with open(f"{directory}likewatchratio.txt","w") as f:
                f.write(str(movie_final))
                return


        #Gets full string (i.e. "14 likes")
        likes_str=likes["title"]
        watches_str=watches["title"]

        #Strips string of extraneous chars
        if likes_str[0:2]=="1 ":
            stripped_likes=likes_str.strip(" like")
        else:
            stripped_likes = likes_str.strip(" likes")
        if watches_str == "1\xa0person":
            stripped_watches=watches_str.strip(" person")
        else:
            stripped_watches = watches_str.strip(" people")

        #Removes commas from string
        if "," in stripped_likes:
            num_likes=int(stripped_likes.replace(",",""))
        else:
            num_likes=int(stripped_likes)
        if "," in stripped_watches:
            num_watches = int(stripped_watches.replace(",", ""))
        else:
            num_watches=int(stripped_watches)

        #Checks if anyone has watched it and updates dictionary
        if num_watches == 0:
            movie_final[url_titles[title_counter]] = "Not enough data"
            title_counter += 1
        else:
            score=num_likes/num_watches
            movie_data["Likes"] = num_likes
            movie_data["Watches"] = num_watches
            movie_data["Ratio"] = score
            movie_final[url_titles[title_counter]] = movie_data
            title_counter += 1

        print(f"Done: {item}")
        os.system(vpn_switch)
        sleep(5)

main()
print(movie_final)