from requests import get
from bs4 import BeautifulSoup
class coronavirus(object):
    def __init__(self):
        self.site1 = BeautifulSoup(get("https://www.worldometers.info/coronavirus/").content, "lxml")
        self.site2 = BeautifulSoup(get("http://koronovirus.site/").content, "lxml")
    def worldometers(self):
        return [self.site1.find_all("span")[4].string.replace(",",""), self.site1.find_all("span")[5].string.replace(",",""), self.site1.find_all("span")[6].string.replace(",",""), str(int(self.site1.find_all("span")[4].string.replace(",",""))-int(self.site1.find_all("span")[5].string.replace(",",""))-int(self.site1.find_all("span")[6].string.replace(",","")))]
    def monitor(self):
        return [self.site2.find_all("div")[5].text.replace("\t","").replace("\n","").replace("\r","").split()[0], self.site2.find_all("div")[8].text.replace("\t","").replace("\n","").replace("\r","").split()[0], self.site2.find_all("div")[11].text.replace("\t","").replace("\n","").replace("\r","").split()[0], str(int(self.site2.find_all("div")[5].text.replace("\t","").replace("\n","").replace("\r","").split()[0])-int(self.site2.find_all("div")[8].text.replace("\t","").replace("\n","").replace("\r","").split()[0])-int(self.site2.find_all("div")[11].text.replace("\t","").replace("\n","").replace("\r","").split()[0]))]