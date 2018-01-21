
# PyGithub 1.35
import github as gh
print(gh.__file__)
#import sys
#sys.path.append("./PyGithub");
# Logging
import logging
logging.basicConfig(level=logging.INFO)

import ExergyUtilities.util_pretty_print as util_pp

def logg(this_string, this_item):
    logging.info(this_string+"{}".format(this_item.__str__()))

logging.info("Gitub module:".format(gh))

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

def get_all_repos():
    """Get all repos as a dictionary
    """
    list_repos = list()
    for repo in g.get_user().get_repos():
        this_repo_dict = dict()
        #print('{:30} {:40} Fork: {:10}'.format(repo.name, repo.owner.__repr__(), repo.fork))
        this_repo_dict['repo'] = repo
        this_repo_dict['name'] = repo.name
        this_repo_dict['owner'] = repo.owner.name
        this_repo_dict['fork'] = repo.fork
        list_repos.append(this_repo_dict)
        #for i in dir(repo):
        #    print(i)
        #raise


def print_all_repos():
    print()
    print("All repos")
    util_pp.print_table_dicts(list_repos)

def print_my_repos():
    #notforked_repo_list = [repo for repo in list_repos if not repo['fork'] ]
    my_repo_list = [repo for repo in notforked_repo_list if repo['owner'] == None]

    print("My repos")
    util_pp.print_table_dicts(my_repo_list)






if __name__ == "Main":
    list_repos = get_all_repos
    
    username = ""
    password = ""
    
    #username = input("User: ")
    #password = input("Pass: ")
    
    username = "MarcusJones"
    password = "x"
    
    github = gh.Github(username, password)
    logg("Gitub instance:",github)
        
    #print(github)
    
    organization = github.get_user().get_orgs()[0]
    #print(organization)
    logg("Gitub organization:",organization)
    #logging.info()
    
    g = gh.Github(username, password)
    
    logg("Gitub login:",g)
    
    logg("Gitub user:",g.get_user())





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

