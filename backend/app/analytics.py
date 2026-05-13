from collections import defaultdict
from statistics import mean
from typing import Dict, List, Tuple
from .sample_data import CUSTOMER_DATA


def _group_average(key: str, metric: str) -> Tuple[List[str], List[float]]:
    groups: Dict[str, List[float]] = defaultdict(list)
    for row in CUSTOMER_DATA:
        groups[row[key]].append(float(row[metric]))
    labels = list(groups.keys())
    values = [round(mean(groups[label]), 3) for label in labels]
    return labels, values


def _group_sum(key: str, metric: str) -> Tuple[List[str], List[float]]:
    groups: Dict[str, float] = defaultdict(float)
    for row in CUSTOMER_DATA:
        groups[row[key]] += float(row[metric])
    labels = list(groups.keys())
    values = [round(groups[label], 2) for label in labels]
    return labels, values


def _product_mix() -> Tuple[List[str], List[float]]:
    labels = [row["product"] for row in CUSTOMER_DATA]
    values = [row["revenue"] for row in CUSTOMER_DATA]
    return labels, values


def _trend(metric: str) -> Tuple[List[str], List[float]]:
    labels = [row["month"] for row in CUSTOMER_DATA]
    values = [round(float(row[metric]), 3) for row in CUSTOMER_DATA]
    return labels, values


def _scatter_risk_revenue():
    labels = [f'{row["region"]} - {row["segment"]}' for row in CUSTOMER_DATA]
    values = [{"x": round(row["risk"], 2), "y": row["revenue"]} for row in CUSTOMER_DATA]
    return labels, values


def resolve_query(message: str) -> dict:
    q = message.lower().strip()

    if any(term in q for term in ["risk", "revenue risk", "scatter"]):
        labels, values = _scatter_risk_revenue()
        return {
            "intent": "risk_vs_revenue",
            "chart_type": "scatter",
            "title": "Revenue Exposure by Customer Risk",
            "labels": labels,
            "values": values,
            "dataset_label": "Risk vs Revenue",
            "insight": "High-risk accounts are concentrated in Consumer and SMB cohorts, especially where revenue remains material.",
            "cause": "Network latency, lower NPS, and higher churn probability are combining into elevated account risk.",
            "recommendation": "Prioritize save-offers, proactive service assurance, and targeted retention campaigns for high-risk revenue pockets.",
            "impact": "Can reduce preventable churn and protect high-value monthly recurring revenue.",
            "confidence": 0.88,
        }

    if any(term in q for term in ["trend", "over time", "monthly", "line"]):
        metric = "churn" if "churn" in q else "revenue"
        labels, values = _trend(metric)
        return {
            "intent": f"{metric}_trend",
            "chart_type": "line",
            "title": f"{metric.title()} Trend by Month",
            "labels": labels,
            "values": values,
            "dataset_label": metric.title(),
            "insight": f"The {metric} trend shows month-to-month variability across the sample customer base.",
            "cause": "Regional mix, product adoption, and service quality differences affect monthly performance.",
            "recommendation": "Use trend alerts to detect deteriorating regions before churn accelerates.",
            "impact": "Improves early intervention and monthly business review quality.",
            "confidence": 0.84,
        }

    if any(term in q for term in ["product", "recommendation mix", "mix", "donut", "pie"]):
        labels, values = _product_mix()
        return {
            "intent": "product_revenue_mix",
            "chart_type": "doughnut",
            "title": "Revenue Mix by Recommended Product",
            "labels": labels,
            "values": values,
            "dataset_label": "Revenue",
            "insight": "Premium connectivity products contribute the largest revenue share in the current portfolio.",
            "cause": "Enterprise customers show higher ARPU and stronger adoption of fiber, MPLS, SD-WAN, and cloud connectivity products.",
            "recommendation": "Bundle security and service assurance offers with high-performing connectivity products.",
            "impact": "Supports upsell motion and improves attach-rate across enterprise accounts.",
            "confidence": 0.86,
        }

    if any(term in q for term in ["segment", "customer type", "enterprise", "smb", "consumer"]):
        metric = "churn" if "churn" in q else "arpu"
        labels, values = _group_average("segment", metric)
        return {
            "intent": f"{metric}_by_segment",
            "chart_type": "bar",
            "title": f"{metric.upper()} by Customer Segment",
            "labels": labels,
            "values": values,
            "dataset_label": metric.upper(),
            "insight": f"Customer segments show materially different {metric.upper()} profiles.",
            "cause": "Enterprise accounts typically have stronger product stickiness, while Consumer and SMB segments are more price and service sensitive.",
            "recommendation": "Create segment-specific retention and upsell strategies instead of one generic campaign.",
            "impact": "Improves campaign precision and reduces wasted retention spend.",
            "confidence": 0.87,
        }

    if any(term in q for term in ["network", "latency", "quality", "nps"]):
        labels, latency = _group_average("region", "latency")
        _, nps = _group_average("region", "nps")
        return {
            "intent": "network_quality_by_region",
            "chart_type": "radar",
            "title": "Network Quality by Region",
            "labels": labels,
            "values": latency,
            "secondary_values": nps,
            "dataset_label": "Latency",
            "secondary_dataset_label": "NPS",
            "insight": "Regions with higher latency tend to show weaker experience scores.",
            "cause": "Service quality degradation directly affects customer satisfaction and churn risk.",
            "recommendation": "Prioritize network optimization in regions where latency is high and NPS is weak.",
            "impact": "Can improve customer experience, lower ticket volume, and reduce churn risk.",
            "confidence": 0.83,
        }

    metric = "churn" if "churn" in q else "revenue"
    if metric == "revenue":
        labels, values = _group_sum("region", metric)
    else:
        labels, values = _group_average("region", metric)

    return {
        "intent": f"{metric}_by_region",
        "chart_type": "bar",
        "title": f"{metric.title()} by Region",
        "labels": labels,
        "values": values,
        "dataset_label": metric.title(),
        "insight": f"The regional view highlights where {metric} needs management attention.",
        "cause": "Regional performance is shaped by product penetration, service quality, and customer segment mix.",
        "recommendation": "Use region-level drilldowns to assign retention, upsell, or network remediation actions.",
        "impact": "Enables faster executive decision-making during telecom business reviews.",
        "confidence": 0.85,
    }
