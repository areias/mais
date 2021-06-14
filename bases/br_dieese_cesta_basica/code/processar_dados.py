#!/usr/bin/env python
# coding: utf-8

# Fonte: DIEESE
# Série recalculada, conforme mudança metodológica realizada na pesquisa a partir de janeiro 2016. Além  de  ampliar  a  abrangência  da  pesquisa,  o  DIEESE  também  atualizou  a metodologia da Pesquisa Nacional da Cesta Básica de Alimentos. 
# 
# Ver nota Tomada especial de preços a partir de abril de 2020. Clique https://www.dieese.org.br/analisecestabasica/2020/202004cestabasica.pdf para maiores detalhes. 

# In[11]:


import re


# In[12]:


import numpy as np


# In[13]:


import pandas as pd
from bs4 import BeautifulSoup


# In[14]:


def get_table(txt):
    
    # parse html
    soup = BeautifulSoup(txt, "html.parser")
    
    # find table div and ingest into dataframe, setting thousands and decimal operators
    df=pd.read_html(str(soup.find("table")),thousands=".", decimal=",")
    
    # pd.read_html gives back a list of dfs
    df=df[0]

    # create month column
    df['mes']=df.iloc[:,0].apply(lambda x: x.split("-")[0])
    df['mes']=df['mes'].apply(int)

    # create year column
    df['ano']=df.iloc[:,0].apply(lambda x: x.split("-")[1])
    
    # drop joint month-year column
    df=df.drop("Unnamed: 0", axis=1)
    
    # replace - with nan
    df=df.replace("-", np.nan)
    
    return df


# In[15]:


def get_total_hours(duration):
    # transformhs a string like 68h18m into total hours float
    # get total hours
    hours=int(re.search("\d+h",duration).group().replace("h",""))
    # get total mins
    mins=int(re.search("\d+m",duration).group().replace("m",""))
    return hours+(mins/60)


# In[76]:


def split_old_new(df):
    """splits df into two since there are two observations for 
    2015-12, when the methodology changed"""
    
    # indice de troca de metodologia 
    idx=df.loc[df['ano']=="2015(1)","ano"].index[0]
    
    # metodologia velha
    dv=df.loc[:idx-1, :].copy()
    dv.loc[:,'ano']=dv.loc[:,"ano"].apply(int)
    
    # metodologia nova
    dn=df.loc[idx:, :].copy()
    dn.loc[dn['ano']=="2015(1)","ano"]=2015
    dn.loc[:,'ano']=dn.loc[:,"ano"].apply(int)

    return (dv, dn)


# In[77]:


# from wide to long
def wide_to_long(wide_df):
    long_df=pd.melt(wide_df, id_vars=['mes','ano'])
    long_df=long_df.loc[~long_df.value.isna()]
    long_df.columns=['mes', 'ano', 'cidade', 'value']
    return long_df


# In[78]:


with open("../input/dieese-tempo-de-trabalho.html", "r") as f:
    txt = f.read()


# In[79]:


tf=get_table(txt)


# In[80]:


tv,tn=split_old_new(tf)


# In[81]:


tv=wide_to_long(tv)


# In[82]:


tn=wide_to_long(tn)


# In[83]:


tn['horas_de_trabalho']=tn['value'].apply(get_total_hours)


# In[84]:


tv['horas_de_trabalho']=tv['value'].apply(get_total_hours)


# In[85]:


tv.drop("value", axis=1, inplace=True)
tn.drop("value", axis=1, inplace=True)


# In[86]:


with open("../input/dieese-gasto-mensal.html", "r") as f:
    txt = f.read()


# In[87]:


gf=get_table(txt)
gv,gn=split_old_new(gf)


# In[88]:


gv=wide_to_long(gv)
gn=wide_to_long(gn)


# In[89]:


gv.columns=['mes','ano','cidade', 'gasto_mensal']
gn.columns=['mes','ano','cidade', 'gasto_mensal']


# In[90]:


gv=gv.merge(tv, on=['mes','ano','cidade'])
gn=gn.merge(tn, on=['mes','ano','cidade'])


# In[91]:


gn['gasto_mensal']=gn['gasto_mensal'].apply(float)
gv['gasto_mensal']=gv['gasto_mensal'].apply(float)


# In[92]:


gn['data']=pd.to_datetime(gn['mes'].apply(str) + "-" + gn['ano'].apply(str), format="%m-%Y")
gv['data']=pd.to_datetime(gv['mes'].apply(str) + "-" + gv['ano'].apply(str), format="%m-%Y")


# In[93]:


gv.head()


# In[94]:


gn.head()


# In[95]:


gv.describe()


# In[96]:


gn.describe()


# In[97]:


gv.to_csv("../output/br_dieese_cesta_basica_metodologia_velha.csv", index=False)
gn.to_csv("../output/br_dieese_cesta_basica_metodologia_nova.csv", index=False)

