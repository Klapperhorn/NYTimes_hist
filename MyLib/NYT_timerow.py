import datetime as dt

def current_time():
    from datetime import datetime
    print("Current Time = ", datetime.now().strftime("%H:%M:%S"))
    return

def NYT_api_key(keyfile="2022-05-24_NYtimes_key.yaml"):
    import yaml
    with open(keyfile) as file:
        keys = yaml.load(file, Loader=yaml.FullLoader)
        return keys["NYtimes"]['key']
    

def Heute():
    return dt.datetime.now().strftime('%Y-%m-%d')

def D(w):
    from pandas import options
    options.display.max_colwidth = w
    return f"display colwidth set to: {w}"

def normalize(x): 
    return (x-x.min())/(x.max()-x.min()) 

def openFile(filename):
    import json
    with open(filename) as json_file:
        data = json.load(json_file)
    return data

def defaultconverter(o):
    if isinstance(o, dt.datetime):
        return o.__str__()
        
def writeFile(filename, data):
    import json
    with open(f"{filename}.json", 'w') as fp:
        json.dump(data,fp, default = defaultconverter)
    return f"file written to: {filename}"



def runSerach(SuchName, results=2,years=(2020,2023),API_key=NYT_api_key()):
    current_time()
    from pynytimes import NYTAPI
   
    
    nyt=NYTAPI(API_key, parse_dates=True)
    
    query=SuchName.strip()
    import datetime as dt
    
    begin=dt.datetime(years[0], 1, 1)
    end=dt.datetime(years[1], 12, 31)
    if end>dt.datetime.now():
        end=dt.datetime.now()
    print(f"{SuchName} - from {begin} till {end}.")
    
    options={"sort": "newest","sources": ["New York Times"]}
    #"AP","Reuters","International Herald Tribune"
    
    articles = nyt.article_search(query=query,results=results,dates={"begin": begin,"end": end}, options = options)
    
    SuchName = ''.join(filter(str.isalnum, SuchName))
    filename=Heute()+"_NYtimes_"+SuchName.replace(" ","_")
    
    print(SuchName,len(articles))
    
    writeFile(filename,articles)
    return articles