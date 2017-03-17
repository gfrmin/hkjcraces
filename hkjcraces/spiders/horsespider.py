import re

import scrapy
from scrapy.selector import Selector
from hkjcraces.items import horseItem

BASE_URL = "http://www.hkjc.com/english/racing/"

class HorsesSpider(scrapy.Spider):
    name = "horses"
#    allowed_domains = ["http://www.hkjc.com/"]
    start_urls = (
        BASE_URL + "horsesearch.asp?searchtype=name&horsename=&PAGE=60",
    )

    def parse(self, response):
        numberofpages = re\
        .search(r"Page ([0-9]+) of ([0-9]+) Page", response.css(".subheader:nth-child(2)::text").extract_first())\
        .groups()[1]
        for page in range(1, int(numberofpages)+1):
            yield scrapy.Request(BASE_URL + "horsesearch.asp?searchtype=name&horsename=&PAGE=" + str(page), self.parse_horse_list_page)

    def parse_horse_list_page(self, response):
        horsepageurls = response.css(".table_eng_text .table_eng_text .table_eng_text::attr(href)").extract()
        for horsepageurl in horsepageurls:
            yield scrapy.Request(BASE_URL + horsepageurl + "&Option=1", self.parse_horse_page)

    def parse_horse_page(self, response):
        horse = horseItem()
        horseurlinfo = re.search(r"(OtherHorse|horse).asp\?HorseNo=(\w*)", response.url).groups()
        horse['horseid'] = horseurlinfo[1]
        otherhorse = horseurlinfo[0] == 'OtherHorse'
        horse['retired'] = otherhorse

        if not otherhorse:
            horse['horsename'] = response.css(".title_eng_text::text").extract_first().split(u'\xa0')[0].strip()

            informationtabletds = [td.strip(":\r\t\n ") for td in 
                                   map(lambda tds: "".join(tds), 
                                       map(lambda td: td.css("::text").extract(),
                                           response.css("form td td:nth-child(2) font")[0:7] 
                                           + response.css("td:nth-child(4) .table_eng_text")[0:7]))]

            horse['country'], horse['age'] = re.search(r"(\w+)\s+/\s+(\w+)", informationtabletds[0]).groups()

            horse['colour'], horse['sex'] = re.search(r"(\w+)\s+/\s+(\w+)", informationtabletds[1]).groups()

            horse['importtype'] = informationtabletds[2]

            horse['seasonstake'] = informationtabletds[3]

            horse['totalstake'] = informationtabletds[4]
            
            horse['noof123'] = informationtabletds[5]

            horse['numberofstartpast10meetings'] = informationtabletds[6]
                    
            horse['trainername'] = informationtabletds[7]
            horse['trainerid'] = Selector(text = response.css("td:nth-child(4) .table_eng_text")[0].extract()).css("a::attr('href')").extract_first()[-3:]
            
            horse['ownername'] = informationtabletds[8]

            horse['currentrating'] = informationtabletds[9]

            horse['startofseasonrating'] = informationtabletds[10]

            horse['sire'] = informationtabletds[11]
            
            horse['dame'] = informationtabletds[12]

            horse['damessire'] = informationtabletds[13]

        else: # retired horse
            horse['horsename'] = response.css(".subsubheader::text").extract_first().split(u'\xa0')[0].strip()

            informationtabletds = [td.strip(":\r\t\n ") for td in 
                                   map(lambda tds: "".join(tds), 
                                       map(lambda td: td.css("::text").extract(),
                                           response.css("form td:nth-child(2) td:nth-child(2) font")[0:5] 
                                           + response.css("form td td:nth-child(4) font")[0:5]))]

            horse['country'] = informationtabletds[0]
            horse['colour'], horse['sex'] = re.search(r"(\w+)\s+/\s+(\w+)", informationtabletds[1]).groups()
            horse['importtype'] = informationtabletds[2]
            horse['totalstake'] = informationtabletds[3]
            horse['noof123'] = informationtabletds[4]
            horse['ownername'] = informationtabletds[5]
            horse['lastrating'] = informationtabletds[6]
            horse['sire'] = informationtabletds[7]
            horse['dame'] = informationtabletds[8]
            horse['damessire'] = informationtabletds[9]

        yield horse