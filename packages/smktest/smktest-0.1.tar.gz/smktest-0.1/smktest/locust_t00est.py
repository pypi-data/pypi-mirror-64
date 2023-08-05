from   locust import HttpLocust, TaskSet, between, task, seq_task
from   locust.events import request_failure
import requests 
import json
import random


class WebsiteTasks(TaskSet):
    @task(1)
    def get_data_1(self):
        self.client.get("http://localhost:8000/api/v1/projectsss/") 


    @task(1)
    def get_data_2(self):
        self.client.get("http://localhost:8000/api/v1/testing/") 


    @task(1)
    def post_data_3(self):
        self.client.post("http://localhost:8000/api/v1/testing/",{'name': 'LoadTest', 'test_type': 'POST'}) 






class WebsiteUser(HttpLocust):
    task_set  = WebsiteTasks
    min_wait  = 5000
    max_wait  = 15000
