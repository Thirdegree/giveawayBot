import webbrowser, praw

app_id='x'
app_secret='x'
app_uri='https://127.0.0.1:65010/authorize_callback'
app_ua = "Giveaway by /u/thirdegree"
app_scope = 'account creddits edit flair history identity livemanage modconfig modcontributors modflair modlog modothers modposts modself modwiki mysubreddits privatemessages read report save submit subscribe vote wikiedit wikiread'
app_refresh = 'x'


def login():
    r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)
    return r

def onetime():
    r = praw.Reddit(app_ua)
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    url = r.get_authorize_url("hoihcsoice", app_scope, app_uri)
    webbrowser.open(url)
    code = input("Click \"Allow\" then input the string directly after \"&code=\" in the address bar:\n")
    accessInformation = r.get_access_information(code)
    r.refresh_access_information(accessInformation['refresh_token'])
    print("\n\n\nIn obot.py set app_refresh to " + accessInformation['refresh_token'] + "\n\n\n")

if __name__ == '__main__':
    onetime()