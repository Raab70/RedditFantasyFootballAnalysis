#!/usr/bin/env python
import praw
import argparse

#User defined modules
from downloadFP import download_fp
from parseReddit import parse_reddit_comments
#TODO: Compare Reddit suggestions to FP rankings

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze Reddit FF recommendations')
    parser.add_argument('--week', type=int, required=True,
                        help='The current NFL week to be analyzed (REQUIRED)')
    parser.add_argument('--positions',
                        help='comma separated positions to be analyzed, default is all, valid options are rb,wr,flex',
                        metavar='POS1,POS2,...')

    return parser.parse_args()


if __name__ == '__main__':
    #Initial setup bullshit
    options = parse_args()
    if options.positions is not None:
        positions = options.positions.split(',')
    else:
        positions = ['wr', 'rb', 'flex']

    week = options.week
    players_recommended = []

    #Now scrape reddit
    r = praw.Reddit(user_agent='RCR')
    subreddit = r.get_subreddit('fantasyfootball')
    print "Analyzing %d positions: %s" % (len(positions), ",".join(positions))
    for position in positions:
        print "Beginning position %s" % position
        #Rank, Name, team, matchup, low, high, ave, SD
        all_player_data = download_fp(position, week)

        player_names = [row[1] for row in all_player_data]
        submissions = subreddit.search('OFFICIAL [WDIS %s] THREAD: ' % (position.upper()),
                                       period='week', sort='new')

        #Filter out threads whos title contains the word "INDEX"
        threads = filter(lambda x: not "INDEX" in str(x).upper(),submissions)

        print "Beginning analysis on %d threads" % (len(threads))

        for thread in threads:
            #post = thread.selftext
            #Will only contain: scoring,players involved
            #players_involved.append(parseRedditPost(post, all_player_data))

            #Populate the MoreComments objects so we have all comments
            nd = ['placeholder']
            while len(nd) > 0:
                print "Getting more comments. We currently have %d comments. (This can take a while) ..." % (len(thread.comments)-1)
                nd = praw.objects.Submission.replace_more_comments(thread)

            #Will be: scoring, recommendation, over
            status = parse_reddit_comments(thread.comments, player_names)



    #Then we can translate those lists into meaningful stuff and things.


