# User Settings for icurry-webapp:
INTERNAL_CACHE_CLEANER = True # wether the application should clean the cache
                               # itself. If not, clean externally.
MAX_CACHE_AGE = 60*60 #Max age of files in cache specified in seconds

STEP_AMOUNT_MAX = 200 #Maximum of steps allowed for one computation request.
                      #It may be neccessary to run 'icurry_web.py --set' (with
                      #elevated priviliges) to apply the value to the entire application

# path of icurry executable, set if it isnt in system's PATH:
ICURRY_PATH = ""
# path to the webapp's dir, set if deploying with wsgi-server:
WEBAPP_PATH = "./"
