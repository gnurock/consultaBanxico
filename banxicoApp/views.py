#import requests
from django.shortcuts import render

from django.http import HttpResponse
from .services import get_series
from .forms import DateForm
from plotly.offline import plot
from plotly.graph_objs import Scatter
import plotly.express as px
import pandas as pd
from django import forms
import plotly.graph_objects as go

from django.views.generic import (TemplateView, FormView,
)
class SilentAssertionError(Exception):
    silent_variable_failure = True

def home(requests):
    """
    Funcion que se utiliza para renderizar en el home view

    Parametros: 
        -requests : Es el request  que se la manda a esta vista 
    Returns:
        Context:  Regresa  el context que se va renderizar a la vista home y
                  contiene el dataframe ya con los datos filtrados para ser utulizados
                  por la libreria plotty
                  
     """
    context = {}
    #response = requests.get('https://jsonplaceholder.typicode.com/todos/')
    #'SP68257' udis
    context['form'] = DateForm()
    params = {}
    if requests.GET: 
        fecha_ini = requests.GET['fecha_ini']
        fecha_fin = requests.GET['fecha_fin'] 
        if fecha_fin < fecha_ini:
            context["error"]= "No puede ingresa una fecha final menor a la fecha inicial"
        else:
            params= {'fecha_ini':fecha_ini,'fecha_fin':fecha_fin,"serie":'SP68257'}
            context = {
                'series':get_series(params=params)
                
            }
            context['form'] = DateForm()
            df = pd.DataFrame(context['series'][0]['datos'])
            df['dato'] = pd.to_numeric(df['dato'])
            df['fecha'] = pd.to_datetime(df['fecha'],dayfirst=True).dt.strftime('%Y-%m-%d')
            
            plot_div = graficarCurva(df)
            
            context['plot_div']=plot_div
            context['stats'] = {'mean': df['dato'].mean(),
                                'min':  df['dato'].min(),
                                'max':  df['dato'].max()
                                }
            context['datos']= df.to_dict('records')
            context['keys'] =  context['datos'][0].items()
        
    
    return render(requests, 'banxicoApp/home.html', context)

    #return render(request, "main_app/home.html", {"data": todos})

def graficarCurva(df,isTIIE=False):
    """
        Funcionm para graficar
    """
    
   

    if isTIIE:# agregar n lineas de los tipos de series  
        fig = px.line(df, x='fecha_21dias', y='dato_SF60648', title='Serie udis')
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day"),
                    dict(count=1, label="1m", step="month"),
                    dict(step="all")
                ])
            )
        )
        fig.add_trace(go.Scatter(x=df['fecha_21dias'], y=df['dato_SF60649'],
                            mode='lines',
                            name='SF60649'))     

    else:
        fig = px.line(df, x='fecha', y='dato', title='Serie udis')
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1d", step="day"),
                    dict(count=1, label="1m", step="month"),
                    dict(step="all")
                ])
            )
        )
        

    plot_div = plot(fig,
               output_type='div')

    return plot_div



def serie_tiie(requests):
    context = {}
    
    context['form'] = DateForm()
    if requests.GET: 
        fecha_ini = requests.GET['fecha_ini']
        fecha_fin = requests.GET['fecha_fin']
        if fecha_fin < fecha_ini:
            context["error"]= "No puede ingresa una fecha final menor a la fecha inicial" 
        else:
            params= {'fecha_ini':fecha_ini,'fecha_fin':fecha_fin,"serie":'SF60648,SF60649'}
            context = {
                'series': get_series(params=params)
                
            }
            context['form'] = DateForm()
            df = pd.DataFrame(context['series'])
            
            df1 = pd.DataFrame.from_dict(context['series'][0]['datos'])
            df2 = pd.DataFrame.from_dict(context['series'][1]['datos'])
            
            df1 = df1.rename(columns={'fecha':'fecha_21dias','dato':'dato_SF60648'})
            df2 = df2.rename(columns={'fecha':'fecha_91dias','dato':'dato_SF60649'})
            
            df1['dato_SF60648'] = pd.to_numeric(df1['dato_SF60648'])
            df2['dato_SF60649'] = pd.to_numeric(df2['dato_SF60649'])
            df1['fecha_21dias'] = pd.to_datetime(df1['fecha_21dias'],dayfirst=True).dt.strftime('%Y-%m-%d')
            frame = [df1,df2]
            result_f = pd.concat(frame,axis=1)
            result_f = result_f.drop(['fecha_91dias'],axis=1)

            # df['dato_911'] = pd.to_numeric(df['datos'][0]['dato'])
            # df['dato_811'] = pd.to_numeric(df['datos'][1]['dato'])
            # df['fecha'] = pd.to_datetime(df['datos'][0]['fecha'],dayfirst=True).dt.strftime('%Y-%m-%d')
            
            plot_div = graficarCurva(result_f,isTIIE=True)
            
            context['plot_div']=plot_div
            # context['stats'] = {'mean': df['dato'].mean(),
            #                     'min':  df['dato'].min(),
            #                     'max':  df['dato'].max()
            #                     }
            
            context['datos'] = result_f.to_dict('records')
            context['keys'] =  context['datos'][0].items()
       
    return render(requests, 'banxicoApp/tiee.html', context)

def serie_dolar(requests):
    
    context = {}
    context['form'] = DateForm()

    if requests.GET: 
        fecha_ini = requests.GET['fecha_ini']
        fecha_fin = requests.GET['fecha_fin'] 
        if fecha_fin < fecha_ini:
            context["error"]= "No puede ingresa una fecha final menor a la fecha inicial"
        else:
            params= {'fecha_ini':fecha_ini,'fecha_fin':fecha_fin,"serie":'SF60653'}
            context = {
                'series': get_series(params=params)
                
            }
            DateForm
            context['form'] = DateForm()
            df = pd.DataFrame(context['series'][0]['datos'])     
            df['dato'] = pd.to_numeric(df['dato'])
            df['fecha'] = pd.to_datetime(df['fecha'],dayfirst=True).dt.strftime('%Y-%m-%d')
            
            plot_div = graficarCurva(df)
            
            context['plot_div']=plot_div
            context['stats'] = {'mean': df['dato'].mean(),
                                'min':  df['dato'].min(),
                                'max':  df['dato'].max()
                                }
            context['datos']= df.to_dict('records')
            context['keys'] =  context['datos'][0].items()
            
    return render(requests, 'banxicoApp/dolar.html', context)