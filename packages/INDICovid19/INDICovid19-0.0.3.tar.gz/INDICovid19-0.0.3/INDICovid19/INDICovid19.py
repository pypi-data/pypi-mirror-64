"""
API call python package for Covid-19 dataset available in near india real time <code for cause>
@arghadeep.chaudhury@gmail.com
Date: 30-03-2020
Source : https://github.com/amodm/api-covid19-in
"""
import requests
import json
import pandas as pd
from json2xml import json2xml
class indiaGovCoronaAPI:
    def __init__(self):
        self.OCasecounts='https://api.rootnet.in/covid19-in/stats/latest'
        self.OcaseHist='https://api.rootnet.in/covid19-in/stats/history'
        self.OTestStats='https://api.rootnet.in/covid19-in/stats/testing/latest'
        self.OTHist='https://api.rootnet.in/covid19-in/stats/testing/history'
        self.OTStats='https://api.rootnet.in/covid19-in/stats/testing/raw'
        self.OTHostBed='https://api.rootnet.in/covid19-in/stats/hospitals'
        self.Contacts='https://api.rootnet.in/covid19-in/contacts'
        self.NotNAdvs='https://api.rootnet.in/covid19-in/notifications'
        self.unoffsrc='https://api.rootnet.in/covid19-in/unofficial/sources'
        self.unofftrackdata='https://api.rootnet.in/covid19-in/unofficial/covid19india.org'
        self.unoffstatedata='https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise'
        self.unoffstatedatahist='https://api.rootnet.in/covid19-in/unofficial/covid19india.org/statewise/history'
        self.unofftravelhist='https://api.rootnet.in/covid19-in/unofficial/covid19india.org/travelhistory'
AllApi=indiaGovCoronaAPI()
def TotalCaseCount(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.OCasecounts)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['summary']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['summary'],index=[0])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['summary']).to_xml()
    else:
        return 'Param missing'
def TotalStateCount(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.OCasecounts)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['regional']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['regional'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['regional']).to_xml()
    else:
        return 'Param missing'
def TotalStateCountHist(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.OcaseHist)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']).to_xml()
    else:
        return 'Param missing'
def TotalTestCount(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.OTestStats)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data'],index=[0])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']).to_xml()
    else:
        return 'Param missing'
def TotalTestCountHist(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.OTHist)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']).to_xml()
    else:
        return 'Param missing'
def TotalHospitalCount(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.OTHostBed)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['summary']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['summary'],index=[0])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['summary']).to_xml()
    else:
        return 'Param missing'
def TotalHospitalCountState(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.OTHostBed)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['regional']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['regional'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['regional']).to_xml()
    else:
        return 'Param missing'
def StatewiseContact(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.Contacts)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['contacts']['regional']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['contacts']['regional'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['contacts']['regional']).to_xml()
    else:
        return 'Param missing'
        
def DetailPatient(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.unofftrackdata)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['rawPatientData']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['rawPatientData'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['rawPatientData']).to_xml()
    else:
        return 'Param missing'
def UnoffStateData(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.unoffstatedata)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['statewise']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['statewise'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['statewise']).to_xml()
    else:
        return 'Param missing'
def StateDataHist(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.unoffstatedatahist)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['history']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['history'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['history']).to_xml()
    else:
        return 'Param missing'
def TravelHist(oparam='JSON'):
    TotalCaseCount=requests.get(AllApi.unofftravelhist)
    TotalCaseCount=json.loads(TotalCaseCount.content)
    if oparam=='JSON':
        return TotalCaseCount['data']['travel_history']
    elif oparam=='DF':
        return pd.DataFrame(TotalCaseCount['data']['travel_history'])
    elif oparam=='XML':
        return json2xml.Json2xml(TotalCaseCount['data']['travel_history']).to_xml()
    else:
        return 'Param missing'