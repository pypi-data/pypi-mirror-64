import requests
import json
import os
import csv

def crate_file_load_test(data_load):

    file = open("locust_test.py", "w") 
    file.write("from   locust import HttpLocust, TaskSet, between, task, seq_task") 
    file.write("\n")
    file.write("from   locust.events import request_failure") 
    file.write("\n")
    file.write("import requests ") 
    file.write("\n")
    file.write("import json") 
    file.write("\n")
    file.write("import random") 
    file.write("\n")
    file.write("\n")
    file.write("\n")
    
    
    print("GENERATE FILE: locust_test.py")
    
    file.write("class WebsiteTasks(TaskSet):") 
    file.write("\n")
    count = 0
    for i in data_load:
        count  = count + 1
        type_s = i["type"]
        url    = i["URL"]
        data_s = i["DATA"]
    
    
        if type_s ==  "get":
            
            file.write("    @task(1)")  
    
            file.write("\n")
            file.write("    def get_data_"+str(count)+"(self):")
            file.write("\n")
            file.write('        self.client.get("'+str(url)+'") ')  
            file.write("\n")
    
        elif type_s == "post":
            file.write("    @task(1)")  
            file.write("\n")
            file.write("    def post_data_"+str(count)+"(self):")
            file.write("\n")
            file.write('        self.client.post("'+str(url)+'",'+str(data_s)+') ') 
            
    
    
        file.write("\n")
        file.write("\n")
    
    file.write("\n")
    file.write("\n")
    file.write("\n")    
    file.write("\n")
    file.write("\n")
    file.write("class WebsiteUser(HttpLocust):")
    file.write("\n")
    file.write("    task_set  = WebsiteTasks")
    file.write("\n")
    file.write("    min_wait  = 5000")
    file.write("\n")
    file.write("    max_wait  = 15000")
    file.write("\n")
    
# locust  -f locust_test.py --host http://localhost:8000 --no-web -c 1000 -r 100  --run-time 10s  --step-load --step-clients 400  --step-time 10m --csv=example -t10s
    file.close() 
    

def start_load_test(data_load):

    crate_file_load_test(data_load)
    os.system('locust  -f locust_test.py --host http://localhost:8000 --no-web -c 1000 -r 100  --run-time 10s  --step-load --step-clients 200  --step-time 10m --csv=example -t10s')
    
    with open('example_failures.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        ROWs = []
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(f'\t{row[0]} works in the {row[1]} department, and was born in {row[2]}.')
                line_count += 1
    
            if line_count > 1:
                ROWs.append(row)    
            
        print(f'Processed {line_count} lines.')
        
        try:
            assert line_count == 1     
        except AssertionError as e:
            print("---   LOAD TEST ERROR:   ---- ")
            print()
            print(ROWs)
            print()
            print('--- --- --- --- --- --- ')
            e.args += ('some other', 'important', 'information', 42)
            raise    