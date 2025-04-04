import dash
from dash import html, dcc, Input, Output
import pandas as pd
from data_loader import df_player_resume

# Exemple dataframe (ajuste-le selon ton cas réel)
df_player_resume = pd.DataFrame({
    'name': ['John', 'Marc', 'Alice'],
    'nickname': ['Johnny', 'Marco', 'Ally']
})

# Création d'une nouvelle instance Dash
test_app = dash.Dash(__name__)

test_app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-name-test',
        options=[{'label': name, 'value': name} for name in df_player_resume['name']],
        value='John'
    ),
    html.Div(id='nickname-display-test')
])

@test_app.callback(
    Output('nickname-display-test', 'children'),
    Input('dropdown-name-test', 'value')
)
def update_nickname(selected_name):
    nickname = df_player_resume.loc[df_player_resume['name'] == selected_name, 'nickname'].values[0]
    return f'Nickname : {nickname}'

if __name__ == '__main__':
    test_app.run(debug=True, port=8051)
