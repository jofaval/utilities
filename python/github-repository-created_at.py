from sys import argv
import requests
from dateutil.parser import isoparse

PER_PAGE = 100


def get_api_repository_url(
    owner: str,
    repository: str,
) -> str:
    return f'https://api.github.com/repos/{owner}/{repository}?per_page={PER_PAGE}'


def get_repo_detail(
    owner: str,
    repository: str,
) -> str:
    return requests.get(
        get_api_repository_url(owner, repository)
    ).json()


def get_repos_from_user(
    user: str
) -> dict:
    print(f'Will be looking for repos from: "{user}"')

    response = requests.get(
        f'https://api.github.com/users/{user}/repos?per_page={PER_PAGE}'
    ).json()

    print(f'Found a total of {len(response)} repositories')

    return response


def main() -> None:
    owner = argv[-1]
    repos = get_repos_from_user(owner)

    # get only the wanted fields
    repos_created_at = tuple(
        map(lambda x: (x['name'], x['created_at']), repos)
    )

    # prepare the values to be sorted
    repos_created_at = tuple(
        map(lambda x: (x[0], isoparse(x[1]).timestamp()), repos_created_at)
    )
    # actually sort by date
    repos_created_at = sorted(repos_created_at, key=lambda x: x[1])

    # print each repo in its own row/line
    [print(x) for x in repos_created_at]
    # print all of the repos at one
    # print(repos_created_at)


if __name__ == '__main__':
    main()

    # usage example
    # python3 github-repository-created_at.py jofaval
