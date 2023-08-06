import os
import requests

class IS_handler(object):

    def __init__(self):
        self.enabled = True
        self.name = 'The Archive.is'
        self.api_required = False 

    def push(self, uri_org, p_args=[]):

        from_heroku = False
        if 'from_heroku' in p_args:
            from_heroku = p_args['from_heroku']

        if not from_heroku:
            try:
                 if os.environ['PYTHONHOME'].startswith('/app/.heroku/python'):
                    from_heroku = True
            except:
                pass;

        archiveTodaySubmitId = ""

        # get the newest submitid required to push pages
        
        if from_heroku:
            archive_is_domains = ['178.62.195.5', '151.236.217.7']
        else:
            # iterate over those domains til one succeeds or no one
            archive_is_domains = ['archive.li', 'archive.vn','archive.fo', 'archive.md', 'archive.ph', 'archive.today', 'archive.is']

        for host in archive_is_domains:

            try:

                msg = ''

                archiveTodayUserAgent = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64)" , "host": host}
                rid = requests.get('https://'+host+'/',timeout=120, allow_redirects=True, headers=archiveTodayUserAgent)

                rid.raise_for_status()
                htmldata = str(rid.content)

                try:
                    archiveTodaySubmitId = htmldata.split('name="submitid',1)[1].split('value="',1)[1].split('"',1)[0]
                except: 
                    msg = "IndexError (" + self.name+ "): unable to extract 'submitid' "
                    raise  

                # push to the archive
                r = requests.post('https://'+host+'/submit/', timeout=120,
                                                                 data={"anyway":"1" , "url":uri_org, "submitid":archiveTodaySubmitId},
                                                                 allow_redirects=True,
                                                                 headers=archiveTodayUserAgent)          
                r.raise_for_status()
                # extract the link to the archived copy
                if 'Refresh' in r.headers:
                    try:
                        return str(r.headers['Refresh']).split(';url=')[1]
                    except:
                       msg = "IndexError (" + self.name+ "): unable to extract a URL to the archived version from HTTP Refresh header ("+str(r.headers['Refresh'])+")"
                       raise 
                else:
                    if 'Location' in r.headers:
                        return r.headers['Location']
                    else:
                        for r2 in r.history:
                            if 'Location' in r2.headers:
                                return r2.headers['Location']
                msg = "Error ("+self.name+ "): No HTTP Location/Refresh header is returned in the response" 
            except Exception as e:
                if msg == '':
                    msg = "Error (" + self.name+ "): " + str(e)
                    pass;
        return msg
