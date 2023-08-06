
import os
import re

import requests

from .gitgrab import getfolders, download_file, download_pygg
from .configreader import read_pull_config
from .extract import extract
from .readuserinfo import get_credits


VERSION = "v0.0.16"

DEFAULT_CREDIT = "~/pygg.credits.txt"


def get_owner_repo( githuburl ):
    
    regex = r"http[s]?:\/\/github\.com\/([^/]+)\/([^/]+)"

    matches = re.finditer(regex, githuburl)

    for matchNum, match in enumerate(matches, start=1):
        owner = match.group(1)
        repo = match.group(2)

        return owner, repo

    raise Exception(f"cant extract repo ifo, invalid github url='{githuburl}'")


def get_file_path(path, dest, pattern, root):
    if len(dest)==0:
        if path.find(os.sep)>=0:
            return path
        return root + os.sep + path
    pos = pattern.find("*")
    if pos >= 0:
        if not dest.endswith(os.sep):
            dest = dest + os.sep
        dest = dest + path[pos:]
    return dest


def check_valid_dir(basedir):
    
    curdir = os.getcwd()
    destdir = os.path.abspath( basedir )
    
    if not destdir.startswith( curdir ):
        print( f"error: can not write to outbounded dir {destdir} from {url}" )
        return False
    
    if len(destdir) == len( curdir ):
        print( f"error: can not copy to base dir {dest} from {url}" )
        return False
    
    if len(basedir) == 0 or basedir=="." or basedir==os.sep:
        print( f"error: can not sync to base dir {dest} from {url}" )
        return False
    
    return True
  

def gitgrab( login, simulate, cfgpath = "pygg.cfg" ):
    
    config = read_pull_config(cfgpath)
    errors = 0

    for repo_alias, pulls in config.items():
        
        repo_url = pulls[0].repo
        repo_tag = pulls[0].tag
        
        owner, repo = get_owner_repo( repo_url ) 

        baseurl = "https://api.github.com"
        repourl = f"{baseurl}/repos/{owner}/{repo}/contents?ref={repo_tag}"

        print( f"pulling from {repourl}" )
        
        allentries = getfolders( repourl, auth=login )
        allfiles = allentries.keys()
        
        for p in pulls:

            match = extract( p.pattern, allfiles )

            pulled = 0
            
            for m in match:
                
                pulled += 1
                entry = allentries[m]
                dest = get_file_path( entry.path, p.dest, p.pattern, repo_alias )
                url = entry.download_url

                basedir, fnam = os.path.split( dest )
                
                if not check_valid_dir(basedir):
                    errors += 1 
                    continue

                print( f"copy {dest} - from url={url}" )

                if simulate:
                    continue

                os.makedirs(basedir,exist_ok=True)

                if not download_file( url, dest, auth=login ):
                    errors += 1                    
            
            if pulled == 0:
                print( f"nothing to pull for {p}" )

    print( f"{cfgpath} done with {errors} errors" )
        
    
def main_func():
    
    import argparse
    
    parser = argparse.ArgumentParser(prog='pygitgrab', usage='python3 -m %(prog)s [options]',
        description='grab files from remote git repo.',
        epilog='for more information refer to https://github.com/kr-g/pygitgrab'
                                     )
    parser.add_argument("-v", "--version", dest='show_version', action="store_true",
                        help="show version info and exit", default=False )
    parser.add_argument("-L", "--license", dest='show_license', action="store_true",
                        help="show license info and exit", default=False )
    parser.add_argument("-s", "--simulate", dest='simulate', action="store_true",
                        help="dry run, do not download files", default=False )
    
    parser.add_argument("-f", "--file", dest='files', action="append", type=str,
                        nargs=1, help="name of pygg file to read, adds as '.pygg' extension if missing",
                        default=None, metavar='FILE')
    
#    parser.add_argument("-url", dest='urls', action="append", type=str,
#                        nargs=1, help="name of remote pygg file on github to read, adds as '.pygg' extension if missing",
#                        default=None, metavar='URL')
    
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument("-u", "--user", dest='user', action="store", nargs="?",
                        help="authenticate with user, no user for prompt. "
                        + "create a personal access token in your github settings instead of using a password. "
                        + "unauthenticated users have a lower rate for downloading from github. "
                        + "https://developer.github.com/v3/rate_limit/ \n"
                        , default="" )

    group.add_argument("-c", "--credits", dest='credits', action="store", nargs="?",
                        help="read user and personal token from a file instead of prompting. "
                        + f"make sure to put the file not in git controlled directory, (default: '{DEFAULT_CREDIT}')"
                        , default="" )

    args = parser.parse_args()
    #print( args )
    
    if args.show_version:
        print( "Version:", VERSION )
        return
    
    if args.show_license:
        try:
            with open( "LICENSE" ) as f:
                print( f.read() )
        except:
            pass
        try:
            path = "LICENSE" + os.sep
            for sublicense in os.listdir(path):
                with open( path + sublicense ) as f:
                    print( "-" * 7, "incorporated license:", sublicense + "-" * 7 )
                    print( f.read() )
        except:
            pass
        return
    
    credits = args.credits
    if credits == None:
        credits = DEFAULT_CREDIT
    if credits != None and len(credits) == 0:
        credits = None
    
    login=None
    
    if credits!=None:
        credits = os.path.abspath( os.path.expanduser(credits) )
        with open(credits) as f:
            content = f.read().splitlines()
            content = map( lambda x : x.strip(), content )
            content = list(filter( lambda x : len(x)>0, content ))
            
        try:
            user = content[0]
            passwd = content[1]
            login=(user, passwd)
        except:
            raise Exception("invalid credits file format")
        
    if login == None and ( args.user == None or len(args.user)>0 ):
        user, passwd = get_credits(args.user)
        login=(user, passwd) 

    if login != None:
        print( "downloading as user:", login[0] )

    files = [["pygg.cfg"]] if args.files == None else args.files
    
    for f in files:
        fnam = f[0]
        if len( os.path.splitext(fnam)[1] ) == 0:
            fnam += ".pygg" 
        gitgrab( login, args.simulate, fnam )


def main():
    try:
        main_func()
    except KeyboardInterrupt:
        pass
    except Exception as ex:
        print( "error:", ex )


if __name__ == '__main__':
    
    main()
    
