from locust import HTTPUser, task, tag, between


class User(HTTPUser):
    wait_time=between(1,3)

    host='http://127.0.0.1:4500'

    @task(3)
    def testGetMethod(self):
        self.client.get('/getData')

    @task(1)
    def testPostMethod(self):
        payload={'name':'Andrew', 'age':22, 'priority':3}

        self.client.post('/sendData', json=payload)


