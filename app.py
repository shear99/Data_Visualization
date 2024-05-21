from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# 데이터 로드 및 전처리
file_path = 'mnt/data/인구동태건수_및_동태율_추이_출생_사망_혼인_이혼.csv'
df = pd.read_csv(file_path)
df_long = df.melt(id_vars=['기본항목별'], var_name='연도', value_name='값')
df_long['연도'] = df_long['연도'].str.extract('(\d+)').astype(int)

@app.route('/')
def index():
    items = df['기본항목별'].unique()
    return render_template('index.html', items=items)

@app.route('/plot', methods=['POST'])
def plot():
    selected_items = request.form.getlist('items')
    filtered_df = df_long[df_long['기본항목별'].isin(selected_items)]
    fig = px.line(filtered_df, x='연도', y='값', color='기본항목별', markers=True)
    graph = fig.to_html(full_html=False)
    return render_template('plot.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
