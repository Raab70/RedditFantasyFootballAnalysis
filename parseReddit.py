#!/usr/bin/env python
#TODO: Make everything .lower()
#TODO: create tuples of nicknames
#TODO: Fuzzy string matching?

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


def parse_reddit_comments(comments, player_names):
    #scoring, recommendation, over, count
    for comment in comments:
        print "Beginning processing a WDIS which is:\n %s \n" % comment.body
        players_involved = parse_reddit_post(comment.body, player_names)
        if players_involved == -1:
            break

        replies = comment.replies
        player_recommendations = parse_reddit_replies(replies, players_involved)
        print "\n"
        for player in players_involved:
            print "%d Recommendations for %s" % (player_recommendations[player], player)
        print "\n"


    return 0