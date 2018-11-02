from lxml import etree
from urllib import request
import os
import time
# url = "http://weather.unisys.com/hurricane/atlantic/2017/index.php"
# response = request.urlopen(url)
def print_of_place(place):
    try:
        os.makedirs(place)
    except:
        pass
    for year in range(2016, 2018):
    # for year in range(1949, 2013):
        # with open("sss.html", "r") as f:
        #     text = f.read()
        url = "http://weather.unisys.com/hurricane/%s/%s/index.php" % (place, year)
        useragent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
        headers = {'Host' : 'weather.unisys.com', 'User-Agent' : useragent, "Cookie" :"_ga=GA1.2.688097780.1512041599; _gid=GA1.2.1333686273.1512041599"}

        req = request.Request(url, headers=headers)
        response = request.urlopen(req)
        text = response.read()
        html = etree.HTML(text)
        # time.sleep(0.5)
        # //*[@id="content"]/table[1]/tbody/tr[2]
        results = html.xpath('//table[1]/tr')
        # print(results)
        with open(place + "/" + str(year) + ".txt", "w") as f:
            for result in results:
                lists = result.xpath("td/text()")
                print(lists)
                try:
                    f.write(lists[0] + "," + lists[1].strip() + "," + lists[2].strip() + ',' + lists[3].strip()+ ',' + lists[4].strip()+ ',' + lists[5].strip())
                    f.write("\n")
                except:
                    pass

# print_of_place("s_indian")
print_of_place("e_pacific")