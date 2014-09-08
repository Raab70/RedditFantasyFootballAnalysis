#!/usr/bin/env python
import praw
import argparse
import pickle
import os
import datetime

#User defined modules
from downloadFP import download_fp
from parseReddit import initial_split


def parse_args():
    parser = argparse.ArgumentParser(description='Downloads FF recommendations from Reddit, '
                                     'as well as the current weeks fantasypros rankings\n'
                                     'Should be run at least once a week, to not lose fp rankings\n'
                                     'ideally on saturday to get all reddit comments')
    parser.add_argument('--positions',
                        help='comma separated positions to be analyzed, default is all, valid options are rb,wr,flex',
                        metavar='POS1,POS2,...')
    parser.add_argument('--fp', help='flag to bypass downloading fp data, default is true, keep false on sundays\n'
                                     '(I think, watch output to make sure its saved as the correct week)',
                        action='store_false', default=True, required=False)
    parser.add_argument('--verbose', help='print verbose outputs',
                        action='store_true', default=False, required=False)

    return parser.parse_args()


if __name__ == '__main__':
    #Initial setup bullshit
    season_start = datetime.datetime(2014, 9, 2, 0, 0)
    options = parse_args()
    verbose = options.verbose
    dl_fp = options.fp

    if options.positions is not None:
        positions = options.positions.split(',')
    else:
        positions = ['wr', 'rb', 'flex']

    #Download this weeks fp data:
    #Rank, Name, team, matchup, low, high, ave, SD
    days_from_season_start = (datetime.datetime.today() - season_start).days
    week_now = (days_from_season_start / 7) + 1
    if dl_fp:
        for position in positions:
            all_player_data = download_fp(position, week_now)
    print "\n"
    print "------------Beginning Reddit scrape-------------------------------------------------------------------------"
    print "\n"
    #Now scrape reddit
    r = praw.Reddit(user_agent='RCR')
    subreddit = r.get_subreddit('fantasyfootball')
    print "Analyzing %d positions: %s" % (len(positions), ",".join(positions))
    for position in positions:
        print "Beginning position %s" % position

        #player_names = [row[1] for row in all_player_data]
        submissions = subreddit.search('OFFICIAL [WDIS %s] THREAD: ' % (position.upper()),
                                       period='week', sort='new')

        #Filter out threads whos title contains the word "INDEX"
        threads = filter(lambda x: not "INDEX" in str(x).upper(), submissions)

        print "Beginning analysis on %d threads" % (len(threads))

        for thread in threads:
            thread_date = str(thread).split(",")[-1].strip().replace("/", "-")
            thread_date_obj = datetime.datetime.strptime(thread_date, "%m-%d-%Y")
            days_from_season_start = (thread_date_obj - season_start).days
            week = (days_from_season_start / 7) + 1
            if verbose:
                print "\n"
                print "Analyzing thread: %s from week %d" % (str(thread), week)
            #Populate the MoreComments objects so we have all comments
            nd = ['placeholder']
            while len(nd) > 0:
                if verbose:
                    print("Getting more comments. We currently have %d comments."
                          " (This can take a while) ..." % (len(thread.comments)-1))
                nd = praw.objects.Submission.replace_more_comments(thread)
            if verbose:
                print "Finished getting comments. Final total is: %d" % (len(thread.comments))

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
            split_comments = initial_split(thread.comments)
            with open(filename, 'w') as fp:
                pickle.dump(split_comments, fp)
