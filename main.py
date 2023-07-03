
# configuration:-
"""
1 - FB auth:-
    - username: ...
    - password: ...
2 - created FB APP's APP_ID (create at https://developers.facebook.com/apps) # if incorrect: app will just fail
3 - owned FB page username |or| uid |or| url # if incorrect: app will just fail
"""
# init Database
# step 1: get FB page-long_lived-access-token
"""
- check cookies
-   if no cookies exist or are expired: login (to create them)
- check dev-user_access_token
-   if no dev-user_access_token exists or is expired: re-create it
- check dev-page_access_token
-   if no dev-page_access_token exists or is expired or page-changed: re-create it
"""
# step 2: get & format random Hadeeth
# step 3: post Hadeeth on FB page

## -:configuration:- ##
username = "iimosa7777@gmail.com"
password = "*********"
APP_ID = 1033059954377312
fb_page = 'https://www.facebook.com/Auto.Legend.Online.Arabic/'

# check type of fb_page:-
# fb_page = 'https://www.facebook.com/Auto.Legend.Online.Arabic/' => url => username
# fb_page = '1459422877420546' => str_uid => uid
# fb_page = 1459422877420546 => int_uid => uid
# fb_page = 'Auto.Legend.Online.Arabic' => username => username
fb_page_type = type(fb_page)
if fb_page_type is str:
    if len(fb_page) == 16:
        try:
            int(fb_page)
            fb_page_type = 'uid'
        except:
            pass
    fb_page_type = 'username'
    if 'facebook.com' in fb_page:
        fb_page = fb_page.split('facebook.com')[1].split('/')[1]
    else:
        fb_page = fb_page.replace(' ', '').replace('/', '')
elif fb_page_type is int:
    fb_page = str(fb_page)
    if len(fb_page) == 16:
        fb_page_type = 'uid'

# init DB
from db import db
db = db()

## -:step 1:- ##
import json
from udf import facebook
# feth user_access_token
user_access_token = db.config_read('user_access_token')
create_new_user_access_token = False
if user_access_token is None:
    create_new_user_access_token = True
else:
    if not facebook.is_token_valid(user_access_token):
        create_new_user_access_token = True
if create_new_user_access_token:
    # fetch FB cookies
    fb_cookies = db.config_read('fb_cookies')
    if fb_cookies is None:
        fb_cookies = {}
    else:
        fb_cookies = json.loads(fb_cookies)
    create_new_fb_cookies = False
    if not fb_cookies:
        create_new_fb_cookies = True
    else:
        if not facebook.is_cookies_valid(fb_cookies):
            create_new_fb_cookies = True
    if create_new_fb_cookies:
        fb_cookies = facebook.login_fb(username, password)
        # save fb_cookies to db
        db.config_write('fb_cookies', json.dumps(fb_cookies))
    # create new user_access_token
    user_access_token = facebook.get_fb_app_developer_user_access_token(
            APP_ID, fb_cookies, extra_permissions = facebook.PAGES_POSTS_PERMISSIONS
        )
    # save user_access_token to db
    db.config_write('user_access_token', user_access_token)
# fetch page_access_token
current_fb_page_uid = facebook.get_uid_by_username(fb_page, user_access_token)
page_access_token = db.config_read('page_access_token')
create_new_page_access_token = False
if page_access_token is None:
    create_new_page_access_token = True
elif current_fb_page_uid != str(db.config_read('fb_page_uid')):
    # first_run |or| fb_page has changed to another page
    create_new_page_access_token = True
elif not facebook.is_token_valid(page_access_token):
    # page_access_token has expired
    create_new_page_access_token = True
# create new page_access_token
if create_new_page_access_token:
    page_access_token = facebook.get_page_access_token(current_fb_page_uid, user_access_token)
    # save current_fb_page_uid to db
    db.config_write('fb_page_uid', current_fb_page_uid)
    # save page_access_token to db
    db.config_write('page_access_token', page_access_token)

## -:step 2:- ##
from random import choice as random_choice, randint
from requests import get as GET

def get_random_hadeeth_id():
    # get random category id
    category = random_choice(
        GET('https://hadeethenc.com/api/v1/categories/list/?language=ar').json()
      )
    category_id = category['id']
    # get random hadeeth from this category
    random_category_page_id = randint(1, int(category['hadeeths_count']))
    hadeeth_id = GET(
        f'https://hadeethenc.com/api/v1/hadeeths/list/?language=ar&category_id={category_id}&page={random_category_page_id}&per_page=1'
        ).json()['data'][0]['id']
    return hadeeth_id

def fetch_hadeeth_by_id(hadeeth_id):
    hadeeth = GET(f'https://hadeethenc.com/api/v1/hadeeths/one/?language=ar&id={hadeeth_id}').json()
    hadeeth = f"{hadeeth['hadeeth']}\n- {hadeeth['grade']} -"
    return hadeeth

hadeeth = fetch_hadeeth_by_id(get_random_hadeeth_id())
## -:step 3:- ##
from requests import post as POST
POST(
    f"https://graph.facebook.com/v15.0/{current_fb_page_uid}/feed",
    data = {
            'message': hadeeth,
            'access_token': page_access_token,
        },
    )

# NOTE: fix internet disconnect & timeout errors by using "unsafe" methods
