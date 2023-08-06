# API call for the Indian Covid-19 cases real time using python lib for data scientist, ml engineer,data enthusiast and  researchers 

This is a python package having multiple utilities. 
[Github-flavored Markdown](https://github.com/deepstartup/INDICovid19/)

1.INDICovid19.TotalCaseCount:Official data Case counts Total  
2.INDICovid19.TotalStateCount: Official data Case counts Total Statewise
3.INDICovid19.TotalStateCountHist: Official data Case counts Total Statewise History Timeseries
4.INDICovid19.TotalTestCount: Official data Testing stats
5.INDICovid19.TotalTestCountHist: Official data Testing stats History Timeseries
6.INDICovid19.TotalHospitalCount: Official data  Hospitals & bed stats Overall
7.INDICovid19.TotalHospitalCountState: Official data  Hospitals & bed stats Statewise
8.INDICovid19.StatewiseContact : Official data Contact & helpline Statewise
9.INDICovid19.DetailPatient : Unofficial patient tracing data and Details
10.INDICovid19.UnoffStateData : Unofficial statewise stats
11.INDICovid19.StateDataHist : Unofficial statewise stats History
12.INDICovid19.TravelHist : Unofficial patient travel history

**Params (Default return in json format), DF = Returns in DataFrame, XML = Returns in XML for format
#Data Returns in JSON format:
Example : 
import INDICovid19
pyjson=INDICovid19.TotalCaseCount() #return json
pydf=INDICovid19.TotalCaseCount('DF') #return DataFrame
pyxml=INDICovid19.TotalCaseCount('XML') #return XML

#Credit
@covid19india.org (https://github.com/amodm/api-covid19-in)