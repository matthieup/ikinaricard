import requests
import re
import urllib3
from urllib3.exceptions import InsecureRequestWarning
urllib3.disable_warnings(InsecureRequestWarning)


class IkinariCard(object):
    URL = 'https://www.vcsys.com/s/pepper-fs/m/login;jsessionid=5F2B539C46E242AFBE1BED41A4F06B65'
    # define if needed 
    #PROXY = {'https': 'XXXXXX',  'http': 'XXXXXX'}
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
                'Referer': 'https://www.vcsys.com/s/pepper-fs/m/', 'Host': 'www.vcsys.com', "Content-Type": "application/x-www-form-urlencoded"}

    def __init__(self, id_, pass_):
        self.id_ = id_
        self.card1_ = self.id_[0:4]
        self.card2_ = self.id_[4:8]
        self.card3_ = self.id_[8:12]
        self.card4_ = self.id_[12:16]
        self.pass_ = pass_
        self.page_ = requests.post(self.URL, proxies=self.PROXY, headers=self.HEADERS,
                            verify=False, params={'cardId1': str(self.card1_), 'cardId2': str(self.card2_), 'cardId3': str(self.card3_), 'cardId4': str(self.card4_), 'cardPin': str(self.pass_)}).text

    def get_expiry(self):
        date = re.search(
            r".*有効期限：(?P<year>[0-9]*)年(?P<month>[0-9]*)月(?P<day>[0-9]*)日", self.page_)
        if date:
            date_ = "{}/{}/{}".format(date.group('year'),
                                      date.group('month'), date.group('day'))
        return date_ if date_ else None

    def get_points(self):
        points = re.search(
            r'.*積算ﾏｲﾚｰｼﾞ：<span id="pointTotal" style="font-size:x-small;color:#aa0000">(?P<points>[0-9,]*)</span>g<br />', self.page_)
        if points:
            points_ = "{}".format(points.group('points'))
        return points_ if points_ else None


if __name__ == "__main__":
    total_grams = 0
    with open('ikinari.txt') as file_:
        for card_ in file_.readlines():
            (id_, pass_) = card_.strip().split(';')
            a = IkinariCard(id_, pass_)
            (date_, points_) = (a.get_expiry(), a.get_points())
            total_grams = total_grams + int(points_.replace(',', ''))
            print("{} will expire on {} and has {} points".format('-'.join(id_[i:i+4] for i in range(0,len(id_),4)), date_, points_))
    print(f"Total amount eaten: {total_grams}")
