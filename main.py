#seek.com
#------------------------------------------------------------------------------------------------------------#
import requests
from lxml import html
import config
import re
import math
#------------------------------------------------------------------------------------------------------------#
'''
Pull all the information
input required: session id, where, what and page no.
'''
def _extract_info(*args):
    session_id = args[0]
    where = args[1]
    what = args[2]
    page = args[3]
    
    payload = {
        'siteKey': 'AU-Main',
        'sourcesystem': 'houston',
        'userid': session_id,
        'usersessionid': session_id,
        'eventCaptureSessionId': session_id,
        'where': where,
        'page': str(page),
        'seekSelectAllPages': 'true',
        'keywords': what,
        'include': 'seodata',
        'isDesktop': 'true'
        }
    res = requests.get(config.search, headers = config.header, params = payload)    
    output = res.json()
    data = output['data']
    pat = r'\d{4}[-]\d{2}[-]\d{2}'
    for results in data:   
        config.row += 1     
        solMetadata = results['solMetadata']
        jobid = solMetadata['jobId']
        requestToken = solMetadata['searchRequestToken']
        type_ = "standard"
        url = config.job + jobid
        payload = {
                'searchrequesttoken': requestToken,
                'type': type_
            }
        xResponse = requests.get(url, headers = config.header, params = payload)
        pat1 = r'"companyOverallRating"[:](\d[.]?\d+?)'
        rating = re.findall(pat1, xResponse.text)
        companyRating = rating[0] if rating != [] else None
        tree = html.fromstring(xResponse.text)
        job_apply = "//section[@aria-labelledby='jobApplyHeader']/div/div[1]/div/span/div/div/div/div/a"
        job = tree.xpath(job_apply)[0].get("href")
        # gathered_data.append({
        #     'Title': results['title'],
        #     'Company Name': results['advertiser']['description'],
        #     'Date': re.search(pat, results['listingDate'])[0],
        #     'Area': results['area'],
        #     'work type': results['workType'],
        #     'Rating': companyRating,
        #     'Apply': config.url + job
        #     })
        area = results['area'] if results['area'] != '' else results['location']
        cols = [results['title'], results['advertiser']['description'], re.search(pat, results['listingDate'])[0],
        area, results['workType'], companyRating, config.url + job]
        config.worksheet.write_row('A' + str(config.row), cols)
    
if __name__ == "__main__":
    what = input("Enter Position: ")
    where = input("Enter location:")
    session = requests.session()
    response = session.get(config.url, headers = config.header)
    cookies = response.cookies.get_dict()
    session_id = cookies['JobseekerSessionId']    
    
    payload = {
        'siteKey': 'AU-Main',
        'sourcesystem': 'houston',
        'userid': session_id,
        'usersessionid': session_id,
        'eventCaptureSessionId': session_id,
        'where': where,
        'page': '1',
        'seekSelectAllPages': 'true',
        'keywords': what,
        'include': 'seodata',
        'isDesktop': 'true'
        }
    res = session.get(config.search, headers = config.header, params = payload)    
    output = res.json()
    totalCount = output['totalCount']
    gathered_data = []
    
    if totalCount > 0:        
        nCount = 20
        totalpage = math.ceil(totalCount/nCount)    
        for i in range(totalpage):
            print("Processing page {}".format(i+1))
            _extract_info(session_id, where, what, i + 1)
            
        
    else:
        print("Search results not found.")
    config.workbook.close()


    