#!/usr/bin/env python
import praw
import argparse
import pickle
import os

#User defined modules
from downloadFP import download_fp

#TODO: Compare Reddit suggestions to FP rankings


def parse_args():
    parser = argparse.ArgumentParser(description='Analyze Reddit FF recommendations')
    parser.add_argument('--week', type=int, required=True,
                        help='The current NFL week to be analyzed (REQUIRED)')
    parser.add_argument('--positions',
                        help='comma separated positions to be analyzed, default is all, valid options are rb,wr,flex',
                        metavar='POS1,POS2,...')
    parser.add_argument('--verbose', help='print verbose outputs',
                        action='store_true', default=False, required=False)

    return parser.parse_args()


if __name__ == '__main__':
    #Initial setup bullshit
    options = parse_args()
    verbose = options.verbose

    if options.positions is not None:
        positions = options.positions.split(',')
    else:
        positions = ['wr', 'rb', 'flex']

    week = options.week

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
        threads = filter(lambda x: not "INDEX" in str(x).upper(), submissions)

        print "Beginning analysis on %d threads" % (len(threads))

        for thread in threads:

            #Populate the MoreComments objects so we have all comments
            nd = ['placeholder']
            while len(nd) > 0:
                print("Getting more comments. We currently have %d comments."
                      " (This can take a while) ..." % (len(thread.comments)-1))
                nd = praw.objects.Submission.replace_more_comments(thread)

            thread_date = str(thread).split(",")[-1].strip().replace("/", "-")
            #DIRECTORY STRUCTURE:
            base_directory = os.path.join(os.getcwd(), "comments")
            week_directory = os.path.join(base_directory, "week_%02d" % week)
            position_directory = os.path.join(week_directory, position)

            #Create the directory structure if it doesn't exist
            if not os.path.isdir(base_directory):
                os.mkdir(base_directory)
            if not os.path.isdir(week_directory):
                os.mkdir(week_directory)
            if not os.path.isdir(position_directory):
                os.mkdir(position_directory)
            filename = os.path.join(position_directory, "%s_%s_week-%d.pickle" % (thread_date, position, week))

            with open(filename, 'w') as fp:
                pickle.dump(nd, fp)
