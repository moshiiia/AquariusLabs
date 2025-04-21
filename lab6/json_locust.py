from locust import HttpUser, task

class PlaceholderTestUser(HttpUser):
    host = "https://jsonplaceholder.typicode.com"

    @task
    def posts_test(self):
        response = self.client.get("/posts?format=j1")

        # data = response.json()
        # print(data)
