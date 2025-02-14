import os
import platform

from dotenv import load_dotenv

load_dotenv()


PLATFORM_UNIX = False if "Windows" in platform.system() else True 



def something_change_me():
    # DIRECTORIES
    """
    # Directories - `~/.ssh/*`
    
    1. Check that .ssh directory exists
    2. Check that .ssh/config file exists
    3. (Optional) Scan `.ssh/config` for existing configurations
    
    
    # Files - `~/.gitconfig`
    1. Check if `~/.gitconfig` file exists
    
    
    # Config Files
    1. Ask for remote source (GitHub, Azure DevOps)
    2. Ask for user-account name related to remote
    3. Ask for Organisation (GitHub) or Tenant (AzDo)
    4. 
    
    """
    if PLATFORM_UNIX:
        pass
    if os.path.exists(os.environ["SOME_KEY"]):
        pass
    

def generate_gitconfig_block(object):
    
    gitconfig = ""
    # TODO: Add check flag later
    if "generate_default" == True:
        gitconfig += """
        # Default Fallback
        [user]
            name = someone
            email = someone@somewhere.com
            
        """
    
    
    # -- Append `includeIf` block -- #
    if PLATFORM_UNIX:
        gitconfig += """
        ### ---- {SERVICE} | {USERNAME} ---- ###
        [includeIf "gitdir:~/src/github.com/john-doe/"]
            path = ~/src/github.com/john-doe/.gitconfig
        """
    
    # TODO: Split Linux / Mac / Mac (ARM)
    # TODO: Windows Support
    # else:
    #     gitconfig += """
    #     [includeIf "gitdir/i:c:/Users/USERNAME/src/github.com/john-doe/"]
    #         path = ~/src/github.com/john-doe/.gitconfig
    #     """
    
    
    # -- Append `url` block -- #
    gitconfig += """
    [url "john-doe.github.com:john-doe/"]
        insteadOf = git@github.com:john-doe/    
    """
    
    gitconfig += """
    ###-----------------------###
    """
    
    return gitconfig

# TODO: Update param and change IdentityFile
def generate_ssh_config_block(object):
    ssh_config = """
    Host {USERNAME}.{SERVICE}.{SERVICE_EXTENSION}
        HostName {SERVICE}.{SERVICE_EXTENSION}
        User git
        AddKeysToAgent yes
        IdentityFile ~/.ssh/github.com/john-doe/john-doe_id_rsa
        IdentityFile ~/.ssh/{SERVICE}.{SERVICE_EXTENSION}/{USERNAME}/{USERNAME}_id_rsa
        IdentitiesOnly yes   
    """
    
    # Handle Keychain requirement of *nix operating systems
    if "operating_system" == "Linux" or "operating_system" == "Mac":
        ssh_config += "\t UseKeychain yes"
        
    
    return ssh_config


def generate_dev_dirs():
    # os.makedirs() for super_makedir/leaf create
    directory = os.path.join(os.getcwd(), 'playerData')

def main():
    pass

if __name__ == "__main__":
    main()
    