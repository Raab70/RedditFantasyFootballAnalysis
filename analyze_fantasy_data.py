#!/usr/bin/env python
import praw
import os
import argparse

#User defined modules
from downloadFP import downloadFP
from parseReddit import parseRedditPost
from parseReddit import parseRedditComments


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze Reddit FF recommendations')
    parser.add_argument('--week', type=int, required=True,
                        help='The current NFL week to be analyzed (REQUIRED)')
    parser.add_argument('--positions',
                        help='comma separated positions to be analyzed, default is all, valid options are rb,wr,flex',
                        metavar='POS1,POS2,...')

    return parser.parse_args()


if __name__ == '__main__':
    options = parse_args()
    if options.positions is not None:
        positions = options.positions.split(',')
    else:
        positions = ['wr','rb','flex']

    week = options.week
    players_involved = []
    players_recommended = []
    #Now scrape reddit
    r = praw.Reddit(user_agent='RCR')
    subreddit = r.get_subreddit('fantasyfootball')
    print "Analyzing %d positions: %s" % (len(positions),",".join(positions))
    for position in positions:
        print "Beginning position %s" % position
        all_player_data = downloadFP(position,week)
        submissions = subreddit.search('OFFICIAL [WDIS %s] THREAD: ' % (position.upper()),
                                    period='week', sort='new')
        threads = [x for x in submissions]
        titles = [str(t) for t in threads]

        print "Beginning analysis on %d possible threads" % (len(threads))

        for i,thread in enumerate(threads):
            if "INDEX" not in titles[i]:
                post = thread.selftext
                #Will only contain: scoring,players involved
                players_involved.append(parseRedditPost(post, all_player_data))

                #Will be: scoring, recommendation, over
                comments = thread.comments
                players_recommended.append(parseRedditComments(comments, players_involved[-1], all_player_data))



#Then we can translate those two lists into meaningful stuff and things.


