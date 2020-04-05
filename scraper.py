from igramscraper.instagram import Instagram
import requests
import json

instagram = Instagram()

def scrapeAccount(username):
    details = [[]]
    u = username.strip()
    url='https://www.instagram.com/'+u+'/'
    account = instagram.get_account(username)

    # Profile Pic
    picUrl = account.get_profile_picture_url()
    if "44884218_345707102882519_2446069589734326272_n.jpg" in picUrl:
        details[0].append('0')
    else:
        details[0].append('1')

    # Nums / Length Username
    count=0
    for char in str(account.username):
        if char.isnumeric()==True:
            count=count+1
    if len(account.username)==0 or count==0:
        result=0
    else:
        result=count/len(account.username)
    details[0].append(str(round(result,3)))

    # Full Name Words
    result = len(account.full_name.split())             # using split() to count words in string
    details[0].append(str(result))

    # Bio Length
    details[0].append(str(len(account.biography)))
 
    # External URL
    if account.external_url == None:
        details[0].append('0')
    else:
        details[0].append('1')

    # Private
    if account.is_private==False:
        details[0].append('0')
    else:
        details[0].append('1')

    # Verified
    if account.is_verified==False:
        details[0].append('0')
    else:
        details[0].append('1')

    r = requests.get(url)
    body=r.text.split('window._sharedData = ')[1].split(';</script>')[0]
    data = json.loads(body)
    user=data['entry_data']['ProfilePage'][0]['graphql']['user']
    
    # Business
    if user['is_business_account']==False:
        details[0].append('0')
    else:
        details[0].append('1')

    # Post
    details[0].append(str(account.media_count))

    # Followers
    details[0].append(str(account.followed_by_count))
    followers = account.followed_by_count

    # Following
    details[0].append(str(account.follows_count))
    following = account.follows_count

    return details