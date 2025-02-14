# Auto SSH Configuration Tool

## Sample:
`ssh-keygen -t rsa -b 4096 -f ~/.ssh/github.com/john-doe/john-doe_id_rsa -C "john-doe@personal.com"`


## Functionality: 
- Should check for existing ssh configurations that match the input
- Should use a template file to generate relevant ssh config files 
- Initial support should focus on github and azdo
- Need to handle multi OS filepaths etc.
- Maybe use `tree` tool or something to generate nice visuals on cli