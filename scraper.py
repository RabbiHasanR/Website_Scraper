import request
import os
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
        all_course_category=[]
        referer_agent_response=request.Request(link).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            soup = BeautifulSoup(referer_agent_response['referer'].content,features="html.parser")  
            myul=soup.find_all('ul',{'class':'menu-cats'})

            if myul:
                for ul in myul:
                    myli=ul.findChildren('li')
                    for li in myli:
                        #print(li)
                        spans=li.findChildren('span',recursive=False)
                        #print(spans)
                        category={}
                        for s in spans:
                            #print(s)
                            a_tag=s.findChildren('a',recursive=False)
                            #print(a_tag)
                            if a_tag:
                                # print(a_tag[0]['href'],a_tag[0].string)
                                category['href']=a_tag[0]['href']
                                category['category_name']=a_tag[0].string
                        all_course_category.append(category)
        return all_course_category


    def get_courses(self):
        referer_agent_response=request.Request(self.url).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            link=self.all_course_link(referer_agent_response['referer'])
            #print(link)
            course_categorys=self.get_course_category(link)
            if course_categorys:
                #print(course_categorys)
                #root_path=self.create_directory()
                for category in course_categorys:
                    if category:
                        category_name=category['category_name'].strip()
                        split_category=category_name.split('/')
                        #print(split_category[0])
                        #category_path=self.create_category_directory(root_path,split_category[0])
                        all_courses_by_category=self.get_all_course_by_category(category['href'],split_category[0])
                        print('category:',split_category[0],all_courses_by_category)
    
    def get_all_course_by_category(self,link,category_name):
        all_course_by_category=[]
        referer_agent_response=request.Request(link).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            soup=BeautifulSoup(referer_agent_response['referer'].content,features="html.parser")
            all_course_div=soup.find('div',{'class':'response-results courses-listing1 clearfix'}).find_all('div',{'class':'wrap_post_course'})
            print('category_name',category_name,'total course:',len(all_course_div))
            for course in all_course_div:
                course_info={}
                #course_header=course_soup.find('div',{'class':'post_item post_item_courses post_item_courses_3 post_format_standard odd'}).find('div',{'class':'course-preview -course post_content ih-item colored square effect_dir left_to_right'}).find('div',{'class':'course-meta'}).find('header',{'class':'course-header'}).find('h5',{'class':'nomargin'})
                header=course.find('h5',{'class':'nomargin'})
                details_link=course.find('a',{'class':'find-out-more'})
                #print(details_link['href'],' ',header.string)
                course_info['course_header']=header.string
                course_info['href']=details_link['href']
                all_course_by_category.append(course_info)
        return all_course_by_category



    def create_directory(self):
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        directory_name='NewSkilsCourse'
        path = os.path.join(ROOT_DIR, directory_name) 
        os.mkdir(path)
        return path
    
    def create_category_directory(self,parent_path,directory_name):
        path = os.path.join(parent_path, directory_name)
        os.mkdir(path)
        return path

if __name__ == "__main__":
    url=input('Enter Url:')
    scraper=Scraper(url)
    scraper.get_courses()
    #scraper.create_directory()