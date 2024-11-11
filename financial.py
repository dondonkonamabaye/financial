import panel as pn
import pandas as pd
import hvplot.pandas
import warnings
import mysql.connector
import json
import datetime as dt
import os

warnings.filterwarnings("ignore")
pn.extension('tabulator')


x_largeur = 840
y_largeur = 380
w_largeur = 450

segment = pn.widgets.Button(name="Segment Product Country", button_type="warning", icon="clipboard-data", styles={"width": "100%"})
country = pn.widgets.Button(name="Country", button_type="warning", icon="clipboard-data", styles={"width": "100%"})
product = pn.widgets.Button(name="Segment", button_type="warning", icon="clipboard-data", styles={"width": "100%"})

financial = pn.widgets.Button(name="Financial DataFrame", button_type="warning", icon="clipboard-data", styles={"width": "100%"})
export = pn.widgets.Button(name="Export Data", button_type="warning", icon="clipboard-data", styles={"width": "100%"})


segment.on_click(lambda event: show_page("Page1"))
product.on_click(lambda event: show_page("Page2"))
country.on_click(lambda event: show_page("Page3"))
financial.on_click(lambda event: show_page("Page4"))

export.on_click(lambda event: exportFinExcel())

df = pd.read_excel("Financial.xlsx")

df['Year'] = df['Year'].astype("str")

df_financial = df[['Segment', 'Country', 'Product', 'Discount Band', 'Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit', 'Month Name', 'Year']]

dist_feature_bar_segment = pn.widgets.Select(name=f"% Chiffres Financiéres", options=['Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit'], value='Units Sold')

dist_feature_bar_product = pn.widgets.Select(name=f"% Chiffres Financiéres", options=['Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit'], value='Units Sold')

dist_feature_bar_country = pn.widgets.Select(name=f"% Chiffres Financiéres", options=['Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit'], value='Units Sold')

dist_feature_barh_segment = pn.widgets.Select(name=f"% Chiffres Financiéres", options=['Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit'], value='Units Sold')

dist_feature_barh_product = pn.widgets.Select(name=f"% Chiffres Financiéres", options=['Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit'], value='Units Sold')

dist_feature_barh_country = pn.widgets.Select(name=f"% Chiffres Financiéres", options=['Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit'], value='Units Sold')

dist_feature_scatter_segment = pn.widgets.Select(name=f"% Chiffres Financiéres", options=['Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit'], value='Units Sold')


unique_segment = list(df_financial['Segment'].unique())
select_segment = pn.widgets.Select(name="Segment", options=unique_segment)


@pn.depends(symbol_segment = select_segment)
def details_segment(symbol_segment):
    return df_financial[df_financial['Segment'] == symbol_segment].head(5)


unique_country = list(df_financial['Country'].unique())
select_country_1 = pn.widgets.Select(name="Country", options=unique_country)


@pn.depends(symbol_country_1 = select_country_1)
def details_country_1(symbol_country_1):
    return df_financial[df_financial['Country'] == symbol_country_1].head(5)


select_segment_bar = pn.widgets.Select(name="Segment", options=unique_segment)


@pn.depends(symbol_segment_bar = select_segment_bar)
def bar_segment(symbol_segment_bar):
    return df_financial[df_financial['Segment'] == symbol_segment_bar].hvplot.bar(x="Country", y="Units Sold", rot=45, by='Discount Band', width=x_largeur, height=y_largeur)



select_segment_product_bar = pn.widgets.Select(name="Segment", options=unique_segment)


@pn.depends(symbol_segment_product_bar = select_segment_product_bar)
def bar_segment_product(symbol_segment_product_bar):
    return df_financial[df_financial['Segment'] == symbol_segment_product_bar].hvplot.bar(x="Country", y="Units Sold", rot=45, by='Product', width=x_largeur, height=y_largeur)



unique_country = list(df_financial['Country'].unique())
select_country = pn.widgets.Select(name="Country", options=unique_country)



@pn.depends(symbol_country = select_country)
def details_country(symbol_country):
    return df_financial[df_financial['Country'] == symbol_country]



unique_product = list(df_financial['Product'].unique())
select_product = pn.widgets.Select(name="Product", options=unique_product)



@pn.depends(symbol_product = select_product)
def details_product(symbol_product):
    return df_financial[df_financial['Product'] == symbol_product]



def create_bar_segment(sel_cols):
    avg_df_financial = df_financial.groupby("Segment").mean().reset_index()
    return avg_df_financial.hvplot.bar(x="Segment", y=sel_cols,
                                    rot=45, width=w_largeur, height=320).opts(active_tools=[])


def create_bar_product(sel_cols):
    avg_df_financial = df_financial.groupby("Product").mean().reset_index()
    return avg_df_financial.hvplot.bar(x="Product", y=sel_cols,
                                    rot=45, width=w_largeur, height=320).opts(active_tools=[])


def create_bar_country(sel_cols):
    avg_df_financial = df_financial.groupby("Country").mean().reset_index()
    return avg_df_financial.hvplot.bar(x="Country", y=sel_cols,
                                    rot=45, width=w_largeur, height=320).opts(active_tools=[])

def create_barh_segment(sel_cols):
    avg_df_financial = df_financial.groupby("Segment").mean().reset_index()
    return avg_df_financial.hvplot.line(x="Segment", y=sel_cols,
                                    rot=45, width=w_largeur, height=320).opts(active_tools=[])


def create_barh_product(sel_cols):
    avg_df_financial = df_financial.groupby("Product").mean().reset_index()
    return avg_df_financial.hvplot.line(x="Product", y=sel_cols,
                                    rot=45, width=w_largeur, height=320).opts(active_tools=[])


def create_barh_country(sel_cols):
    avg_df_financial = df_financial.groupby("Country").mean().reset_index()
    return avg_df_financial.hvplot.line(x="Country", y=sel_cols,
                                    rot=45, width=w_largeur, height=320).opts(active_tools=[])

def create_scatter_segment(sel_cols):
    avg_df_financial = df_financial.groupby("Segment").mean().reset_index()
    return avg_df_financial.hvplot.scatter(x="Manufacturing Price", y=sel_cols,
                                    rot=45, width=w_largeur, height=320).opts(active_tools=[])


def exportPivot(df_financial):
    df_financial_pivot = pd.pivot_table(data=df_financial, index=['Segment', 'Product', 'Country'] ,values=['Units Sold', 'Manufacturing Price',  'Sale Price', 'Gross Sales', 
'Discounts', 'Sales', 'COGS', 'Profit'])

    df_financial_pivot['Units Sold'] = df_financial_pivot['Units Sold'].fillna(0)
    df_financial_pivot['Manufacturing Price'] = df_financial_pivot['Manufacturing Price'].fillna(0)

    df_financial_pivot['Sale Price'] = df_financial_pivot['Sale Price'].fillna(0)
    df_financial_pivot['Gross Sales'] = df_financial_pivot['Gross Sales'].fillna(0)

    df_financial_pivot['Discounts'] = df_financial_pivot['Discounts'].fillna(0)
    df_financial_pivot['Sales'] = df_financial_pivot['Sales'].fillna(0)

    df_financial_pivot['COGS'] = df_financial_pivot['COGS'].fillna(0)
    df_financial_pivot['Profit'] = df_financial_pivot['Profit'].fillna(0)

    return df_financial_pivot


df_pivot = exportPivot(df_financial)

select_country_pivot = pn.widgets.Select(name="Country", options=unique_country)


@pn.depends()
def details_country_pivot():
    return df_pivot



def exportFinExcel():
    excel_financial = 'ExcelFinancial.xlsx'

    df_financial_pivot = exportPivot(df_financial)
    df_financial_pivot.to_excel(excel_financial)
    os.system(excel_financial)


def show_page(page_key):
    main_area.clear()
    main_area.append(mapping[page_key])



def CreatePage1():
        return pn.Tabs(

            pn.Column(
                 
                select_segment_bar, bar_segment, name="Bar per Segment - Country by Discount Band",
            ),

            pn.Column(
                 
                select_segment_product_bar, bar_segment_product, name="Bar per Segment - Country by Product",
            ),

            pn.Column(
                pn.Row(
                    pn.Column(
                        pn.pane.Markdown("### Type de Données Financiaire par Année"),
                        dist_feature_scatter_segment,
                        pn.bind(create_scatter_segment, dist_feature_scatter_segment), align="center",
                    ),
                    
                    pn.Column(
                        pn.pane.Markdown("### Type de Données Financiaire par Année"),
                        dist_feature_scatter_segment,
                        pn.bind(create_scatter_segment, dist_feature_scatter_segment), align="center",
                    )
                ), name="Scatter per Manufacturing Price",
            )
        )



def CreatePage2():
        return pn.Column(
        pn.Row(
            pn.Column(
                select_segment, details_segment, name="Top 10 Details per Segment",
            ),

            pn.Column()
        ),

        pn.Row(
            pn.Column(
                pn.pane.Markdown("### Type de Données Financiaire par Année"),
                dist_feature_bar_segment,
                pn.bind(create_bar_segment, dist_feature_bar_segment), align="center", name="Financial Details Line Graph per Segment",
            ),

            pn.Column(
                pn.pane.Markdown("### Type de Données Financiaire par Année"),
                dist_feature_bar_segment,
                pn.bind(create_barh_segment, dist_feature_bar_segment), align="center", name="Financial Details Line Graph per Product",
            ),
        ),
    )


def CreatePage3():
        return pn.Column(
        pn.Row(
            pn.Column(
                select_country_1, details_country_1, name="Top 10 Details per Country",
            ),

            pn.Column()
        ),
            
        pn.Row(
            pn.Column(
                pn.pane.Markdown("### Type de Données Financiaire par Année"),
                dist_feature_bar_country,
                pn.bind(create_bar_country, dist_feature_bar_country), align="center", name="Financial Details Line Graph per Country",
            ),

            pn.Column(
                pn.pane.Markdown("### Type de Données Financiaire par Année"),
                dist_feature_bar_country,
                pn.bind(create_barh_country, dist_feature_bar_country), align="center", name="Financial Details Line Graph per Country",
            )
        ),
        )


def CreatePage4():
        return pn.Column(
                details_country_pivot, name="Top 10 Details per Country",
            )


mapping = { 
    "Page1": CreatePage1(), 
    "Page2": CreatePage2(), 
    "Page3": CreatePage3(),
    "Page4": CreatePage4(), 
}


logout   =  pn.widgets.Button(name="Déconnexion", button_type="warning", icon="clipboard-data", styles={"width": "100%"})
logout.js_on_click(code="""window.location.href = './logout'""")

sidebar = pn.Column(pn.pane.Markdown("## Menu"), segment, product, country, financial, export, logout, styles={"width": "100%", "padding": "15px"})
main_area = pn.Column(mapping['Page1'], styles={"width":"100%"})

template = pn.template.FastListTemplate(
    title=f"""Bienvenue {pn.state.user}""",
    sidebar=[sidebar],
    main=[main_area],
    header_background="#47C7DA",
    accent_base_color="#47C7DA",
    site="Dashboard for Financial Data Visualisation",  logo="logo.png", 
    # theme=pn.template.DarkTheme,
    sidebar_width=250,
    busy_indicator=None,
)

template.servable()