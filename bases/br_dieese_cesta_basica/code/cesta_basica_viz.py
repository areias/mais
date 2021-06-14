#!/usr/bin/env python
# coding: utf-8

# # Pesquisa Nacional da Cesta Básica de Alimentos
# 
# Fonte: https://www.dieese.org.br/cesta/

# In[1]:


import plotly.express as px
import pandas as pd


# In[2]:


gv=pd.read_csv("../output/br_dieese_cesta_basica_metodologia_velha.csv")
gn=pd.read_csv("../output/br_dieese_cesta_basica_metodologia_nova.csv")


# In[3]:


fig = px.line(gn, x="data", y="gasto_mensal", color='cidade', 
              title="Gasto Mensal por Cidade da Cesta Basica de Alimentos")
#fig.show()
fig.write_image("../images/gasto_mensal.png")


# In[4]:


fig = px.line(gn, x="data", y="horas_de_trabalho", color='cidade', 
              title="Horas de trabalho necessárias ao indivíduo que ganha salário mínimo, <br>para adquirir a Cesta Basica de Alimentos")
#fig.show()
fig.write_image("../images/horas_de_trabalho.png")


# In[5]:


fig = px.line(gv, x="data", y="gasto_mensal", color='cidade', 
              title="Gasto Mensal por Cidade da Cesta Basica de Alimentos <br>Metodologia velha")
#fig.show()
fig.write_image("../images/gasto_mensal_velha.png")


# In[6]:


fig = px.line(gv, x="data", y="horas_de_trabalho", color='cidade', 
              title="Horas de trabalho necessárias ao indivíduo que ganha salário mínimo, <br>para adquirir a Cesta Basica de Alimentos <br>Metodologia Velha")
#fig.show()
fig.write_image("../images/horas_de_trabalho_velha.png")


# In[ ]:




