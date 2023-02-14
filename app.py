# ---Library Prep---
## Data Wrangling & Visualization
import pandas as pd
import plotly_express as px
import math

## Dash
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc # Untuk mengatur tema Dash
from dash_bootstrap_components._components.Container import Container
from dash.dependencies import Input, Output

# ---Read Data---

promotion = pd.read_csv('promotion_clean.csv')

# ---Data Preparation---

## Rename categorical values
promotion['KPIs_met >80%'] = promotion['KPIs_met >80%'].map({0: 'No', 1: 'Yes'})
promotion['awards_won?'] = promotion['awards_won?'].map({0: 'No', 1: 'Yes'})
promotion['is_promoted'] = promotion['is_promoted'].map({0: 'No', 1: 'Yes'})
promotion['gender'] = promotion['gender'].map({'f': 'Female', 'm': 'Male'})

## Change data types
promotion[['date_of_birth','join_date']] = promotion[['date_of_birth','join_date']].astype('datetime64')
promotion[['department',
           'region',
           'education',
           'gender',
           'recruitment_channel',
           'KPIs_met >80%',
           'awards_won?',
           'is_promoted']] = promotion[['department',
                                        'region',
                                        'education',
                                        'gender',
                                        'recruitment_channel',
                                        'KPIs_met >80%',
                                        'awards_won?',
                                        'is_promoted']].astype('category')

# ---CARD VALUE COMPONENT---

## Card General Information

card_information = [
    dbc.CardHeader("Dashboard General Information"),
    dbc.CardBody(
        [
            html.P("This is the information of employeed in Our Start-Uphelp to identify who is a potential candidate for promotion",
                    className="card-text"),
        ]
    ),
]

## Card Value Information From sum_promoted

total_employee = len(promotion.index)

# Mempersiapkan id untuk mengisi Card
card_employee = [
    # Membuat Judul Card
    dbc.CardHeader("Total Employee"),
    # Memasukan Informasi Pada Card
    dbc.CardBody(
        html.H2(total_employee)
    )
]

promoted_employee = promotion[promotion['is_promoted'] == 'Yes']
sum_promoted = promoted_employee.shape[0]

card_promoted = [
    dbc.CardHeader("Who is Promoted?"),
    dbc.CardBody(
        html.H2(sum_promoted)
    ),
]

KPI_meet = promotion[promotion['KPIs_met >80%'] == 'Yes']
sum_KPI = KPI_meet.shape[0]

card_KPI = [
    dbc.CardHeader("Who meet the KPI?"),
    dbc.CardBody(
        html.H2(sum_KPI)
    ),
]

age_avg = promotion['age'].mean()
age_average = math.ceil(age_avg)

card_age = [
    dbc.CardHeader("Average Age"),
    dbc.CardBody(
        html.H2(age_average)
    ),
]

# ---DROPDOWN COMPONENT---
# DROPDOWN VALUE (HAVE HIGEST PROMOTION RATE)
list_category=[
            {'label': 'Department', 'value': 'department'},
            {'label': 'Region', 'value': 'region'},
            {'label': 'Gender', 'value': 'gender'},
            {'label': 'Department', 'value': 'department'},
            {'label': 'Recruitment Channel', 'value': 'recruitment_channel'},
            {'label': 'KPIs met > 80%?', 'value': 'KPIs_met >80%'},
            {'label': 'Awards won?', 'value': 'awards_won?'}
]

distribution_plot = px.box(
    promotion,
    x = 'department',
    y = 'length_of_service',
    color = 'is_promoted',
    color_discrete_sequence = ['tomato','darkslateblue'],
    title = 'Length of Service Distribution',
    labels={
        'length_of_service': 'Length of Service (years)',
        'is_promoted': 'Is Promoted?',
        'department': 'Department'
    }
)

# Melakukan filter tangga
data_2020 = promotion[promotion['join_date'] >= '2020-09-01']

# Melakukan Perhitungan jumlah kemunculan dengan crosstab
data_agg = pd.crosstab(
    index = data_2020['join_date'],
    columns = 'freq').reset_index()

# Melakukan Perhitungan jumlah kemunculan dengan groupby & count
data_agg = data_2020.groupby(['join_date']).count()['employee_id'].reset_index()

line_plot = px.line(
    data_agg,
    x = 'join_date',
    y = 'employee_id',
    markers=True,
    labels={
        'join_date':'Join date',
        'employee_id':'Number of employee'
    }
)

# ---Dash Dashboard---

## Mempersiapkan template Dash
app = dash.Dash(
    # Mengatur themes
    external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

## Memberikan nama untuk bagian tab web ketika dihover
app.title = 'Dashboard Analytics' 

# Mengatur layouting pada Dash

app.layout = html.Div(children=[

    ## Membuat NavBar ver 1
    #dbc.NavbarSimple(
    #    # Memberikan Gambar 
    #    html.Img(src = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Bank_BTN_logo.svg/2560px-Bank_BTN_logo.svg.png", 
    #                     height= "25px"), 
    #    brand="Promotion Dashboard Analytics", # Memberikan Title
    #    color="yellow", # Memberikan warna pada background NavBar
    #    )

    # Membuat NavBar ver 2
    
    dbc.Navbar(
        children = [
            # HTML Aligment
                html.A(
                    # Membuat Row
                    dbc.Row([   
                        # Mengatur posisi Kolom 1, agar gambar tidak mepet ke kiri
                        dbc.Col(width = 1),
                        # Memngatur posisi kolom 2, untuk gambar
                        dbc.Col(html.Img(src = "https://i.pinimg.com/originals/34/2b/47/342b47045be85622764172d3d6047aaf.png", 
                                        height= "35px"),
                                        width= 1),
                        # Mengatur posisi kolom 3, untuk nama dashboard
                        dbc.Col(dbc.NavbarBrand("Promotion Dashboard", className="ms-2"), width=2),
                        
                    ])
                ),
                # Menambahkan Menu
                #dbc.Col(width=7),
                #dbc.NavItem(dbc.NavLink(html.A("Home", 
                #                               href="#home",
                #                               className='text-dark font-weight-bold'))),
                #dbc.NavItem(dbc.NavLink(html.A("Analytics", 
                #                               href="#analytics",
                #                               className='text-dark font-weight-bold'))),
        ],
        color = "yellow"
    ),

    # General Infromtion
    
    ## ROW 1 -> CARD GENERAL INFORMATION

    html.Br(),

    html.Div([

    dbc.Row(
        [
        # Col Spacing
        dbc.Col(width = 3),
        # Col Info
        dbc.Col(dbc.Card(card_information, 
                         color="primary", 
                         outline=True, 
                         style = {"textAlign": "center"}),
                          width=6)
        ]
    ),

    html.Br(), html.Hr(),

    ## ROW 2 -> CARD TOTAL EMPLOYEE
    dbc.Row([
    dbc.Col([
        html.Br(),
        dbc.Row(
        [
        # Col Spacing    
        #dbc.Col(width = 3),
        # Col Info
        dbc.Col(dbc.Card(card_employee,
                         color = "green",
                         inverse = True,
                         style = {"textAlign": "center"}), 
                         width=12),
        ]
    ),

    html.Br(), html.Br(),

    ## ROW 3 -> CARD ANALYTICS

     dbc.Row(
        [
        # Col Spacing
        #dbc.Col(width =3),
        # Col Info 1
        dbc.Col(dbc.Card(card_promoted, color="warning", inverse=True, style = {"textAlign": "center"}), width=6),
        # Col Info 2
        dbc.Col(dbc.Card(card_KPI, color="info", inverse=True, style = {"textAlign": "center"}), width=6),
        # Col Info 3
        #dbc.Col(dbc.Card(card_age, color="danger", inverse=True, style = {"textAlign": "center"}), width=2),
        ]
    ),
    ], width = 4),

    dbc.Col([
        html.H3("Employee Growth", style= {"textAlign": "center"}),
        dcc.Graph(id = "line_plot",
                  figure = line_plot,
                  style={'height': '50vh'})
    ], width = 8)

    ]),
    
    html.Br(), html.Hr(),

    # Analytics

    dbc.Row([
        html.H1("Promotion Analyis", style= {"textAlign": "center"}),
        dbc.Tabs([
            # Tab 1
            dbc.Tab([
                dbc.Card([
                    dbc.CardHeader("Please Select Country:"),
                    dbc.CardBody(
                        dcc.Dropdown(id = "category_promotion",
                                    options = list_category,
                                    value= "department")
                        ),
                        dcc.Graph(id = 'highest_promotion_rate')     
                ])
            ], label = "Ranking"),
            # Tab 2
            dbc.Tab(
                dcc.Graph(id = "distribution_plot",
                         figure = distribution_plot),
                label = "Distribution"
            )
        ])
    ]),


    # COL 1 
    #dbc.Col([
    #    # ROW 1 -> Title & Dropdown
    #    dbc.Row([
    #    html.H1("Promotion Analyis", style= {"textAlign": "center"}),
    #    dbc.Col(width =1),
    #    dbc.Col([
    #        dbc.Card([
    #            dbc.CardHeader("Please Select Country:"),
    #            dbc.CardBody(
    #                dcc.Dropdown(id = "category_promotion",
    #                            options = list_category,
    #                            value= "department")
    #            )
    #        ]),
    #    ], 
    #    width= 10)
    #]),
    #    # ROW 2 -> VISUALIZATION HIGEST PROMOTION RATE
    #    dbc.Row(
    #        dcc.Graph(id = 'highest_promotion_rate')
    #    ),
    #], width = 6),

], style= {
    "paddingLeft": "30px",
    "paddingRight": "30px"
})

])


# CALLBACK DROPDOWN HIGEST PROMOTION RATE
@app.callback(
    Output(component_id='highest_promotion_rate', component_property='figure'),
    Input(component_id='category_promotion', component_property='value')
)
# VISUALIZATION HIGHEST PROMOTION RATE
def update_bar_plot(bar_plot_value):
    promot_gender = pd.crosstab(
        index = promoted_employee[bar_plot_value],
        columns='Percentage',
        normalize = True
    ).sort_values(by='Percentage',ascending=False).round(2).reset_index()
    bar_plot = px.bar(promot_gender,
       x = bar_plot_value,
       y = 'Percentage',
       labels={
          bar_plot_value : str(bar_plot_value.title())
      })
    return bar_plot


# Render Dash
if __name__ == "__main__":
    app.run_server()
