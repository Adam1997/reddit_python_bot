THIS IS A WORK IN PROGRESS

This reddit bot uses Python3, Praw and the Reddit API to analyse popularity of different brands in subreddits.

You must rename PLEASE_READ_README_config.py as config.py and enter the correct reddit account details in that file.

To create a reddit bot, you need to create a new instance of the Searcher class in the client.py file.

The first parameter needs to specify a valid subreddit, and the second parameter must specify a .txt file containing
a list of brands to be searched for.

TO-BE-FIXED/ADDED:
- exceptions
- alternate search items
- graph formatting

To run the program, navigate to the directory on the command line and use the following command:
python3 client.py
