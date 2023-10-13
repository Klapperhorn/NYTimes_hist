import datetime as dt
import pandas as pd

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
    filename=filename.split(".json")[0]
    with open(f"{filename}.json", 'w') as fp:
        json.dump(data,fp, default = defaultconverter)
    return f"file written to: {filename}"

def name_file(SuchName,Heute=Heute()):
    filename=Heute+"_NYtimes_"+SuchName.strip('"').replace(" ","_")+".json"
    return filename

def runSerach(SuchName, results=2,years=(2020,2023),API_key=NYT_api_key()):
    current_time()
    from pynytimes import NYTAPI
   
    
    nyt=NYTAPI(API_key, parse_dates=True)
    
    query=SuchName.strip()
    if query[0]!='"' and query[-1]!='"':
        query='"'+query+'"'
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
    filename=name_file(SuchName,Heute=Heute())
    
    print(SuchName,len(articles))
    
    writeFile(filename,articles)
    return articles



def generate_neutral_series(sample="M"):

    normal_columns=['abstract','pub_date']
    
    start_date=dt.datetime(1960, 12, 31, 0,0)
    start_date = start_date.replace(tzinfo=dt.timezone.utc)
    
    df=pd.DataFrame(columns=normal_columns)
    df["pub_date"]=[start_date,dt.datetime.now().replace(tzinfo=dt.timezone.utc)]
    df=df.fillna(0)
    neutral=pd.DataFrame(df.set_index("pub_date").resample(sample).size().rename("empty"))
    
    
    return neutral
    
def GiveFilenamesFromSearch(SL):
    import glob
    filenames=[]
    
    for DataName in SL:
        DataName=DataName.replace(" ","")
        filenames+=glob.glob(f"*_NYtimes_{DataName}*.json")
        
    print("Number of Json Files: ", len(filenames))
    return filenames
    


def load_recent_search(filename,type_of_material=["News","articles"],sample="Y"):    
    try:
        df=pd.read_json(filename, convert_dates=['pub_date']).drop_duplicates("web_url",keep="first")
        df=df[df.type_of_material.isin(type_of_material)]
        print(f"{filename} - article count: {len(df)}", end=" -- ")
    except:
        print(f"{filename} not found.")   
        
    try:
        timerow=df.set_index("pub_date").resample(sample).size()
        # make timerow:
        return timerow
    except:
        print("error")
    

def load_recent_search_list(SL,sample="Y"):
    
    neutral=generate_neutral_series(sample=sample)
    df=pd.DataFrame(neutral)
    for SuchName in SL:
        print(SuchName)
        filename=name_file(SuchName,Heute=Heute())
        print(filename)
        df_new=load_recent_search(filename,sample=sample).rename(SuchName)

        if isinstance(df_new,pd.Series):
            print(SuchName, len(df_new))
            df=df.join(df_new).fillna(0)
    if isinstance(df,pd.DataFrame):
        df.drop(columns=["empty"],inplace=True)
        return df
    else:
        print("no files found :(")

        
        

def load_filenames(SL,sample="Y"):
    
    neutral=generate_neutral_series(sample=sample)
    df=pd.DataFrame(neutral)
    article_counts={}
    for filename in SL:
        SuchName=filename.split("_NYtimes_")[-1].split(".")[0]
        print(SuchName,filename)
        df_new=load_recent_search(filename,sample=sample).rename(SuchName)

        if isinstance(df_new,pd.Series):
            print("Data points:" , len(df_new))
            df=df.join(df_new).fillna(0)
    if isinstance(df,pd.DataFrame):
        df.drop(columns=["empty"],inplace=True)
        df=df.fillna(0)
        return df
    else:
        print("no files found :(")
