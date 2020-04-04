from urllib import request
import re
import os
import time


class spider:
    def __init__(self):
        self.cnt = 0

    def reset(self):
        self.cnt = 0

    def GetNumber(self):
        return self.cnt

    def GetHtml(self, url):
        r = request.urlopen(url)
        html = r.read()
        html = str(html, encoding='utf-8')
        return html

    def GetImages(self, html, pattern):
        pattern = re.compile(pattern)
        img_list = pattern.findall(html)
        return img_list

    def callback(self, a, b, c):
        progress = 100.0 * a * b / c
        if progress > 100.0:
            progress = 100.0
        print('image %d:  %.0f%%' % (self.cnt + 1, progress))

    def DownloadImages(self, img_list, path, rename=True, start=0):
        if not os.path.exists(path):
            os.mkdir(path)
        for img in img_list:
            if self.cnt < start:
                self.cnt = self.cnt + 1
                continue
            if rename:
                idx = str.rfind(img, '.')  # use name 0001.jpg、0002.jpg、...
                if idx != -1:
                    filename = path + str.format('/%04d' % self.cnt) + img[idx:]
                    request.urlretrieve(img, filename, self.callback)
                    self.cnt = self.cnt + 1
            else:
                idx = str.rfind(img, '/')  # use original name
                if idx != -1:
                    filename = path + img[idx:]
                    request.urlretrieve(img, filename, self.callback)
                    self.cnt = self.cnt + 1

            # time.sleep(1)

    def start(self, url, pattern, path, rename=True, maxtimes=50, start=0):
        print('get html...')
        html = self.GetHtml(url)
        print('get image urls...')
        img_list = self.GetImages(html, pattern)
        print('image number: %d' % len(img_list))
        print('download images...')
        for tries in range(1, maxtimes):
            try:
                self.DownloadImages(img_list, path, rename, start)
                break
            except:
                if tries <= maxtimes:
                    print('Link is disconnected and try the %d time to connect again!' % (tries + 1))
                    time.sleep(2)  # sleep
                    start = self.GetNumber()
                    self.reset()
                    continue
                else:
                    print('Has tried %d times to access url %s, all failed!' % maxtimes)
                    break

        print('finish!')


if __name__ == "__main__":
    url = 'https://www.cs.toronto.edu/~vmnih/data/mass_roads/train/map/index.html'
    pattern = r'href="(.*?.tif)"'
    path = 'dataset/train/mask'
    maxtimes = 1000
    start = 0

    sp = spider()
    sp.start(url, pattern, path, False, maxtimes, start)

