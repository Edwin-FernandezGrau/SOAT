# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 08:49:47 2021

@author: EFERNANDEZ
"""
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 08:31:20 2021

@author: EFERNANDEZ
"""
import streamlit as st
import pandas as pd


ruta = 'Tarifario SOAT 202102.xlsx'
t_digital = pd.read_excel(ruta,sheet_name= "TD_Crecer_M",header = 7, index_col =[0, 1],engine ='xlrd')
t_fisico = pd.read_excel(ruta,sheet_name= "TF_Crecer_M",header = 7, index_col =[0, 1],engine ='xlrd')

todos = "ALL"

uso = list(t_digital.index.unique(0))
uso.append(todos)
clase = list(t_digital.index.unique(1))
clase.append(todos)
departamento = list(t_digital.columns)
departamento = departamento[2:]
departamento.append(todos)

st.title(""" Tarifario SOAT """)

#fi_uso = uso[:-1] 
#fi_clase = clase[:-1]
#fi_departamento = departamento[:-1]

def main():
    
   
    f_uso = st.sidebar.selectbox("Seleccione el USO", uso)
    
    
    f_clase = st.sidebar.selectbox("Seleccione la CLASE", clase)
    
    
    f_departamento = st.sidebar.selectbox("Seleccione la DEPARTAMENTO", departamento)
    

    
  
    if f_uso == todos :
       fi_uso = uso[:-1] 
    else:
        fi_uso = []
        fi_uso.append(f_uso)
        
        
    if f_clase == todos :
       fi_clase = clase[:-1]
    else:   
       fi_clase = []
       fi_clase.append(f_clase)
     
        
    if f_departamento == todos :
       fi_departamento = departamento[:-1] 
    else:   
       fi_departamento = []
       fi_departamento.append(f_departamento)
    
    fi_departamento.insert(0,"DESCRIPCION")
    
    st.write(""" DIGITAL """)  
    
    bd = t_digital[t_digital.index.isin(fi_uso, level=0)]
    bd = bd[bd.index.isin(fi_clase, level=1)]
      
    st.dataframe(bd[fi_departamento], width=1200, height=500)
      
    st.write(""" FISICO """) 
    
    bf = t_fisico[t_fisico.index.isin(fi_uso, level=0)]
    bf = bf[bf.index.isin(fi_clase, level=1)]
    
    st.dataframe( bf[fi_departamento], width=1200, height=500)
    
   
#    st.write(""" DIGITAL """)    
#    st.dataframe(t_digital.loc[([f_uso],[f_clase]),[f_departamento]], width=1200, height=500)
        
#    st.write(""" FISICO """)    
#    st.dataframe(t_fisico.loc[([f_uso],[f_clase]),[f_departamento]], width=1200, height=500)
    
    
main()      