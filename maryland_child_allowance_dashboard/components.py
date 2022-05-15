import time
import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
import base64
import plotly.express as px
import plotly.graph_objects as go
from flask import Flask
from dash.exceptions import PreventUpdate
from dash import dash_table
import charts
import os
import json

# D1D3D4 grey
# f7f7f7 light grey
# fffbff off white
components_colors = {
    "Color": ["Current", "Default"],
    "Main Background": ["white", "white"],
    "Header Background": ["white", "white"],
    "Main Header Text": ["#E02A3E", "#E02A3E"],
    "Containers Background": ["#D1D3D4", "#D1D3D4"],
    "Containers Label": ["black", "black"],
    "Buttons": ["#E02A3E", "#E02A3E"],
    "Buttons Text": ["white", "white"],
    "Logo Text": ["black", "black"],
    "Filters Label": ["black", "black"],
}


def init_header_text():
    header_text = html.Div(
        "Maryland Child Benefit Dashboard",
        id="main_header_text",
        className="main-header",
        style=dict(
            color="#9D2235",
            fontWeight="bold",
            fontSize="",
            marginTop="",
            marginLeft="",
            width="100%",
            paddingTop="1vh",
            paddingBottom="",
            display="flex",
            alignItems="center",
            justifyContent="center",
        ),
    )

    return header_text


def init_header_subtext():
    sub_text = html.Div(
        "A child allowance would send unconditional monthly checks to parents and legal guardians across the state. Parents would receive a check per child. For example, with a $100 monthly child allowance a mother of three would receive $300 monthly to help support her family.",
        id="logo_text",
        className="sub-text",
        style=dict(
            color=components_colors["Logo Text"][0],
            fontWeight="",
            fontSize="",
            marginTop="",
            marginLeft="",
            width="100%",
            paddingTop="0.5vh",
            paddingLeft="",
            paddingBottom="0.5vh",
            display="flex",
            alignItems="center",
            justifyContent="center",
        ),
    )

    return sub_text


def init_table_text():
    table_text = html.Div(
        "Counties with smaller populations may have larger margins of error due to smaller sample sizes in Census data.",
        id="table_text",
        className="table-text",
        style=dict(
            color=components_colors["Logo Text"][0],
            fontWeight="",
            fontSize="",
            marginTop="",
            marginLeft="",
            textAlign="center",
            paddingTop="",
        ),
    )

    return table_text


def init_db_header_text():
    db_header_text = dbc.Col(
        [init_header_text(), init_header_subtext()],
        xs=dict(size=9, offset=0),
        sm=dict(size=9, offset=0),
        md=dict(size=8, offset=0),
        lg=dict(size=8, offset=0),
        xl=dict(size=8, offset=0),
    )

    return db_header_text


# Creating a header for the filters section.
# TODO: fix these path imports
def init_db_logo_img():
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    logo_file = os.path.join(THIS_FOLDER, "mca-logo.png")

    encoded = base64.b64encode(open(logo_file, "rb").read())
    logo_img = html.Div(
        html.Img(
            src="data:image/jpg;base64,{}".format(encoded.decode()),
            id="logo_img",
            height="",
            width="",
            className="mylogo",
        ),
        style=dict(paddingTop="", paddingBottom="",),
    )

    db_logo_img = dbc.Col(
        [logo_img],
        xs=dict(size=3, offset=0),
        sm=dict(size=3, offset=0),
        md=dict(size=2, offset=0),
        lg=dict(size=2, offset=0),
        xl=dict(size=2, offset=0),
    )

    return db_logo_img


filters_header = html.Div(
    html.H1(
        "Apply Filters",
        className="",
        id="filters_header",
        style=dict(
            fontSize="", fontWeight="bold", color="#E02A3E", marginTop=""
        ),
    ),
    style=dict(display="", marginLeft="", textAlign="center", width="100%"),
)

# Creating a radio button with two options: All Children and Young Children.
age_text = html.Div(
    html.H1(
        "Eligible Age Group",
        className="filters-header",
        id="age_text",
        style=dict(
            fontSize="",
            fontWeight="bold",
            color=components_colors["Filters Label"][0],
            marginTop="",
        ),
    ),
    style=dict(display="", marginLeft="", textAlign="left", width="100%"),
)
age_filter = html.Div(
    [
        dbc.RadioItems(
            options=[
                {"label": "All Children (0 - 18)", "value": "all"},
                {"label": "Young Children (0 - 4)", "value": "young"},
            ],
            value="all",
            id="age_filter",
            inline=False,
            label_class_name="filter-label",
            input_class_name="filter-button",
            input_checked_class_name="filter-button-checked",
            input_checked_style=dict(
                backgroundColor="#E02A3E", border="2px solid #E02A3E"
            ),
        ),
    ]
)

age_filter_div = html.Div(
    [age_text, age_filter],
    style=dict(
        fontSize="",
        display="inline-block",
        marginLeft="",
        textAlign="",
        marginBottom="",
        verticalAlign="",
    ),
)

# Creating a radio button with two options.
allowance_text = html.Div(
    html.H1(
        "Child Allowance",
        className="filters-header",
        id="allowance_text",
        style=dict(
            fontSize="",
            fontWeight="bold",
            color=components_colors["Filters Label"][0],
            marginTop="",
        ),
    ),
    style=dict(display="", marginLeft="", textAlign="left", width="100%"),
)
# Creating a radio button that allows the user to select between two options.
allowance_filter = html.Div(
    [
        dbc.RadioItems(
            options=[
                {"label": "$100 Monthly", "value": "100"},
                {"label": "$200 Monthly", "value": "200"},
            ],
            value="200",
            id="allowance_filter",
            inline=False,
            label_class_name="filter-label",
            input_class_name="filter-button",
            input_checked_class_name="filter-button-checked",
            input_checked_style=dict(
                backgroundColor="#E02A3E", border="2px solid #E02A3E"
            ),
        ),
    ]
)

allowance_filter_div = html.Div(
    [allowance_text, allowance_filter],
    style=dict(
        fontSize="",
        display="inline-block",
        marginLeft="3vw",
        textAlign="",
        marginBottom="",
        verticalAlign="",
    ),
)

location_text = html.Div(
    html.H1(
        "Location",
        className="filters-header",
        id="location_text",
        style=dict(
            fontSize="",
            fontWeight="bold",
            color=components_colors["Filters Label"][0],
            marginTop="",
        ),
    ),
    style=dict(display="", marginLeft="", textAlign="left", width="100%"),
)
location_filter = html.Div(
    [
        dbc.RadioItems(
            options=[
                {"label": "County", "value": "county"},
                {"label": "State legislative districts", "value": "districts"},
            ],
            value="county",
            id="location_filter",
            inline=False,
            label_class_name="filter-label",
            input_class_name="filter-button",
            input_checked_class_name="filter-button-checked",
            input_checked_style=dict(
                backgroundColor="#E02A3E", border="2px solid #E02A3E"
            ),
        ),
    ]
)

location_filter_div = html.Div(
    [location_text, location_filter],
    style=dict(
        fontSize="",
        display="inline-block",
        marginLeft="3vw",
        textAlign="",
        marginBottom="",
        verticalAlign="",
    ),
)

filters_button = html.Div(
    [
        dbc.Button(
            "Apply",
            size="lg",
            outline=False,
            color="primary",
            className="me-1",
            n_clicks=0,
            id="filters_button",
            style=dict(
                fontWeight="bold",
                border="1px solid transparent",
                backgroundColor=components_colors["Buttons"][0],
                color=components_colors["Buttons Text"][0],
            ),
        )
    ],
    style=dict(display="block", paddingTop="0.5vh"),
)


filters_buttons_div = html.Div(
    [filters_button],
    style=dict(
        width="100%",
        display="flex",
        alignItems="center",
        justifyContent="center",
    ),
)

filters_div = html.Div(
    [age_filter_div, allowance_filter_div, location_filter_div],
    style=dict(
        width="100%",
        paddingTop="1vh",
        paddingBottom="1vh",
        display="flex",
        alignItems="center",
        justifyContent="center",
    ),
)
