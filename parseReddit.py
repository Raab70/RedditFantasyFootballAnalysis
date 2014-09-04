#!/usr/bin/env python
import praw

#TODO: create tuples of nicknames
#TODO: Fuzzy string matching?
#TODO: https://pypi.python.org/pypi/python-Levenshtein/0.11.2
#TODO: Resolve last name differences with matchups from all_player_data

def parse_reddit_post(post_text, player_names):
    players_involved = []
    for player_name in player_names:
        if player_name in post_text:
            players_involved.append(player_name)

    if len(players_involved) == 0:
        last_names = [name.split(" ")[1] for name in player_names]
        for i, last_name in enumerate(last_names):
            if last_name in post_text:
                players_involved.append(player_names[i])
    if len(players_involved) == 0:
        return -1
    else:
        return players_involved


def parse_reddit_replies(replies, players_involved):
    recommendations = {name: 0 for name in players_involved}
    last_names = [name[1] for name in players_involved]
    print "Processing %d replies" % (len(replies))
    for reply in replies:
        reply_text = reply.body
        current_reply = []
        #First let's check all last names
        for i, player in enumerate(last_names):
            if player in reply_text:
                current_reply.append(player)
            #If only one player is mentioned, the reply is recommending this player
            #Throw out all other replies (This is a first pass)
            if len(current_reply) == 1:
                recommendations[players_involved[i]] += 1
    return recommendations

def parse_post_set(comment,players):
    return


def parse_reddit_comments(comments, player_names,verbose=False):
    #scoring, recommendation, over, count

    #comments are a list of tuples where the first element is the comment
    #text and the second element is a list of the comment replies text
    comments = initial_split(comments)
    for i,c in enumerate(comments):
        if verbose:
            print "Comment %d has %d replies" % (i,len(c[1]))
        res = parse_post_set(c,player_name)
    return 0

#Function to initially split comments into comment and reply tuples separate of PRAW
def initial_split(comments):
    split_comments = []
    for comment in comments:
        post_text = comment.body.lower()

        #Remove any objects that are not of type praw.objects.Comment
        replies = filter(lambda x: isinstance(x,praw.objects.Comment) , comment.replies)

        #Just extract the text from the bodies
        reply_text = [r.body.lower() for r in replies]

        #Store the comment and its replies as a tuple
        split_comments.append((post_text,reply_text))
    return split_comments
