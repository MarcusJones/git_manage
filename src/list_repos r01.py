#%% General imports
import sys
import os
import github as gh
import ExergyUtilities.util_pretty_print as util_pp
import pandas as pd


import datetime
#%% Logging
import logging
logger = logging.getLogger()
logger.handlers = []

# Set level
logger.setLevel(logging.DEBUG)

# Create formatter
FORMAT = "%(asctime)s : %(message)s"
DATE_FMT = "%Y-%m-%d %H:%M:%S"
formatter = logging.Formatter(FORMAT, DATE_FMT)

# Create handler and assign
handler = logging.StreamHandler(sys.stderr)
handler.setFormatter(formatter)
logger.handlers = [handler]
logging.debug("Logging started")

logging.getLogger("github.Requester").setLevel(logging.WARNING)

# Disable NaturalNameWarning
import warnings
import tables
warnings.filterwarnings('ignore', category=tables.NaturalNameWarning)

#%% Paths

PATH_SAVE = r"/home/batman/git/util_ManageGitRepos/saved"
PATH_SAVE = r"/home/batman/TEMP SAVE OCEAN GIT"
#%% Functions
def get_sha_for_tag(repository, tag):
    """
    Returns a commit PyGithub object for the specified repository and tag.
    """
    branches = repository.get_branches()
    matched_branches = [match for match in branches if match.name == tag]
    if matched_branches:
        return matched_branches[0].commit.sha

    tags = repository.get_tags()
    matched_tags = [match for match in tags if match.name == tag]
    if not matched_tags:
        raise ValueError('No Tag or Branch exists with that name')
    return matched_tags[0].commit.sha

def get_all_repos(g):
    """Get all repos as a dictionary
    """
    all_repos = dict()
    for i,repo in enumerate(g.get_user().get_repos()):
        this_repo_dict = dict()
        #print('{:30} {:40} Fork: {:10}'.format(repo.name, repo.owner.__repr__(), repo.fork))
        this_repo_dict['repo'] = repo
        this_repo_dict['name'] = repo.name
        this_repo_dict['owner'] = repo.owner.name
        this_repo_dict['fork'] = repo.fork
        print(i,this_repo_dict)
        all_repos[this_repo_dict['name']] = this_repo_dict
        #for i in dir(repo):
        #    print(i)
        #raise
    logging.debug("Returning {} repos".format(len(all_repos)))
    return all_repos

def print_all_repos():
    print()
    print("All repos")
    util_pp.print_table_dicts(list_repos)

def print_repos(owner=None):
    #notforked_repo_list = [repo for repo in list_repos if not repo['fork'] ]
    my_repo_list = [repo for repo in list_repos if repo['owner'] == owner]

    print("My repos")
    util_pp.print_table_dicts(my_repo_list)



def get_commits(branch_object):
    messages = list()
    b_commits = [c for c in this_repo.get_commits(b.name)]
    for j,c in enumerate(b_commits):
        cdict = dict()
        if c.author:
            cdict['author'] = c.author.login
            cdict['message'] = c.commit.message
            cdict['date'] = c.commit.last_modified
            cdict = {**cdict, **c.stats.raw_data}
            messages.append((cdict))
    branch_df = pd.DataFrame(messages)
    return branch_df


#%% API
#branch_object=b
#dir(c.commit)
#c.commit.last_modified
#dir(c.stats)
#stats_dict = c.stats.raw_data
#c.stats.additions.bit_length()
#c.stats.deletions.bit_length()
#dir(c)
#for s in c.stats:    print(s)
#c.author
dir(b)
dir(this_repo)

# Get contributors
res = this_repo.get_stats_contributors()
for i in res: print(i.author.name, i.total, len(i.weeks))

dir(i)
i.author
i.total
dir(i.weeks[0])




# Get last year of activity (list of 52 weeks)
res = this_repo.get_stats_commit_activity()


# Get all open PRs
for i in this_repo.get_pulls(): print(i)

# Get punchcard
res = this_repo.get_stats_punch_card()
#dir(res)
# Raw data: 168 hours of the week. [daynum, hournum, numcommits]
raw1 = res.raw_data



#%% Login
username = ""
password = ""
#username = input("User: ")
password = input("Pass: ")

github = gh.Github(username, password)
logging.debug("Github instance: {}".format(github))

organization = github.get_user().get_orgs()[0]

g_login = gh.Github(username, password)

logging.debug("Github login instance: {}".format(g_login))

#%% Get all repos
if 0:
    all_repos = get_all_repos(g_login)
    ocean_repos = {k : all_repos[k ]for k in all_repos if all_repos[k]['owner'] == "Ocean Protocol Foundation"}
    #my_repo_list = [repo for repo in list_repos if repo['owner'] == None]

#%% Get ocean repos as dictionary
ocean_org = g_login.get_organization("oceanprotocol")
ocean_repos = ocean_org.get_repos()
ocean_repos_dict = {r.name : r for r in ocean_repos}
ocean_repos_dict_SMALL = {k: ocean_repos_dict[k] for k in ("keeper-contracts","dev-ocean")}

#%% Ocean Repos
for this_repo_name,this_repo in ocean_repos_dict_SMALL.items():
    logging.debug("Fetching repo {}".format(this_repo_name))
    
    # Iterate branches
    for i,b in enumerate(this_repo.get_branches()):
        branch_df = get_commits(b)
        save_path = os.path.join(PATH_SAVE,this_repo_name,b.name+".csv")
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        #branch_df.to_hdf(save_path,b.name)
        branch_df.to_csv(save_path)
        logging.debug("\tBranch {:2}: {}, {} commits, saved".format(i, b.name, len(branch_df)))


#%% 
this_repo.stats
dir(this_repo)
this_repo.stargazers_count
this_repo.watchers_count
#%%
    
res = this_repo.get_stats_contributors()
for stat in this_repo.get_stats_contributors():
    author = str(stat.author)
    author = (author.replace('NamedUser(login="', "")).replace('")', "")
    for week in stat.weeks:
        date = str(week.w)
        date = date[:10]
#%%
for r in organization_df['repo'].unique():
    print(r)
    sub_df = organization_df[organization_df['repo']==r]
    counts = sub_df['author'].value_counts()
    counts = counts[0:3]
    ranking_str = ["{}: {}".format(*t) for t in counts.iteritems()]
    print("\t",", ".join(ranking_str))

#organization_df.groupby(['author','repo']).agg(['count'])
#organization_df.groupby(['author','repo']).size()
#[c for c in b_commits[799].get_comments()]
#b_commits[799].comments_url
#r.get_commits(b.name)

#%% 
organization_df.to_csv("commits.csv")

#%% Hacking

b.sha

collabs = [c for c in r.get_collaborators()]

commits = [c for c in r.get_commits()]

r.get_commits("develop")


c = commits[51]

c.author
c.committer
c.files
c.stats
comments = [c for c in c.get_comments()]

#%% OLD
if __name__ == "__main__":
    print("asdf")
    list_repos = get_all_repos
    username = "MarcusJones"
    password = ""
    #username = input("User: ")
    password = input("Pass: ")
    
    
    github = gh.Github(username, password)
    logg("Github instance:",github)
        
    #print(github)
    
    organization = github.get_user().get_orgs()[0]
    #print(organization)
    logg("Github organization:",organization)
    #logging.info()
    
    g = gh.Github(username, password)
    
    logg("Github login:",g)
    
    logg("Github user:",g.get_user())




#%% OLD
#repository_name = "Old_Python" 

#this_repo = g.get_user().get_repo(repository_name)


#owner = this_repo.owner
#print(owner)

#for i in dir(repo):
#    print(i)

#
# 
# 
# repository_name = input("Github repository: ")
# repository = organization.get_repo(repository_name)
# 
# branch_or_tag_to_download = input("Branch or tag to download: ")
# sha = get_sha_for_tag(repository, branch_or_tag_to_download)

#directory_to_download = raw_input("Directory to download: ")
#download_directory(repository, sha, directory_to_download)


# def download_directory(repository, sha, server_path):
#     """
#     Download all contents at server_path with commit tag sha in 
#     the repository.
#     """
#     contents = repository.get_dir_contents(server_path, ref=sha)
# 
#     for content in contents:
#         print("Processing {}".format(content.path))
#         if content.type == 'dir':
#             download_directory(repository, sha, content.path)
#         else:
#             try:
#                 path = content.path
#                 file_content = repository.get_contents(path, ref=sha)
#                 file_data = base64.b64decode(file_content.content)
#                 file_out = open(content.name, "w")
#                 file_out.write(file_data)
#                 file_out.close()
#             except (gh.GithubException, IOError) as exc:
#                 logging.error('Error processing %s: %s', content.path, exc)

