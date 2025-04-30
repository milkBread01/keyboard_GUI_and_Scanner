


""" 
                              FORMAT
{
    "Default": {
        "name": "Default",
        "keys": {
                "1": {"LABEL": "Email", "TYPE": "website", "VALUE": "https://..."},
                "22": {"LABEL": "Email", "TYPE": "website", "VALUE": "https://..."}
                }
        "primary": "True"
    }
    
}



"""
# Search previously created text document for profiles 
def search_for_existing_profiles(profile_file):
    existing_profile_names=[]
    content = ""
    with open(profile_file, "r") as file:
        content = file.read()
    
    for line in content:
        print (line) 
