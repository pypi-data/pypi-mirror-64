# PR Man!

## TLDR

```
> prman -m "This PR is created with prman!"

The repository name: simulation
The project id: oilrig/simulation
The current branch: f/OIL-123-add-tests
The PR name: OIL 123: add tests
Fetching the project...
Fetching PR's...
Fetching approvers...
Select approvers:
* lemar_david_99 (Lemar David)
* jFISHER_20 (Jared Fisher)
* choiii (Peyton Choi)

> david_99;fisher_20;peyton

Pushing to the origin...
Creating the PR...
The PR is created:
https://gitlab.com/oilrig/simulation/merge_requests/42
```

## Why?

Creating a PR in GitLab UI takes so much time.
You need to click a button, select options like 'Squash', 'Remove source branch when merged'.
You need to select minimal approvers count.
You need to select approvers.
You should set approvers as assignee to give them email about your PR.

It is a pure nightmare.
Just run `prman` in your repo directory.
Type approvers like `david_99; fisher_20; peyton` (search by substring, multiple items divided by `;`).
It pushes your branch to the origin automatically.
A Pull Request is done!

## How to install it?

* Install [pipx](https://pipxproject.github.io/pipx/).
It is like a pip+venv for CLI apps.
`python3 -m pip install --user pipx`.
* `pipx install prman`.
* Go to [GitLab Access Tokens UI](https://gitlab.com/profile/personal_access_tokens).
* Name: `prman`; Scopes: `api`; Create personal access token.
* `prman config set gitlab.token YOUR_TOKEN` (the config is stored in `~/.config/prman/config.json`).
