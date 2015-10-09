#!/usr/bin/env python
#
# this is a modified version of the Google App Engine Tutorial
import webapp2, os, urllib, urllib2, json
import jinja2
import logging

JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=["jinja2.ext.autoescape"],
    autoescape=True)

def summarizeArticle(userurl):
    baseurl = "http://clipped.me/algorithm/clippedapi.php?url="
    url = baseurl + userurl
    try:
        read = urllib2.urlopen(url).read()
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        elif hasattr(e, 'code'):
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        return None
    else:
        return json.loads(read)

def translate(term, params={}):
    baseurl = "http://syslang.com?"
    params["src"] = "en"
    params["dest"] = "zh-cn"
    params["text"] = term
    params["email"] = "dorothynkong@gmail.com"
    params["password"] = "Frengly"
    params["outformat"] = "json"
    url = baseurl + urllib.urlencode(params)
    return json.loads(urllib2.urlopen(url).read())

def translateChar(term, params={}):
    baseurl = "http://syslang.com?"
    params["src"] = "zh-cn"
    params["dest"] = "en"
    params["text"] = term
    params["email"] = "dorothynkong@gmail.com"
    params["password"] = "Frengly"
    params["outformat"] = "json"
    url = baseurl + urllib.urlencode(params)
    return json.loads(urllib2.urlopen(url).read())

class Article:
    def __init__(self, link, archive={}):
        summarized = summarizeArticle(link)
        self.archive = archive
        self.title = summarized["title"]
        self.article = ""
        for line in summarized["summary"][0:-1]:
            self.article += line + " "
        self.wordlist = self.article.split()
        self.translation = translate(self.article)["translation"]
        chars = self.translation.split()
        self.vocab = chars
#        for char in chars:
#           self.vocab[char] = translateChar(term=char)["translation"]

    # def translateWord(self, word, params={}):
    #     baseurl = "http://syslang.com?"
    #     params["src"] = "en"
    #     params["dest"] = "zh-cn"
    #     params["text"] = word
    #     params["email"] = "dorothynkong@gmail.com"
    #     params["password"] = "Frengly"
    #     params["outformat"] = "json"
    #     url = baseurl + urllib.urlencode(params)
    #     return json.loads(urllib2.urlopen(url).read())[""]


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values={}
        link = self.request.get("link")
        go = self.request.get("gobtn")
        logging.info(link)
        logging.info(go)

        if len(link) > 0:
            template_values["link"] = link
            articledictionary = Article(link)
            template_values["summary"] = articledictionary.article
            template_values["title"] = articledictionary.title
            template_values["vocab"] = articledictionary.vocab
            template_values["translation"] = articledictionary.translation
            template = JINJA_ENVIRONMENT.get_template("link.html")
            self.response.write(template.render(template_values))
        else:
            template_values["prompt"] = "You must enter a link!"
            template = JINJA_ENVIRONMENT.get_template("index.html")
            self.response.write(template.render(template_values))

application = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
# http://www.globalpost.com/dispatch/news/regions/asia-pacific/china/141115/hong-kong-student-leaders-blocked-traveling-beijing
#,('/api/results.json',jsonHandler)