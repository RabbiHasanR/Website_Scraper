import request
import os
from bs4 import BeautifulSoup

class Scraper():

    def __init__(self,url):
        self.url=url


    def get_all_course_link(self,response):
        soup = BeautifulSoup(response.content,features="html.parser")
        atag = soup.find("li", {"class": "menu-item menu-item-type-custom menu-item-object-custom menu-item-723369"}).find('a')
        if atag:
            return atag['href']
        # if myli:
        #     for li in myli:
        #         children = li.findChildren("a" , recursive=False)
        #         if children:
        #             #print(children[0]['href'],children[0].string)
        #             return children[0]['href']

    
    def get_course_category(self,link):
        all_course_category=[]
        referer_agent_response=request.Request(link).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            soup = BeautifulSoup(referer_agent_response['referer'].content,features="html.parser")  
            category_menu_ul=soup.find_all('ul',{'class':'menu-cats'})
            if category_menu_ul:
                for ul in category_menu_ul:
                    category_li=ul.find_all('li')
                    for li in category_li:
                        category={}
                        #print(li)
                        spans=li.find_all('span')
                        atag=spans[-1].find('a')
                        if atag:
                            category['href']=atag['href']
                            category['category_name']=atag.text
                        all_course_category.append(category)
        return all_course_category

                        # #print(spans)
                        
                        # for s in spans:
                        #     #print(s)
                        #     a_tag=s.findChildren('a',recursive=False)
                        #     #print(a_tag)
                        #     if a_tag:
                        #         # print(a_tag[0]['href'],a_tag[0].string)
                        #         category['href']=a_tag[0]['href']
                        #         category['category_name']=a_tag[0].string
                        # all_course_category.append(category)
        # return all_course_category


    def get_courses(self):
        referer_agent_response=request.Request(self.url).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            link=self.all_course_link(referer_agent_response['referer'])
            #print(link)
            course_categorys=self.get_course_category(link)
            print(course_categorys)
            # if course_categorys:
            #     #print(course_categorys)
            #     root_path=self.create_directory()
            #     for category in course_categorys:
            #         if category:
            #             category_name=category['category_name'].strip()
            #             split_category=category_name.split('/')
            #             #print(split_category[0])
            #             category_path=self.create_category_directory(root_path,split_category[0])
            #             #print(category_path)
            #             all_courses_by_category=self.get_all_course_by_category(category['href'],split_category[0])
            #             #print('category:',split_category[0],all_courses_by_category)
            #             for course in all_courses_by_category:
            #                 self.create_file(category_path,course['course_header'])

    def get_course_list_div(self):
        referer_agent_response=request.Request(link).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            soup=BeautifulSoup(referer_agent_response['referer'].content,features="html.parser")
            course_list_div=soup.find('div',{'class':'response-results courses-listing1 clearfix'}).find_all('div',{'class':'wrap_post_course'})
            return course_list_div
    
    def get_course_title_and_details_page_link(self,course_list_div):
        all_course_by_category=[]
        if course_list_div is not None:
            for course in course_list_div:
                course_info={}
                header=course.find('h5',{'class':'nomargin'})
                details_link=course.find('a',{'class':'find-out-more'})
                course_info['course_header']=header.string
                course_info['href']=details_link['href']
                all_course_by_category.append(course_info)
        return all_course_by_category


    
    def get_course_header_and_details_page_link(self,link,category_name):
        
    
    def get_course_and_furture_details(self,course_content_div):
        box_single_div=course_content_div.select('div[class="box-single"]')
        details_info=[]
        if box_single_div:
            for box in box_single_div:
                all_li=box.find_all('li')
                if all_li:
                    for li in all_li:
                        details_info.append(li.text)
        return details_info

    def get_course_description(self,course_content_div):
        course_desc=course_content_div.find('div',{'class':'wywl_benefits'}).find_all('p')
        # course_desc=course_benifits.find_all('p')
        description=''
        for de in course_desc:
            description+=de.string
        return description
        
    def get_learn_info(self,course_content_div):
        return course_content_div.find('ul',{'class':'learn-mod'}).text

    
    def get_benifits_of_course(self,course_content_div):
        return course_content_div.find('ul',{'class':'learn-benefit'}).text
    
    def get_course_lessons(self,course_content_div):
        course_lessons=[]
        course_lessons_div=course_content_div.find_all('div',{'class':'lesson-title'})
        if course_lessons_div:
            for lesson in course_lessons_div:
                course_lessons.append(lesson.find('span',{'class':'timer-l'}).text)
        return course_lessons




    def get_course_details(self,link):
        referer_agent_response=request.Request(link).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            soup=BeautifulSoup(referer_agent_response['referer'].content,features="html.parser")
            course_content_div=soup.find('div',{'class':'course-content clearfix popup-container new-c-content'})
            #box_single_div=find_div.find_all('div',{'class':'box-single'})
            # print('details_info:',details_info)
            # print('course description:',desc)
            # print('what_you_learn:',what_you_learn)
            # print('benifits_of_taking_course:',benifits_of_taking_course)
            # print('course modules:',course_lessons)







    def create_directory(self):
        '''
        create new directory name is NewSkilsCourse
        '''
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        directory_name='NewSkilsCourse'
        path = os.path.join(ROOT_DIR, directory_name) 
        if not os.path.exists(path)
            os.mkdir(path)
        return path
    
    def create_category_directory(self,parent_path,directory_name):
        '''
        create file based on category name
        '''
        path = os.path.join(parent_path, directory_name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def create_file(self,path,file_name):
        '''
        create file based on course name
        '''
        file_name = file_name.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}) #replace all special charecter from category name
        file_name=file_name.replace(' ','') # replace all whitespace from category name
        if not os.path.exists(path+'\\'+file_name):
            with open(path.strip()+'\\'+file_name+'.txt', 'w') as f:
                f.write(file_name)
                f.close()

if __name__ == "__main__":
    url=input('Enter Url:')
    scraper=Scraper(url)
    scraper.get_courses()
    # scraper.get_course_details(url)
    #scraper.create_directory()