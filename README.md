# Mist-Site-Settings-Applier
A script for bulk applying changes to site settings in Mist

## Requirements/Dependencies
This script requires the [mistapi](https://pypi.org/project/mistapi/) package to function.

## Description
This script allows the user to pull down Mist Site Settings (in the GUI this is Organization > Site Configuration > Site
Name). This results in a json file with all of the site settings. The user can then modify or create their own json file
containing settings they would like to change. Then these settings can be bulk uploaded to any number of sites at once. 
This script can also be used for creating and restoring backups for site settings.
### Environment File
It is recommended to set up an environment file with the name: mist_env with a token to expedite the authentication process. 
[Here](https://api-class.mist.com/rest/create/api_tokens/) is more info on how to get a Mist token. 
Below is an example of an environment file:
```commandline
MIST_HOST = api.mist.com
MIST_APITOKEN = xxxxxx
MIST_ORG_ID = 203d3d02-xxxx-xxxx-xxxx-76896a3330f4
```
You can find more info on environment files [here](https://github.com/tmunzer/mist_library).
### Suggested Workflow
The script was designed with the following workflow in mind:
1. Configure desired settings in a test site in the GUI.
2. Pull down the site settings for that site.
3. Copy out the relevant site settings into a new file. **Important: The proper JSON hierarchy and format must be 
maintained.**
   1. You are free to (and recommended to) leave out settings that you don't want to change.
   2. However, you must include the parents to the settings you would like to change.
   3. Example: If you would like to change just the custom version for AP33s your file could look like:
      ```
      {
       "auto_upgrade": {
         "custom_versions": {
           "AP33": "0.14.28806"
         }
        }
       }
      ```
   4. Ensure that prerequisite settings are either already enabled or are included. The above example would not work if 
      the site didn't already have these two settings set under "auto_upgrade":
      ```
        "enabled": true,
        "version": "custom"
      ```
4. Use the script to push your settings to as many sites as you want.
