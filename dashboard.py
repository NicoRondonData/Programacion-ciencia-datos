# Primero, asegúrate de tener Dash instalado:
# pip install dash

import dash
from dash import html, dcc, Input, Output
import plotly.express as px
import  pandas as pd
import  numpy as np


df_wine_combined = pd.read_csv("winequality_combined.csv")
# Crea una aplicación Dash
app = dash.Dash(__name__)

# Define el layout de la aplicación
app.layout = html.Div([
    html.H1("Dashboard de Calidad de Vinos"),
    html.Label("Selecciona el rango de calidad del vino:"),

    # Dropdown para selección de calidad del vino
    dcc.Dropdown(
        id='quality-dropdown',
        options=[
            {'label': 'Alta', 'value': 'alta'},
            {'label': 'Baja', 'value': 'baja'}
        ],
        value='alta'  # Valor por defecto
    ),

    # Gráfico de la matriz de correlación
    dcc.Graph(id='correlation-graph'),


])


@app.callback(
    Output('correlation-graph', 'figure'),
    [Input('quality-dropdown', 'value')]
)
def update_correlation_graph(selected_quality):
    # Filtrar el dataframe basado en la calidad seleccionada
    filtered_df = df_wine_combined[df_wine_combined['quality_label'] == selected_quality]

    # Seleccionar solo las columnas numéricas para la correlación
    numeric_filtered_df = filtered_df.select_dtypes(include=[np.number])

    # Calcular la matriz de correlación para el dataframe filtrado numérico
    correlation_matrix = numeric_filtered_df.corr()

    # Crear la figura de la matriz de correlación
    fig = px.imshow(correlation_matrix, text_auto=True)
    return fig


# Correr el servidor
if __name__ == '__main__':
    app.run_server(debug=True)
