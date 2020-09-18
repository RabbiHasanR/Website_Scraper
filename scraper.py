import request
from bs4 import BeautifulSoup

class Scraper():

    def __init__(self,url):
        self.url=url


    def all_course_link(self,response):
        soup = BeautifulSoup(response.content,features="html.parser")
        myli = soup.findAll("li", {"class": "menu-item menu-item-type-custom menu-item-object-custom menu-item-723369"})
        if myli:
            for li in myli:
                children = li.findChildren("a" , recursive=False)
                if children:
                    #print(children[0]['href'],children[0].string)
                    return children[0]['href']

    
    def get_course_category(self,link):
        referer_agent_response,google_agent_response,randm_agent_response=request.Request(link).get_all_response()
        if referer_agent_response is not None:
            soup = BeautifulSoup(referer_agent_response.content,features="html.parser")  
            myul=soup.find_all('ul',{'class':'menu-cats'})

            if myul:
                for ul in myul:
                    myli=ul.findChildren('li')
                    for li in myli:
                        #print(li)
                        spans=li.findChildren('span',recursive=False)
                        #print(spans)
                        for s in spans:
                            #print(s)
                            a_tag=s.findChildren('a',recursive=False)
                            #print(a_tag)
                            if a_tag:
                                print(a_tag[0]['href'],a_tag[0].string)


    def get_courses(self):
        referer_agent_response,google_agent_response,randm_agent_response=request.Request(self.url).get_all_response()
        if referer_agent_response is not None:
            link=self.all_course_link(referer_agent_response)
            #print(link)
            self.get_course_category(link)
        else:
            if google_agent_response is  not None:
                pass
            else:
                if randm_agent_response is not None:
                    pass
if __name__ == "__main__":
    url=input('Enter Url:')
    scraper=Scraper(url)
    scraper.get_courses()