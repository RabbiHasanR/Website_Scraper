from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import time
import concurrent.futures
import asyncio
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
            


    def get_response_using_google_agent(self,timeout=7):
        '''
        get url response using google user agent
        '''
        result={}
        google_header={'User-Agent': user_agent.google_user_agent()}
        try:
            response = requests.get(self.url, headers=google_header,allow_redirects=True,timeout=timeout)#
            result['google']=response
            return result
            
        except :
            result['google']=None
            return result
            
            

    def get_response_using_user_agent(self,timeout=7):
        '''
        get url response using random user agent
        '''
        result={}
        random_header={'User-Agent': user_agent.user_agent()}
        try:
            response = requests.get(self.url, headers=random_header,allow_redirects=True,timeout=timeout)# 
            result['random']=response
            return result
            
        except :
            result['random']=None
            return result


    def parallel_process(self):
        fun_list=[self.get_response_using_referer,self.get_response_using_google_agent,self.get_response_using_user_agent]
        result_list=[]
        with concurrent.futures.ProcessPoolExecutor() as executor:
            for fun in fun_list:
                result_list.append(executor.submit(fun))
        executor.shutdown(wait=True)
        return result_list

    def get_all_response(self):
        referer_response=None
        google_response=None
        random_response=None
        result=self.parallel_process()
        for r in result:
            result=r.result()
            if 'referer' in result:
                referer_response=result['referer']
            elif 'google' in result:
                google_response=result['google']
            else:
                random_response=result['random']
        return referer_response,google_response,random_response



if __name__ == "__main__":
    url=input('Enter Url:')
    c=Request(url)
    start_time=time.time()
    print(c.get_all_response())
    print('crawler time:',time.time()-start_time)


    

            