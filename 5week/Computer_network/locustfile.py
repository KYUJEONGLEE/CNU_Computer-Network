from locust import HttpUser, task, between

class User(HttpUser):

    wait_time = between(1, 1)

    @task
    def get_index(self):
        self.client.get('/')
        self.client.get('/index.html')
        self.client.get('/myimage.jpg')
        self.client.get('/notfound.html')
        self.client.get('/mystyle.css')
        self.client.get('/myscript.js')
        self.client.get('/201602037.html')


