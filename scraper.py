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

    def get_course_category(self,link):
        all_course_category=[]
        referer_agent_response=request.Request(link).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            soup = BeautifulSoup(referer_agent_response['referer'].content,features="html.parser")
            all_category_options=soup.find('select',{'class':'course_category_filter'}).find_all('option')
            for option in all_category_options:
                category={}
                if option.text!='Choose Category':
                    category['href']=option['value']
                    category['category_name']=option.text
                    all_course_category.append(category)
        return all_course_category


    def get_courses(self):
        referer_agent_response=request.Request(self.url).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            link=self.get_all_course_link(referer_agent_response['referer'])
            course_categorys=self.get_course_category(link)
            if course_categorys:
                root_path=self.create_directory()
                for category in course_categorys:
                    if category:
                        all_courses_by_category,category_path=self.get_all_course_by_cateory(category['href'],category['category_name'],root_path)
                        self.save_course_details_file(category_path,all_courses_by_category)

    def get_course_list_div(self,link):
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


    
    def get_all_course_by_cateory(self,link,category_name,root_path):
        course_list_div=self.get_course_list_div(link)
        if course_list_div:
            category_path=self.create_category_directory(root_path,category_name)
            all_course_by_category=self.get_course_title_and_details_page_link(course_list_div)
            return all_course_by_category,category_path

        
    
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
        course_benefits_div=course_content_div.find('div',{'class':'wywl_benefits'})
        if course_benefits_div:
            course_desc=course_benefits_div.find_all('p')
            # course_desc=course_benifits.find_all('p')
            description=''
            for de in course_desc:
                if de is not None and de.string is not None:
                    description+=de.string
            return description
        else:
            return 'Not found any description.'
        
    def get_learn_info(self,course_content_div):
        learn_info_ul=course_content_div.find('ul',{'class':'learn-mod'})
        if learn_info_ul:
            return learn_info_ul.text
        else:
            return 'Nothing found for learn info.'

    
    def get_benifits_of_course(self,course_content_div):
        benifits_ul=course_content_div.find('ul',{'class':'learn-benefit'})
        if benifits_ul:
            return benifits_ul.text
        else:
            return 'Nothing found for course benifits info.'

    
    def get_course_lessons(self,course_content_div):
        course_lessons=[]
        course_lessons_div=course_content_div.find_all('div',{'class':'lesson-title'})
        if course_lessons_div:
            for lesson in course_lessons_div:
                course_lessons.append(lesson.find('span',{'class':'timer-l'}).text)
        return course_lessons


    def save_course_details_file(self,category_path,all_courses):
        for course in all_courses:
            course_info=self.get_course_details(course['href'])
            self.create_file(category_path,course['course_header'],course_info)


    def get_course_details(self,link):
        referer_agent_response=request.Request(link).get_response_using_referer()
        if referer_agent_response['referer'] is not None:
            soup=BeautifulSoup(referer_agent_response['referer'].content,features="html.parser")
            course_content_div=soup.find('div',{'class':'course-content clearfix popup-container new-c-content'})
            course_details=self.get_course_and_furture_details(course_content_div)
            course_description=self.get_course_description(course_content_div)
            course_learn_info=self.get_learn_info(course_content_div)
            course_benifits=self.get_benifits_of_course(course_content_div)
            course_lessons=self.get_course_lessons(course_content_div)
            return {'course_details':course_details,'course_description':course_description,
            'course_learn_info':course_learn_info,'course_benifits':course_benifits,'course_lessons':course_lessons}

    def create_directory(self):
        '''
        create new directory name is NewSkilsCourse
        '''
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        directory_name='NewSkilsCourse'
        path = os.path.join(ROOT_DIR, directory_name) 
        if not os.path.exists(path):
            os.mkdir(path)
        return path
    
    def create_category_directory(self,parent_path,category_name):
        '''
        create file based on category name
        '''
        category_name=self.remove_special_character_and_spaces_from_string(category_name)
        path = os.path.join(parent_path, category_name)
        if not os.path.exists(path):
            os.mkdir(path)
        return path

    def remove_special_character_and_spaces_from_string(self,giveString):
        modifyString = giveString.translate ({ord(c): " " for c in "!@#$%^&*()[]{};:,./<>?\|`~-=_+"}) #replace all special charecter from category name
        modifyString=modifyString.replace(' ','') # replace all whitespace from category name
        return modifyString


    def create_file(self,path,file_name,course_info):
        '''
        create file based on course name
        '''
        file_name=self.remove_special_character_and_spaces_from_string(file_name)
        if not os.path.exists(path+'\\'+file_name):
            with open(path.strip()+'\\'+file_name+'.txt', 'w',encoding="utf-8") as f:
                f.write('Course details \n')
                if course_info['course_details']:
                    for info in course_info['course_details']:
                        f.write(info+"\n")
                f.write('\nCourse Description\n')
                f.write(course_info['course_description']+'\n')
                f.write('\n'+course_info['course_learn_info']+'\n')
                f.write('\n'+course_info['course_benifits']+'\n')
                f.write('\nCourse Lessons\n')
                if course_info['course_lessons']:
                    for lesson in course_info['course_lessons']:
                        f.write(lesson+'\n')

                f.close()


if __name__ == "__main__":
    url=input('Enter Url:')
    scraper=Scraper(url)
    scraper.get_courses()