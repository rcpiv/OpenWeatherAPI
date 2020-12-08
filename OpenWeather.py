key = '5b165ce4e5ec30e63777ebca46447180' # Set API key

import requests
import statistics as stat #Load required packages
import csv

cities = {'headers':['City','Min 1','Max 1','Min 2','Max 2','Min 3','Max 3',\
                             'Min 4', 'Max 4','Min 5','Max 5','Min Avg','Max Avg']}

out = open('open-weather.csv', 'w', newline='', encoding='latin')
writer = csv.writer(out)
writer.writerow(cities['headers'])
    
locs = [['Anchorage','USA'],['Buenos Aires','Argentina'],\
       ['Sao Jose dos Campos','Brazil'],['San Jose','Costa Rica'],\
       ['Nanaimo','Canada'],['Ningbo','China'],['Giza','Egypt'],['Mannheim','Germany'],\
       ['Hyderabad','India'],['Tehran','Iran'],['Bishkek','Kyrgyzstan'],\
       ['Riga','Latvia'],['Quetta','Pakistan'],['Warsaw','Poland'],\
       ['Dhahran','Saudia Arabia'],['Madrid','Spain'],['Oldham','England']]

in_month = {'01':31,'02':28,'03':31,'04':30,'05':31,'06':30,'07':31,'08':31,\
           '09':30,'10':31,'11':30,'12':31}    
    
for loc in locs:
    URL = 'https://api.openweathermap.org/data/2.5/forecast?'
    URL = URL + 'q=' + loc[0] + ',' + loc[1] + '&appid=' + key + '&units=metric'
    
    response = requests.get( URL ) 
    
    data = response.json() 
    
    min_temps = {1:[],2:[],3:[],4:[],5:[]} # Dictionary for minimum temperatures
    max_temps = {1:[],2:[],3:[],4:[],5:[]} # Dictionary for maximum temperatures
    mins = [] # List of average minimum temperatures
    maxs = [] # List of average maximum temperatures
    
    today = int(data['list'][0]['dt_txt'][8:10]) #Finds todays date
    month = data['list'][0]['dt_txt'][8:10]
    
    if data['list'][0]['dt_txt'][11:19] != '03:00:00':
        day1 = (today+1) % in_month[data['list'][0]['dt_txt'][5:7]]
    else:
        day1 = today
    if day1 == 0:
        day1 = in_month[data['list'][0]['dt_txt'][5:7]]
    day2 = (day1+1) % in_month[data['list'][0]['dt_txt'][5:7]]
    if day2 == 0:
        day2 = in_month[data['list'][0]['dt_txt'][5:7]]
    day3 = (day2+1) % in_month[data['list'][0]['dt_txt'][5:7]]
    if day3 == 0:
        day3 = in_month[data['list'][0]['dt_txt'][5:7]]
    day4 = (day3+1) % in_month[data['list'][0]['dt_txt'][5:7]]
    if day4 == 0:
        day4 = in_month[data['list'][0]['dt_txt'][5:7]]
    day5 = (day4+1) % in_month[data['list'][0]['dt_txt'][5:7]]
    if day5 == 0:
        day5 = in_month[data['list'][0]['dt_txt'][5:7]]
        
    
    day = 0
    
    for run in range(0,len(data['list'])): # Loop to assign temperature data to dictionaries
        day = int(data['list'][run]['dt_txt'][8:10])
        if day == day1:
            min_temps[1].append(data['list'][run]['main']['temp_min'])
            max_temps[1].append(data['list'][run]['main']['temp_max'])
        elif day == day2:
            min_temps[2].append(data['list'][run]['main']['temp_min'])
            max_temps[2].append(data['list'][run]['main']['temp_max'])
        elif day == day3:
            min_temps[3].append(data['list'][run]['main']['temp_min'])
            max_temps[3].append(data['list'][run]['main']['temp_max'])
        elif day == day4:
            min_temps[4].append(data['list'][run]['main']['temp_min'])
            max_temps[4].append(data['list'][run]['main']['temp_max'])
        elif day == day5:
            min_temps[5].append(data['list'][run]['main']['temp_min'])
            max_temps[5].append(data['list'][run]['main']['temp_max'])
    
    for i in range(1,6):
        maxs.append(max(max_temps[i])) 
        mins.append(min(min_temps[i])) 
        
        max_avg = stat.mean(maxs) # Finds mean of all maximum temps
        min_avg = stat.mean(mins) # Finds mean of all minimum temps
    
    loc2 = loc[0] + ', ' + loc[1]
    
    cities[loc[0]] = [loc2,mins[0],maxs[0],mins[1],maxs[1],mins[2],maxs[2],\
                      mins[3],maxs[3],mins[4],maxs[4], "{:.2f}".format(min_avg), "{:.2f}".format(max_avg)]
    writer.writerow(cities[loc[0]])

out.close()