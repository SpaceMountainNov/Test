
print('Please wait while the program is loading...')

layout = dbc.Container(
            [
        # dcc.Store stores the intermediate value
        dcc.Store(id='intermediate-value'),
        
        dbc.Row(
            id ="data_row",
        ),

        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Label("x-Achse"),
                        dcc.Dropdown(
                            id="data-x-label",
                            options=[
                                {"label": s, "value": s} for s in df.keys()
                            ],
                            className="dropdown",
                            #style={'width': '95%', 'margin':'auto', },
                            disabled = False,
                            clearable= False,
                            value = 'laufleistung'
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("y-Achse"),
                        dcc.Dropdown(
                            id="data-y-label",
                            options=[
                                {"label": s, "value": s} for s in df.keys() 
                            ],
                            className="dropdown",
                            #style={'width': '95%', 'margin':'auto', },
                            value = df.keys()[ next(i for i, string in enumerate(df.keys()) if 'soc' in str.lower(string))] #suche mir in der liste eine kombination die den Substring 'soc' enthält. Unabhängig davon ob der derTeilstring im Suchstring uppercase oder lowercase ist ist
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("z-Achse"),
                        dcc.Dropdown(
                            id="vehicle-datasets",
                            options=[
                                {"label": s, "value": s} for s in df.keys()
                            ],
                            className="dropdown",
                            #multi = True,
                            #style={'width': '95%', 'margin':'auto', },
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("z-Werte"),
                        dcc.Dropdown(
                            id="z-values",
                            options=[
                                {"label": s, "value": s} for s in ["empty"] #["VW","SK","AU","SE"] #HArdCoded für Test. Wird bei auswahl von id="vehicle-datasets" überladen
                            ],
                            className="dropdown",
                            #multi = True,
                            disabled = False,
                            #style={'width': '95%', 'margin':'auto', },
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.Label("kilometer selection"),
                        html.Div(
                            [
                                dcc.RangeSlider( 
                                    min = df.laufleistung.min(),
                                    max = df.laufleistung.max(), 
                                    id = "distance-slider",
                                    step=None,
                                    marks={km: str(km) for km in range(int(df.laufleistung.min()),
                                                                        int(df.laufleistung.max() + 1), 
                                                                        int(math.floor((df.laufleistung.max() - df.laufleistung.min())/9)),
                                                                    )
                                    },
                                    value=[ df.laufleistung.min(), df.laufleistung.max()],
                                ),
                            ],
                            className = 'range',
                            #style={'width': '93%', 'margin':'auto', },                
                        ),
                    ],
                    width = 4,
                ),
            ],
            id = 'row-input'
        ),

        dbc.Row(
            [   
                dbc.Col(
                    dbc.Card(
                        [
                            dbc.CardHeader("Selected Protocol Datasets"),
                            dbc.CardBody(
                                [   
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dbc.Row(
                                                                        [    
                                                                            dbc.Col(
                                                                                dcc.Dropdown(
                                                                                    id="choose-labelForFilter",
                                                                                    options=[
                                                                                        {"label": s, "value": s} for s in df.keys() 
                                                                                    ],
                                                                                    className="dropdown",
                                                                                    style={'width': '100%', 'margin':'auto', },
                                                                                    placeholder = 'wähle label',
                                                                                    clearable=True,
                                                                                    #style={'margin':'auto', },
                                                                                ), 
                                                                                width = 5  
                                                                            ),                             
                                                                            dbc.Col(
                                                                                dcc.Dropdown(
                                                                                    id="choose-comparisonOperators",
                                                                                    options=[
                                                                                        {"label": s, "value": s} for s in ['>', '>=', '==', '<=', '<']
                                                                                    ],
                                                                                    className="dropdown",
                                                                                    style={'width': '100%', 'margin':'auto', },
                                                                                    placeholder = 'wähle Vergleichsoperator',
                                                                                    clearable=True,
                                                                                    #style={'margin':'auto', },
                                                                                ),
                                                                                width = 1
                                                                            ),
                                                                            dbc.Col(
                                                                                dcc.Input(
                                                                                    id = "input-numericBorder",
                                                                                    type = "text",
                                                                                    #size = "30",
                                                                                    placeholder = " search value",
                                                                                    debounce= False,
                                                                                    #style={"lineHeight": "inherit"},                 
                                                                                    style={ 'width': '100%', 
                                                                                            'height': '95%', 
                                                                                            'margin':'auto',
                                                                                            'borderRadius': '5px',
                                                                                            'overflow': 'hidden',
                                                                                            'border': '2px solid lightgrey'},
                                                                                    
                                                                                    #style={'marginRight':'10px', 'width': '100%'},
                                                                                ),
                                                                                width = 4,
                                                                            ),

                                                                            dbc.Col(
                                                                                dbc.Button( "Add", color="primary", id= "button-addFilterOption" , n_clicks=0, style = { 'width' : '100%', 'margin': 'auto', 'display' : 'inline-block', 'white-space':'nowrap' }, disabled= True),
                                                                                width = 2
                                                                            ),
                                                                        ],
                                                                        style = { 'margin-top': '10px'},
                                                                    ),
                                                                )
                                                            ]
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dcc.Store(id='filter-persistance'),
                                                                dbc.Col(
                                                                    dcc.Dropdown(
                                                                        id="choose-logicalOperator",
                                                                        options=[
                                                                            {"label": s[0], "value": s[0], 'disabled': s[1]} for s in [['and', False], [ 'or', False] , [ 'nor', True] , ['xor', True]]
                                                                        ],
                                                                        className="dropdown",
                                                                        style={'width': '100%', 'margin':'auto', },
                                                                        placeholder = 'wähle logischen Operator',
                                                                        clearable=True,
                                                                    ),
                                                                    width = 1
                                                                ),
                                                                dbc.Col(                                                       
                                                                        dcc.Dropdown( id = 'display-actualFilter' ,options = [] , placeholder = 'Filteroptioen', multi=True, disabled=False),
                                                                        width = 9
                                                                ),
                                                                dbc.Col( dbc.Button( "Apply", color="primary", id= "button-addFilter" , n_clicks=0, style = { 'width' : '100%', 'heigth' : '100%' ,'margin': 'auto', 'display' : 'inline-block', 'white-space':'nowrap', 'font-size': 'clamp (0.4rem, 3vw, 1.4rem);'  }, disabled = True),  width = 2)
                                                            ],
                                                            style = { 'margin-top': '10px'},
                                                        ),
                                                    ]
                                                ),

                                        ]  
                                    ),
                                    
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                dataTable(1, True, 11, True, persist = True), #data_table11
                                                #width = 4
                                                
                                            ),
                                        ],
                                        #style = { 'margin': 'auto'}
                                        style = { 'margin-top': '10px'},
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(       
                                                #dataTable(2, True, 12, True, "keine Filter"),
                                                #width = 4
                                                #dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in testdf.columns])   
                                            )
                                        ],
                                        #style = { 'margin': 'auto'}
                                        #style = { 'margin-top': '10px'},
                                    ),
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    
                                                ]
                                            ),
                                        ]
                                    )


                                ]                
                            ),

                        ]
                    ),
                width = 5
                ),
                dbc.Col(
                        dbc.Row(

                            id  =  "data-table-inline",
                            style={ 'margin': 'auto', 'width': '98%'} # 'width': '71%'
                            
                        ),
                    width = 7,
                ),

            ],
            id = 'filter-table',
            style = { 'margin-top': '25px', }, 
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("boxplot binning"), 
                        dcc.Dropdown(
                            id="choose-binning-boxplot",
                            options=[
                                {"label": s, "value": s} for s in ['2500', '5000', '7500','10000', '12500','15000']
                            ],
                            className="dropdown",
                            style={'width': '100%', 'margin':'auto', },
                            clearable=False,
                            value = '5000'
                        ),
                    ],
                    width=1
                ),
                dbc.Col(
                    [
                        dbc.Label("boxplot modus"),
                        dcc.Dropdown(
                            id="scatter-chooser",
                            options=[
                                {"label": s, "value": s} for s in ['solo', 'multi']
                            ],
                            className="dropdown",
                            style={'width': '100%', 'margin':'auto', },
                            clearable=False,
                            value = 'solo'
                        ),
                    ],
                    width= 1,
                ),
                dbc.Col(
                    daq.ToggleSwitch(
                        id = 'two-charts-toggle',
                        value = False
                    ),
                    width= 1
                ),
                dbc.Col(
                    [
                        dcc.Store(id='numberOfDT10'),
                        dbc.ButtonGroup( 
                            [
                                dbc.Button("-", outline=True, color="primary", id = "minus_table10"),
                                dbc.Button("+", outline=True, color="primary", id = "plus_table10" ),
                            ],
                            id="plus-minus_table10"
                        ),
                    ],

                    width={"size": 2, "order": "last", "offset": 5},
                )
            ],
            style={ 'margin-top': '8px', 'margin-bottom' :'8px'},
            align = 'center',
        ),

        dbc.Row(
            [
                dbc.Col(
                    [  

                        html.Hr(),
                        dbc.Alert(

                            "Hello! I am an alert",
                            id="alert-fade",
                            dismissable=True,
                            is_open=False,
                        ),
                        #html.Div(id="accordion-contents"), #className="mt-3"
                    ],
                    #width = 12,
                )
            ],
        ),
    ],
    fluid = True
)
