#!/usr/bin/env python
import praw
import argparse
import pickle
import os
import sys

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
    parser.add_argument('--verbose', help='print verbose outputs',
                        action='store_true', default=False, required=False)
    parser.add_argument('--test', help='Run in testing mode with using a saved download',
                        action='store_true', default=False, required=False)
    parser.add_argument('--save', help='Save output for use in testing',
                        action='store_true', default=False, required=False)

    return parser.parse_args()


if __name__ == '__main__':
    #Initial setup bullshit
    options = parse_args()
    test = options.test
    verbose = options.verbose
    save = options.save
    if test:
        print 'Running in testing mode'
    if options.positions is not None:
        positions = options.positions.split(',')
    else:
        positions = ['wr', 'rb', 'flex']

    week = options.week
    players_recommended = []

    #Now scrape reddit
    r = praw.Reddit(user_agent='RCR')
    subreddit = r.get_subreddit('fantasyfootball')
    pickle_dir = os.path.abspath('./pickle')
    fp_dir = os.path.abspath('./fp')
    if not os.path.exists(pickle_dir):
        os.mkdir(pickle_dir)
    if not os.path.exists(fp_dir):
        os.mkdir(fp_dir)
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

            if test:
                #Load all pickle files in the current directory, should eventually change this
                #to take a path to a pickle as an input but this works for now.
                nd = []
                files = os.listdir(os.getcwd())
                pickle_files = [f for f in files if f.endswith('pickle')]
                if len(pickle_files) == 0:
                    print "Run in testing mode but no pickle files found"
                    print "Please run in save mode before running in test mode"
                    sys.exit(1)

                for f in pickle_files:
                    with open(f, 'r') as fp:
                        tmp = pickle.load(fp)
                    nd.append(tmp)
                #Remove the more comments BS
                #thread.comments.pop()
            else:
                #Populate the MoreComments objects so we have all comments
                nd = ['placeholder']
                while len(nd) > 0:
                    print("Getting more comments. We currently have %d comments."
                          " (This can take a while) ..." % (len(thread.comments)-1))
                    nd = praw.objects.Submission.replace_more_comments(thread)

            if save:
                thread_date = str(thread).split(",")[-1].strip().replace("/", "-")

                with open(os.path.join(pickle_dir,"%s_%s_week-%d.pickle" % (thread_date, position, week)), 'w') as fp:
                    pickle.dump(nd, fp)

            #Will be: scoring, recommendation, over
            status = parse_reddit_comments(thread.comments, player_names, verbose=verbose)



    #Then we can translate those lists into meaningful stuff and things.
