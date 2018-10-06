import time
import requests
from github import Github
import os, re
import base64
import logging
import re
from datetime import datetime, timedelta
from collections import Counter

"""
Top Organization Contributors


Walk every issue of every repo of an
organization, and compile a count of
contributions - comments, issues, pull
requests.
"""

OUTPUT_DIR = 'output_%s'%(datetime.now().strftime("%Y%m%d_%H%M%S"))
os.mkdir(OUTPUT_DIR)

LOG_FILE = os.path.join(OUTPUT_DIR,'log_top25.log')
GHR_FILE = os.path.join(OUTPUT_DIR,'repos.txt')

ALL_FILE = os.path.join(OUTPUT_DIR,'dcppc_all_contributors.csv')
TOP_FILE = os.path.join(OUTPUT_DIR,'dcppc_top25_contributors.csv')

ISS_FILE = os.path.join(OUTPUT_DIR,'dcppc_issues_contributors.csv')
PRS_FILE = os.path.join(OUTPUT_DIR,'dcppc_pulls_contributors.csv')


# Limit the number of repos (for testing)
# If -1, do all repos
LIMIT = -1

# Set up logging
logging.basicConfig(level=logging.INFO,
                    filename=LOG_FILE,
                    filemode='w')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
logging.getLogger('').addHandler(console)


def main():

    logging.info("Setting up github api")
    
    # set up API with access token
    org = 'dcppc'
    access_token = os.environ['GITHUB_TOKEN']

    # Github -> get organization -> get repository
    g = Github(access_token)
    org = g.get_organization(org)
    repos = org.get_repos(type='all')

    master_issue_contributors = Counter()
    master_pr_contributors = Counter()
    master_contributors = Counter()

    count = 0 
    logging.info("Iterating through repositories")
    for repo in repos:
        
        logging.info("  On repository %s"%(repo.name))

        logging.info("    Iterating through issues")

        # Keep it simple:
        # Just create a list of usernames,
        # one per issue, and count them up 
        # at the end with a Counter()

        issue_contributor_list = []

        for i,issue in enumerate(repo.get_issues(state="open")):
            if (i+1)%50==0:
                logging.info("    On open issue %d..."%(i+1))
            issue_contributor_list.append(issue.user.login)

        for i,issue in enumerate(repo.get_issues(state="closed")):
            if (i+1)%50==0:
                logging.info("    On closed issue %d..."%(i+1))
            issue_contributor_list.append(issue.user.login)

        issue_contributors = Counter(issue_contributor_list)
        master_issue_contributors += issue_contributors

        logging.info("    Finished counting issue contributors")

        # ---

        pr_contributor_list = []

        for p,pr in enumerate(repo.get_pulls(state="open")):
            if (p+1)%50==0:
                logging.info("    On open PR %d..."%(p+1))
            pr_contributor_list.append(pr.user.login)

        for p,pr in enumerate(repo.get_pulls(state="closed")):
            if (p+1)%50==0:
                logging.info("    On closed PR %d..."%(p+1))
            pr_contributor_list.append(pr.user.login)

        pr_contributors = Counter(pr_contributor_list)
        master_pr_contributors += pr_contributors

        logging.info("    Finished counting PR contributors")

        # ---

        logging.info("  Done with repo %s"%(repo.name))

        with open(GHR_FILE,'a') as f:
            f.write(repo.name)
            f.write("\n")

        count += 1
        if LIMIT>0 and count>=LIMIT:
            break

        time.sleep(1)

    master_contributors = master_issue_contributors + master_pr_contributors

    topN = master_contributors.most_common()
    top25 = master_contributors.most_common(25)

    topPR = master_pr_contributors.most_common()
    topiss = master_issue_contributors.most_common()

    with open(TOP_FILE,'w') as f:
        f.write("login,count\n")
        for top in top25:
            f.write("%s,%s\n"%(top))

    with open(ALL_FILE,'w') as f:
        f.write("login,count\n")
        for top in topN:
            f.write("%s,%s\n"%(top))

    with open(ISS_FILE,'w') as f:
        f.write("login,count\n")
        for top in topiss:
            f.write("%s,%s\n"%(top))

    with open(PRS_FILE,'w') as f:
        f.write("login,count\n")
        for top in topPR:
            f.write("%s,%s\n"%(top))

    logging.info("Finished writing top 25 contributors file: %s"%(TOP_FILE))

    logging.info("Finished writing all contributors file: %s"%(ALL_FILE))


if __name__=="__main__":
    main()

