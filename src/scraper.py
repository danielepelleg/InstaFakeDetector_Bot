from igramscraper.instagram import Instagram
import requests
import time
import random
import datetime
from datetime import timedelta
import json

instagram = Instagram()

"""
Get the local time in day, day_number month year hour minute seconds format
"""
def get_time(epoch):
    a = time.strftime('%m/%d/%y', time.localtime(epoch))
    return a

"""
Take a media and check if his date of pubblication is in the last year and in which month
"""
def check_date(medias):
    month=[0,0,0,0,0,0,0,0,0,0,0,0]
    number_of_month=0
    date_list=[]
    for media in medias:
        date_to_check = datetime.datetime.strptime(get_time(media.created_time), '%m/%d/%y')
        if datetime.datetime.today() - date_to_check < timedelta(days=360):
            date_list.append(date_to_check)

    for date in date_list:
        last_post_date = date_list[len(date_list)-1]
        days=30
        counter=0
        while days<=360:
            if datetime.datetime.today() - date < timedelta(days=days):
                month[counter]+= 1
                if date == last_post_date:
                    number_of_month=counter+1
                break
            counter+=1
            days+=30
    totalPosts = 0
    # print(month)
    for i in month:
        totalPosts += i
    if len(date_list)==0:
        return 0
    else:
        return totalPosts / number_of_month

"""
    Scraper for private accounts
"""
def scrapeDefault(account):
    details = [[]]
    u = account.username.strip()
    url='https://www.instagram.com/'+u+'/'
    
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

    time.sleep(random.randrange(1,3))

    print('Dictionary:-\t', details)
    print('Dictionary Length: -\t', len(details[0]))

    return details

"""
    Scraper for Open Accounts
"""
def scrapeOpen(account):
    details = [[]]
    u = account.username.strip()
    url='https://www.instagram.com/'+u+'/'

    # Profile Pic
    picUrl=account.get_profile_picture_url()
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

    # Verified
    if account.is_verified == False:
        details[0].append('0')
    else:
        details[0].append('1')

    r = requests.get(url)
    body = r.text.split('window._sharedData = ')[1].split(';</script>')[0]
    data = json.loads(body)
    user = data['entry_data']['ProfilePage'][0]['graphql']['user']

    # Business
    if user['is_business_account'] == False:
        details[0].append('0')
    else:
        details[0].append('1')

    # Post
    mediaCount = str(account.media_count)
    details[0].append(mediaCount)

    # Followers
    details[0].append(str(account.followed_by_count))

    # Following
    details[0].append(str(account.follows_count))

    time.sleep(random.randrange(1,3))

    # Last Post Recent
    if mediaCount == '0':
        details[0].append('0')
    else:
        timestamp = int(user['edge_owner_to_timeline_media']['edges'][0]['node']['taken_at_timestamp'])
        if datetime.datetime.today() - datetime.datetime.strptime(get_time(timestamp), '%m/%d/%y') < timedelta(days=180):
            details[0].append('1')
        else:
            details[0].append('0')

    medias = instagram.get_medias(account.username, 100)

    time.sleep(random.randrange(1,3))

    # %Post Single Day (Day with the max of post on the total of posts)
    if mediaCount == '0':
        details[0].append('0')
    else:
        max=0
        post=1
        i=0
        while i < len(medias):
            for x in range(i+1, len(medias)):
                if time.strftime('%m/%d/%y', time.localtime(medias[i].created_time)) == time.strftime('%m/%d/%y', time.localtime(medias[x].created_time)):
                    post += 1
            if post > max:
                max = post
            i += post
            post = 1
        percentage = (max*100)/len(medias)
        details[0].append(str(round(percentage,3)))
    
    # Index of Activity (in the last year)
    if mediaCount == '0':
        details[0].append('0')
    else:
        details[0].append(str(round(check_date(medias),3)))

    # Average of Likes
    if mediaCount == '0':
        details[0].append('0')
    else:
        total_likes = 0
        for media in medias:
            total_likes += media.likes_count
        average_likes = total_likes/len(medias)        
        details[0].append(str(round(average_likes,3)))

    print('Dictionary:-\t', details)
    print('Dictionary Length: -\t', len(details[0]))

    return details

"""
    Scrape account with different scrapers if the account is private or not
"""
def scrapeAccount(username):
    try:
        print(username)
        account = instagram.get_account(username)

        if (account.is_private):
            return scrapeDefault(account)
    
        else:
            return scrapeOpen(account)

    except (Exception):
        return None