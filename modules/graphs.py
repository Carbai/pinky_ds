import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

def graph_pies(df, year):
    df_year=df[df['Year']==year]#datetime.datetime(2023, 1, 1)]
    df_year_p = pd.DataFrame({
    'Gender': ['Male', 'Female'],
    'Percentage': [round((df_year['males_Totale'].values/df_year['all_Totale'].values*100)[0],2),
                round((df_year['females_Totale'].values/df_year['all_Totale'].values*100)[0],2)]
    #[round((data_2023['male_Totale']/data_2023['all_Totale']*100).astype(float),2),
    #            round((data_2023['female_Totale']/data_2023['all_Totale']*100).astype(float),2)]  
    })
    fig_pie = make_subplots(rows=1, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}]], vertical_spacing=0)
    fig_pie.add_trace(go.Pie(values=df_year_p['Percentage'],labels=df_year_p['Gender'],hole=0.95,marker=dict(
                                colors=['#47a8f5','lightgrey'],  # Assign custom colors
                                line=dict(color='rgba(0,0,0,0)', width=0), # Avoid default white border
        ),
        textinfo='none'
    ), row=1, col=1)

    gradient_colors = ['#47a8f5', 'rgba(0,0,0,0)', '#47a8f5']  # Gradient from blue to transparent

    fig_pie.add_trace(go.Pie(
        labels=['', '', ''],  # Empty labels
        values=[df_year_p[df_year_p['Gender']=='Male']['Percentage'].values[0], df_year_p[df_year_p['Gender']=='Female']['Percentage'].values[0]],  # Values for gradient overlay
        hole=0.93,  # Same hole size to align with the main chart
        marker=dict(
            colors=gradient_colors,
            line=dict(color='rgba(0,0,0,0)', width=0)  # No borders for gradient
        ),
        textinfo='none',
        sort=False  # Disable sorting to match exact overlay
    ), row=1, col=1)

    fig_pie.add_annotation(
        text=df_year_p[df_year_p['Gender']=='Male']['Percentage'].values[0].astype(str)+'%',  # Bold text for "Male" and percentage
        xanchor="center",  # X position (centered in the chart)
        x=sum(fig_pie.get_subplot(1, 1).x) / 2,
        y=0.55,  # Y position (centered in the chart)
        font=dict(size=50, color="#47a8f5"),  # Customize font size and color
        showarrow=False  # Disable arrow
    )

    fig_pie.add_annotation(
        text="Male",  # Bold text for "Male" and percentage
        xanchor="center",  # X position (centered in the chart)
        x=sum(fig_pie.get_subplot(1, 1).x) / 2,
        y=0.35,  # Y position (centered in the chart)
        font=dict(size=30, color="grey"),  # Customize font size and color
        showarrow=False  # Disable arrow
    )
    ## Female data
    fig_pie.add_trace(go.Pie(values=df_year_p['Percentage'],labels=df_year_p['Gender'],hole=0.95,marker=dict(
                                colors=['lightgrey','#FF77B7'],  # Assign custom colors
                                line=dict(color='rgba(0,0,0,0)', width=0),
        ),
        textinfo='none', rotation=df_year_p[df_year_p['Gender']=='Female']['Percentage'].values[0]/100*360,
    ), row=1, col=2)

    gradient_colors = ['#FF77B7', 'rgba(0,0,0,0)']  # Gradient from blue to transparent

    fig_pie.add_trace(go.Pie(
        labels=['', ''],  # Empty labels
        values=[df_year_p[df_year_p['Gender']=='Female']['Percentage'].values[0], df_year_p[df_year_p['Gender']=='Male']['Percentage'].values[0]],#[df_2023[df_2023['Gender']=='Female']['Percentage'].values[0]/100*360, 140, 200],  # Values for gradient overlay
        hole=0.93,  # Same hole size to align with the main chart
        marker=dict(
            colors=gradient_colors,
            line=dict(color='rgba(0,0,0,0)', width=0)  # No borders for gradient
        ),
        textinfo='none',
        sort=False  # Disable sorting to match exact overlay
        ), row=1, col=2)

    fig_pie.add_annotation(
        text=df_year_p[df_year_p['Gender']=='Female']['Percentage'].values[0].astype(str)+'%',  # Bold text for "Male" and percentage
        x=sum(fig_pie.get_subplot(1, 2).x) / 2,  # X position (centered in the chart)
        y=0.55,  # Y position (centered in the chart)

        font=dict(size=50, color="#FF77B7"),  # Customize font size and color
        showarrow=False,  # Disable arrow
        xanchor="center"
    )

    fig_pie.add_annotation(
        text="Female",  # Bold text for "Male" and percentage
        x=sum(fig_pie.get_subplot(1, 2).x) / 2,#x=0.84,  # X position (centered in the chart)
        y=0.35,  # Y position (centered in the chart)
        font=dict(size=30, color="grey"),  # Customize font size and color
        showarrow=False,  # Disable arrow,
        xanchor="center"
    )

    fig_pie.update_layout(showlegend=False, hovermode=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    return fig_pie

def graph_sunbursts(df, year, colors_map_males=px.colors.sequential.Blues, colors_map_females=px.colors.sequential.RdPu):
    colors_map_females[0]='rgba(0,0,0,0)'
    colors_map_males[0]='rgba(0,0,0,0)'
    data_year=df[df['Year']==datetime.datetime(year, 1, 1)]
    
    df_year = pd.DataFrame({
    'Gender': ['Male', 'Female'],
    'Percentage': [round(data_year['males_Totale'].values[0],2),
                round(data_year['females_Totale'].values[0],2)],
    'Partner o ex':[round(data_year['males_Partner or Ex Partner'].values[0],2),
                round(data_year['females_Partner or Ex Partner'].values[0],2)],
    'Altro conoscente': [round(data_year['males_Altro conoscente '].values[0],2),
                round(data_year['females_Altro conoscente '].values[0],2)],
    'Altro parente': [round(data_year['males_Altro parente'].values[0],2),
                round(data_year['females_Altro parente'].values[0],2)],
    'Non identificato': [round(data_year['males_Autore non identificato'].values[0],2),
                round(data_year['females_Autore non identificato'].values[0],2)],
    'Sconosciuto alla vittima':[round(data_year['males_Autore sconosciuto alla vittima'].values[0],2),
                round(data_year['females_Autore sconosciuto alla vittima'].values[0],2)]
    })
    fig_pies = make_subplots(rows=1, cols=2, specs=[[{"type": "sunburst"},{"type": "sunburst"}]])
    fig_pies.add_trace(go.Sunburst(name='',
       # labels=["", "Partner o ex", "", "", "", ""],
        labels=["Male", "Partner or ex", "Unidentified", "Acquaintance", "Relative", "Stranger"],
        parents=["", "Male", "Male", "Male", "Male", "Male", "Male", "Male" ],
        values=[int(df_year[df_year['Gender']=='Male']['Percentage'].values[0]),
                #int(df_2023_all[df_2023_all['Gender']=='Female']['Percentage'].values[0]),
                int(df_year[df_year['Gender']=='Male']['Partner o ex'].values[0]),
                int(df_year[df_year['Gender']=='Male']['Non identificato'].values[0]),
                int(df_year[df_year['Gender']=='Male']['Altro conoscente'].values[0]),
                int(df_year[df_year['Gender']=='Male']['Altro parente'].values[0]),
                int(df_year[df_year['Gender']=='Male']['Sconosciuto alla vittima'].values[0])],
                branchvalues='total',
                marker=dict(
                pattern=dict(
                   # shape=["", "/", "/", ".", ".", "/", "/", ".", "/"], solidity=0.9
                ),colors=colors_map_males
            ), 
    ), row=1, col=1)
    # Get the original colors from the figure
    original_colors = fig_pies.data[0].marker.colors
    # Access the labels in the sunburst trace
    labels = fig_pies.data[0].labels
    fig_pies.add_trace(go.Sunburst(name='',
       # labels=[" ", " ", " ", " ", " ", "Partner or ex"],
        labels=["Female", "Unidentified",  "Acquaintance", "Stranger","Relative", "Partner or ex"],
        parents=["", "Female", "Female", "Female", "Female", "Female", "Female", "Female" ],
        values=[int(df_year[df_year['Gender']=='Female']['Percentage'].values[0]),
                int(df_year[df_year['Gender']=='Female']['Non identificato'].values[0]),
                #int(df_2023_all[df_2023_all['Gender']=='Female']['Percentage'].values[0]),
                int(df_year[df_year['Gender']=='Female']['Altro conoscente'].values[0]),
                int(df_year[df_year['Gender']=='Female']['Sconosciuto alla vittima'].values[0]),
                int(df_year[df_year['Gender']=='Female']['Altro parente'].values[0]),
                int(df_year[df_year['Gender']=='Female']['Partner o ex'].values[0])],
                branchvalues='total',
                marker=dict(line=dict(width=0.2, color='rgb(122,1,119)'),
                pattern=dict(
                   # shape=["", "/", "/", ".", ".", "/", "/", ".", "/"], solidity=0.9
                ),colors=colors_map_females
            )
    ), row=1, col=2)
    fig_pies.update_traces(textinfo='label+percent parent')
    fig_pies.update_layout(margin = dict(t=0, l=0, r=0, b=0), font=dict(family='RobotoBold'),
                           paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    return fig_pies

def graph_bars(df, type, colors):#_males=px.colors.sequential.Blues, colors_map_females=px.colors.sequential.RdPu):
    if type not in ['males', 'females']:
        raise ValueError("Type value must be males or females.")
    
    fig_bar = px.bar(
        df,
        x='Year',
        y='Count',
        color='Category',
        text='Percentage',  # Add the label text
        barmode='stack',
       # title='Homicides by Category and Year',
        labels={'Count': 'Number of Homicides', 'Category': 'Killer Type'},
        color_discrete_sequence=colors)

    fig_bar.update_traces(
        textangle=0,
        insidetextanchor='middle')

    fig_bar.update_layout(
        font=dict(family='RobotoBold'),margin = dict(t=0, l=0, r=0, b=0),
                           paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')

    x_labels=df['Year'].dt.year.to_list()
    fig_bar.update_xaxes(tickvals=x_labels, tickformat='%Y')
    fig_bar.update_yaxes(visible=False)
    return fig_bar

def graph_cloropleth(data, geo, color_col='', type='abs'):#ita, map_df, ita_with_pop, type=['abs','norm']):
    if type=='abs':
        title='Women killed by partner or ex'
    elif type=='norm':
        title='Women killed by partner or ex per 100000 people'
    else:
        raise ValueError("Error type not available. Try abs or norm.")
    
    fig_map = px.choropleth(data, geojson=geo, locations="reg_name", color=color_col,#"Females - Partner or ex partner",
                              featureidkey="properties.reg_name")
    fig_map.update_geos(fitbounds="locations", visible=False)
    fig_map.update_coloraxes(colorscale="RdPu", colorbar=dict(
            title='',
            orientation="h",  # Horizontal orientation
            x=0.5,  # Centered horizontally
            y=0.1,  # Positioned below the graph
            xanchor="center",  # Center alignment for the colorbar
            yanchor="top", len=0.6, thickness=20)) 
    fig_map.update_traces(
        hovertemplate='<b>%{location}</b><br>Feminicides number=%{z}')
    fig_map.update_layout(
        title=dict(
            text=title,#"Women killed by partner or ex",  # Title text
            x=0.5,  # Center the title horizontally (0 = left, 0.5 = center, 1 = right)
            xanchor="center",  # Anchor the title to its center
            yanchor="top"  # Anchor to the top of the figure
        ), font=dict(family='RobotoBold'),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',geo=dict(bgcolor= 'rgba(0,0,0,0)'),
               autosize=False,
            margin = dict(
                    l=0,
                    r=0,
                    b=0,
                    t=5,
                    pad=4,
                    autoexpand=True
                ),
                width=600,
    )

    return fig_map