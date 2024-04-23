# import libraries
import sqlite3
from datetime import datetime as dt
from argon2 import PasswordHasher
ph = PasswordHasher()

# connect database
conn = sqlite3.connect('twitterlike.db')
conn.commit()
curr = conn.cursor()

## create tables
# user profile table
user_profile_sql = '''CREATE TABLE IF NOT EXISTS user_profile (user_id TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL, full_name TEXT NOT NULL, email TEXT NOT NULL, profile_image TEXT NOT NULL, registration_date TIMESTAMP, PRIMARY KEY (user_id))'''
curr.execute(user_profile_sql)

# tweet table
tweet_sql = '''CREATE TABLE IF NOT EXISTS tweet (user_id TEXT NOT NULL, tweet_id TEXT NOT NULL, tweet_content TEXT NOT NULL, create_time TIMESTAMP, PRIMARY KEY (tweet_id), FOREIGN KEY (user_id) REFERENCES user_profile(user_id))'''
curr.execute(tweet_sql)

# follower table
follow_sql = '''CREATE TABLE IF NOT EXISTS follower (follow_id TEXT NOT NULL, follower_userid TEXT NOT NULL, following_userid TEXT NOT NULL, PRIMARY KEY (follow_id), FOREIGN KEY (follower_userid) REFERENCES user_profile(user_id))'''
curr.execute(follow_sql)

# like table
like_sql = '''CREATE TABLE IF NOT EXISTS like (like_id TEXT NOT NULL, user_id TEXT NOT NULL, tweet_id TEXT NOT NULL, PRIMARY KEY (like_id), FOREIGN KEY (user_id) REFERENCES user_profile(user_id))'''
curr.execute(like_sql)

# commment table
comment_sql = '''CREATE TABLE IF NOT EXISTS comment (comment_id TEXT NOT NULL, user_id TEXT NOT NULL, tweet_id TEXT NOT NULL, comment_text TEXT NOT NULL, comment_time TIMESTAMP, PRIMARY KEY (comment_id), FOREIGN KEY (user_id) REFERENCES user_profile(user_id))'''
curr.execute(comment_sql)

## data population

try:  
    # add users
    hash = ph.hash("Howard@1")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("1", "HowardLeong", hash, "Howard Leong", "howard@ucalgary.ca", "howard_headshot.png", dt.now()),)
    hash = ph.hash("Aniket@1")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("2", "AniketBusulu", hash, "Aniket Busulu", "aniket@ucalgary.ca", "aniket_headshot.png", dt.now()),)
    hash = ph.hash("Shubhang@1")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("3", "ShubhangPeri", hash , "Shubhang Peri", "shubhang@ucalgary.ca", "shubhang_headshot.png", dt.now()),)
    hash = ph.hash("Jon@12345")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("4", "JonStewart", hash , "JonStewart", "jon@ucalgary.ca", "jon_headshot.png", dt.now()),)
    hash = ph.hash("Conan@12345")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("5", "ConanOBrien", hash , "Conan OBrien", "conan@ucalgary.ca", "conan_headshot.png", dt.now()),)
    hash = ph.hash("Sam@12345")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("6", "SamHarris", hash , "Sam Harris", "sam@ucalgary.ca", "sam_headshot.png", dt.now()),)
    hash = ph.hash("Bill@12345")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("7", "BillMaher", hash, "Bill Maher", "bill@ucalgary.ca", "bill_headshot.png", dt.now()),)
    hash = ph.hash("Steven@12345")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("8", "StevenBarlett", hash, "Steven Barlett", "steven@ucalgary.ca", "steven_headshot.png", dt.now()),)
    hash = ph.hash("Asheesh@12345")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("9", "AsheeshAdvani", hash, "Asheesh Advani", "asheesh@ucalgary.ca", "asheesh_headshot.png", dt.now()),)
    hash = ph.hash("Ray@12345")
    curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, ("10", "RayDalio", hash, "Ray Dalio", "ray@ucalgary.ca", "ray_headshot.png", dt.now()),)

    # create tweets
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("1", "1", "NFL views on 𝕏 up 41% YoY.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("1", "2", "More than 10 per human on average.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("2", "3", "The more remote the location, the better the connectivity.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("2", "4", "Trending well.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("3", "5", "Four more Starships, the last of V1.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("3", "6", "Still hard to believe Starship is real.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("4", "7", "Grok punches above its weights.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("4", "8", "met a meta metameme?", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("5", "9", "Met a non-meta meta build in Diablo?", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("5", "10", "Legacy media companies are  trying to kill this platform.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("6", "11", "Big companies steadily increase their Dilbert score over time like entropy.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("6", "12", "Also check their Highlights section.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("7", "13", "Starship stage separation.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("7", "14", "And AirPlay or Chromecast.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("8", "15", "𝕏 will overlay title in the upper potion of the image of a URL card.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("8", "16", "If you want to try a Tesla for a few days, you can rent one @Hertz.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("9", "17", "All design & engineering of the original @Tesla Roadster is now fully open source.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("9", "18", "What tangled webs we weave.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("10", "19", "This letter about OpenAI was just sent to me.", dt.now()),)
    curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, ("10", "20", "X Corp will be donating all revenue from advertising.", dt.now()),)

    # create following
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (1, 1, 2)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (2, 1, 5)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (3, 1, 9)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (4, 2, 8)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (5, 2, 3)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (6, 3, 5)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (7, 4, 1)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (8, 4, 7)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (9, 5, 8)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (10, 6, 3)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (11, 6, 10)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (12, 6, 2)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (13, 7, 10)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (14, 7, 5)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (15, 7, 2)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (16, 8, 1)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (17, 8, 10)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (18, 9, 6)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (19, 9, 7)""")
    curr.execute("""INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (20, 9, 8)""")

    # add likes
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (1, 1, 1)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (2, 1, 2)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (3, 1, 3)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (4, 2, 4)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (5, 2, 5)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (6, 3, 6)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (7, 4, 7)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (8, 4, 8)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (9, 5, 9)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (10, 6, 10)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (11, 6, 11)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (12, 6, 12)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (13, 7, 13)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (14, 7, 14)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (15, 7, 15)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (16, 8, 16)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (17, 8, 17)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (18, 9, 18)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (19, 9, 19)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (20, 10, 20)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (21, 6, 1)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (22, 6, 2)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (23, 7, 1)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (24, 7, 3)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (25, 7, 4)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (26, 8, 4)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (27, 8, 7)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (28, 9, 3)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (29, 9, 2)""")
    curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (30, 10, 10)""")

    # add comments
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("1", "1", "1", "Posts on 𝕏 that are added to your highlights tab will get greater reach", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("2", "1", "2", "All trolls go to heaven 😇", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("3", "2", "3", "My wallpaper", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("4", "3", "1", "𝕏 is nothing without its people", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("5", "3", "5", "Fraud has both civil & criminal penalties", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("6", "4", "6", "drop the OpenAI just Microsoft, its cleaner.", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("7", "4", "7", "The ratings on the OpenAI Telenovela are off the hook 🤣🤣", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("8", "5", "5", "As always, everything is open source, including the data.", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("9", "6", "9", "Media Matters is pure evil", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("10", "7", "10", "Looks like http://Instability.AI is still available", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("11", "8", "5", "Who will be President in 2032?", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("12", "8", "2", "Microsoft Clippy might paperclip us all!", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("13", "9", "14", "The future of space exploration is bright", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("14", "9", "18", "Beautiful pictures of Starship", dt.now()),)
    curr.execute("""INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, ("15", "10", "18", "Starship hot stage separation", dt.now()),)
except: 
    pass

conn.commit()