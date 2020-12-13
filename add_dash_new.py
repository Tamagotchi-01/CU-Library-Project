import dash
# import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# marker_colorscale=plotly.colors.sequential.Viridis
# go.Scatter(marker_colorscale=plotly.colors.sequential.Viridis)

# password = [['pigwinner', '123456']]

book_hist_user = pd.read_csv('book_hist_user.csv')

user_cate_type = book_hist_user.groupby(['Category_Lv1', 'type']).size().to_frame().reset_index()
user_cate_type2 = book_hist_user.groupby(['Category_Lv1', 'type_2']).size().to_frame().reset_index()
user_cate_type = user_cate_type[user_cate_type['type'] != 'อื่นๆ']
user_cate_type2 = user_cate_type2[
    (user_cate_type2['type_2'] != 'OtherType') & (user_cate_type2['type_2'] != 'Unidentified')]

df_user = pd.read_csv('df_user.csv')
book_hist_cate1 = pd.read_csv('book_hist_cate1.csv')
book_hist_user_fixnull = pd.read_csv('book_hist_user_fixnull.csv')
n_book_cate = pd.read_csv('n_book_cate.csv')
Top_cat = pd.read_csv('Top_cat.csv')
Top20_eachCat_df = pd.read_csv('Top20_eachCat_df.csv')
topBook_eachCate = pd.read_csv('topBook_eachCate.csv')

markdown_text = '''
References:

Science:
    Faculty of Science
Technology:
    Faculty of Psychology
    Faculty of Engineerings
    Faculty of Veterinary 
    The Petroleum and Petrochemical College
    School of Agricultural Resources
Education:
    Faculty of Education
Management:
    Faculty of Economics
    Faculty of Commerce and Accountancy
    Sasin School of Management
Arts:
    Faculty of Architecture
    Faculty of Fine and Applied Arts 
Languistics:
    Faculty of Arts
Health:
    Faculty of Medicine 
    Faculty of Allied Health Sciences
    Faculty of Pharmaceutical Sciences
    Faculty of Dentistry
    Faculty of Sports Science
    College of Public Health Sciences
    Faculty of Nursing
Social:
    Faculty of Laws
    Faculty of Communication Arts
    Faculty of Political Science
    College of Population Studies
Unidentified:
    No information 
OtherType
    General Patrons (Not Professor or Student)
____________________________________________________________________________

2. dewey decimal classification: 
Dewey Decimal Classification is a proprietary library classification system first published in the United States by Melvil Dewey. The code contains three digits of numbers.

000 – Computer science, information & general works
    000 : Computer science, knowledge & systems
    010 : Bibliographies
    020 : Library & information sciences
    030 : Encyclopedias & books of facts
    040 : Unassigned (formerly Biographies)
    050 : Magazines, journals & serials
    060 : Associations, organizations & museums
    070 : News media, journalism & publishing
    080 : Quotations
    090 : Manuscripts & rare books
100 – Philosophy & psychology
    100 : Philosophy
    110 : Metaphysics
    120 : Epistemology
    130 : Parapsychology & occultism
    140 : Philosophical schools of thought
    150 : Psychology
    160 : Philosophical logic
    170 : Ethics
    180 : Ancient, medieval, & Eastern philosophy
    190 : Modern Western philosophy
200 – Religion
    200 : Religion
    210 : Philosophy & theory of religion
    220 : The Bible
    230 : Christianity
    240 : Christian practice & observance
    250 : Christian orders
    260 : Social & ecclesiastical theology
    270 : History of Christianity
    280 : Christian denominations
    290 : Other religions
300 – Social sciences
    300 : Social sciences
    310 : Statistics
    320 : Political science
    330 : Economics
    340 : Law
    350 : Public administration & military science
    360 : Social problems & social services
    370 : Education
    380 : Commerce, communications & transportation
    390 : Customs, etiquette & folklore
400 – Language
    400 : Language
    410 : Linguistics
    420 : English & Old English languages
    430 : German & related languages
    440 : French & related languages
    450 : Italian, Romanian & related languages
    460 : Spanish, Portuguese, Galician
    470 : Latin & Italic languages
    480 : Classical & modern Greek languages
    490 : Other languages
500 – Pure Science
    500 : Science
    510 : Mathematics
    520 : Astronomy
    530 : Physics
    540 : Chemistry
    550 : Earth sciences & geology
    560 : Fossils & prehistoric life
    570 : Biology
    580 : Plants
    590 : Animals (Zoology)
600 – Technology
    600 : Technology
    610 : Medicine & health
    620 : Engineering
    630 : Agriculture
    640 : Home & family management
    650 : Management & public relations
    660 : Chemical engineering
    670 : Manufacturing
    680 : Manufacture for specific uses
    690 : Construction of buildings
700 – Arts & recreation
    700 : Arts
    710 : Area planning & landscape architecture
    720 : Architecture
    730 : Sculpture, ceramics & metalwork
    740 : Graphic arts & decorative arts
    750 : Painting
    760 : Printmaking & prints
    770 : Photography, computer art, film, video
    780 : Music
    790 : Outline of sports, games & entertainment
800 – Literature
    800 : Literature, rhetoric & criticism
    810 : American literature in English
    820 : English & Old English literatures
    830 : German & related literatures
    840 : French & related literatures
    850 : Italian, Romanian & related literatures
    860 : Spanish, Portuguese, Galician literatures
    870 : Latin & Italic literatures
    880 : Classical & modern Greek literatures
    890 : Other literatures
900 – History & geography
    900 : History
    910 : Geography & travel
    920 : Biography & genealogy
    930 : History of ancient world (to ca. 499)
    940 : History of Europe
    950 : History of Asia
    960 : History of Africa
    970 : History of North America
    980 : History of South America
    990 : History of other areas'''

## ---- Page 1 Prepare
# pie
labels = df_user.groupby('type').size().to_frame().reset_index()['type']
values = df_user.groupby('type').size().to_frame().reset_index()[0]
# heat map
x = book_hist_cate1['type_2']
y = book_hist_cate1['Category_Lv1']
z = book_hist_cate1['BorrowingTimes'].values.tolist()
# top 1 book eah cate
name = topBook_eachCate['title'].unique()
name_2 = topBook_eachCate['Category_Lv1'].unique()
checkout = topBook_eachCate['checkout_total'].unique()

color = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
background = 'whitesmoke'

# color = ['aliceblue', 'aqua', 'aquamarine', 'darkturquoise', 'paleturquoise', 'lightgreen', 'lightpink', 'lightsalmon',
#          'lightseagreen', 'mediumpurple']
trace = []
for i in range(len(name)):
    trace.append(go.Bar(y=[name[i]], x=[checkout[i]],
                        marker_color=color[i],
                        name=name_2[i],
                        orientation='h'))
Type_options = [{'label': 'Patrons Categorized by Acedemic', 'value': 0},
                {'label': 'Patrons Categorized by Profession', 'value': 1}]
Type_options_2 = [{'label': 'Patrons Categorized by Acedemic Degree', 'value': 0},
                  {'label': 'Patrons Categorized by Profession', 'value': 1}]

## ----- Page 2 Prepare
Cate_options = []
for Category in Top20_eachCat_df['Category_Lv1'].unique():
    Cate_options.append({'label': str(Category), 'value': Category})
Top_options = [{'label': 'Top 5', 'value': 5}, {'label': 'Top 10', 'value': 10}, {'label': 'Top 15', 'value': 15},
               {'label': 'Top 20', 'value': 20}]

Field_options = []
for Field in book_hist_cate1['type_2'].unique():
    Field_options.append({'label': str(Field), 'value': Field})

# Type_options = [{'label':'Type1','value':0},{'label':'Type2','value':1}]
# ----------------------------------------------------------------------------------------------------------

app = dash.Dash()
server = app.server

# auth = dash_auth.BasicAuth(app,password)

# style={'margin-top':'100px'}
app.layout = html.Div([
    html.Div([html.H1('Chulalongkorn Central Library')], style={'margin-bottom': '30px', 'textAlign': 'center','backgroundColor':background}),
    html.Div([
        dcc.Tabs([
            dcc.Tab(label='Overview Data', children=[
                html.Div([
                    html.P(),
                    html.Div([
                        html.Div(
                            [dcc.Dropdown(id='type-picker2', options=Type_options, value=Type_options[0]['value'])],
                            style={'width': '50%', 'margin-left': '350px','backgroundColor':background}),
                        html.Div([dcc.Graph(id='useronly_Pie')])
                    ], style={'width': '40%', 'display': 'inline-block'}),
                    html.Div([dcc.Graph(id='books-bar',
                                        figure={'data': [
                                            go.Bar(x=n_book_cate['Book Category'], y=n_book_cate['Number of Books'],
                                                   textposition='auto',marker_color=color[0])],
                                                'layout': go.Layout(title='Total Number of Books by Category',
                                                                    xaxis={'title': 'Book Category'},
                                                                    yaxis={'title': 'Number of Books'},
                                                                    height=500,plot_bgcolor=background,paper_bgcolor=background)}
                                        )], style={'width': '55%', 'display': 'inline-block', 'margin-left': '30px'}),

                    html.Div([dcc.Graph(id='book-bar',
                                        figure={'data': [go.Bar(y=Top_cat['Category_Lv1'], x=Top_cat['checkout_total'],
                                                                orientation='h',marker_color=color[0])],
                                                'layout': go.Layout(title='Number of Borrowed Books by Category',
                                                                    margin={'l': 500, 'r': 300},plot_bgcolor=background,paper_bgcolor=background)
                                                })], style={'margin-top': '20px'}),
                    html.Div([dcc.Graph(id='top1-eachcate',
                                        figure={'data': trace,
                                                'layout': go.Layout(title='The Most Popular Book by Category',
                                                                    margin={'l': 500, 'r': 300},plot_bgcolor=background,paper_bgcolor=background)}
                                        )]),
                    html.Div([dcc.Graph(id='book-heat',
                                        figure={'data': [go.Heatmap(x=x, y=y, z=z, colorscale='Peach')],
                                                'layout': go.Layout(
                                                    title='Heat Map: Demonstrating the number of books in each category that are borrowed by each profession'
                                                    , xaxis={'title': 'Profressions'}, margin={'l': 500, 'r': 400},plot_bgcolor=background,paper_bgcolor=background)
                                                })])
                ])
            ]),
            # --------------------------------------------------------------------------------------------------------
            dcc.Tab(label='More Detail', children=[

                html.Div([
                    html.P(),
                    html.Div([
                        dcc.Dropdown(id='cate-picker', options=Cate_options, value=Top20_eachCat_df['Category_Lv1'][0]),
                    ]),
                    html.P(),

                    html.Div([
                        html.Div([
                            html.Div([dcc.Dropdown(id='type-picker', options=Type_options_2,
                                                   value=Type_options[0]['value'])],
                                     style={'width': '50%', 'margin-left': '350px'}),
                            html.Div([dcc.Graph(id='pie')])
                        ], style={'width': '40%', 'display': 'inline-block'}),

                        html.Div([
                            html.Div([dcc.Graph(id='heatmap')]),
                            html.P([])
                        ], style={'width': '57%', 'display': 'inline-block', 'float': 'right', 'margin-top': '40px'})
                    ]),
                    html.P(),
                    html.Div([
                        dcc.Dropdown(id='top-picker', options=Top_options, value=Top_options[0]['value'])
                    ], style={'width': '20%', 'margin-left': '1100px'}),
                    html.Div([
                        html.Div([dcc.Graph(id='graph')
                                  ])])
                ]),
                html.Div([
                    html.Div([
                        html.Div(
                            [dcc.Dropdown(id='field-picker-x', options=Field_options, value=Field_options[0]['value'])],
                            style={'width': '45%', 'display': 'inline-block'}),
                        html.Div(
                            [dcc.Dropdown(id='field-picker-y', options=Field_options, value=Field_options[0]['value'])],
                            style={'width': '45%', 'display': 'inline-block'})
                    ], style={'width': '40%', 'margin-left': '1000px'}),
                    html.Div([
                        dcc.Graph(id='scatter')
                    ])
                ])
            ]),
            dcc.Tab(label='Reference', children=[
                html.Div([
                    dcc.Markdown(children=markdown_text, style={"white-space": "pre"})
                ])
            ])
        ])
    ],style={'backgroundColor':background})
],style={'backgroundColor':background})


# ----------------------------------------------------------------------------------------------------------
## ---- Page 1 Callback ----
@app.callback(Output('useronly_Pie', 'figure'),
              [Input('type-picker2', 'value')])
def update_pie(selected_type):
    label_1 = df_user.groupby('type').size().to_frame().reset_index()['type']
    value_1 = df_user.groupby('type').size().to_frame().reset_index()[0]
    label_2 = df_user.groupby('type_2').size().to_frame().reset_index()['type_2']
    value_2 = df_user.groupby('type_2').size().to_frame().reset_index()[0]

    label = [label_1, label_2]
    value = [value_1, value_2]
    return {'data': [go.Pie(labels=label[selected_type], values=value[selected_type], hole=.5, marker=dict(colors=color))],
            'layout': go.Layout(title=Type_options[selected_type]['label'] + ' Degree as of 25 August 2020',
                                height=500,plot_bgcolor=background,paper_bgcolor=background)}


## ---- Page 2 Callback -----
@app.callback(Output('graph', 'figure'),
              [Input('cate-picker', 'value'),
               Input('top-picker', 'value')])
def updata_figure(selected_cate, selected_top):
    # Data only for selected year from dropdown
    filtered_df = Top20_eachCat_df[Top20_eachCat_df['Category_Lv1'] == selected_cate][:selected_top]
    return {'data': [go.Bar(y=filtered_df['title'], x=filtered_df['checkout_total'], orientation='h',
                            hovertext=filtered_df['title'],marker_color=color[0])],
            'layout': go.Layout(margin={'l': 400, 'r': 300},
                                title='Top {} Books of {} Category'.format(selected_top, selected_cate), height=600,plot_bgcolor=background,paper_bgcolor=background)}


@app.callback(Output('pie', 'figure'),
              [Input('cate-picker', 'value'),
               Input('type-picker', 'value')])
def update_pie(selected_cate, selected_type):
    label_1 = user_cate_type[user_cate_type['Category_Lv1'] == selected_cate]['type']
    value_1 = user_cate_type[user_cate_type['Category_Lv1'] == selected_cate][0]
    label_2 = user_cate_type2[user_cate_type2['Category_Lv1'] == selected_cate]['type_2']
    value_2 = user_cate_type2[user_cate_type2['Category_Lv1'] == selected_cate][0]
    label = [label_1, label_2]
    value = [value_1, value_2]
    return {'data': [go.Pie(labels=label[selected_type], values=value[selected_type], hole=.5, marker=dict(colors=color))],
            'layout': go.Layout(
                title='Patrons categorized by academic degree and <br>borrow book in {} category'.format(selected_cate),
                height=500,plot_bgcolor=background,paper_bgcolor=background)}


@app.callback(Output('heatmap', 'figure'),
              [Input('cate-picker', 'value')])
def update_heat(selected_cate):
    x = book_hist_user_fixnull[book_hist_user_fixnull['Category_Lv1'] == selected_cate]['type_2']
    y = book_hist_user_fixnull[book_hist_user_fixnull['Category_Lv1'] == selected_cate]['Category_Lv2']
    z = book_hist_user_fixnull[book_hist_user_fixnull['Category_Lv1'] == selected_cate][
        'BorrowingTimes'].values.tolist()
    return {'data': [go.Heatmap(x=x, y=y, z=z, colorscale='Peach')],
            'layout': go.Layout(
                title='Heat Map: Heat Map Demonstrating the relation <br>between sub-Category from {} and profession'.format(
                    selected_cate)
                , xaxis={'title': 'Profressions'}, hovermode='closest', margin={'l': 300, 'r': 200}, height=450,plot_bgcolor=background,paper_bgcolor=background)}


@app.callback(Output('scatter', 'figure'),
              [Input('field-picker-x', 'value'),
               Input('field-picker-y', 'value')])
def update_scatter(selected_field_x, selected_field_y):
    #     selected_field_x = 'art'
    #     selected_field_y = 'sci'
    temp_x = book_hist_cate1[book_hist_cate1['type_2'] == selected_field_x].reset_index()  #
    temp_y = book_hist_cate1[book_hist_cate1['type_2'] == selected_field_y].reset_index()  #
    trace2 = []
    for i in range(len(temp_x)):
        trace2.append(go.Scatter(
            x=temp_x['BorrowingTimes'].to_list()[i:i + 1], y=temp_y['BorrowingTimes'].to_list()[i:i + 1],
            name=temp_x['Category_Lv1'][i],
            mode='markers', marker_line_width=2, marker_size=18,
            marker_color=color[i]
        ))

    return {'data': trace2,
            'layout': go.Layout(
                title='Relationship of Borrowing Between {} Professtion and {} Profession'.format(selected_field_x,
                                                                                                  selected_field_y),
                yaxis_zeroline=False, xaxis_zeroline=False,
                xaxis={'title': selected_field_x}, yaxis={'title': selected_field_y}, margin={'l': 300, 'r': 300},plot_bgcolor=background,paper_bgcolor=background)}


if __name__ == '__main__':
    app.run_server()