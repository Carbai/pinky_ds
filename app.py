import pandas as pd
import json
import sys
sys.path.append('modules')
from data_processor import DataProcessor
import graphs
import datetime
import geopandas as gpd
import plotly_express as px
import pyproj
from dash import Dash, html, dcc, Input, Output

## data wrangling
istat_data=pd.read_excel('./data/omicidi-relazione-autore-DCPC-anni-2002-2023.xlsx',sheet_name=None) ## read data from local file
data=DataProcessor(istat_data)
data_df=data.merge_df() ## generate dataframe storing all data required for this project
fig_pie=graphs.graph_pies(data_df, year=datetime.datetime(2023, 1, 1))
years=data_df.Year.dt.year.to_list()

fig_sunbust = graphs.graph_sunbursts(data_df, year=2023)
bar_df_f=data.get_bar_df(data_df, type='females')
fig_bar_f = graphs.graph_bars(bar_df_f, type='females', colors=px.colors.sequential.RdPu)
bar_df_m=data.get_bar_df(data_df, type='males')
fig_bar_m = graphs.graph_bars(bar_df_m, type='males', colors=px.colors.sequential.Blues)

##geography data
regions_name_map={'Valle d\'Aosta/\nVallée d\'Aoste':'Valle d\'Aosta/Vallée d\'Aoste',
                  'Piemonte ':'Piemonte',
                  'Friuli-Venezia Giulia ':'Friuli-Venezia Giulia'}
cols=['reg_name','Males - Partner or ex partner', 'Males - Altro Parente', 'Males - Altro conoscente', 'Males - Autore sconosciuto alla vittima',
      'Males - Autore non identificato', 'Males - Totale', 'Females - Partner or ex partner', 'Females - Altro Parente', 'Females - Altro conoscente', 'Females - Autore sconosciuto alla vittima',
      'Females - Autore non identificato', 'Females - Totale']

ita_pop=pd.read_csv('data/DCIS_POPRES1_10012025160913907.csv')
df_geo=data.get_regions(cols=cols,regions_dict=regions_name_map,population=ita_pop)
fp = "./data/limits_IT_regions.geojson"
map_df = gpd.read_file(fp)
map_df.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
fig_map=graphs.graph_cloropleth(df_geo, map_df, color_col='Females - Partner or ex partner', type='abs')
fig_map_norm=graphs.graph_cloropleth(df_geo, map_df, color_col='Females - Partner or ex partner - norm', type='norm')

## get stories text
f = open('./data/stories.json')
project = json.load(f)
title=project['project']
desc=project['goal']
stories=project['stories']


## dash app
app = Dash(__name__)
app.title='PinkyDS'
server= app.server
app.layout = html.Div(
                children=[
                    html.H1(title),
                    html.H2(desc),
              ## First story container
              html.Div(className='container', children=[
                html.H3(stories[0]['title']),
                html.H4(stories[0]['statement']),
                html.Div(className='dropdown_container', children=[
                dcc.Dropdown(years, years[-1], placeholder='Select year', id='year_dropdown', className='year_dropdown')]),
                dcc.Graph(mathjax=True, className='plot_perc_killing', id='fig_pie', figure=fig_pie),
                html.H5(stories[0]['description']),
                html.Button('Reveal full story',className='reveal_button',id='reveal_button',title='Reveal', n_clicks=0),
                html.Div(className='story1', id='story1', hidden=True,
                         children=[
                                html.Div(className='dropdown_container', children=[
                                dcc.Dropdown(years, years[-1], placeholder='Select year', id='year_dropdown2', className='year_dropdown')]),
                                dcc.Graph(mathjax=True, className='pies_by_killer', id='pies_by_killer', figure=fig_sunbust),
                                html.H4('''Across the years women have been killed mostly by their partner and ex partner while the percentage of males killed by their partner is very low.'''),
                                html.Div(className='bar_container',children=[
                                dcc.Graph(mathjax=True, className='bar_males', figure=fig_bar_m),
                                dcc.Graph(mathjax=True, className='bar_females', figure=fig_bar_f)]),
                                html.H4(stories[0]['explaination'])])]),
                
              ## Second story container
              html.Div(className='container', children=[ 
                html.Div(children=[html.H3(stories[1]['title'])], className='story2_title'),
                html.H4(stories[1]['statement']),
                html.Div(className='parent_map_container',id='parent_map_container',children=[
                  html.Div(className='map_container',id='map_container', children=[
                          dcc.Graph(id='map_plot',figure=fig_map)]),
                  html.Div(className='nplot_container',id='nplot_container',children=[
                          dcc.Graph(id='map_nplot',figure=fig_map_norm)], hidden=True),
                  
                ]),
                html.Div(className='nplot_caption_container',id='nplot_caption_container',children=[
                          html.H4(stories[1]['explaination'])], hidden=True),
                html.Button('Reveal full story',className='reveal_button2',id='reveal_button2',title='Reveal2', n_clicks=0)]),
              
              
              ## Third story container 
              html.Div(className='container', children=[
                html.H3(stories[2]['title']),
                html.H4(stories[2]['statement']),
                html.Button('Reveal full story',className='reveal_button2',id='reveal_button3',title='Reveal3', n_clicks=0),
                html.Div(id='story3', hidden=True,
                         children=[html.H4(stories[2]['explaination'])])])
                ])

@app.callback(
    Output('fig_pie', 'figure'),
    Input('year_dropdown', 'value')
)
def update_output(value):
    return graphs.graph_pies(data_df, year=datetime.datetime(value, 1, 1)) 

@app.callback(
    Output('pies_by_killer', 'figure'),
    Input('year_dropdown2', 'value')
)
def update_output(value):
    return graphs.graph_sunbursts(data_df, year=value) 

@app.callback(Output('story1', 'hidden'),
              Input('reveal_button', 'n_clicks'),
              prevent_initial_call=True)

def reveal_story(n_clicks):
  return n_clicks % 2 == 0

@app.callback(Output('reveal_button', 'children'),
              Input('reveal_button', 'n_clicks'),
              prevent_initial_call=True)

def update_button(n_clicks):
  if n_clicks % 2 != 0:
    return 'Hide full story'
  return 'Reveal full story'

@app.callback(Output('reveal_button2', 'children'),
              Input('reveal_button2', 'n_clicks'), prevent_initial_call=True)

def update_button2(n_clicks):
  if n_clicks % 2 != 0:
    return 'Hide full story'
  return 'Reveal full story'

@app.callback([Output('nplot_container', 'hidden'),
               Output('nplot_caption_container', 'hidden')],
              Input('reveal_button2','n_clicks'), prevent_initial_call=True)

def reveal_story2(n_clicks):
  return n_clicks % 2 == 0, n_clicks % 2 == 0

@app.callback(Output('reveal_button3', 'children'),
              Input('reveal_button3', 'n_clicks'), prevent_initial_call=True)

def update_button3(n_clicks):
  if n_clicks % 2 != 0:
    return 'Hide full story'
  return 'Reveal full story'

@app.callback(Output('story3', 'hidden'),
              Input('reveal_button3', 'n_clicks'),
              prevent_initial_call=True)

def reveal_story3(n_clicks):
  return n_clicks % 2 == 0

app.run(host='0.0.0.0',port='0.0.0.0')
