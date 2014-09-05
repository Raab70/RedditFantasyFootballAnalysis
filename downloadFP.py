import os
#TODO: get weeks to download from the current date
#TODO: use try/catch to check if weeks have been posted yet.


def download_fp(pos, week):

    #The file is old, download a new one
    curl_str = ("curl -s http://www.fantasypros.com/nfl/rankings/%s.php?export=xls > "
                "%s/week-%s-%s-raw.xls" % (pos, os.path.join(os.getcwd(), "fp"), week, pos))
    sed_str = ("sed '1,4d' %s/week-%s-%s-raw.xls > %s/week_%s_%s.tsv"
               % (os.path.join(os.getcwd(), "fp"), week, pos, os.path.join(os.getcwd(), "fp"), week, pos))
    print "Downloading and parsing FantasyPros data for week %d and position %s" % (week, pos)
    os.system(curl_str)
    os.system(sed_str)

    #now load the file, it is current
    with open("%s/week_%s_%s.tsv" % (os.path.join(os.getcwd(), "fp"), week, pos), 'r') as tsv:
        all_player_data = [line.lower().strip().split('\t') for line in tsv]

    return all_player_data[2:]  # remove the first two rows, an empty one and the titles
