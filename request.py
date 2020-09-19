import requests
import user_agent


class Request():

    def __init__(self,url):
        self.url=url 

    def get_response_using_referer(self,timeout=7):
        '''
        get url response using google referer and random user agent
        '''
        result={}
        random_header={'referer': 'http://www.google.com/url?sa=t&q={input_url}'.format(input_url=self.url),'User-Agent': user_agent.user_agent()}
        try:
            response = requests.get(self.url, headers=random_header,allow_redirects=True,timeout=timeout) # 
            result['referer']=response
            return result
        except :
            result['referer']=None
            return result
            

    

            