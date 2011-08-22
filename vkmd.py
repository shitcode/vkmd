#-=-coding:utf-8-=-
import urllib
import urllib2
import cookielib
import re
import os
import sys
import getopt

class VkAgent:
    def __init__(self, email, passw):
        self.urlopener() #install cookie support
        auth = {'act':'login', 'q':'1', 'al_frame':'1', 'captcha_sid':'', 'captcha_key':'', 'from_host':'vk.com', 
            'vk':'1', 'email':email, 'pass':passw, 'expire':''}
        self.request('https://login.vk.com/?act=login', auth)
        
    def urlopener(self):
        cj = cookielib.CookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)
        
    def request(self, url, post=None):
        if post: post = urllib.urlencode(post)
        content = urllib2.urlopen(urllib2.Request(url,post)).read()
        return content

def main():
    htmlsc = (('&', '&amp;'), ('<', '&lt;'), ('>', '&gt;'), ('"', '&quot;'), ('', '/'))
    vk = VkAgent(email, passw)
    page = vk.request('http://vk.com/audio?id=%s' % uid)
    tr = re.search(ur'<b id\=\"audio_summary\">(?P<au>(.+?))<\/b>', page, re.UNICODE|re.DOTALL|re.MULTILINE)
    trc = re.search(ur"(\d+)",tr.group('au')).group(0) #count tracks
    try: os.mkdir(uid) #directory to save to
    except OSError: pass 
    
    for i in range(0,int(trc),50): #TODO (0
        page = vk.request('http://vk.com/audio?id=%s&offset=%s' % (uid,i))
        tracks = re.split(ur'<td class\=\"play_btn\">', page)
        for j in tracks[1:-2]:
            link = re.search(ur'<input type\=\"hidden\" id="audio_info[0-9]+_[0-9]+" value="(?P<link>(.+?)),[0-9]+" \/\>', j).group('link')
            name = re.search(ur'<div class="title_wrap">(?P<name>(.+?))</div>', j, re.DOTALL|re.MULTILINE).group('name')
            name = unicode(name, 'windows-1251')
            name = re.sub(ur'<[^>]+>', ur'', name, re.UNICODE|re.DOTALL|re.MULTILINE)
            name = re.sub(ur'&#(\d+);', lambda x: unichr(int(x.group(1))), name)
            for k in htmlsc:
                name = re.sub(k[1], k[0], name)
            if os.path.exists(uid+'/'+name + u'.mp3'): continue
            try: u = urllib2.urlopen(link, timeout=10)
            except: continue
            f = open(uid+'/'+name + u'.mp3', 'w')
            f.write(u.read())
            u.close(); f.close()
            print link + ' saved'
            

if __name__ == '__main__':
    opts, args = getopt.getopt(sys.argv[1:], "u:p:i:", ["help", "output="])
    param = {}
    for i in opts: param[i[0]] = i[1]
    email = param['-u'] #your mail
    passw = param['-p'] #your password
    uid = param['-i'] #profile id
    
    main()
