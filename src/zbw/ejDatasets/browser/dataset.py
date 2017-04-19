from Products.Five.browser import BrowserView
from ckanapi import RemoteCKAN


class Ckan(BrowserView):

    def get_dataset(self):
        """
        first test
        """
        url = "http://134.245.93.80:5000"
        demo = RemoteCKAN(url)
        pkg = demo.action.package_show(id='is-a-firm-a-firm-a-stackelberg-experiment')
        resources = pkg['resources']
        evil_html = u"<html><head><title>Test</title></head><body><h1>Resources</h1>"
        for res in resources:
            evil_html += u"<p><a href='{}'><br />{}</p>{}".format(res['url'],
                    res['name'], res['description'])
        evil_html += u"</body></html>"

        return evil_html

# dataverse Token (bunke):
# 22a77c03-b4c5-41fe-9cca-995c9a5c601a
# test doi: doi:10.7910/DVN/P9VSZA
