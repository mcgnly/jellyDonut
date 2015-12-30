def SaveTweetId(tweetId):
    #update what was the last tweet I looked at
    #save this number to a file and read it in at the top
    #unless there are no new tweets

        value = (tweetId)
        s = str(value)
        with open('lastTweetId.txt', 'w') as f:
            f.write(s)
        f.closed