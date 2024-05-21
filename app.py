from flask import Flask, render_template, request
import pandas as pd
import plotly.express as px

app = Flask(__name__)

# 데이터 로드
df = pd.read_csv('mnt/data/인구동태건수_및_동태율_추이_출생_사망_혼인_이혼.csv')

@app.route('/')
def index():
    items = df['기본항목별'].unique()
    return render_template('index.html', items=items)

@app.route('/plot', methods=['POST'])
def plot():
    selected_items = request.form.getlist('items')
    filtered_df = df[df['기본항목별'].isin(selected_items)]
    fig = px.line(filtered_df, x='연도', y='값', color='기본항목별', markers=True)
    graph = fig.to_html(full_html=False)
    return render_template('plot.html', graph=graph)

if __name__ == '__main__':
    app.run(debug=True)
