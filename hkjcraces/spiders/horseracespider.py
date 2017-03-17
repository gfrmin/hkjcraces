import re

import scrapy
from hkjcraces.items import horseraceItem

BASE_URL = "http://www.hkjc.com/english/racing/"

class HorseracesSpider(scrapy.Spider):
    name = "horseraces"
    #    allowed_domains = ["http://www.hkjc.com/"]
    start_urls = (
        BASE_URL + "horsesearch.asp?searchtype=name&horsename=&PAGE=1",
    )

    def parse(self, response):
        numberofpages = re \
            .search(r"Page ([0-9]+) of ([0-9]+) Page", response.css(".subheader:nth-child(2)::text").extract_first()) \
            .groups()[1]
        for page in range(1, int(numberofpages) + 1):
            yield scrapy.Request(BASE_URL + "horsesearch.asp?searchtype=name&horsename=&PAGE=" + str(page),
                                 self.parse_horse_list_page)

    def parse_horse_list_page(self, response):
        horsepageurls = response.css(".table_eng_text .table_eng_text .table_eng_text::attr(href)").extract()
        for horsepageurl in horsepageurls:
            yield scrapy.Request(BASE_URL + horsepageurl + "&Option=1", self.parse_horse_page)

    def parse_horse_page(self, response):
        horseurlinfo = re.search(r"(OtherHorse|horse).asp\?HorseNo=(\w*)", response.url).groups()
        racetable = response.css(".bigborder")
        if len(racetable) == 1:
            racetablerows = filter(lambda tr: len(tr.css("td").css("::text").extract()) > 14, racetable.css("tr")[1:]) # keep only data rows from race table
            for rowid, racetablerow in enumerate(racetablerows[1:]):
                tds = [td.strip() for td in racetablerow.css("td").css("::text").extract()]
                nonemptytds = filter(lambda td: td != "", tds)
                horserace = horseraceItem()

                horserace['horseid'] = horseurlinfo[1]

                horserace['race'] = nonemptytds[0]  
                horserace['placing'] = nonemptytds[1] 
                horserace['racedate'] = nonemptytds[2]
                horserace['location'] = nonemptytds[3]
                horserace['track'] = nonemptytds[4]
                horserace['course'] = nonemptytds[5]
                horserace['distance'] = nonemptytds[6]
                horserace['going'] = nonemptytds[7]
                horserace['raceclass'] = nonemptytds[8] 
                horserace['draw'] = nonemptytds[9]
                horserace['rating'] = nonemptytds[10] 
                horserace['trainerid'] = re.search(r"trainercode=(\w+)&", racetablerows[3].extract()).groups()[0]
                horserace['trainername'] = nonemptytds[11]
                horserace['jockeyid'] = re.search(r"JockeyCode=(\w+)&", racetablerows[3].extract()).groups()[0]
                horserace['jockeyname'] = nonemptytds[12]
                horserace['lengthbehindwinner'] = nonemptytds[13]
                horserace['winningodds'] = nonemptytds[14]
                horserace['actualweight'] = nonemptytds[15] 
                horserace['runningpositions'] = nonemptytds[16] 
                horserace['finishtime'] = nonemptytds[17]  
                horserace['ondateweight'] = nonemptytds[18]  
                horserace['gears'] = nonemptytds[19]
                yield horserace

