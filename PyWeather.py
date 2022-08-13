#PyWeather V2.03 by Jarrett McAlicher - 7/29/2018
#Git
#2.03 5/29/2021 Fix "None type error"
ver=2.03

import sys
import xml.etree.ElementTree as et

if sys.version_info[0]==2:
    print('Must use Python 3. Does not work with Python2.')
else:
    import urllib.request
    def weburl(url):
        file=urllib.request.urlopen(url)
        return file
    
#setup the Paramaters     
parms=sys.argv

if len(parms)==3:
    job=parms[2]
elif len(parms)==2:
    job='current'
else:
    print('\nMust Specify Paramaters: Zipcode and Task (current or forecast)\n')
    quit()

zip=parms[1]
daypart=''
verbose=False

# Define Functions 
def k2f(temp):
    f=round((float(temp)*1.8)-459.67,1)
    f=str(f)
    return f

def get_today(day):
    if day>8:
        daytext="DAY ERROR"
    else:
        daylist=["None","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        daytext=daylist[day]
    return daytext


#Get Current Weather
def get_weather(zip):
    zip=str(zip)
    apikey = "2aa44873ae871775ddd135a80a6adc0d"
    url="http://api.openweathermap.org/data/2.5/weather?zip="+zip+",us&&mode=xml&APPID="+apikey
    
    if verbose==True:
        print (url)
    
    file = weburl(url)
    weatherdata= file.read()
    file.close()
    tree=et.fromstring(weatherdata)

    if verbose==True:
        print("Printing Tree:")
        print(tree)
        print(tree[0])
        print(tree[1])
        print(tree[2])
        print(tree[3])
        print(tree[4])
        print(tree[5])
        print(tree[6])
        print(tree[7])
        print(tree[8])
        print(tree[9])
        print(tree[10])
        
    temperature=k2f(tree[1].get('value'))
    precipitation=tree[8].get('value')
    if tree[8].get('value')!=None:
        print (f'\n Current Temperature is {temperature} degrees, with {precipitation}.\n')   
    else:
        print(f'\n Current Temperature is {temperature} degrees, with no precipitation.\n') 

#get forecast 
def get_forecast(zip,debug=False):
    zip=str(zip)
    apikey = "2aa44873ae871775ddd135a80a6adc0d"
    url="http://api.openweathermap.org/data/2.5/forecast?zip="+zip+",us&&mode=xml&APPID="+apikey
    file = weburl(url)
    weatherdata= file.read()
    file.close()
    root=et.fromstring(weatherdata)
    if debug==True:
        print('\n')
        print(weatherdata)    
    
    # more setup for this function
    from datetime import date
    from datetime import time
    from datetime import datetime
    get_step_number=[0,3,6,9,12,15,18,21]
    current=root[4][0].attrib['from']
    dcurrent=datetime.strptime(current,'%Y-%m-%dT%H:%M:%S') 
    hr=dcurrent.hour 
    starthour=dcurrent.hour
    #set daynumber
    if starthour==0:
        daynumber=1
    else:
        daynumber=0
    #set daypart 
    def daypart(hr):
        if hr==0 or hr==3:
            daypart='morning'
        elif hr==6 or hr==9 or hr==12 or hr==15:
            daypart='day'
        elif hr==18 or hr==21:
            daypart='evening'
        else:
            daypart='daypart error'
        return daypart
    
    #set iteration
    xml_step=0 #init position in xml data
    step_number=get_step_number.index(starthour)
    if debug==True: print('We are staring with step #'+str(step_number))
    while daynumber <=3: #Change the number here for more days.
        temp=[]
        icon=''
        low_temp=0
        high_temp=0
        mintemp=[]
        maxtemp=[]
        dcurrent=''
        hr=''
        cchr=''  
        if daynumber>0: step_number=0
        #Iterate thru forecast
        while step_number<=7:
            #pull date info
            xcurrent=root[4][xml_step].attrib['from']
            wcurrent=datetime.strptime(xcurrent,'%Y-%m-%dT%H:%M:%S') 
            tcurrent=wcurrent.strftime("%u") 
            dcurrent=get_today(int(tcurrent))
            thr=int(wcurrent.strftime("%H"))
            cchr=daypart(thr)
            if daynumber==0: dname='Today'
            elif daynumber==1: dname='Tomorrow'
            else: dname=dcurrent            
            #create temp list
            #2.03 updated to #5 (need to update to a better method of pulling this data)
            mintemp.append(root[4][xml_step][5].get('min'))
            maxtemp.append(root[4][xml_step][5].get('max'))
            icon=root[4][xml_step][0].get('name')
            try:
                low_temp=k2f(float(min(mintemp)))
            except TypeError:
                if debug==True: print(mintemp)
            try:
                high_temp=k2f(float(max(maxtemp)))
            except TypeError:
                if debug==True: print(maxtemp)  
                      
            if debug==True:
                print('\n-----------------------------------------')
                print('step #'+str(step_number) +'| Day#'+str(daynumber)+' | xml# '+str(xml_step)) 
                print(str(mintemp) +' '+str(maxtemp))
                print(icon)
                print(wcurrent)
                print('tcurrent day '+str(tcurrent))
                print('dcurrent '+dcurrent)
                print('current hour '+str(thr))
                print('current daypart '+cchr)
                print(dname)
                print('-----------------------------------------\n')
                
            if step_number==1:
                print (' ')
                if daynumber<=3: print(wcurrent.strftime("%A %B %e, %G"))                
                print(dname +' '+cchr+' the low temp will be '+str(low_temp)+' with '+icon)
                mintemp=[]
                maxtemp=[]
                
            elif step_number in(5,7):               
                print(dname +' '+cchr+' the high temp will be '+str(high_temp)+' with '+icon)
                mintemp=[]
                maxtemp=[]                                              
         
            xml_step+=1
            step_number+=1
        temp=[]
        mintemp=[]
        maxtemp=[]
        daynumber+=1
    
#Main Funciton
def main(zip,job):
    print ('\nPyWeather '+str(ver)+' | weather data provided by OpenWeatherMap.org')
    if job=='forecast':
        get_forecast(zip)
        print('\n')
    elif job=='debug':
        job='forecast'
        debug=True
        get_forecast(zip,debug)
    else:
        get_weather(zip)

#Running the Program
if __name__=="__main__":
    main(zip,job)
