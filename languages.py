# import x 

# dk_user_name = "navn" 
# dk_user_name_rules = f"{x.USER_NAME_MIN} til {x.USER_NAME_MAX} tegn" 
# dk_user_name_ex = f"navn {x.USER_NAME_MIN} til {x.USER_NAME_MAX} tegn" 
# dk_user_name_already_exists = f"navnet findes allerede" 


# en_user_name = "name" 
# en_user_name_rules = f"{x.USER_NAME_MIN} to {x.USER_NAME_MAX} characters" 
# en_user_name_ex = f"name {x.USER_NAME_MIN} to {x.USER_NAME_MAX} characters" 
# en_user_name_already_exists = f"name already exists" 


# mini‐dict of translations keyed by your URL param (‘dk’ or ‘en’)
translations = {
    'dk': {
        'more_items': 'Vis mere',
        'login' : 'Log ind',
        'search' : 'Søg',
    },
    'en': {
        'more_items': 'Show more',
        'login' : 'Login',
        'search' : 'Search',
    },
}

# defining a function to translate the keys
def translate(key: str, lan: str = 'dk') -> str:
    """
    Look up `key` in the given `lan`, falling back to key itself.
    """
    return translations.get(lan, translations['dk']) .get(key, key)


