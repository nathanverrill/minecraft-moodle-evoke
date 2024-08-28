# FastAPI script for EVOKE API see https://fastapi.tiangolo.com/
# Nathan Verrill 3 JUN 2022 for World Bank
# usage:
# ...setup python virtual environment:
# source env/bin/activate
# python3 -m pip install --upgrade pip
# python3 -m pip install -r requirements.txt
# ...run fastapi application
# uvicorn main:app --reload  
# ...view interactive api documentation
# http://127.0.0.1:8000/docs


# python libraries
from typing import Union

from fastapi import FastAPI

from pydantic import BaseModel

from moodle import Moodle


# declare api application
app = FastAPI()


#################################
# so image always included with badge; change as needed
NO_BADGE_IMAGE = 'https://www.sticker.com/picture_library/product_images/custom-blank/custom-square-blank-stickers.png'


#################################
# Evoke Badge
# An extensible badge representation not constrained by moodle 
class EvokeBadge(BaseModel):                                
    badgeOwnerMoodleId: int                                 # moodle user id
    badgeName: str                                          # specified in Moodle badge administration
    badgeDescription: str                                   # specified in Mooble badge administration
    badgeImageUrl: Union[str, None] = NO_BADGE_IMAGE        # always have an image URL available to not break web UI
    badgeId: str                                            # set by moodle. string to use moodle's badge hash for id, since the int moodle badge id is optional
    isBobCool: Union[str, None] = 'Nope' 
    extra: Union[str, None] = ''                            # use extra for additional content in str or stringified json format 

#################################
# Minecraft User
# A representation of a Minecraft usesr 
class MinecraftUser(BaseModel):  
    minecraftUsername:          str
    moodleId:                   int
    evokeId:                    int
    evokeBadges:                Union[EvokeBadge, None] = None

#################################
# Establish connection to Moodle
# 1. instantiate moodle api
# 2. return moodle object that can be used by other functions
def moodle_connect():
    # change as needed
    # MOODLE_API_URL = 'https://staging.evokenet.org/moodle/webservice/rest/server.php'
    # MOODLE_API_TOKEN = '5c80c940860bea1decd3bd9134d514b8'

    # moodle cloud test site
    MOODLE_API_URL = 'https://evoke-api-test.moodlecloud.com/webservice/rest/server.php'
    MOODLE_API_TOKEN = '0a034657a01911e377d14186f64d9746'

    # instantiate api proxy
    moodle = Moodle(MOODLE_API_URL, MOODLE_API_TOKEN)    

    # return moodle instance so other functions can use it
    return moodle  

#################################
# Get badge from Moodle and return evoke badge
# 1. request moodle badges (mbs) for specified user
# 2. create evoke badge using moodle data
# 3. return evoke badge
def badgesFromMoodle(moodle, moodleUserId):


    # request badges for specified user using moodle web services api
    # returns 0 to many badges in a moodlepy `badgeresponse` object
    # mb = moodlebadge, used to avoid ambiguity with Evoke Badge naming
    mbs = moodle.core.webservice.moodle.core.bagdes.get_user_badges(userid=moodleUserId)

    # for testing purposes, using just the first badge returned
    # TODO handle multiple badges
    mb = mbs[0]                                                   

    # create EvokeBadge object with data returned from moodle
    evokeBadge = EvokeBadge(
        badgeOwnerMoodleId      = moodleUserId, 
        badgeName               = mb.name,
        badgeDescription        = mb.description,
        badgeImageUrl           = mb.badgeurl,
        badgeId                 = mb.uniquehash,
        extra                   = f'NOTE: If user has multiple badges, API only returns first badge at this time.'
    )

    return evokeBadge


#################################
# Fast API badge methods
@app.get("/moodle-badges-for-user/{moodle_user_id}")
def read_item(moodle_user_id: int, q: Union[str, None] = None):

    moodle = moodle_connect()

    # get evoke badge created with moodle data
    return badgesFromMoodle(moodle, moodle_user_id)             
    
@app.get("/v1/moodle-badges-for-user/{moodle_user_id}")
def read_item(moodle_user_id: int, q: Union[str, None] = None):

    moodle = moodle_connect()

    # get evoke badge created with moodle data
    return badgesFromMoodle(moodle, moodle_user_id)  

#################################
# Fast API default getter
@app.get("/")
def read_root():
    return {"EVOKE": "EVOKE API Proof of Concept APIs"}



