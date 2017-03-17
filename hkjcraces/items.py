# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class horseItem(scrapy.Item):
    horseid = scrapy.Field()
    horsename = scrapy.Field()
    retired = scrapy.Field()
    country = scrapy.Field()
    age = scrapy.Field()
    trainerid = scrapy.Field()
    trainername = scrapy.Field()
    colour = scrapy.Field()
    sex = scrapy.Field()
    ownername = scrapy.Field()
    importtype = scrapy.Field()
    currentrating = scrapy.Field()
    lastrating = scrapy.Field()
    seasonstake = scrapy.Field()
    startofseasonrating = scrapy.Field()
    totalstake = scrapy.Field()
    sire = scrapy.Field()
    noof123 = scrapy.Field()
    dame = scrapy.Field()
    numberofstartpast10meetings = scrapy.Field()
    damessire = scrapy.Field()

class horseraceItem(scrapy.Item):
    horseid = scrapy.Field()
    race = scrapy.Field()
    placing = scrapy.Field()
    racedate = scrapy.Field()
    location = scrapy.Field()
    track = scrapy.Field()
    course = scrapy.Field()
    distance = scrapy.Field()
    going = scrapy.Field()
    raceclass = scrapy.Field()
    draw = scrapy.Field()
    rating = scrapy.Field()
    trainerid = scrapy.Field()
    trainername = scrapy.Field()
    jockeyid = scrapy.Field()
    jockeyname = scrapy.Field()
    lengthbehindwinner = scrapy.Field()
    winningodds = scrapy.Field()
    actualweight = scrapy.Field()
    runningpositions = scrapy.Field()
    finishtime = scrapy.Field()
    ondateweight = scrapy.Field()
    gears = scrapy.Field()
