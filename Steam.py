#Import necessary modules
import requests
import json
import csv
import bokeh
import pandas as pd
from bokeh.charts import Bar, output_file, save, Donut

#Ask the user what type of information they want
style = input("What do you want to request:  \n1: Achievements  \n2: Playtime in Recent Games  \n3: Global Achievement Stats ")
#Assign variable for the base url
base_url = 'http://api.steampowered.com/'
key = '8E889E83A42C15D13E11EA54405CF63A'

#Empty lists for storing
name_list = []
done_list = []
title_list = []
play_list = []
name2_list = []
percentage_list = []

#Function for getting completed achievements
def achievements():
    
    #Ask uer for the AppID and set up the base URL
    appid = input("Enter the app ID of the game: ")
    base_url = "http://api.steampowered.com/"
    
    #Construct the URL based on info given
    url = base_url + 'ISteamUserStats/GetPlayerAchievements/v0001/?appid=' + appid + '&key=' + key + '&steamid=' + SteamID
    r = requests.get(url)
    steam = r.json()
    
    #Append the lists above and prrp for CSV writing
    for n in steam['playerstats']['achievements']:
        name = n["apiname"]
        done = n["achieved"]     
        name_list.append(name)
        done_list.append(done)
    
    #Open CSV
    csvfile = open("Steam.csv", "w")
    csvwriter = csv.writer(csvfile, delimiter = ",")

    # Establish header row.
    csvwriter.writerow(["Name", "Achieved"])
    
    #Write the CSV file
    rows = list(zip(name_list, done_list))
    for row in rows:
        csvwriter.writerow(row)
    csvfile.close()
    
    #Give csv file for bokeh to read
    steamb = pd.read_csv("Steam.csv")

    #Create a bar plot using bokeh
    bar = Bar(steamb, "Name", legend=False, values="Achieved", title="Achievements (Zoom is required to see all achievement names for some games) ", color='#000000', xlabel="Console Name of the Achievement", ylabel= "Achieved (Yes if bar is present")

    #Create graph file
    output_file("bar.html")
    save(bar)
    print("complete")

#Funtion to find a player game time for the recents games they played
def time():
    #Construct the URL and get the JSON file
    base_url = "http://api.steampowered.com/"               
    url = base_url + 'IPlayerService/GetRecentlyPlayedGames/v0001/?key=' + key + '&steamid=' + SteamID +'&format=json'
    r = requests.get(url)
    game = r.json()
    
    #Creates the CSV file that is going to be plotted
    for n in game["response"]["games"]:
        title = n["name"]
        play = n["playtime_forever"]
        title_list.append(title)
        play_list.append(play)    
    
    #Open and prep CSV for writing     
    csvfile = open("playtimebroken.csv", "w")
    csvwriter = csv.writer(csvfile, delimiter = ",")

    # Establish header row.
    csvwriter.writerow(["name", "playtime_forever"])
    
    #Write CSV
    rows = zip(title_list, play_list)
    for row in rows:
        csvwriter.writerow(row)

    #Close the file
    csvfile.close()
    
    #The code below switches the : to a - in game titles to avoid probelms with bokeh. Without this change games with : in them will not be displayed on the graph
    input_file = open('playtimebroken.csv', 'r')
    output = open('playtimefixed.csv', 'w')
    data = csv.reader(input_file)
    writer = csv.writer(output)
    specials = ':'

    for line in data:
        line = [value.replace(specials, ' -') for value in line]
        writer.writerow(line)
    
    #Closes the files
    input_file.close()
    output.close()
    
    #Variable for the csv file to be plotted
    steamb = pd.read_csv("playtimefixed.csv")

    #Create a bar plot using bokeh
    bar = Bar(steamb, "name", legend=False, values="playtime_forever", title="Playtime of Most Recent Games", bar_width=0.2, color='#2171b5', xlabel = "Name", ylabel = "Playtime (minutes)")

    #Create graph file
    output_file("bartime.html")
    save(bar)
    print("complete")

#Function for Global Percentage
def percent():
    
    #Ask user
    appid = input("Enter the app ID of the game: ")
    base_url = "http://api.steampowered.com/"               
    url = base_url + 'ISteamUserStats/GetGlobalAchievementPercentagesForApp/v0002/?gameid=' + appid +'&format=json'
    r = requests.get(url)
    game = r.json()
    
    #Creates the CSV file that is going to be plotted
    for n in game["achievementpercentages"]["achievements"]:
        name2 = n["name"]
        percentage = n["percent"]
        name2_list.append(name2)
        percentage_list.append(percentage)    
        
    csvfile = open("Percent.csv", "w")
    csvwriter = csv.writer(csvfile, delimiter = ",")

    # Establish header row.
    csvwriter.writerow(["Name", "Percent"])
    
    #Write the CSV file
    rows = list(zip(name2_list, percentage_list))
    for row in rows:
        csvwriter.writerow(row)
    csvfile.close()
    
    #Create bar chart
    percentbar = pd.read_csv("Percent.csv")
    barpercent = Bar(percentbar, "Name", legend=False, values="Percent", title="Global Percentages of achievements", bar_width=0.5, color='#268999', xlabel = "Name", ylabel = "Percentage of User with Achievement")
    output_file("barpercent.html")
    save(barpercent)
    print("complete")
    
#If else staments to determine what information the user is looking for based on input
if style.lower() == "1":
    SteamID = input("What is your Steam ID: ")      #Required SteamID to see the stats for the user
    achievements()
    
elif style.lower() == "2":
    SteamID = input("What is your Steam ID: ")      #Required SteamID to see the stats for the user
    time()
    
elif style.lower() == "3":
    percent()
    
else:
    print("Enter the number not the text")
    
input("Press any key to end the code...")           #Press a key to end the code


#Use these to test if you don't have Steam
#Tinhorn's Steam ID: 76561198061868064
#COD Black ops 3 AppID: 311210
#key 8E889E83A42C15D13E11EA544