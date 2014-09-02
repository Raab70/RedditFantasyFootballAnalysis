import os

def downloadFP(pos,week):
    #Check how old the player data is
    download=True

    #if not os.path.isfile(playersfile):
    #    open(playersfile, 'a').close()
    #    download = True

    #edit_time = datetime.datetime.fromtimestamp(os.path.getctime(playersfile))
    #now = datetime.datetime.now()
    #td = now - edit_time
    if download:
        #The file is old, download a new one
        curl_str = "curl http://www.fantasypros.com/nfl/rankings/%s.php?export=xls > %s/week-%s-%s-raw.xls" % (pos,os.getcwd(),week,pos)
        sed_str = "sed '1,4d' %s/week-%s-%s-raw.xls > %s/week_%s_%s.tsv" % (os.getcwd(),week,pos,os.getcwd(),week,pos)
        os.system(curl_str)
        os.system(sed_str)

    #now load the file, it is current
    with open("%s/week_%s_%s.tsv"%(os.getcwd(),week,pos),'r') as tsv:
        all_player_data = [line.strip().split('\t') for line in tsv]

    return all_player_data