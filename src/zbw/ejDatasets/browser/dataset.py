from Products.Five.browser import BrowserView
from ckanapi import RemoteCKAN
import random
import requests
from hurry.filesize import size
import logging



# for testing only! edawax demo server, fixed ids
url = "http://134.245.93.80:5000"
demo = RemoteCKAN(url)
ids = ["is-a-firm-a-firm-a-stackelberg-experiment",
       "title-of-your-article-replication-data"]
id = random.choice(ids)
pkg = demo.action.package_show(id=id)
resources = pkg['resources']



class Ckan(BrowserView):
    """
    not in use, yet
    """

    def get_dataset(self):
        """
        first test
        """
        evil_html = u"<html><head><title>Test</title></head><body>"
        evil_html += u"<h2><a href='{}'>{}</a></h2>".format(url+"/dataset/"+id, pkg['title'])
        evil_html += u"<h3>Resources</h3>"
        for res in resources:
            evil_html += u"<p><a href='{}'><br />{}</p>{}".format(res['url'],
                    res['name'], res['description'])
        evil_html += u"</body></html>"

        return evil_html

    def resources(self):
        return resources
        
        

# dataverse Token (bunke):
# 22a77c03-b4c5-41fe-9cca-995c9a5c601a
# test doi: doi:10.7910/DVN/P9VSZA


class Dataverse(BrowserView):

    base_url = "https://dataverse.harvard.edu"
    token = '22a77c03-b4c5-41fe-9cca-995c9a5c601a'
    logger = logging.getLogger('Dataverse')
    
    def get_files(self):
        """ this should call an adapter """
        
        def fdict(rfile):
            df = rfile['dataFile']
            keys = ['contentType', 'filename', 'filesize', 'id',
            'originalFormatLabel', 'description']
            
            dd = {k: df.get(k, '') for k in keys}

            dd['url'] = u"{}/api/access/datafile/{}".format(self.base_url, dd['id'])
            if dd['originalFormatLabel'] == 'UNKNOWN':
                dd['originalFormatLabel'] = ''
            dd['filesize'] = size(int(dd['filesize']))
            
            return dd
            
        doi = self.context.dataset
        if not doi.startswith('doi:'):
            doi = 'doi:{}'.format(doi)
        url = '{}/api/datasets/:persistentId/'.format(self.base_url)
        
        try:
            req = requests.get(url, params={'persistentId': doi}, timeout=1)
        except requests.exceptions.RequestException as e:
            self.logger.error(e)
            return []
        except requests.exceptions.Timeout as e:
            self.logger.error(e)
            return []
        
        if req.status_code == 200:
            resp_data = req.json()
            files = resp_data['data']['latestVersion']['files']
            return map(fdict, files)
        else:
            msg = req.json()['message']
            e = u"[{}]: {}".format(req.status_code, msg)
            self.logger.error(e)
            return []









        
