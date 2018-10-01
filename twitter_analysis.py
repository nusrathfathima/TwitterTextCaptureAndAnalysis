import operator
from datetime import datetime
# # Uncomment below block of code if you want to dynamically generate the text document by entering a search string and running twitter.py
# import twitter
# output_file_path = twitter.INPUT_FILE_PATH

n=int(input("Enter number of records to be displayed: "))

# For now, we will be reading the text document directly instead of generating it from twitter.py
# Note: Comment the below line of code if you are wishing to dynamically generate the text document by uncommenting the above block of code.
file_path = './algorithm.txt'

f = open(file_path, 'r', encoding='utf-8')
followers_count = []
lines = f.readlines()
usernames = {}	# In this dictionary, key = (line number - 1) and value = username
followers_count = {} # In this dictionary, key = (line number - 1) and value = number of followers
retweet_count = {} # In this dictionary, key = (line number - 1) and value = retweet count
tweets_per_user = {} # In this dictionary, key = username and value = tweets per user for the entire timeline
tweets_per_user_per_hour = {} # In this dictionary, key = username and value = tweets per user in a given hour
time_stamps = {} # In this dictionary, key = (line number - 1) and value = datetime object of time stamp

# Now, we populate the above dictionaries by reading each line from the text document.
for i in range(len(lines)):
	line_list = lines[i].split(' ')
	usernames[i] = line_list[0]
	followers_count[i] = int(line_list[-1][:-1])
	retweet_count[i] = int(line_list[-2])
	datetime_object = datetime.strptime(line_list[1][1:], '%d/%b/%Y:%H:%M:%S')
	time_stamps[i] = datetime_object

	try:
		tweets_per_user[usernames[i]] += 1
	except KeyError:
		tweets_per_user[usernames[i]] = 1


# a. The top n users who have tweeted the most for the entire timeline.
sorted_tweets_per_user = sorted(tweets_per_user.items(), key=operator.itemgetter(1), reverse=True)

f_tweets_per_user = open('./tweets_per_user.txt', 'w', encoding='utf-8')

f_tweets_per_user.write('This file consists top {} users who have tweeted the most for the entire timeline.\n\n\n'.format(n))
for a in range(n):
	f_tweets_per_user.write('User: {}; Number of tweets: {}\n'.format(sorted_tweets_per_user[a][0], str(sorted_tweets_per_user[a][1])))


# b. The top n users who have tweeted the most for every hour.
count = 0

f_tweets_per_user_per_hour = open('./tweets_per_user_per_hour.txt', 'w', encoding='utf-8')
for b in range(len(lines)-1):
	if count == 0: 
		initial_timestamp = time_stamps[b]
	
	time_diff = time_stamps[b] - time_stamps[b+1]
	hour_diff = time_stamps[b].hour - time_stamps[b+1].hour
	count += 1
	if time_diff.seconds > 3600 or hour_diff > 0 or b == len(lines)-2:
		if b == len(lines)-2: 
			count += 1
		final_timestamp = time_stamps[b]

		sorted_tweets_per_user_per_hour = sorted(tweets_per_user_per_hour.items(), key=operator.itemgetter(1), reverse=True)
		
		# Since the tweets are listed in reverse chronological order in the text document, 
		# the start range will depend on final timestamp and end range will depend on initial timestamp.
		hour_range_start = final_timestamp.replace(second=0, minute=0)
		hour_range_end = initial_timestamp.replace(second=59, minute=59)
		
		f_tweets_per_user_per_hour.write("Number of tweets between {} and {}: {}\n".format(hour_range_start, hour_range_end, count))
		f_tweets_per_user_per_hour.write("Following are top {} users who have tweeted the most during this hour.\n".format(n))
		
		for z in range(n):
			f_tweets_per_user_per_hour.write('User: {}; Number of tweets: {}\n'.format(sorted_tweets_per_user_per_hour[z][0], str(sorted_tweets_per_user_per_hour[z][1])))
		f_tweets_per_user_per_hour.write('\n\n')

		count = 0
		tweets_per_user_per_hour = {}
	else:
		try:
			tweets_per_user_per_hour[usernames[b]] += 1
		except KeyError:
			tweets_per_user_per_hour[usernames[b]] = 1

			
# c. The top n users who have the maximum followers.
sorted_followers_count = sorted(followers_count.items(), key=operator.itemgetter(1), reverse=True)

f_followers = open('./users_by_followers.txt', 'w', encoding='utf-8')

f_followers.write('This file consists top {} users who have the maximum followers\n\n\n'.format(n))
for c in range(n):
	f_followers.write('User: {}; Number of followers: {}\n'.format(usernames[sorted_followers_count[c][0]], str(sorted_followers_count[c][1])))
	

# d. The top n tweets which have the maximum retweet count.
sorted_retweet_count = sorted(retweet_count.items(), key=operator.itemgetter(1), reverse=True)

f_retweets = open('./users_by_retweets.txt', 'w', encoding='utf-8')

f_retweets.write('This file consists top {} tweets which have the maximum retweet count.\n\n\n'.format(n))
for d in range(n):
	f_retweets.write('Retweet Count = {} for the following tweet:\n'.format(str(sorted_retweet_count[d][1])))
	f_retweets.write(lines[sorted_retweet_count[d][0]])
	f_retweets.write('\n')
