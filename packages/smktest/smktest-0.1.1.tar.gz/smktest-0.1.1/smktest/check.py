import os
import time
import subprocess
import requests 
import json
#from   .create_load_test_file import *
import logging

def get_url_delete(URL,data):

    try:
        if URL[len(URL)-1] == '/':
            A = ''
        else:
            A = '/'
    
        URL = URL + A
        NAME = data.keys()
        VALUE = data.values()
        URL_GET = "?"
    
        for n,v in zip(NAME,VALUE):
            if n != 'id':
                URL_GET = URL_GET + str(n) + "=" + str(v) + '&'
        URL_GET = URL +URL_GET[0:len(URL_GET)-1]    
      
        response = requests.get(URL_GET)
        data = response.json()
        data = data['results']
        data = data[0]
        URL_DELETE = URL + str(data['id'])
    except:
        A = "NO EXISTE LOS DATOS"
        URL_DELETE = ""
    return URL_DELETE

def print_logs(NAME,PASS,URL,LOGS):
    if PASS =='OK':
        COLOR_CODE ='\033[92m'
    elif PASS =='ERROR':
        COLOR_CODE ='\033[91m'
    elif PASS == "HEADER":  COLOR_CODE= '\033[95m'
    elif PASS =="OKBLUE": COLOR_CODE= '\033[94m'
    elif PASS =="OKGREEN": COLOR_CODE= '\033[92m'
    elif PASS =="WARNING": COLOR_CODE= '\033[93m'
    elif PASS =="FAIL": COLOR_CODE= '\033[91m'
    elif PASS =="ENDC": COLOR_CODE= '\033[0m'
    elif PASS =="BOLD": COLOR_CODE= '\033[1m'
    elif PASS =="UNDERLINE": COLOR_CODE= '\033[4m'

    if len(URL) >= 40:
        URL = URL[0:37] + "..."

    print(COLOR_CODE + "|TYPE_TEST: =%12s | PASS: %8s    | URL: %40s| LOGS :%50s"%(NAME,PASS,URL,LOGS))    

def urlfilter(URL,data):
    if len(data) > 0 or data == None:
        if URL[len(URL)-1] == '/':
            A = ''
        else:
            A = '/'
        URL = URL + A
        NAME = data.keys()
        VALUE = data.values()
        URL_GET = "?"
        for n,v in zip(NAME,VALUE):
            if n != 'id':
                URL_GET = URL_GET + str(n) + "=" + str(v) + '&'
        URL_GET = URL +URL_GET[0:len(URL_GET)-1]    
    else:
        URL_GET = URL
    return URL_GET

class ping():
    def __init__(self,server):
        self.server  = server  # Service address to test
 
    def check(self):
        ip      = self.server
        output, error = subprocess.Popen((['ping', ip, '-c', '3']), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

        if len(error) == 0:
            
            PASS     = "OK"
            logs     = "SUCCESS"
            request  = 200
            passTest = True
        else:
            logs          = "Error 404: Fail Ping ("+str(ip)+")"
            request       = 404
            PASS          = "ERROR"
            passTest      = False

        print("PASSTEST PING: ",passTest)

        self.request  = request
        self.passTest = passTest
        self.logs     = logs
        
        return self.request,self.passTest,self.logs

        

class apirest():
    def __init__(self,URL,data=None,token=None,request_data=None):
        self.url          = URL
        self.data         = data
        self.token        = token      
        self.request_data = request_data
         
    def get(self):
        url          = self.url 
        data         = self.data
        data_request = {"A":"A"}
        token        = self.token
        request_data = self.request_data


        if token != None:
            head={'Authorization': token}
            response = requests.get(url, headers=head)
        else:
            response  = requests.get(url)
        code      = response.status_code    
        try:
            response = response.json()
            response = response.encode('ascii','ignore')
        except:
          print("ERROR")       
        print(response)         
        
        print("COOOODE:     ",code, url)
        print()
        print()
        print(request_data)
        print()
        print()

        if code == 200 or code == 202 or code == 203:
            CONTENT  = True   
            logs     = "OK SUCCESS"
            PASS     = "OK"
            passTest = True

            if request_data!= None:
                if request_data == response:
                    passTest= True
                else:
                    passTest= False
                    logs  = "ERROR GET: DATA request_data == request NOT IS IQUAL"
        else:
            CONTENT = False  
            code = 404  
            logs = "WARNING: Data not found ("+str(data)+")"
            PASS = "WARNING"
            passTest = False
        request = code  
            #// Check if exist the data filter
            


        data_request["request"]   = request  
        data_request["passTest"]  = passTest  
        data_request["logs"]      = logs
        

        self.request  = request
        self.passTest = passTest
        self.logs     = logs
        return  self.request,self.passTest,self.logs

    def post(self):
        url          = self.url 
        data2        = self.data
        token        = self.token
        request_data = self.request_data

        if True==True:
            # 1 Step: DELETE OLD DATA.
            # // 1 Step: DELETE OLD DATA.
            # 2 Step: POST DATA
            if token != None:
                head={'Authorization': token}
                response = requests.post(url,data=data2,headers=head)
            else:
                response  = requests.post(url,data=data2)           
            code     = int(response.status_code)

            print("PRINT CODE POST: ", code)

            try:
                response = response.json()
                response = response.encode('ascii','ignore')
            except:
                print("ERROR")

            # // 2 Step: POST DATA
            # Check if exist the data filter
            resp = response
            # resp      = response['results']
            if code ==  200 or code == 201:
                CONTENT = True   
                logs  = "SUCCESS"
                PASS     = "OK"
                passTest= True
                if request_data!= None:
                    if request_data == response and request_data != None:
                        passTest= True
                    else:
                        passTest= False
                        logs  = "ERROR POST:  DATA request_data == request NOT IS IQUAL"
            else:
                print("CLOSE ")
                passTest= False
                CONTENT = False  
                code = 404  
                logs = "WARNING: Data not found API ADRESS ("+str(url) +" "+ str(data2)+")"
                PASS = "WARNING"

            #// Check if exist the data filter
           
      #  else:
      #      code = 404
      #      logs = "FATAL ERROR APIsPost, CHECK THE >"+ str(url)
      #      request = 405
      #      passTest = False
      #  
        request = code
     
        self.request  = request
        self.passTest = passTest
        self.logs     = logs
        return  self.request,self.passTest,self.logs


    def put(self):
        url          = self.url 
        data         = self.data
        data_request = {"A":"A"}
        token        = self.token

        if token != None:
            head={'Authorization': token}
            response = requests.put(url,data=data,headers=head)
        else:
            response  = requests.put(url, data=data)

        code      = response.status_code

        print("COOOODE PUT:     ",code, url)

        if code == 200 or code == 202 or code == 203:
            CONTENT = True   
            logs  = "OK SUCCESS"
            PASS     = "OK"
            passTest= True
        else:
            CONTENT = False  
            code = 404  
            logs = "WARNING: Data not found ("+str(data)+")"
            PASS = "WARNING"
            passTest = False
         
        request = code  
        data_request["request"]   = request  
        data_request["passTest"]  = passTest  
        data_request["logs"]      = logs
        
        self.request  = request
        self.passTest = passTest
        self.logs     = logs

        return  self.request,self.passTest,self.logs

# D = apirest("http://localhost:8000/api/v1/project/",{"project": "Trust"}).get()

class smktest:
    class ping():
        name   = ''
        school = ''
        def __init__(self,server):
            self.server  = server  # Service address to test
        def check(self):
            ip      = self.server
            output, error = subprocess.Popen((['ping', ip, '-c', '2']), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
            if len(output) > 0:
                CODE = 200
                PASS = "OK"
                logs = "Test Ping Success CODE 200"
            else:
                logs = "Error Ping Test CODE 404"
                CODE = 404
                PASS = "ERROR"

            self.CODE = CODE
            return self

    class perform(): 
        def __init__(self,TYPE_TEST,URL,data=None,token=None,request_data=None):
            
            self.TYPE_TEST = TYPE_TEST  # Service address to test
            self.data      = data
            self.URL       = URL
            self.request   = 0
            self.token     = token
            self.request_data = request_data


            CODE = 0
            passTest = True
            if TYPE_TEST == "ping":
                DATA     = ping(URL).check()
                request  = DATA[0]
                passTest = DATA[1]
                logs     = DATA[2]

                test_metadata = "- TYPE:  PING TEST | CHECK THE SERVER ADRESS: ("+str(URL)+")"
                failure_list = ['','ERROR CASES:','','1. Inactive Service.','2. Service Address Error.']    

                assert passTest == True,"\n---- SMOKE TEST ERROR ----\n%s\n----FAILURE-LIST----\n%s"%(test_metadata,'\n'.join(failure_list)) 
                           
            elif TYPE_TEST == "ping_fail":
                DATA     = ping(URL).check()
                request  = DATA[0]
                passTest = DATA[1]
                logs     = DATA[2]

                test_metadata = "- TYPE:  PING TEST | CHECK THE SERVER ADRESS: ("+str(URL)+")"
                failure_list = ['','ERROR CASES:','','1. Inactive Service.','2. Service Address Error.']    

                assert passTest == False,"\n---- SMOKE TEST ERROR ----\n%s\n----FAILURE-LIST----\n%s"%(test_metadata,'\n'.join(failure_list)) 
                           

 
            elif TYPE_TEST == "api_get":
                
                DATA = apirest(URL,data,token=token,request_data=request_data).get()

                request  = DATA[0]
                passTest = DATA[1]
                logs     = DATA[2]

                test_metadata = "- TYPE:  API GET  TEST | CHECK THE SERVER ADRESS: ("+str(URL)+")"
                failure_list = ['','ERROR CASES:','','1. Inactive Service.','2. API Address Error.',]    


                assert  passTest == True,"\n---- SMOKE TEST ERROR ----\n%s\n----FAILURE-LIST----\n%s"%(test_metadata,'\n'.join(failure_list))      

            elif TYPE_TEST == "api_get_fail":
                DATA = apirest(URL,data).get()
                request  = DATA[0]
                passTest = DATA[1]
                logs     = DATA[2]

                test_metadata = "- TYPE:  API GET  TEST | CHECK THE SERVER ADRESS: ("+str(URL)+")"
                failure_list = ['','ERROR CASES:','','1. Inactive Service.','2. API Address Error.',]    
                assert  passTest == False,"\n---- SMOKE TEST ERROR ----\n%s\n----FAILURE-LIST----\n%s"%(test_metadata,'\n'.join(failure_list))      

            
            elif TYPE_TEST == "api_post":

                DATA = apirest(URL,data=data,token=token,request_data=request_data).post()
                print(DATA)
                request  = DATA[0]
                passTest = DATA[1]
                logs     = DATA[2]

                test_metadata = "- TYPE:  API POST  TEST | CHECK THE SERVER ADRESS: ("+str(URL)+")"
                failure_list = ['','ERROR CASES:','','1. Inactive Service.','2. API Address Error.','3. Incorrect data structure']   
                
                print(request)

                assert  passTest == True,"\n---- SMOKE TEST ERROR ----\n%s\n----FAILURE-LIST----\n%s"%(test_metadata,'\n'.join(failure_list))     

            elif TYPE_TEST == "api_post_fail":
                DATA = apirest(URL,data).post()
                request  = DATA[0]
                passTest = DATA[1]
                logs     = DATA[2]

                test_metadata = "- TYPE:  API POST  TEST | CHECK THE SERVER ADRESS: ("+str(URL)+")"
                failure_list = ['','ERROR CASES:','','1. Inactive Service.','2. API Address Error.','3. Incorrect data structure']        

                assert  passTest == False,"\n---- SMOKE TEST ERROR ----\n%s\n----FAILURE-LIST----\n%s"%(test_metadata,'\n'.join(failure_list))        

            elif TYPE_TEST == "api_put":

                DATA = apirest(URL,data=data,token=token).put()
                print(DATA)
                request  = DATA[0]
                passTest = DATA[1]
                logs     = DATA[2]

                test_metadata = "- TYPE:  API POST  TEST | CHECK THE SERVER ADRESS: ("+str(URL)+")"
                failure_list = ['','ERROR CASES:','','1. Inactive Service.','2. API Address Error.','3. Incorrect data structure']   
                
                assert  passTest == True,"\n---- SMOKE TEST ERROR ----\n%s\n----FAILURE-LIST----\n%s"%(test_metadata,'\n'.join(failure_list))   
              #  return request
            else:
                test_metadata = "- TYPE:  VERB ACCION NO EXIST: ("+str(URL)+") + >>>"+str(TYPE_TEST)+""
                failure_list = ['','ERROR CASES:','','1. ERROR INSERT CASE']   
                passTest = False 
                assert  passTest == True,"\n---- SMOKE TEST ERROR ----\n%s\n----FAILURE-LIST----\n%s"%(test_metadata,'\n'.join(failure_list))                                       


    #class load(): 
    #    def __init__(self,data_load):
    #        self.data_load = data_load
    #        start_load_test(data_load)


