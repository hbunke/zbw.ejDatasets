from Products.Five.browser import BrowserView
# from ckanapi import RemoteCKAN
# import random
import requests
from hurry.filesize import size
import logging
from Products.ATContentTypes.utils import DT2dt
import datetime
# from collections import namedtuple
from toolz.dicttoolz import keyfilter


def dataset_pid(paper):
    """
    necessary since Dataverse switched to DOI (2013-10-01)
    """

    def format_doi(doi):
        if not doi.startswith('doi:'):
            doi = 'doi:{}'.format(doi)
        return doi

    def format_hdl(hdl):
        return "hdl:1902.1/{}".format(hdl)
    
    pid = paper.getDataset()
    switch_date = datetime.datetime(2013, 9, 30)
    paper_date = DT2dt(paper.created()).replace(tzinfo=None)
    if switch_date > paper_date:
        return format_hdl(pid)
    return format_doi(pid)


class View(BrowserView):
    """
    views and methods for dataset of article
    """
    
    def ckan_files(self):
        """
        get dataset files from CKAN (Journal Data Archive)
        """
        pass

    def dataverse_files(self):
        """
        get dataset files from Dataverse (Harvard)
        """
        base_url = "https://dataverse.harvard.edu"
        logger = logging.getLogger('Dataverse')
        url = '{}/api/datasets/:persistentId/'.format(base_url)
        pid = dataset_pid(self.context)

        def fdict(rfile):
            d = rfile['dataFile']
            keys = ['originalFormatLabel', 'contentType', 'filename',
                    'filesize', 'id', 'description']
            df = keyfilter(lambda k: k in keys, d)
            df.update({'url': u"{}/api/access/datafile/{}".format(base_url,
                d['id']), 'filesize': size(int(d['filesize']))})
            return df
            
        try:
            # XXX: timeout should be <=1 for production!
            req = requests.get(url, params={'persistentId': pid}, timeout=5)
        except requests.exceptions.RequestException as e:
            logger.error(e)
            return
        except requests.exceptions.Timeout as e:
            logger.error(e)
            return
        
        if req.status_code == 200:
            resp_data = req.json()
            files = resp_data['data']['latestVersion']['files']
            return map(fdict, files)
        else:
            msg = req.json()['message']
            e = u"[{}]: {}".format(req.status_code, msg)
            logger.error(e)
            return
    
    def dataset_url(self):
        """
        construct dataset URL (handle.net or doi.org)
        """
        pid_type, pid = dataset_pid(self.context).split(':')
        return {'doi': "http://dx.doi.org/{}".format(pid),
                'hdl': "http://hdl.handle.net/{}".format(pid)}[pid_type]


# class Ckan(BrowserView):
    # """
    # not in use, yet
    # """

# # for testing only! edawax demo server, fixed ids
    # url = "http://134.245.93.80:5000"
    # demo = RemoteCKAN(url)
    # ids = ["is-a-firm-a-firm-a-stackelberg-experiment",
        # "title-of-your-article-replication-data"]
    # id = random.choice(ids)
    # pkg = demo.action.package_show(id=id)
    # resources = pkg['resources']


    # def get_dataset(self):
        # """
        # first test
        # """
        # evil_html = u"<html><head><title>Test</title></head><body>"
        # evil_html += u"<h2><a href='{}'>{}</a></h2>".format(url + "/dataset/" +
                # id, pkg['title'])
        # evil_html += u"<h3>Resources</h3>"
        # for res in resources:
            # evil_html += u"<p><a href='{}'><br />{}</p>{}".format(res['url'],
                    # res['name'], res['description'])
        # evil_html += u"</body></html>"

        # return evil_html

    # def resources(self):
        # return resources
        









        
