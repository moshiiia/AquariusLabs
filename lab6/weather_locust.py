from locust import HttpUser, task

class WeatherTestUser(HttpUser):
    host = "https://wttr.in"

    @task
    def get_weather_test(self):
        response = self.client.get("/Novosibirsk?format=j1")

        #data = response.json()
        #print(data)
