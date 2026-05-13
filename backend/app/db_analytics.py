from typing import Dict, List, Tuple, Any
from .database import query_rows

def parse_query(query: str) -> str:
    q = query.lower()
    has_region = any(x in q for x in ['region', 'east', 'west', 'north', 'south', 'geo', 'map'])
    has_segment = any(x in q for x in ['segment', 'enterprise', 'smb', 'consumer', 'customer type'])
    if any(x in q for x in ['risk', 'exposure', 'scatter']): return 'risk_vs_revenue'
    if any(x in q for x in ['trend', 'monthly', 'over time', 'line']): return 'churn_trend' if 'churn' in q else 'revenue_trend'
    if any(x in q for x in ['product', 'mix', 'donut', 'pie']): return 'product_revenue_mix'
    if any(x in q for x in ['network', 'latency', 'quality', 'nps']): return 'network_quality_by_region'
    if any(x in q for x in ['arpu']) and has_segment: return 'arpu_by_segment'
    if any(x in q for x in ['revenue', 'sales', 'mrr']) and has_segment: return 'revenue_by_segment'
    if any(x in q for x in ['churn', 'loss', 'retention']) and has_segment: return 'churn_by_segment'
    if any(x in q for x in ['revenue', 'sales', 'mrr']) and has_region: return 'revenue_by_region'
    if any(x in q for x in ['churn', 'loss', 'retention']) and has_region: return 'churn_by_region'
    if any(x in q for x in ['discount']): return 'discount_analysis'
    if any(x in q for x in ['revenue', 'sales', 'mrr']): return 'revenue_by_region'
    return 'churn_by_region'

def _run_intent(intent: str) -> Tuple[str, List[str], List[Any], str, str]:
    if intent == 'churn_by_region':
        rows = query_rows('SELECT region AS label, ROUND(AVG(churn),3) AS value FROM customers GROUP BY region ORDER BY value DESC')
        return 'bar', [r['label'] for r in rows], [r['value'] for r in rows], 'Churn by Region', 'Avg Churn'
    if intent == 'revenue_by_region':
        rows = query_rows('SELECT region AS label, ROUND(SUM(revenue),2) AS value FROM customers GROUP BY region ORDER BY value DESC')
        return 'bar', [r['label'] for r in rows], [r['value'] for r in rows], 'Revenue by Region', 'Revenue'
    if intent == 'churn_by_segment':
        rows = query_rows('SELECT segment AS label, ROUND(AVG(churn),3) AS value FROM customers GROUP BY segment ORDER BY value DESC')
        return 'bar', [r['label'] for r in rows], [r['value'] for r in rows], 'Churn by Segment', 'Avg Churn'
    if intent == 'revenue_by_segment':
        rows = query_rows('SELECT segment AS label, ROUND(SUM(revenue),2) AS value FROM customers GROUP BY segment ORDER BY value DESC')
        return 'bar', [r['label'] for r in rows], [r['value'] for r in rows], 'Revenue by Segment', 'Revenue'
    if intent == 'arpu_by_segment':
        rows = query_rows('SELECT segment AS label, ROUND(AVG(arpu),2) AS value FROM customers GROUP BY segment ORDER BY value DESC')
        return 'bar', [r['label'] for r in rows], [r['value'] for r in rows], 'ARPU by Segment', 'ARPU'
    if intent == 'product_revenue_mix':
        rows = query_rows('SELECT product AS label, ROUND(SUM(revenue),2) AS value FROM customers GROUP BY product ORDER BY value DESC')
        return 'doughnut', [r['label'] for r in rows], [r['value'] for r in rows], 'Revenue Mix by Product', 'Revenue'
    if intent in ['churn_trend','revenue_trend']:
        metric = 'churn' if intent == 'churn_trend' else 'revenue'
        agg = 'AVG' if metric == 'churn' else 'SUM'
        rows = query_rows(f'SELECT month AS label, ROUND({agg}({metric}),3) AS value FROM customers GROUP BY month ORDER BY month')
        return 'line', [r['label'] for r in rows], [r['value'] for r in rows], f'{metric.title()} Trend', metric.title()
    if intent == 'risk_vs_revenue':
        rows = query_rows('SELECT region || " - " || segment AS label, ROUND(risk,2) AS x, ROUND(revenue,2) AS y FROM customers ORDER BY risk DESC')
        return 'scatter', [r['label'] for r in rows], [{'x': r['x'], 'y': r['y']} for r in rows], 'Revenue Exposure by Customer Risk', 'Risk vs Revenue'
    rows = query_rows('SELECT region AS label, ROUND(AVG(latency),2) AS latency, ROUND(AVG(nps),2) AS nps FROM customers GROUP BY region')
    return 'radar', [r['label'] for r in rows], [r['latency'] for r in rows], 'Network Quality by Region', 'Latency'

def insight_for(intent: str, labels: List[str], values: List[Any]) -> Dict[str, Any]:
    top_label = labels[0] if labels else 'N/A'
    if intent.startswith('churn'):
        return {'insight': f'Highest churn concentration is in {top_label}.','cause':'Likely service-quality, pricing, or plan-fit pressure in that cohort.','recommendation':'Launch targeted retention offers and proactive service assurance for the highest-risk cohort.','impact':'Can reduce preventable churn by 8-12% in the managed cohort.','confidence':0.91}
    if intent.startswith('revenue') or intent == 'product_revenue_mix':
        return {'insight': f'{top_label} is the strongest revenue contributor.','cause':'Higher ARPU, product penetration, or enterprise concentration is driving the result.','recommendation':'Prioritize upsell bundles and account expansion where revenue density is highest.','impact':'Improves revenue focus and sales campaign ROI.','confidence':0.89}
    if intent == 'risk_vs_revenue':
        return {'insight':'Revenue exposure is visible where high-risk accounts still carry material value.','cause':'Churn risk, network issues, and weak satisfaction can combine into revenue leakage.','recommendation':'Create a save desk queue ranked by risk-weighted revenue.','impact':'Protects high-value customers before churn occurs.','confidence':0.88}
    return {'insight':'Network quality differs by region and should be reviewed against churn/NPS.','cause':'Latency and customer experience variance affect retention.','recommendation':'Prioritize remediation in high-latency regions with weak NPS.','impact':'Improves NPS, lowers tickets, and reduces churn risk.','confidence':0.86}

def resolve_db_query(message: str) -> dict:
    intent = parse_query(message)
    chart_type, labels, values, title, dataset_label = _run_intent(intent)
    return {'intent': intent, 'chart_type': chart_type, 'title': title, 'labels': labels, 'values': values, 'dataset_label': dataset_label, **insight_for(intent, labels, values)}
