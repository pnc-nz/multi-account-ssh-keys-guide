# Multi-Account SSH Configuration Guide

This guide will help you create and configure the necessary files to enable `git` to support multiple version control systems dynamically, based on folder hierarchy and remote URL.

To achieve this, it will require the following steps to be completed:
  1. Update `~/.ssh/config`
  2. Update the top-level `~/.gitconfig`
  3. Update the per account `.gitconfig` files



## Example VCS Accounts
In the example below, our device will be configured in the scenario of three GitHub accounts and one Azure DevOps account.

**GitHub**
- Personal GitHub - john-doe@personal.com
- Personal GitHub - anonymous-john@domain.com
- Work GitHub - john-doe@contoso.com

**Azure DevOps**
- Work Azure DevOps - john-doe@contoso.com


## Example Directory Structures
```
~/.ssh/
│
│ # Files
├── config
│
│ # Directories
├── dev.azure.com/
│   └── contoso/
│      └── john-doe/
│
├── github.com/
│   ├── john-doe/
│   ├── anonymous-john/
│   └── contoso/
│      └── john-doe/


~/src/
├── dev.azure.com/
│   └── contoso/
│      └── john-doe/
│
├── github.com/
│   ├── john-doe/
│   ├── anonymous-john/
│   └── contoso/
│      └── john-doe/
```

# Generate Client SSH Keys
Generate the SSH key-pairs for each account you want to configure:
```bash
# Personal GitHub - john-doe@personal.com
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github.com/john-doe/john-doe_id_rsa -C "john-doe@personal.com"

# Personal GitHub - anonymous-john@domain.com
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github.com/anonymous-john/anonymous-john_id_rsa -C "anonymous-john@domain.com"

# Work GitHub - john-doe@contoso.com
ssh-keygen -t rsa -b 4096 -f ~/.ssh/github.com/contoso/john-doe/john-doe_id_rsa -C "john-doe@contoso.com"

# Work Azure DevOps - john-doe@contoso.com
ssh-keygen -t rsa -b 4096 -f ~/.ssh/dev.azure.com/contoso/john-doe/john-doe_id_rsa -C "john-doe@contoso.com"
```
The -C flag is for adding a comment (optional).


# SSH Configuration File
The SSH configuration file `config` will need to be updated to include configuration keys for each source you want to add.


### (OPTIONAL) Create `config` file if it doesn't exist
```bash
touch ~/.ssh/config && chmod 600 ~/.ssh/config
```

## Example File
```bash
# Personal GitHub - john-doe@personal.com
Host john-doe.github.com
  HostName github.com
  User git
  AddKeysToAgent yes
  IdentityFile ~/.ssh/github.com/john-doe/john-doe_id_rsa
  IdentitiesOnly yes
  UseKeychain yes	# -- MAC/LINUX ONLY; COMMENT IF ON WINDOWS -- #


# Personal GitHub - anonymous-john@domain.com
Host anonymous-john.github.com
  HostName github.com
  User git
  AddKeysToAgent yes
  IdentityFile ~/.ssh/github.com/anonymous-john/anonymous-john_id_rsa
  IdentitiesOnly yes
  UseKeychain yes	# -- MAC/LINUX ONLY; COMMENT IF ON WINDOWS -- #


# Work GitHub - john-doe@contoso.com
Host work.github.com
  HostName github.com
  User git
  AddKeysToAgent yes
  IdentityFile ~/.ssh/github.com/contoso/john-doe/john-doe_id_rsa
  IdentitiesOnly yes
  UseKeychain yes	# -- MAC/LINUX ONLY; COMMENT IF ON WINDOWS -- #


# Work Azure DevOps - john-doe@contoso.com
Host work.ssh.dev.azure.com
  HostName ssh.dev.azure.com
  User git
  AddKeysToAgent yes
  IdentityFile ~/.ssh/dev.azure.com/contoso/john-doe/john-doe_id_rsa
  IdentitiesOnly yes
  UseKeychain yes	# -- MAC/LINUX ONLY; COMMENT IF ON WINDOWS -- #

# Default Account
Host *
  IdentitiesOnly yes
```

# Top-Level Git `.gitconfig` File 
We will configure our top-level `.gitconfig` file to handle three things here:
1. A default/fallback account if no account-level `.gitconfig` file is found
2. Dynamic`.gitconfig` file usage based on current directory
3. URL re-writing to match the `Host` configuration key values in our  `.ssh/config` file

### (OPTIONAL) Create `.gitconfig` file if it doesn't exist
```bash
touch ~/.gitconfig && chmod 600 ~/.gitconfig
```

## Operating System Specific Configuration Keys
When setting these keys, remember to set the appropriate key if you are on Windows. The example below will use MacOS/Linux.

### Windows:
```bash
[includeIf "gitdir/i:c:/Users/USERNAME/src/.../.../..."]
  path = ~/src/.../.../.../.gitconfig
```

### Mac/Linux
```bash
[includeIf "gitdir:~/src/.../.../.../"]
  path = ~/src/.../.../.../.gitconfig
```

## Samples
```bash
# --------- Default Account - Fallback if no config ------------- #
[user]
    name = Default User
    email = default@domain.com


# --------- Personal GitHub - john-doe@personal.com ------------- #
[includeIf "gitdir:~/src/github.com/john-doe/"]
    path = ~/src/github.com/john-doe/.gitconfig

[url "john-doe.github.com:john-doe/"]
    insteadOf = git@github.com:john-doe/


# --------- Personal GitHub - anonymous-john@domain.com --------- #
[includeIf "gitdir:~/src/github.com/anonymous-john/"]
    path = ~/src/github.com/anonymous-john/.gitconfig

[url "anonymous-john.github.com:anonymous-john/"]
    insteadOf = git@github.com:anonymous-john/


# --------- Work GitHub - john-doe@contoso.com ----------------- #
[includeIf "gitdir:~/src/github.com/contoso/john-doe/"]
    path = ~/src/github.com/contoso/john-doe/.gitconfig

[url "work.github.com:contoso/"]
    insteadOf = git@github.com:contoso/


# --------- Work Azure DevOps - john-doe@contoso.com ----------- #
[includeIf "gitdir:~/src/dev.azure.com/john-doe/"]
    path = ~/src/dev.azure.com/contoso/john-doe/.gitconfig

[url "work.ssh.dev.azure.com:contoso/"]
    insteadOf = git@ssh.dev.azure.com:contoso/
```


# Account-Level `.gitconfig` Files

Create a `.gitconfig` **for each account** you want to configure. Using our examples above, we will create 4 config files in total, three for the GitHub accounts and one for the Azure DevOps account.

# Samples
`~/src/github.com/john-doe/.gitconfig`
```bash
[user]
   name = John Doe
   email = ID+john-doe@users.noreply.github.com
```

`~/src/github.com/anonymous-john/.gitconfig`
```bash
[user]
   name = anonymous-john
   email = ID+anonymous-john@users.noreply.github.com
```

`~/src/github.com/contoso/john-doe/.gitconfig`
```bash
[user]
   name = John Doe
   email = ID+john-doe@users.noreply.github.com
```

`~/src/dev.azure.com/contoso/john-doe/.gitconfig`
```bash
[user]
   name = John Doe
   email = john-doe@contoso.com
```

## GitHub: Email Privacy Information
GitHub uses your commit email address to associate commits with your account on GitHub. You can choose the email address that will be associated with the commits you push from the command line as well as web-based Git operations you make.

To use your `noreply` email address for commits you push from the command line, use that email address when you set your commit email address in Git. To use your noreply address for web-based Git operations, set your commit email address on GitHub and choose to Keep my email address private.

**Accounts created after July 18, 2017**
> Your noreply email address for is an ID number and your username in the form of `ID+USERNAME@users.noreply.github.com`. 
- **NOTE**: Replace `ID` with your GitHub User ID. 
Easily checked with GitHub API: https://api.github.com/users/john-doe

**Accounts created before July 18, 2017 and `Keep my email address private` enabled**
>  Your noreply email address is `USERNAME@users.noreply.github.com`. You can get an ID-based noreply email address by selecting (or deselecting and reselecting) Keep my email address private in your email settings.

### Source
[GitHub - Setting your commit email address](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-email-preferences/setting-your-commit-email-address#setting-your-commit-email-address-on-github)



# Usage

Clone new repositories as you normally would, for example:
```bash
git clone git@github.com:john-doe/sample-repo.git
git clone git@github.com:anonymous-doe/sample-repo.git
git clone git@ssh.dev.azure.com:v3/contoso/projects/acme-codebase
```


# Existing Repositories - Update Remote(s)

You can update previously configured repositories to use the SSH remote URL now that your keys are configured.

For example, within the `~/src/github.com/john-doe/sample-repo` folder:
```bash
git remote set-url origin git@john-doe.github.com:john-doe/sample-repo.git
```


# References

- https://gist.github.com/yinzara/bbedc35798df0495a4fdd27857bca2c1
- https://stackoverflow.com/a/58550269
- https://psychowhiz.medium.com/configuring-multiple-ssh-keys-for-git-on-the-same-device-41c29320e5fe
- https://learn.microsoft.com/en-us/azure/devops/repos/git/use-ssh-keys-to-authenticate?source=recommendations&view=azure-devops
    - https://learn.microsoft.com/en-us/azure/devops/repos/git/use-ssh-keys-to-authenticate?view=azure-devops#migrate


# FAQ
## Mac/Linux
### `UseKeyChain` 
- Within `~/.ssh/config` file, make sure to include `UseKeychain yes`
- You will receive an error on Windows if you erraneously include this configuration key

## Windows

### Case-Insensitive Paths for VS Code
- Need to have path in a Windows friendly format when declaring `includeIf` gitdirs, 
	- e.g. `c:\Users\pnc-nz\.\.\.\`
	- VS Code requires case insensitive flag within your `includeIf`, specified as `gitdir/i:`
	- `[includeIf "gitdir/i:c:/Users/USERNAME/src/github.com/john-doe/"]`
	- See [this as reference](https://github.com/Microsoft/vscode/issues/62921#issuecomment-437693020)

### System Env Var `%HOMEPROFILE%` to work as `HOME`
- Configure `%HOMEPROFILE%` as `HOME` in Windows to allow for using
	- Refer: https://stackoverflow.com/questions/44019492/git-for-windows-does-not-load-userprofile-gitconfig-when-launched-run-as    