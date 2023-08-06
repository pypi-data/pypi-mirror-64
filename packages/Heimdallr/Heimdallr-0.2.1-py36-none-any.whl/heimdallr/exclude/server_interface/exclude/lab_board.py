#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from odin.lab_board.gcal import get_cal
from odin.lab_board.layout import (lab_board_interval2_component_id,
                                   lab_board_interval_component_id,
                                   lab_board_layout,
                                   lab_board_live_update_calendar_id,
                                   lab_board_live_update_graph_id,
                                   lab_board_live_update_text_id,
                                   )

__author__ = 'Christian Heider Nielsen'
__doc__ = ''

import datetime

import dash

import dash_html_components as html
import plotly
from dash.dependencies import Input, Output
from pyorbital.orbital import Orbital

satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = lab_board_layout


@app.callback(Output(lab_board_live_update_text_id, 'children'),
              [Input(lab_board_interval_component_id, 'n_intervals')])
def update_metrics(n):
  lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
  style = {'padding': '5px',
           'fontSize':'16px'
           }

  return [html.Span(f'Longitude: {lon:.2f}', style=style),
          html.Span(f'Latitude: {lat:.2f}', style=style),
          html.Span(f'Altitude: {alt:0.2f}', style=style)
          ]


# Multiple components can update every time interval gets fired.
@app.callback(Output(lab_board_live_update_graph_id, 'figure'),
              [Input(lab_board_interval_component_id, 'n_intervals')])
def update_graph_live(n):
  satellite = Orbital('TERRA')
  data = {'time':     [],
          'Latitude': [],
          'Longitude':[],
          'Altitude': []
          }

  # Collect some data
  for i in range(180):
    time = datetime.datetime.now() - datetime.timedelta(seconds=i * 20)
    lon, lat, alt = satellite.get_lonlatalt(time)
    data['Longitude'].append(lon)
    data['Latitude'].append(lat)
    data['Altitude'].append(alt)
    data['time'].append(time)

  # Create the graph with subplots
  fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
  fig['layout']['margin'] = {'l':30,
                             'r':10,
                             'b':30,
                             't':10
                             }

  fig['layout']['legend'] = {'x':      0,
                             'y':      1,
                             'xanchor':'left'
                             }

  fig.append_trace({'x':   data['time'],
                    'y':   data['Altitude'],
                    'name':'Altitude',
                    'mode':'lines+markers',
                    'type':'scatter'
                    }, 1, 1)

  fig.append_trace({'x':   data['Longitude'],
                    'y':   data['Latitude'],
                    'text':data['time'],
                    'name':'Longitude vs Latitude',
                    'mode':'lines+markers',
                    'type':'scatter'
                    }, 2, 1)

  return fig


@app.callback(Output(lab_board_live_update_calendar_id, 'children'),
              [Input(lab_board_interval2_component_id, 'n_intervals')])
def update_calendar_live(n):
  return get_cal()


'''
@app.callback(Output(lab_board_live_update_calendar_id, 'children'),
              [Input(lab_board_interval2_component_id, 'n_intervals')])
def update_calendar_iframe_live(n):
  return [dash_dangerously_set_inner_html.DangerouslySetInnerHTML(lab_board_calendar)]
'''

if __name__ == '__main__':
  app.run_server(debug=True)
