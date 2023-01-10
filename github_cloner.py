import os
import requests
import sys
from threading import Thread

USERNAME = sys.argv[1]
os.mkdir(USERNAME)
os.chdir(USERNAME)

def clone_repositories():
  # Create a folder to store the repositories
  os.mkdir('repos')
  os.chdir('repos')

  response = requests.get(f'https://api.github.com/users/{USERNAME}/repos')
  if response.status_code == 200:
    repositories = response.json()
    for repository in repositories:
      if repository['fork']:
        continue
      repository_name = repository['name']
      os.system(f'git clone https://github.com/{USERNAME}/{repository_name}.git')
  else:
    print('An error occurred while getting the list of repositories')

def clone_gists():
  # Create a folder to store the gists
  os.chdir('..')
  os.mkdir('gists')
  os.chdir('gists')

  response = requests.get(f'https://api.github.com/users/{USERNAME}/gists')
  if response.status_code == 200:
    gists = response.json()
    for gist in gists:
      gist_name = gist['id']
      os.system(f'git clone {gist["git_pull_url"]} {gist_name}')
  else:
    print('An error occurred while getting the list of gists')

# Create threads for cloning the repositories
repositories_thread = Thread(target=clone_repositories)
repositories_thread.start()
repositories_thread.join()

# Create threads for cloning the gists
gists_thread = Thread(target=clone_gists)
gists_thread.start()
gists_thread.join()
