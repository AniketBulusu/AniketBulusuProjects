### LIBRARIES ###
import sqlite3
import init_db as db
from datetime import datetime as dt
from argon2 import PasswordHasher

ph = PasswordHasher()


### FUNCTIONS ###

# prints welcome window
def welcome():
    print("=======================================")
    print("|          WELCOME TO TWITTER         |")
    print("=======================================")
    print("Choose one of the following options: ")
    print("1. Login")
    print("2. Registration")


# prints directory window
def directory():
    print("======================================")
    print("|              Directory             |")
    print("======================================")
    print("1. Post a new tweet")
    print("2. View your feed")
    print("3. Manage following")
    print("4. Exit")


## LOGIN / REGISTRATION

# user_id generation
# @return: new user_id
def user_id():

    # search for the maximum number of user_id in the user_profile table
    user_id = db.curr.execute("SELECT MAX(cast(user_id AS INTEGER)) FROM user_profile")
    user_id = db.curr.fetchone()

    # first user
    if user_id[0] is None:
        return 1

    # subsequent users
    else:
        return int(user_id[0]) + 1


# check username
# @param: username input by user
# @return: boolean True when there is such username in the user_profile table
def check_username(username):

    # search for username in user_profile table
    db.curr.execute("SELECT * FROM user_profile WHERE username=?", (username,))
    existing_user = db.curr.fetchone()

    return existing_user is not None


# check password
# @param: username and password input by user
# @return: boolean True when the password matches the username in the user_profile table
def check_password(username, password):

    # search for the username's password
    db.curr.execute("SELECT password FROM user_profile WHERE username=?", (username,))
    password_match = db.curr.fetchone()

    if password_match is None:
        return False
    try:
        return ph.verify(password_match[0], password)
    except:
        return False


# check email
# @param: email input by user
# @return: boolean True when there is such email in the user_profile table
def check_email(email):

    # search whether email is in the user_profile table
    db.curr.execute("SELECT * FROM user_profile WHERE email=?", (email,))
    existing_email = db.curr.fetchone()

    return existing_email is not None


# registration - adds new user to the user_profile table
# @param:
    # user_id: the new user_id generated
    # username: username input by the user
    # password: password input by the user
    # full_name: full name input by the user
    # email: email input by the user
    # profile_img: profile image input by the user
def new_user_entry(user_id, username, password, full_name, email, profile_img):

    # generate registration date
    registration_date = dt.now()

    # add new user to the table
    db.curr.execute("""INSERT INTO user_profile (user_id, username, password, full_name, email, profile_image, registration_date) VALUES (?, ?, ?, ?, ?, ?, ?) """, (user_id, username, password, full_name, email, profile_img, registration_date))
    db.conn.commit()


# login flow
# @return: user_id of the login
def login():

    # username input
    username = str(input("Username: "))

    # error handling when no username is entered
    while len(username) == 0:
        print("Error: Username must be at least one character.")
        username = str(input("Username: "))

    # password input
    password = str(input("Password: "))

    # error handling when no password is entered
    while len(password) == 0:
        print("Error: Password must be at least one character.")
        password = str(input("Enter Password again"))

    # check if password and username match the database
    username_match = check_username(username)
    password_match = check_password(username, password)

    # if login is successful, direct to the directory
    if username_match and password_match:
        print("Login successful!")

    # if login is not successful (password and username did not match), ask for login details again
    while not password_match or not username_match:
        print("Error: Username or password does not match. Please retry.")
        main()

    # get the user_id of the user logged in
    db.curr.execute("SELECT user_id FROM user_profile WHERE username=?", (username,))
    user_id = db.curr.fetchone()

    return user_id[0]


# password strength
# @return: boolean True if it is a strong password
def password_strength(password):

    special = "[@_!#$%^&*()<>?/|\+-~`=}{~:;.]"
    a, b, c, d = 0, 0, 0, 0

    # checks if the password contains at least 8 characters, lowercase, uppercase, digits, and special characters
    if (len(password) >= 8):
        for char in password:
            if (char.islower()):
                a += 1
            if (char.isupper()):
                b += 1
            if (char.isdigit()):
                c += 1
            if (char in special):
                d += 1

    if (a >= 1 and b >= 1 and c >= 1 and d >= 1 and a + b + c + d == len(password)):
        return True
    else:
        return False


# registration flow
# @return: new user_id generated
def registration():

    # username input
    username = str(input("Username: "))

    # error handling when no username is entered
    while len(username) == 0:
        print("Error: Username must be at least one character.")
        username = str(input("Username: "))

    # password input
    password = str(input("Password: "))

    # error handling when password is not strong
    while password_strength(password) == False:
        print("Error: Password must contain at least 8 characters, lowercase, uppercase, digits, and special characters.")
        password = str(input("Password: "))

    # hashing password
    hashed = ph.hash(password)

    # check if the user is an existing user
    username_match = check_username(username)

    # if an existing account is found, ask for login or registration again
    if username_match:
        print("Error: An existing account is found with the username. Please register again or login instead.")
        main()

    # if it is a new account being registered
    else:

        # full name prompt
        full_name = str(input("Full Name: "))
        while len(full_name) == 0:
            print("Error: Full name must be at least one character.")
            full_name = str(input("Full Name: "))

        # email prompt
        email = str(input("Email: "))
        while len(email) == 0:
            print("Error: Email must be at least one character.")
            email = str(input("Email: "))

        # check whether email exists
        while check_email(email):
            print("Error: The email is already associated with an account. Please use a different email.")
            email = str(input("Email: "))

        # upload profile image
        profile_img = str(input("Enter profile image: "))
        while len(profile_img) == 0:
            print("Error: Profile image must be at least one character.")
            profile_img = str(input("Enter profile image: "))

        # generate new user id
        new_userid = user_id()

        # add this new user to the user_profiles table
        new_user_entry(new_userid, username, hashed, full_name, email, profile_img)

        return new_userid


## TWEETING
# tweet_id generation
# @return: new tweet_id
def tweet_id():

    # search for the maximum number of tweet_id in the tweet table
    tweet_id = db.curr.execute("SELECT MAX(cast(tweet_id AS INTEGER)) FROM tweet")
    tweet_id = db.curr.fetchone()

    # if first tweet
    if tweet_id[0] is None:
        return 1

    # for subsequent tweets
    else:
        return int(tweet_id[0]) + 1


# post tweet
def post_tweet(user_id):

    # prompt for tweet content
    post_a_tweet = str(input("Post a new tweet: "))
    while len(post_a_tweet) == 0:
        print("Error: Tweet must contain at least one character.")
        post_a_tweet = str(input("Post a new tweet: "))

    # generate create time of the tweet
    create_time = dt.now()

    # add the tweet to the tweet table
    db.curr.execute("""INSERT INTO tweet (user_id, tweet_id, tweet_content, create_time) VALUES (?, ?, ?, ?) """, (user_id, tweet_id(), post_a_tweet, create_time))
    db.conn.commit()


## FEED
# view feed
def view_feed(user_id):

    # joining 3 tables: user_profiles for username of the tweeter; tweet table for all the tweets of the following user_id; follower table for selecting following_userids.
    # the t. is an alias for the tweet table that is to represent the table's column. i.e. t.user_id
    db.curr.execute("SELECT (SELECT Username FROM user_profile where user_id= t.user_id) username, t.tweet_id, t.tweet_content, t.create_time from tweet t where user_id in (SELECT following_userid FROM follower WHERE follower_userid=?) ORDER by create_time DESC", (user_id,))
    tweets = db.curr.fetchall()

    # dismantling the tuple returned
    tweet_ids = []
    usernames_list = []
    date_time_list = []
    tweets_content_list = []
    for item in tweets:
        tweet_ids.append(item[1])
        usernames_list.append(item[0])
        date_time_list.append(item[3])
        tweets_content_list.append(item[2])

    # find number of likes for each tweet
    likes_num = []
    for id in tweet_ids:
        num = db.curr.execute("SELECT COUNT(DISTINCT user_id) FROM like WHERE tweet_id=?", (id,))
        likes_num.append(num.fetchone()[0])

    # find the comments for each tweet
    comments = {}
    temporary_comment_list = []
    for i in range(len(tweet_ids)):
        comments_tuple = db.curr.execute("SELECT comment_text FROM comment WHERE tweet_id=?", (tweet_ids[i],))
        for item in comments_tuple:
            temporary_comment_list.append(item[0])

        comments[i] = temporary_comment_list
        temporary_comment_list = []

    # printing the results
    print("%-15s %-10s %-30s %-100s %-5s %-100s" % ("USERNAME", "TWEET_ID", "TIME", "TWEET", "LIKES", "COMMENTS",))

    for i in range(len(tweets)):
        print("%-15s %-10s %-30s %-100s %-5s %-100s" % (
        usernames_list[i], tweet_ids[i], date_time_list[i], tweets_content_list[i], likes_num[i], comments[i],))

    return tweet_ids


# manage feed selection
def manage_feed():
    print("--------------------------------------")
    print("1. Like")
    print("2. Comment")
    print("3. Main menu")


## LIKE
# like_id generator
# @return: new like_id
def like_id():

    # search for the maximum number of like_id in the like table
    like_id = db.curr.execute("SELECT MAX(cast(like_id AS INTEGER)) FROM like")
    like_id = db.curr.fetchone()

    # for first like
    if like_id[0] is None:
        return 1

    # for subsequent likes
    else:
        return int(like_id[0]) + 1


# add new like entry to like table
def like(user_id, tweet_id):

    # add like to the like table
    db.curr.execute("""INSERT INTO like (like_id, user_id, tweet_id) VALUES (?, ?, ?)""", (like_id(), user_id, tweet_id))
    db.conn.commit()


## COMMENT
# comment_id generator
# @return: new comment_id
def comment_id():

    # search for the maximum number of comment_id in the comment table
    comment_id = db.curr.execute("SELECT MAX(cast(comment_id AS INTEGER)) FROM comment")
    comment_id = db.curr.fetchone()

    # for first comment
    if comment_id[0] is None:
        return 1

    # for subsequent comments
    else:
        return int(comment_id[0]) + 1


# add new comment entry to comment table
def comment(user_id, tweet_id, comment):

    # generate comment time
    comment_time = dt.now()

    # add comment to the comment table
    db.curr.execute(
        """INSERT INTO comment (comment_id, user_id, tweet_id, comment_text, comment_time) VALUES (?, ?, ?, ?, ?) """, (comment_id(), user_id, tweet_id, comment, comment_time))
    db.conn.commit()


## FOLLOWING
# manage following
def manage_following():
    print("--------------------------------------")
    print("1. Follow users")
    print("2. Unfollow users")
    print("3. Main menu")


# search for the username given id
# @param: id of the username being looked for
def search_username(id):

    db.curr.execute("SELECT username FROM user_profile WHERE user_id=?", (id,))
    existing_username = db.curr.fetchone()
    return existing_username[0]


# check if the user_id exists in the user_profile table
# @param: id to be checked
def check_userid(id):

    db.curr.execute("SELECT * FROM user_profile WHERE user_id=?", (id,))
    exist = db.curr.fetchone()

    return exist is not None


# print list of users
# @return:
# filtered_ids: list of ids
# usernames_of_filtered_ids: list of corresponding usernames
def filter_follow(user_id, follow):

    filtered_ids = []
    usernames_of_filtered_ids = []

    # if following
    if follow == 1:
        # get all the user_ids where the user is currently following
        db.curr.execute("SELECT following_userid FROM follower WHERE follower_userid = ?", (str(user_id),))
        follower_table = db.curr.fetchall()

        # get all user_ids
        db.curr.execute("SELECT user_id FROM user_profile WHERE user_id != ?", (str(user_id),))
        users = db.curr.fetchall()

        # look for user_ids where the user has not followed yet
        for user in users:
            user_id = user[0]
            user_not_followed = True

            for follower in follower_table:
                # when the user id has already been followed
                if user_id == follower[0]:
                    user_not_followed = False
                    break

            # append ids of users who are not being followed
            if user_not_followed:
                filtered_ids.append(user_id)

        # find the usernames for each id
        for user_id in filtered_ids:
            usernames_of_filtered_ids.append(search_username(user_id))

    # if unfollowing
    elif follow == 2:
        # get all the user_ids where the user is currently following
        db.curr.execute("SELECT following_userid FROM follower WHERE follower_userid = ?", (str(user_id),))
        following_table = db.curr.fetchall()

        # when no users are being followed
        if len(following_table) == 0:
            print("You are not currently following anyone.")
        else:
            for following_ids in following_table:
                filtered_ids.append(following_ids[0])

            # find the usernames for each id
            for user_id in filtered_ids:
                usernames_of_filtered_ids.append(search_username(user_id))

    return filtered_ids, usernames_of_filtered_ids


# check if the current user is currently following a user
# @return: boolean True when the current user is not currently following a user
def check_follow(user_id, following_id):
    db.curr.execute("SELECT * FROM follower WHERE follower_userid=? AND following_userid=?", (user_id, following_id,))
    following = db.curr.fetchall()

    # when you're not following
    if following is None:
        return True

    # when you're currently following
    elif following is not None:
        return False


# follow id generator
# @return: new follow_id
def follow_id():
    # search for the maximum number of follow_id from the follower table
    follow_id = db.curr.execute("SELECT MAX(cast(follow_id AS INTEGER)) FROM follower")
    follow_id = db.curr.fetchone()

    # for first follow
    if follow_id[0] is None:
        return 1

    # for subsequent follows
    else:
        return int(follow_id[0]) + 1


# follow users
def follow_users(user_id):
    # follow index
    follow = 1

    # get a filtered list of ids and usernames
    ids_to_follow, usernames_to_follow = filter_follow(user_id, follow)

    # print out the available users to follow
    print("===================================")
    print("|    Users Available to Follow    |")
    print("===================================")
    print("Number of users: ", len(ids_to_follow))

    if len(ids_to_follow) > 0:

        print(" ")
        print("%3s %15s" % ("ID", "USERNAME"))

        for i in range(len(ids_to_follow)):
            print("%3s %15s" % (ids_to_follow[i], usernames_to_follow[i]))

        # ask for which user to follow
        userid_follow_selection = str(input("Which User ID would you like to follow?: "))

        while userid_follow_selection not in ids_to_follow:
            print(
                "Error: Invalid option. User not found, it is currently followed, or you're trying to follow yourself.")
            userid_follow_selection = str(input("Which User ID would you like to follow?: "))

        # add new follow entry
        db.curr.execute('''INSERT INTO follower (follow_id, follower_userid, following_userid) VALUES (?, ?, ?)''', (str(follow_id()), str(user_id), userid_follow_selection))
        db.conn.commit()

        print("User with ID", userid_follow_selection, "has been followed.")

    else:
        pass


# unfollow users
def unfollow_users(user_id):
    # unfollow index
    follow = 2

    # get a filtered list of IDs and usernames that the user is currently following
    ids_to_unfollow, usernames_to_unfollow = filter_follow(user_id, follow)

    # print out the users currently being followed
    print("===================================")
    print("|     Users Currently Followed    |")
    print("===================================")
    print("Number of users followed: ", len(ids_to_unfollow))

    if len(ids_to_unfollow) > 0:

        print(" ")
        print("%3s %15s" % ("ID", "USERNAME"))

        for i in range(len(ids_to_unfollow)):
            print("%3s %15s" % (ids_to_unfollow[i], usernames_to_unfollow[i]))

        # ask for which user to unfollow
        userid_unfollow_selection = str(input("Which User ID would you like to unfollow?: "))
        while userid_unfollow_selection not in ids_to_unfollow:
            print("Error: Invalid option. User not found or not currently being followed.")
            userid_unfollow_selection = str(input("Which User ID would you like to unfollow?: "))

        # remove the follow entry
        db.curr.execute('''DELETE FROM follower WHERE follower_userid = ? AND following_userid = ?''', (str(user_id), userid_unfollow_selection))
        db.conn.commit()

        print("User with ID ", userid_unfollow_selection, "has been unfollowed.")

    else:
        pass


# main
def main():
    # connect to a new database
    conn = sqlite3.connect('twitterlike.db')
    curr = conn.cursor()

    # welcome option
    welcome()
    welcome_option = str(input("What would you like to do?: "))

    while welcome_option not in ["1", "2"]:
        print("Error: Invalid option. Please enter 1 or 2.")
        welcome_option = str(input("What would you like to do?: "))

    # login
    if welcome_option == "1":
        new_userid = login()

    # registration
    elif welcome_option == "2":
        new_userid = registration()

    while True:

        # print directory
        directory()

        # directory input
        directory_selection = str(input("What would you like to do?: "))

        # error handling
        while directory_selection not in ["1", "2", "3", "4"]:
            print("Error: Please enter a correct directory number between 1 to 4.")
            directory_selection = str(input("What would you like to do?: "))

        # post tweet
        while directory_selection == "1":
            post_tweet(new_userid)
            break

        while directory_selection == "2":

            tweetid_ls = view_feed(new_userid)

            manage_feed()

            feed_selection = input("What would you like to do?: ")

            while feed_selection not in ["1", "2", "3"]:
                print("Error: Please enter a correct directory number between 1 to 3.")
                feed_selection = input("What would you like to do?: ")

            # like
            while feed_selection == "1":
                tweet_id_like = input("Which tweet ID would you want to like?: ")

                if str(tweet_id_like) not in tweetid_ls or len(str(tweet_id_like)) == 0:
                    print("Error: Please enter a valid tweet ID or you might not be currently following anyone. Please try again.")
                    break

                like(new_userid, tweet_id_like)
                break

            # comment
            while feed_selection == "2":
                tweet_id_comment = input("Which tweet ID would you want to comment?: ")

                if str(tweet_id_comment) not in tweetid_ls or len(str(tweet_id_comment)) == 0:
                    print("Error: Please enter a valid tweet ID or you might not be currently following anyone. Please try again.")
                    break

                comment_text = str(input("What's your comment?: "))

                while len(comment_text) == 0:
                    print("Error: Comments must not be blank.")
                    comment_text = input("What's your comment?: ")

                comment(new_userid, tweet_id_comment, comment_text)
                break

            if feed_selection == "3":
                break

        # manage following
        while directory_selection == "3":

            manage_following()

            follow_selection = input("What would you like to do?: ")

            while follow_selection not in ["1", "2", "3"]:
                print("Error: Invalid selection. Please enter a number from 1-3.")
                follow_selection = (input("What would you like to do?: "))

            # follow users
            if follow_selection == "1":
                follow_users(new_userid)

            # unfollow users
            elif follow_selection == "2":
                unfollow_users(new_userid)

            elif follow_selection == "3":
                break

        # exit
        if directory_selection == "4":
            print("Thank you for using Twitter. See you again!")
            break


main()
db.conn.close()