import requests
import datetime

from requests import ConnectionError

GITHUB_BASE_URL = "https://api.github.com/repos/"

def fetch_from_github_api(user, repo_name):
    
    """
    param user: repo ower str
    param repo_name: repon repo_name
    return: dictionary of caculated counts of open issues
    """
    response_dict = {}
    response_dict['total_count'] = 0
    response_dict['tf_count'] = 0
    response_dict['sd_count'] = 0
    response_dict['sd_old_count'] = 0
    issue_url_builder = GITHUB_BASE_URL + user+ '/' + repo_name +"/issues?state=open&page=%s"
    counter = 1
    while True:
        try:
            response = requests.get(url=issue_url_builder % counter)
        except ConnectionError:
            raise ConnectionError("Unable to fetch data, connection error")
        else:
            if response.status_code == 200:
                data = response.json()
                counter +=1
                if not data:
                    break
                response_dict['total_count'] += len(data)
                now = datetime.datetime.now()
                tf_hour_old = now - datetime.timedelta(hours=24)
                seven_day_old = now - datetime.timedelta(days=7)
                for i in xrange(len(data)):
                    created_at = datetime.datetime.strptime(data[i]["created_at"], "%Y-%m-%dT%H:%M:%SZ")
                    if tf_hour_old < created_at <= now:
                        response_dict["tf_count"] += 1
                    elif seven_day_old < created_at <= tf_hour_old:
                        response_dict["sd_count"] += 1
                    elif created_at < seven_day_old:
                        response_dict["sd_old_count"] += 1
            else:
                raise Exception("NOT FOUND")
    return response_dict
    
