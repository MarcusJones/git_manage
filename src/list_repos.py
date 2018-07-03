#%% General imports
import sys
import os
import github as gh
import ExergyUtilities.util_pretty_print as util_pp
import pandas as pd
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



#%% Login
username = "MarcusJones"
password = ""
#username = input("User: ")
password = input("Pass: ")

github = gh.Github(username, password)
logging.debug("Github instance: {}".format(github))

organization = github.get_user().get_orgs()[0]

g_login = gh.Github(username, password)

logging.debug("Github login instance: {}".format(g))

#%% Get repos

all_repos = get_all_repos(g)
ocean_repos = {k : all_repos[k ]for k in all_repos if all_repos[k]['owner'] == "Ocean Protocol Foundation"}
#my_repo_list = [repo for repo in list_repos if repo['owner'] == None]

#for k in all_repos:
#    print(k)
    
#%% 
for i,k in enumerate(ocean_repos):
    print(i,k)

#%% Ocean Repos
r = ocean_repos["keeper-contracts"]['repo']

r_subset = ["keeper-contracts","engineering"]

r_subset = ocean_repos.keys()
 
#r_subset = ["keeper-contracts"]

#logging.getLogger('github')
organization_df = pd.DataFrame()
for r_name in ocean_repos:
    #organization_df['repo']
    this_repo = ocean_repos[r_name]['repo']
    if r_name not in r_subset:
        continue
    
    logging.debug("Iterate branches of {}".format(this_repo.name))
    repo_df = pd.DataFrame()

    for i,b in enumerate(this_repo.get_branches()):
        #print(b.name)
        b_commits = [c for c in this_repo.get_commits(b.name)]
        c = b_commits[0]
        messages = list()
        for i,c in enumerate(b_commits):
            if c.author:
                messages.append((i,c.author.login,c.commit.message))
        #messages = [ for c in b_commits if c]
        
        branch_df = pd.DataFrame(messages, columns=['num','author', 'message'])
        branch_df['branch'] = b.name
        #ranking = df['author'].value_counts()[0:3]
        #ranking_str = ["{}: {}".format(*t) for t in ranking.iteritems()]
        logging.debug("Branch {:2}: {}, {}, commits".format(i, b.name, len(b_commits)))
        #logging.debug("{}".format(", ".join(ranking_str)))
        #df['repo'] = this_repo.name
        repo_df = repo_df.append(branch_df)
        
        logging.debug("Appended {} rows, {} total".format(len(df),len(repo_df)))
    repo_df['repo'] = this_repo.name
    #masterranking = repo_df['author'].value_counts()[0:3]
    #logging.debug("Overall commits for this repo: {}".format(", ".join(ranking_str)))
    logging.debug("".format())

    organization_df = organization_df.append(repo_df)


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

