#!/usr/bin/env python


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

def parse_reddit_replies(replies, players_involved, player_names):
    pass

def parse_reddit_comments(comments, player_names):
    #scoring, recommendation, over, count
    player_recommendations = []
    for comment in comments:
        players_involved = parse_reddit_post(comment.body, player_names)
        if players_involved == -1:
            break

        replies = comment.replies
        player_recommendations.extend(parse_reddit_replies(replies, players_involved, player_names))

    return player_recommendations