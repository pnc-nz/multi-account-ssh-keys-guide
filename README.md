# multi-account-ssh-keys-guide
My guide on how to manage multiple accounts with different SSH-Keys

# TODO: Adjust capability for organisation directories like
# ~/.ssh/github.com/contoso/john-doe/john-doe_id_rsa

# Generate Client SSH Keys

Create a key for each repo
```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github.com/john-doe/john-doe_id_rsa -C "john-doe@personal.com"
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github.com/anonymous-john/anonymous-john_id_rsa -C "anonymous.john@domain.com"
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github.com/contoso/john-doe/john-doe_id_rsa -C "john-doe@contoso.com"
ssh-keygen -t rsa -b 4096 -f ~/.ssh/dev.azure.com/contoso/john-doe/john-doe_id_rsa -C "john-doe@contoso.com"
```
- The text passed after the `-C` flag is just a comment, you may use any value.

# Generate the SSH Configuration File

If the config file does not exist:

```bash
touch ~/.ssh/config
chmod 600 ~/.ssh/config
```

# Update the SSH Configuration File

`~/.ssh/config`
```bash
# Primary Personal GitHub - john-doe@personal.com
Host john-doe.github.com
  HostName github.com
  User git
  AddKeysToAgent yes
  #####################
  ## Mac/Linux Only ###
  UseKeychain yes	###
  #####################
  IdentityFile ~/.ssh/github.com/john-doe/john-doe_id_rsa
  IdentitiesOnly yes

# Secondary Personal GitHub - anonymous.john@domain.com
Host anonymous-john.github.com
  HostName github.com
  User git
  AddKeysToAgent yes
  #####################
  ## Mac/Linux Only ###
  UseKeychain yes	###
  #####################
  IdentityFile ~/.ssh/github.com/anonymous-john/anonymous-john_id_rsa
  IdentitiesOnly yes

# Work GitHub
Host work.github.com
  HostName github.com
  User git
  AddKeysToAgent yes
  #####################
  ## Mac/Linux Only ###
  UseKeychain yes	###
  #####################
  IdentityFile ~/.ssh/github.com/contoso/john-doe/john-doe_id_rsa
  IdentitiesOnly yes

# Work Azure
Host work.ssh.dev.azure.com
  HostName ssh.dev.azure.com
  User git
  AddKeysToAgent yes
  #####################
  ## Mac/Linux Only ###
  UseKeychain yes	###
  #####################
  IdentityFile ~/.ssh/dev.azure.com/contoso/john-doe/john-doe_id_rsa
  IdentitiesOnly yes

Host *
  IdentitiesOnly yes
```

# Top-Level `.gitconfig` Configuration File
Edit this in whatever editor your prefer - if it does not exist for some reason, create it with:
```bash
touch ~/.gitconfig
```

`~/.gitconfig`
```bash
[user]
    name = Default User
    email = default@domain.com

# GitHub Personal - john-doe
[includeIf "gitdir:~/src/github.com/john-doe/"]
    path = ~/src/github.com/john-doe/.gitconfig

[url "john-doe.github.com:john-doe/"]
    insteadOf = git@github.com:john-doe/

# GitHub Secondary - anonymous-john
[includeIf "gitdir:~/src/github.com/anonymous-john/"]
    path = ~/src/github.com/anonymous-john/.gitconfig

[url "anonymous-john.github.com:anonymous-john/"]
    insteadOf = git@github.com:anonymous-john/

# GitHub Work - John-Doe @ Contoso
[includeIf "gitdir:~/src/github.com/contoso/john-doe/"]
    path = ~/src/github.com/contoso/john-doe/.gitconfig

[url "work.github.com:contoso/"]
    insteadOf = git@github.com:contoso/

# Azure Work - John-Doe @ Contoso
[includeIf "gitdir:~/src/dev.azure.com/john-doe/"]
    path = ~/src/dev.azure.com/contoso/john-doe/.gitconfig

[url "work.ssh.dev.azure.com:contoso/"]
    insteadOf = git@ssh.dev.azure.com:contoso/

```


# Per Account `.gitconfig` Configuration Files

Create a `.gitconfig` for each repo or tree directory depending on how you defined your top-level `.gitconfig` file.


## GitHub: Primary

`~/src/github.com/john-doe/.gitconfig`
```bash
[user]
   name = John Doe
   email = 00000001+john-doe@users.noreply.github.com
```
- **NOTE**: Replace `00000001` with your GitHub User ID. 
Easily checked with GitHub API: https://api.github.com/users/john-doe

## GitHub: Secondary

`~/src/github.com/anonymous-john/.gitconfig`
```bash
[user]
   name = anonymous-john
   email = 00000002+anonymous-john@users.noreply.github.com
```
- **NOTE**: Replace `00000002` with your GitHub User ID. 
Easily checked with GitHub API: https://api.github.com/users/john-doe


## GitHub: Work

`~/src/github.com/contoso/john-doe/.gitconfig`
```bash
[user]
   name = John Doe
   email = 00000003+john-doe@users.noreply.github.com
```
- **NOTE**: Replace `00000003` with your GitHub User ID. 
Easily checked with GitHub API: https://api.github.com/users/john-doe


## Azure: Work

`~/src/dev.azure.com/contoso/john-doe/.gitconfig`
```bash
[user]
   name = John Doe
   email = john-doe@contoso.com
```

# New Repositories - Clone with modified SSH URL

Clone new repositories like
```bash
git clone git@john-doe.github.com:john-doe/sample-repo.git
git clone git@john-doe.github.com:anonymous-doe/sample-repo.git
```

Cloning new org repositories with the account you want to use:
```bash
# Primary: GitHub
cd ~/src/github.com/john-doe/
git clone git@john-doe.github.com:contoso/sample-repo.git

# Secondary: GitHub
cd ~/src/github.com/anonymous-john/
git clone git@anonymous-john.github.com:contoso/sample-repo.git

# Work: GitHub
cd ~/src/github.com/contoso/john-doe/
git clone git@work.github.com:contoso/sample-repo.git

# Work: Azure
cd ~/src/dev.azure.com/contoso/john-doe/
git clone git@work.ssh.dev.azure.com:contoso/sample-repo.git
```


# Existing Repositories - Update Remote(s)

Check current remote with `git remote -v`
- These likely still point to your old HTTPS or SSH configuration

Update each repository to use the your custom SSH URL:
*(This is defined as `Host` within the `~/.ssh/config` file)*

## GitHub Primary SSH URL

`git remote set-url origin git@john-doe.github.com:john-doe/sample-repo.git`

## GitHub Secondary SSH URL

`git remote set-url origin git@anonymous-john.github.com:anonymous-john/sample-repo.git`

## GitHub Work SSH URL

`git remote set-url origin git@work.github.com:contoso/john-doe/sample-repo.git`

## Azure Work SSH URL

`git remote set-url origin git@work.ssh.dev.azure.com:v3/contoso/sample-repo.git`


# Privatize GitHub Emails

- https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address#setting-your-commit-email-address-on-github


# References

- https://gist.github.com/yinzara/bbedc35798df0495a4fdd27857bca2c1
- https://stackoverflow.com/a/58550269
- https://psychowhiz.medium.com/configuring-multiple-ssh-keys-for-git-on-the-same-device-41c29320e5fe
- https://learn.microsoft.com/en-us/azure/devops/repos/git/use-ssh-keys-to-authenticate?source=recommendations&view=azure-devops
    - https://learn.microsoft.com/en-us/azure/devops/repos/git/use-ssh-keys-to-authenticate?view=azure-devops#migrate


# FAQ
## Mac/Linux
### `UseKeyChain` 
-  Within `~/.ssh/config` file, make sure to include `UseKeychain yes`

## Windows

### Case-Insensitive Paths for VS Code
- Need to have path in a Windows friendly format when declaring `includeIf` gitdirs, 
	- e.g. `c:\Users\ego\.\.\.\`
	- VS Code requires case insensitive flag within your `includeIf`, specified as `gitdir/i:`
	- `[includeIf "gitdir/i:c:/Users/eGo/src/github.com/pnc-nz/"]`
	- Refer: https://github.com/Microsoft/vscode/issues/62921#issuecomment-437693020

### `%HOMEPROFILE%` to work as `HOME` Environment Variable
- Configure `%HOMEPROFILE%` as `HOME` in Windows to allow for using
	- Refer: https://stackoverflow.com/questions/44019492/git-for-windows-does-not-load-userprofile-gitconfig-when-launched-run-as    