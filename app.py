import plotly.express as px
from shiny.express import input, ui, render
from shiny import reactive, req
from shinywidgets import render_plotly, render_widget
import pandas as pd
import palmerpenguins
import seaborn as sns
from shinyswatch import theme


penguins_df = palmerpenguins.load_penguins()

ui.page_opts(
    title="Jeremy's Penguin Interactive App", fillable=True, theme=theme.cyborg
)

with ui.sidebar(position="left", open="open", bg="f8f8f8"):
    ui.h2("Sidebar", style="text-align: center;", bg="#0a0a0a")
    ui.input_selectize(
        "selected_attribute_list",
        "Attribute",
        choices={"bill_length_mm": "Bill Length (mm)", "bill_depth_mm": "Bill Depth (mm)", "flipper_length_mm": "Flipper Length (mm)", "body_mass_g": "Body Mass (g)"},
    )

    
    ui.input_numeric("plotly_bin_count", "Plotly Count", value=25)
    ui.input_slider("seaborn_bin_count", "Seaborn Bins", 1, 100, 50)
    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        choices=["Adelie", "Gentoo", "Chinstrap"],
        selected="Adelie",
        inline=False,
    )
    ui.input_checkbox_group(
        "selected_islands_list",
        "Islands",
        choices=["Torgersen", "Dream", "Biscoe"],
        selected=["Torgersen", "Dream", "Biscoe"],
        inline=False,
    )
    ui.hr()
    ui.a(
        "Jeremy's GitHub",
        href="https://github.com/jfrummel/cintel-02-data",
        target="_blank",
    )

# Main Content


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Data Table", style="text-align: center;")

        @render.data_frame
        def penguins_table():
            return render.DataTable(
                filtered_data(), selection_mode="row", width="400px", height="250px"
            )

    with ui.card(full_screen=True):
        ui.card_header("Data Grid", style="text-align: center;")

        @render.data_frame
        def penguins_grid():
            return render.DataGrid(
                filtered_data(),
                filters=False,
                selection_mode="row",
                width="400px",
                height="250px",
            )


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Histogram", style="text-align: center;")

        @render_widget
        def plot_1():
            histo = px.histogram(
                filtered_data(),
                x=input.selected_attribute_list(),
                nbins=input.plotly_bin_count(),
                color="species",
                
            ).update_layout(
                title={"text": "Palmer Penguins", "x": 0.5},
                yaxis_title="Count",
                xaxis_title=input.selected_attribute_list(),
            )

            return histo

    with ui.card(full_screen=True):
        ui.card_header("Seaborn Histogram", style="text-align: center;")

        @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")
        def plot_2():
            ax = sns.histplot(
                filtered_data(),
                x=input.selected_attribute_list(),
                bins=input.seaborn_bin_count(),
                hue="species",
                element="step",
                legend=True
            )
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selected_attribute_list())
            ax.set_ylabel("Count")
            return ax


with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species", style="text-align: center;")

        @render_plotly
        def plotly_scatterplot():
            scatterplot = px.scatter(
                filtered_data(), x="body_mass_g", y="bill_length_mm", color="species"
            ).update_layout(
                title={"text": "Bill Length vs Penguin Mass"},
                yaxis_title="Bill Length (mm)",
                xaxis_title="Body Mass (g)",
            )
            return scatterplot


# Defining Functions
# ------------------
# Define a function using the def keyword, followed by the function name, parentheses, and a colon.
# The function name should describe what the function does.
# In the parentheses, specify the inputs needed as arguments the function takes.


# Decorators
# ----------
# Use the @ symbol to decorate a function with a decorator.
# Decorators a concise way of calling a function on a function.
# We don't typically write decorators, but we often use them.


@reactive.calc
def filtered_data():
    req(input.selected_species_list())
    req(input.selected_islands_list())
    req(input.selected_attribute_list())
    isSpeciesMatch = penguins_df["species"].isin(input.selected_species_list())
    islandSelect = penguins_df["island"].isin(input.selected_islands_list())
    selectedAttribute = penguins_df[input.selected_attribute_list()]
    return penguins_df[isSpeciesMatch & islandSelect & selectedAttribute]
