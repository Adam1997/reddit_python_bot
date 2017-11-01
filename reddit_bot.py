import praw
import config
import file_creator
import time
import os
import matplotlib.pyplot as plt
import prawcore


#make a class
class Searcher:

    def __init__(self):
        self.subr = self.getSubreddit()
        self.listSearchItems = []
        self.scoringDict = {}
        self.searchDict = {}
        self.inputFile = None
        self.r = self.botlogin()

    def getSubreddit(self):
        print("Enter valid subreddit: \n")
        subreddit = input()
        return subreddit


    def setup(self):
        #need exceptions
        print("Do you want to make a new text file to search from? [y/n]")
        if input() == 'y':
            self.inputFile = file_creator.writeFile()
        else:
            print("Enter the name of the text file you want to use: ")
            self.inputFile = input()


        with open(self.inputFile,"r+") as infile, open('output.txt', "w") as outfile:
            #temporary holders
            self.company_name = ""
            self.company_alt_terms = []
            for line in infile:
                #if not empty line
                if not line.strip(): continue
                #if there is a colon
                if line.find(":") != -1:
                    outfile.write(line.lower())
                    #return the first cut bit refer to documentation
                    if len(self.company_alt_terms) != 0:
                        #add previous company details
                        self.company_alt_terms.insert(0, self.company_name)
                        #add new company
                        self.scoringDict[self.company_name] = 0
                        #set previous company name to contents of alt terms list then reset alt terms list
                        self.searchDict[self.company_alt_terms[0]] = self.company_alt_terms
                        self.company_alt_terms = []
                        #set new company name
                        self.company_name = line.lower().partition(":")[0]
                    else:
                        self.company_name = line.lower().partition(":")[0]
                        self.scoringDict[self.company_name] = 0
                if line.find("-") != -1:
                    #remove /n tag
                    self.company_alt_terms.append((line.lower().partition("-")[2]).split("\n")[0])
            print(self.scoringDict)
            print(self.searchDict)

    def botlogin(self):
        #instance of reddit
        #TO-DO AUTHENTICATION EXCEPTION
        print("Logging in...")
        self.r = praw.Reddit(username = config.username,
                    password = config.password,
                    client_id = config.client_id,
                    client_secret = config.client_secret,
                    user_agent = "test reddit bot")
        print("Logged in!")
        return self.r


    def runbot(self):
        #Let number of posts be n, Let number of companies be m, Let number of terms be l
        #Time Complexity: O(m*n*l)
        try:
            self.setup()
            for post in self.r.subreddit(self.subr).hot(limit=100):
                print(post.title)
                #iterate over companies
                for company_name in self.scoringDict.keys():
                    #boolean controller to ensure the company is not counted twice in a post i.e. if "Apple" and "iOS" are both mentioned
                    over_count = False
                    #iterate over alternate terms
                    for search_item in self.searchDict[company_name]:
                        if search_item in post.title.lower():
                            time.sleep(1)
                            if over_count == False:
                                print("\n ************ \n" + "added 1 to " + company_name + " for " + search_item + " found" + "\n ************ \n ")
                                self.scoringDict[company_name] = self.scoringDict[company_name] + 1
                                over_count = True
            self.display()
        except prawcore.exceptions.Redirect:
            print("Subreddit was not accessible")
        except prawcore.exceptions.OAuthException:
            print("user details are incorrect")

    def deleteItems(self, dict):
        for i in list(dict):
            if dict[i] == 0:
                dict.pop(i)


    def display(self):
        self.listNames = []
        for i in self.scoringDict.keys():
            newString = i[0].upper() + i[1:]
            self.listNames.append(newString)
        self.deleteItems(self.scoringDict)
        plt.bar(range(len(self.scoringDict)), self.scoringDict.values(), align='center', color='r')
        plt.xticks(range(len(self.scoringDict)), self.listNames)
        plt.ylabel("Count")
        plt.xlabel("Company Names")
        plt.title("Results of Reddit Search Algorithm")
        plt.show()
