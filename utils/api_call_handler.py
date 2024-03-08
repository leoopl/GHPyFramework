from pip._vendor import requests

from utils.json_handler import JSONHandler


class APICallHandler:

    def __init__(self):
        self.position = 0
        self.config = JSONHandler('./').open_json('config_dev.json')
        self.tokens_len = len(self.config['tokens'])
        self.username = self.config['tokens'][self.position]['username']
        self.auth_token = self.config['tokens'][self.position]['token']
        self.headers = {"Authorization": f"token {self.auth_token}"}

    def request(self, request_url):

        retry = 1
        while True:
            try:
                request = requests.get(request_url, params=[], auth=(self.username, self.auth_token))

                if request.status_code == 200:
                    break
                elif request.status_code == 403 or request.status_code == 401:
                    print(
                        "Your limit for this account reached the maximum. Add a new account to config_dev.json or wait 60 minutes for the limit to be freed. User: " + self.username)

                    self.position = self.position + 1
                    if self.position == self.tokens_len:
                        self.position = 0

                    self.username = self.config['tokens'][self.position]['username']
                    self.auth_token = self.config['tokens'][self.position]['token']


                else:
                    if 'page' in request_url:
                        print(request.status_code)
                        print(request_url)
                        return []
                    else:
                        print(request.status_code)
                        print(request_url)
                        return {}

            except Exception as e:
                print('Error in: ' + request_url)
                print('Retry number ' + str(retry))
                print(e)
                retry = retry + 1

        return request.json()
    
    # GRAPHQL API
    def graphql_request(self, query, variables):
        request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=self.headers)
        if request.status_code == 200:
            return request.json()
        elif request.status_code == 403 or request.status_code == 401:
            self.possiton = self.possiton + 1
            if self.possiton == self.tokens_len:
                self.possiton = 0
            self.auth_token = self.config['tokens'][self.position]['token']
            self.headers = {"Authorization": f"token {self.auth_token}"}
            return self.run_query(query, variables)
        else:
            raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))