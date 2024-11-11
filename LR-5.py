# Run this app with `python LR-5.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Загрузка данных из CSV файла
data = pd.read_csv('https://docs.google.com/spreadsheets/d/1_yQjOJGR5R0b0YkoD0c_rKo1kH_CXRWqUAmylDpz1ms/export?format=csv')

def generate_table(dataframe, max_rows=100):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

# Создание экземпляра приложения Dash
app = dash.Dash(__name__)

# Определение макета приложения
app.layout = html.Div([
    html.H1("Дашборд для анализа данных о студентских оценках или успеваемости", style={'textAlign': 'center'}),

    # Выпадающий список для выбора предмета
    html.Div([
        html.Label("Выберите предмет:"),
        dcc.Dropdown(
            id='subject-dropdown',
            options=[{'label': subj, 'value': subj} for subj in data['Предмет'].unique()],
            value=data['Предмет'].unique()[0],  # Значение по умолчанию
            clearable=False,
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    # Индикаторы текущих значений оценок
    html.Div(id='current-grades', style={'marginTop': '20px'}),

    # График средней оценки по предмету
    dcc.Graph(id='average-grade-graph'),

    # Выпадающий список для выбора группы
    html.Div([
        html.Label("Выберите группу:"),
        dcc.Dropdown(
            id='group-dropdown',
            options=[{'label': group, 'value': group} for group in data['Группа'].unique()],
            value=data['Группа'].unique()[0],
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),

    # График оценок по группе
    dcc.Graph(id='grades-by-group-graph'),

    # Таблица с ключевыми показателями
    html.Div(id='grades-table', style={'marginTop': '20px'}),

    html.Div([
        html.H4(children='Успеваемость студентов'),
        generate_table(data)  # This call is now valid since generate_table is defined above
    ])
])

# Обновление графика средней оценки по предмету
@app.callback(
    Output('average-grade-graph', 'figure'),
    Input('subject-dropdown', 'value')
)
def update_average_grade_graph(selected_subject):
    filtered_data = data[data['Предмет'] == selected_subject]
    average_grade = filtered_data.groupby('ФИО')['Оценка'].mean().reset_index()

    fig = px.line(average_grade, x='ФИО', y='Оценка', title=f'Оценки по предмету: {selected_subject}')
    return fig

# Обновление графика оценок по группе
@app.callback(
    Output('grades-by-group-graph', 'figure'),
    Input('group-dropdown', 'value')
)
def update_grades_by_group(selected_group):
    filtered_data = data[data['Группа'] == selected_group]

    fig = px.bar(filtered_data, x='ФИО', y='Оценка', color='Предмет',
                 title=f'Оценки для группы {selected_group}')
    return fig

# Запуск сервера
if __name__ == '__main__':
    app.run_server(debug=True)