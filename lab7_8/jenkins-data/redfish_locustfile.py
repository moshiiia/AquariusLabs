from locust import HttpUser, task

USERNAME = "root"
PASSWORD = "0penBmc"

class RedfishTestUser(HttpUser):
    host = "https://127.0.0.1:2443"
    
    def on_start(self):
        self.client.auth = (USERNAME, PASSWORD)
        self.client.verify = False

    @task
    def system_info_test(self):
        self.client.get("/redfish/v1/Systems/system")

    @task
    def power_state_test(self):
        response = self.client.get("/redfish/v1/Systems/system/")
        response.json().get("PowerState")
    