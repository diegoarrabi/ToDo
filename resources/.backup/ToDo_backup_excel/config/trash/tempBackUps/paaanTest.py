
import pandas as pd
import numpy as np

def getDF():
    list1=['EVALS - HOSPPEDS X5', '11/03', 'TODAY!']
    list2=['FM - DIRECT OBSERVATION OF HISTORY', '11/03', 'TODAY!']
    list3=['FM - Focused Note', '11/08', '5 Days']
    list4=['FM - Oral Presentation', '11/09', '6 Days']
    list5=['Story', '11/13', '10 Days']
    list6=['FM - Physical Exam (Only 1)', '11/13', '10 Days']

    masterList = []
    masterList.append(list1)
    masterList.append(list2)
    masterList.append(list3)
    masterList.append(list4)
    masterList.append(list5)
    masterList.append(list6)

    df = pd.DataFrame(masterList, columns= ["assignment", "due date", "days"])
    return df

def dfdark(df):

    propsHead = 'font-family: SF Pro Display; color: #FFFFFF; font-size:1.2em;'
    propsBody = 'font-family: SF Pro Rounded; color: black; font-size:1em;'

    styleList = [{"selector":"th.col_heading",
            "props": f'background-color:grey; text-align: left;{propsHead}'},
        {"selector":"tbody tr:nth-child(even)",
            "props": f"background-color: lightgrey; text-align: left;{propsBody}"},
        {"selector":"tbody tr:nth-child(odd)",
            "props": f"background-color: white; text-align: left;{propsBody}"},
        {"selector":"td.col1",
            "props": "text-align: center"},
        {"selector":"td.col2",
            "props": "text-align: center"},
        {"selector":"th.col2",
            "props": "text-align: center"},
            ]
    
    lengthofToday = len(df[df['days'].str.contains("!")])
    if lengthofToday > 0:
        for i in range(lengthofToday):
            tempToday = {}
            dict_keys = ['selector', 'props']
            tempToday[dict_keys[0]] = ""
            tempToday[dict_keys[1]] = 'color: red'
            tempToday['selector'] = (f"tbody tr:nth-child({i+1})")
            styleList.append(tempToday)
            del tempToday

    for i in styleList:
        print(i)

    
            

    

    
trial = getDF()

dfdark(trial)