# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import re

df=pd.read_json (r'Downloads/All_Beauty.json', lines=True)
df_meta= pd.read_json (r'Downloads/meta_All_Beauty.json', lines=True)
dfmeta_sub = df_meta[["description","title", "image",  "asin",'rank']]
df_sub = df[["asin", "reviewText",'overall']]
df_sub1=df_sub.groupby('asin', as_index=False).agg(list)
#df_sub1=df_sub.groupby("asin")["reviewText"].apply(list)


df_total = pd.merge(df_sub1, dfmeta_sub, on="asin", how='left')
df_remove = df_total.dropna()
df_remove = df_remove.reset_index(drop=True)
df_remove = df_remove[df_remove['image'].str.len()!=0]
df_remove = df_remove[df_remove["reviewText"].str.len()>2]
df_remove["reviewText"] = df_remove["reviewText"].str[:3]
df_remove["overall"] = df_remove["overall"].str[:3]
df_remove = df_remove[df_remove['description'].str.len()!=0]


def func(x):
    ans=[]
    for item in x:
        if not isinstance(item, float):      
            a= re.sub(r"<.*?>","",item)
            a = re.sub('&nbsp;',' ',a)
            ans.append(a)
    return ans
        
df_remove["reviewText"]=df_remove["reviewText"].apply(func)
df_remove["description"]=df_remove["description"].apply(func)
df_remove['rank']=df_remove["rank"].str.split(" ").str[0]

df_remove = df_remove.reset_index(drop=True)
df_sample = df_remove.sample(n = 4048)
df_sample['description'] = ['\n'.join(map(str, l)) for l in df_sample['description']]
df_sample.to_json(r'Desktop/all_beauty.json',orient='records')