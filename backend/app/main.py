from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .models import ChatRequest, ChatResponse, ChartPayload, ChartDataset, InsightPayload
from .database import init_db, query_rows
from .db_analytics import resolve_db_query

app = FastAPI(title='Telecom Intelligence Assistant API', version='2.0.0')
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])

@app.on_event('startup')
def startup():
    init_db()

@app.get('/health')
def health():
    return {'status':'ok','service':'Telecom Intelligence Assistant API','architecture':'No LLM · Intent → SQL → Chart → Insight'}

@app.get('/database/status')
def database_status():
    return init_db()

@app.get('/kpis')
def kpis():
    row = query_rows('SELECT ROUND(SUM(revenue),2) total_revenue, ROUND(AVG(churn),3) avg_churn, ROUND(AVG(arpu),2) avg_arpu, ROUND(AVG(nps),1) avg_nps, COUNT(*) rows FROM customers')[0]
    return row

@app.get('/sample-data')
def sample_data():
    return query_rows('SELECT * FROM customers ORDER BY id')

@app.get('/geo/regions')
def geo_regions():
    return query_rows('''SELECT region, ROUND(AVG(churn),3) AS churn, ROUND(SUM(revenue),2) AS revenue, ROUND(AVG(nps),1) AS nps, ROUND(AVG(latency),1) AS latency FROM customers GROUP BY region ORDER BY churn DESC''')

@app.post('/chat', response_model=ChatResponse)
def chat(req: ChatRequest):
    routed = resolve_db_query(req.message)
    datasets = [ChartDataset(label=routed['dataset_label'], data=routed['values'])]
    chart = ChartPayload(type=routed['chart_type'], title=routed['title'], labels=routed['labels'], datasets=datasets, xAxis='Risk' if routed['chart_type']=='scatter' else None, yAxis='Revenue' if routed['chart_type']=='scatter' else None, meta={'source':'sqlite_intent_to_sql','llm_required':False})
    analysis = InsightPayload(insight=routed['insight'], cause=routed['cause'], recommendation=routed['recommendation'], impact=routed['impact'], confidence=routed['confidence'])
    return ChatResponse(response_type='chart', intent=routed['intent'], chart=chart, analysis=analysis, answer=f"Generated {routed['title']} using deterministic Intent → SQL → Chart routing.")
