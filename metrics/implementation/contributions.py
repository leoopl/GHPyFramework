import requests
from datetime import datetime
from pymongo.database import Database
from dateutil.relativedelta import relativedelta


class ContributionsAPI:

	def __init__(self):
		self.github_token = ["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", "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"]
		# self.database = database
		self.possiton = 0
		self.tokens_len = len(self.github_token)
		self.headers = {"Authorization": f"token {self.github_token[self.possiton]}"}

	def run_query(self, query, variables):
		request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=self.headers)
		if request.status_code == 200:
			return request.json()
		elif request.status_code == 403 or request.status_code == 401:
			self.possiton = self.possiton + 1
			if self.possiton == self.tokens_len:
				self.possiton = 0
			self.headers = {"Authorization": f"token {self.github_token[self.possiton]}"}
			return self.run_query(query, variables)
		else:
			raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
	


	def getAllContributionsFromUser(self, user: str):
		today = datetime.now()
		one_yrs_ago = today - relativedelta(years=1)

		today_iso_date = today.isoformat()
		one_yrs_ago_iso_date = one_yrs_ago.isoformat()
		
		query = '''
			query($user : String!, $from: DateTime!, $to: DateTime!) { 
				user(login: $user) {
					contributionsCollection(from: $from, to: $to) {
						contributionCalendar {
							totalContributions
						}
					}
				}
			}'''

		variables = {
  			"user": user,
  			"from": one_yrs_ago_iso_date,
			"to": today_iso_date
		}	

		result = self.run_query(query, variables) #execute query
		contributions = result["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
		# self.database['users_api'].insert_one({"contributions_number": contributions})
		print(contributions)

GithubGraphql = ContributionsAPI()
users = ["leoopl", "Miller202", "Raksantos", "AndressaM"]
for user in users:
	GithubGraphql.getAllContributionsFromUser(user)
	