import urllib.request
import re
from bs4 import BeautifulSoup



def check_exist(id,option="id"):
    id_str = str(id)
    url="https://twitter.com/intent/user?user_id="
    if option == "name":
        id_str = id_str.lower()
        url = "https://twitter.com/intent/user?screen_name="
    try:
        response = urllib.request.urlopen(
        url+id_str)
        html = response.read().decode()
        soup = BeautifulSoup(html, 'html.parser')
        #print(soup.title.text)
        soup.find_all("span",class_="nickname")[0].text
        return True
    except Exception as e:
        # print(e,id_str)
        return False
    
# check_exist("exterminus","name") 
