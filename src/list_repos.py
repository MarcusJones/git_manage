import github as gh
import sys
sys.path.append("./PyGithub");

print(gh)
print(gh.__name__)

eclipse_workspace = r"C:\NeonWorkspace"

# Authenticate to github.com and create PyGithub "Github" object
#username = raw_input("Github Username:")
#pw = gh.getpass()


pw = ""
pw = input("Pass: ")
g = gh.Github("MarcusJones", pw)

for repo in g.get_user().get_repos():
    print('{:30} {:40} Fork: {:10}'.format(repo.name, repo.owner.__repr__(), repo.fork))
