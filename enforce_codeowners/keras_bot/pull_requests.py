import os

import github

codeowners_url = ('https://raw.githubusercontent.com/'
                  'keras-team/keras-contrib/master/CODEOWNERS')

repo_id = 'keras-team/keras-contrib'

import urllib.request


def parse_codeowners():
    response = urllib.request.urlopen(codeowners_url)
    data = response.read()
    text = data.decode('utf-8')
    map_path_owner = []
    for line in text.splitlines():
        line = line.strip()
        if line.startswith('#') or line == '':
            continue
        x = line.split(' ')
        path = x[0]
        owner = x[-1]
        owner = owner[1:]  # removes '@'
        map_path_owner.append((path, owner))
        if not path.startswith('examples'):  # examples don't have tests.
            map_path_owner.append(('tests/' + path, owner))
    return map_path_owner


def send_message(pull_request, owner, files_changed):
    message = """Hello, I'm a bot! I can make mistakes, notify gabrieldemarmiesse if I made one.

I see that you modified the following file{plural}: 
{files_changed}

The owner of those file is @{owner}

@{owner} could you please take a look at it whenever 
you have the time and add a review? Thank you in advance for the help.
"""

    files_changed_formatted = '\n'.join('* ' + x for x in files_changed)
    plural = 's' if len(files_changed) > 1 else ''
    message = message.format(files_changed=files_changed_formatted,
                             owner=owner,
                             plural=plural)
    print('Would send message:\n')
    print(message)


def already_notified_owner(pull_request):
    for comment in pull_request.get_comments():
        if comment.user.login != 'bot-of-gabrieldemarmiesse':
            continue
        if 'owner' in comment.body and 'review' in comment.body:
            return True
    return False


def examine_single_pull_request(pull_request, map_path_owner):
    if 'adam' in pull_request.title:
        pass
    owners_to_notify = []
    for file_changed in pull_request.get_files():
        for file_owned, owner in map_path_owner:
            if file_changed.filename == file_owned and owner != pull_request.user.login:
                owners_to_notify.append((file_changed.filename, owner))

    if len(set(x[1] for x in owners_to_notify)) > 1:
        # let's not notify multiple people, otherwise it's going to turn into
        # a mess for big PRs with multiple files.
        return

    # let's avoid sending a message if we already sent one.
    if already_notified_owner(pull_request):
        return
    if owners_to_notify:
        owner_to_notify = owners_to_notify[0][1]
        files_changed = [x[0] for x in owners_to_notify]
        send_message(pull_request, owner_to_notify, files_changed)


def examine_pull_requests():
    map_path_owner = parse_codeowners()

    client = github.Github(os.environ['GITHUB_TOKEN'])
    repo = client.get_repo(repo_id)

    for pull_request in repo.get_pulls():
        examine_single_pull_request(pull_request, map_path_owner)


examine_pull_requests()