#!/usr/bin/env python
import praw
import os
import argparse

#User defined modules
import downloadFP

def parse_args():
    parser = argparse.ArgumentParser(description='Analyze Reddit FF recommendations')
    parser.add_argument('--week',type=int,required=True,
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

    #Now scrape reddit
    r = praw.Reddit(user_agent='test')
    submissions = r.get_subreddit('fantasyfootball')
    for position in positions:
        players = downloadFP(position,week)
        threads_generator = submissions.search('OFFICIAL [WDIS %s]' % (position))
        threads = [x for x in threads_generator]
        sorted(threads, key=lambda thread: threads.created)
        for thread in theads:
            post = thread.selftext
            comments = thread.comments


