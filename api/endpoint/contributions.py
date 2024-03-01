import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta


class graphQL:

	def __init__(self, github_token):
		self.headers = {"Authorization": f"token {github_token}"}

	def run_query(self, query, variables):
		request = requests.post('https://api.github.com/graphql', json={'query': query, 'variables': variables}, headers=self.headers)
		if request.status_code == 200:
			return request.json()
		else:
			raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
	


	def getAllContributionsFromUser(self, user):
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
		return result["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]

token = "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"
GithubGraphql = graphQL(token)
users = ["leoopl", "Miller202", "Raksantos", "AndressaM"]
for user in users:
	contributions = GithubGraphql.getAllContributionsFromUser(user)
	print(contributions)