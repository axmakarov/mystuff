# -*- coding: utf-8 -*-

# pip install googleads

import json
import logging
import sys
from googleads import adwords
from googleads import oauth2


logging.basicConfig(level=logging.INFO)
logging.getLogger('suds.transport').setLevel(logging.DEBUG)


# OAuth2 credential information. In a real application, you'd probably be
# pulling these values from a credential storage.
CLIENT_ID = '187376050914-b95hgu77nv4c1ld18gcj1e93nlfes82s.apps.googleusercontent.com'
CLIENT_SECRET = '4l07Oasm0snptfzRLbpw9Ihp'
REFRESH_TOKEN = '1/fON1tNVljx1X9YoOqlMUaFEfeDAAJwPqjdDgOZ8B_vpIgOrJDtdun6zK6XiATCKT'

# AdWords API information.
DEVELOPER_TOKEN = 'DBIbVe5MLt76TKcMgOjoiw'
USER_AGENT = 'test'
CLIENT_CUSTOMER_ID = '6754700755' # main customer id, do not delete!!!
#CLIENT_CUSTOMER_ID = '5185208581'

oauth2_client = oauth2.GoogleRefreshTokenClient(CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN)
adwords_client = adwords.AdWordsClient(DEVELOPER_TOKEN, oauth2_client, USER_AGENT, CLIENT_CUSTOMER_ID)
report_downloader = adwords_client.GetReportDownloader(version='v201603')



# return dictionary (domain) -> (customerId)
def get_client_map():
    # Initialize appropriate service.
    managed_customer_service = adwords_client.GetService('ManagedCustomerService', version='v201603')

    # Construct selector to get all accounts.
    selector = {
        'fields': ['CustomerId', 'Name'],
        'paging': {
            'startIndex': '0',
            'numberResults': '1000'
        }
    }
    accounts = {}

    # Get serviced account graph.
    page = managed_customer_service.get(selector)
    if 'entries' in page and page['entries']:
        # Map from customerID to account.
        for account in page['entries']:
            accounts[account['name']] = account['customerId']

    return accounts


# download report
def download_report(report, filename):
    # You can provide a file object to write the output to. For this demonstration
    # we use sys.stdout to write the report to the screen.
    body = report_downloader.DownloadReportAsString(report, skip_report_header=False, skip_column_header=False, skip_report_summary=False, include_zero_impressions=False)
    with open(filename, 'w') as text_file:
        text_file.write(body.encode('utf8'))




# Create report definition.
report = {
    'reportName': 'Last 7 days CRITERIA_PERFORMANCE_REPORT',
    'dateRangeType': 'LAST_7_DAYS',
    'reportType': 'CRITERIA_PERFORMANCE_REPORT',
    'downloadFormat': 'CSV',
    'selector': {
        'fields': ['CampaignId', 'AdGroupId', 'Id', 'CriteriaType','Criteria', 'FinalUrls', 'Impressions', 'Clicks', 'Cost']
    }
}

#download_report(report, 'report.csv')
#print json.dumps(get_client_map())