# app.py for use in Hugging Face, Gradio

import hashlib
from datetime import datetime

import gradio as gr
import joblib
import pandas as pd


# =========================
# 1. Load Models
# =========================
demand_model = joblib.load("demand_model.joblib")
failure_model = joblib.load("delivery_failure_model.joblib")
maintenance_model = joblib.load("maintenance_model.joblib")
FEATURES = joblib.load("features.joblib")


# =========================
# 2. Shared State + Logs
# =========================
shared_state = {}
decision_logs = []


# =========================
# 2B. RAG-lite Knowledge Base
# =========================
# RAG-lite: rule-based retrieval from a structured knowledge base.
# Future upgrade: replace this with vector database + semantic retrieval
# from SOPs, delivery FAQs, maintenance policies, and escalation guides.
SUPPORT_KB = {
    "high_delivery_failure": {
        "question": "What should we do if delivery failure risk is high?",
        "answer": "Confirm customer availability, check address accuracy, choose a safer delivery time slot, and notify the customer before dispatch.",
    },
    "high_maintenance_risk": {
        "question": "What should we do if maintenance risk is high?",
        "answer": "Avoid assigning the vehicle to long routes. Send it for inspection or allocate a backup vehicle.",
    },
    "high_demand": {
        "question": "What should we do if predicted parcel volume is high?",
        "answer": "Prepare extra fleet capacity, allocate more warehouse manpower, and monitor hub congestion.",
    },
    "high_overall_risk": {
        "question": "What should we do if overall risk is high?",
        "answer": "Escalate to supervisor review and prioritize preventive actions before dispatch.",
    },
    "normal_operations": {
        "question": "What if all risks are low?",
        "answer": "Proceed with normal operations while continuing routine monitoring.",
    },
}


# =========================
# 3. Build Input DataFrame
# =========================
def build_input_df(
    distance_km,
    num_stops,
    hub_congestion,
    traffic_level,
    weather_rain,
    vehicle_mileage_km,
    days_since_service,
    driver_experience,
    current_load,
):
    input_df = pd.DataFrame([{
        "distance_km": distance_km,
        "num_stops": num_stops,
        "hub_congestion": hub_congestion,
        "traffic_level": traffic_level,
        "weather_rain": weather_rain,
        "vehicle_mileage_km": vehicle_mileage_km,
        "days_since_service": days_since_service,
        "driver_experience": driver_experience,
        "current_load": current_load,
    }])

    return input_df[FEATURES]


# =========================
# 4. Specialist Agents
# =========================
# This section simulates a simplified multi-agent AI architecture.
# Each agent is responsible for a specific operational task.
def demand_agent(input_df):
    demand = demand_model.predict(input_df)[0]
    shared_state["demand_agent"] = {"predicted_volume": round(float(demand), 2)}
    return demand


def delivery_risk_agent(input_df):
    failure_prob = failure_model.predict_proba(input_df)[0][1]
    shared_state["delivery_risk_agent"] = {
        "failure_probability": round(float(failure_prob), 3)
    }
    return failure_prob


def maintenance_agent(input_df):
    maintenance_prob = maintenance_model.predict_proba(input_df)[0][1]
    shared_state["maintenance_agent"] = {
        "maintenance_probability": round(float(maintenance_prob), 3)
    }
    return maintenance_prob


def support_agent(demand, failure_prob, maintenance_prob, final_risk):
    retrieved_answers = []

    if demand >= 150:
        retrieved_answers.append(SUPPORT_KB["high_demand"]["answer"])

    if failure_prob >= 0.5:
        retrieved_answers.append(SUPPORT_KB["high_delivery_failure"]["answer"])

    if maintenance_prob >= 0.5:
        retrieved_answers.append(SUPPORT_KB["high_maintenance_risk"]["answer"])

    if final_risk >= 0.7:
        retrieved_answers.append(SUPPORT_KB["high_overall_risk"]["answer"])

    if not retrieved_answers:
        retrieved_answers.append(SUPPORT_KB["normal_operations"]["answer"])

    shared_state["support_agent"] = {"retrieved_guidance": retrieved_answers}
    return retrieved_answers


def explain_agent(input_df):
    explanations = []
    row = input_df.iloc[0]

    if row["traffic_level"] > 0.7:
        explanations.append("High traffic level is a major contributor to delivery delay risk.")

    if row["hub_congestion"] > 0.75:
        explanations.append("Severe hub congestion may significantly slow parcel processing.")

    if row["weather_rain"] == 1:
        explanations.append("Rain conditions moderately increase delivery disruption risk.")

    if row["vehicle_mileage_km"] > 160000:
        explanations.append("High vehicle mileage is a strong indicator of breakdown probability.")

    if row["days_since_service"] > 120:
        explanations.append("Overdue servicing increases mechanical failure risk.")

    if row["current_load"] > 70:
        explanations.append("Heavy load increases both handling time and delivery risk.")

    if not explanations:
        explanations.append("No significant risk factors detected.")

    shared_state["explain_agent"] = {"explanations": explanations}
    return explanations


# =========================
# 5. Control Tower Agent
# =========================
# Control Tower combines outputs from multiple agents
# to produce coordinated operational recommendations.
def control_tower_agent(demand, failure_prob, maintenance_prob):
    recommendations = []

    final_risk = (
        0.4 * failure_prob
        + 0.4 * maintenance_prob
        + 0.2 * min(demand / 250, 1)
    )

    if demand >= 150:
        recommendations.append("Prepare extra fleet capacity.")

    if failure_prob >= 0.5:
        recommendations.append("High delivery failure risk — confirm customer availability.")

    if maintenance_prob >= 0.5:
        recommendations.append("Vehicle maintenance required before dispatch.")

    if final_risk >= 0.7:
        recommendations.append("Overall risk is high — assign supervisor review.")

    if not recommendations:
        recommendations.append("Proceed with normal operations.")

    shared_state["control_tower_agent"] = {
        "final_risk_score": round(float(final_risk), 3),
        "recommendations": recommendations,
    }

    return final_risk, recommendations


# =========================
# 6. Master Orchestrator
# =========================
def run_ninjai_system(
    distance_km,
    num_stops,
    hub_congestion,
    traffic_level,
    weather_rain,
    vehicle_mileage_km,
    days_since_service,
    driver_experience,
    current_load,
):
    shared_state.clear()

    input_df = build_input_df(
        distance_km,
        num_stops,
        hub_congestion,
        traffic_level,
        weather_rain,
        vehicle_mileage_km,
        days_since_service,
        driver_experience,
        current_load,
    )

    demand = demand_agent(input_df)
    failure_prob = delivery_risk_agent(input_df)
    maintenance_prob = maintenance_agent(input_df)

    final_risk, recommendations = control_tower_agent(
        demand,
        failure_prob,
        maintenance_prob,
    )

    support_guidance = support_agent(
        demand,
        failure_prob,
        maintenance_prob,
        final_risk,
    )

    explanations = explain_agent(input_df)

    result = {
        "predicted_volume": round(float(demand), 2),
        "failure_probability": round(float(failure_prob), 3),
        "maintenance_probability": round(float(maintenance_prob), 3),
        "final_risk_score": round(float(final_risk), 3),
        "recommendations": recommendations,
        "support_guidance": support_guidance,
        "explanations": explanations,
        "shared_state": shared_state.copy(),
    }

    decision_logs.append(result)
    return result


# =========================
# 6B. Pretty UI Formatter
# =========================
def get_risk_level(risk_score):
    if risk_score >= 0.7:
        return "🔴 High"
    if risk_score >= 0.4:
        return "🟡 Moderate"
    return "🟢 Low"


def format_control_tower_report(result):
    risk_level = get_risk_level(result["final_risk_score"])

    recommendations = "\n".join([f"- {item}" for item in result["recommendations"]])
    guidance = "\n".join([f"- {item}" for item in result["support_guidance"]])
    explanations = "\n".join([f"- {item}" for item in result["explanations"]])

    return f"""
## 🚚 Control Tower Summary
| Metric | Result |
|---|---:|
| 📦 Predicted Parcel Volume | **{result["predicted_volume"]}** |
| ⚠️ Delivery Failure Probability | **{result["failure_probability"]}** |
| 🔧 Maintenance Risk Probability | **{result["maintenance_probability"]}** |
| 🧠 Final Risk Score | **{result["final_risk_score"]}** |
| 🚦 Overall Risk Level | **{risk_level}** |
---
## ✅ Recommended Actions
{recommendations}
---
## 📚 RAG-lite Support Guidance
{guidance}
---
## 🔍 Explainability Notes
{explanations}
"""


def run_control_tower_ui(
    distance_km,
    num_stops,
    hub_congestion,
    traffic_level,
    weather_rain,
    vehicle_mileage_km,
    days_since_service,
    driver_experience,
    current_load,
):
    result = run_ninjai_system(
        distance_km,
        num_stops,
        hub_congestion,
        traffic_level,
        weather_rain,
        vehicle_mileage_km,
        days_since_service,
        driver_experience,
        current_load,
    )

    pretty_report = format_control_tower_report(result)
    return pretty_report, result


# =========================
# 6C. Batch CSV Prediction
# =========================
def run_batch_prediction(csv_file):
    if csv_file is None:
        return pd.DataFrame({"error": ["Please upload a CSV file."]})

    batch_df = pd.read_csv(csv_file.name)

    required_columns = [
        "distance_km",
        "num_stops",
        "hub_congestion",
        "traffic_level",
        "weather_rain",
        "vehicle_mileage_km",
        "days_since_service",
        "driver_experience",
        "current_load",
    ]

    missing_columns = [
        col for col in required_columns
        if col not in batch_df.columns
    ]

    if missing_columns:
        return pd.DataFrame({
            "error": [f"Missing required columns: {missing_columns}"]
        })

    output_rows = []

    for _, row in batch_df.iterrows():
        result = run_ninjai_system(
            distance_km=row["distance_km"],
            num_stops=row["num_stops"],
            hub_congestion=row["hub_congestion"],
            traffic_level=row["traffic_level"],
            weather_rain=row["weather_rain"],
            vehicle_mileage_km=row["vehicle_mileage_km"],
            days_since_service=row["days_since_service"],
            driver_experience=row["driver_experience"],
            current_load=row["current_load"],
        )

        risk_level = get_risk_level(result["final_risk_score"])

        output_rows.append({
            "trip_id": row.get("trip_id", ""),
            "driver_id": row.get("driver_id", ""),
            "vehicle_id": row.get("vehicle_id", ""),
            "route_zone": row.get("route_zone", ""),
            "planned_dispatch_hour": row.get("planned_dispatch_hour", ""),
            "predicted_volume": result["predicted_volume"],
            "failure_probability": result["failure_probability"],
            "maintenance_probability": result["maintenance_probability"],
            "final_risk_score": result["final_risk_score"],
            "risk_level": risk_level,
            "top_recommendation": result["recommendations"][0],
            "explanation_summary": result["explanations"][0],
        })

    return pd.DataFrame(output_rows)


# =========================
# 7. Simulated dApp Proof
# =========================
def create_delivery_proof(parcel_id, driver_id, customer_id, delivery_status):
    proof_data = {
        "parcel_id": parcel_id,
        "driver_id": driver_id,
        "customer_id": customer_id,
        "delivery_status": delivery_status,
        "timestamp_utc": datetime.utcnow().isoformat(),
    }

    proof_string = str(proof_data)
    proof_hash = hashlib.sha256(proof_string.encode()).hexdigest()

    return {
        "proof_data": proof_data,
        "proof_hash": proof_hash,
        "blockchain_status": "Simulated only - not yet written to blockchain",
    }


def view_decision_logs():
    return decision_logs


def clear_decision_logs():
    decision_logs.clear()
    return {"status": "Decision logs cleared."}


# =========================
# 8. Gradio App
# =========================
with gr.Blocks(title="Ninja Van AI Control Tower") as demo:
    gr.Markdown(
        """
        # 🚚 Ninja Van AI Control Tower
        **A multi-agent AI prototype for predictive, explainable, and coordinated logistics decision-making.**
        This demo combines:
        - 📦 Demand forecasting
        - ⚠️ Delivery failure risk prediction
        - 🔧 Predictive maintenance
        - 📚 RAG-lite support guidance
        - 🔍 Explainability
        - 🧠 Control tower recommendations
        - 📂 Batch CSV prediction for daily trip planning
        - 🔐 Simulated dApp proof-of-delivery
        """
    )

    with gr.Tab("🧠 AI Control Tower"):
        with gr.Row():
            with gr.Column():
                distance_km = gr.Number(label="Distance (km)", value=15)
                num_stops = gr.Number(label="Number of Stops", value=6)
                hub_congestion = gr.Slider(0, 1, value=0.8, label="Hub Congestion")
                traffic_level = gr.Slider(0, 1, value=0.7, label="Traffic Level")
                weather_rain = gr.Radio([0, 1], value=1, label="Weather Rain? 0 = No, 1 = Yes")

            with gr.Column():
                vehicle_mileage_km = gr.Number(label="Vehicle Mileage (km)", value=190000)
                days_since_service = gr.Number(label="Days Since Last Service", value=130)
                driver_experience = gr.Number(label="Driver Experience (years)", value=2)
                current_load = gr.Slider(0, 100, value=85, label="Current Load (%)")

        predict_button = gr.Button("🚀 Run Multi-Agent Control Tower")

        pretty_output = gr.Markdown(label="Control Tower Report")
        raw_output = gr.JSON(label="Raw Agent Output")

        predict_button.click(
            fn=run_control_tower_ui,
            inputs=[
                distance_km,
                num_stops,
                hub_congestion,
                traffic_level,
                weather_rain,
                vehicle_mileage_km,
                days_since_service,
                driver_experience,
                current_load,
            ],
            outputs=[pretty_output, raw_output],
        )

    with gr.Tab("📂 Batch CSV Prediction"):
        gr.Markdown(
            """
            ### 📂 Batch CSV Prediction
            Upload a pre-dispatch daily planning CSV.
            Each row represents one planned delivery trip or route.  
            The Control Tower evaluates each row and returns a risk table for operational planning.
            """
        )

        csv_upload = gr.File(
            label="Upload sample_operations_input.csv",
            file_types=[".csv"],
        )

        batch_button = gr.Button("📊 Run Batch Prediction")

        batch_output = gr.Dataframe(
            label="Batch Control Tower Output",
            interactive=False,
            wrap=True,
        )

        batch_button.click(
            fn=run_batch_prediction,
            inputs=[csv_upload],
            outputs=[batch_output],
        )

    with gr.Tab("🔐 Simulated dApp Proof-of-Delivery"):
        parcel_id = gr.Textbox(label="Parcel ID", value="NV001")
        driver_id = gr.Textbox(label="Driver ID", value="D001")
        customer_id = gr.Textbox(label="Customer ID", value="C001")
        delivery_status = gr.Dropdown(
            ["Delivered", "Failed Delivery", "Returned", "Pending"],
            value="Delivered",
            label="Delivery Status",
        )

        proof_button = gr.Button("Generate Proof Hash")
        proof_output = gr.JSON(label="Simulated Blockchain Proof")

        proof_button.click(
            fn=create_delivery_proof,
            inputs=[parcel_id, driver_id, customer_id, delivery_status],
            outputs=proof_output,
        )

    with gr.Tab("📜 Decision Logs"):
        view_logs_button = gr.Button("View Decision Logs")
        clear_logs_button = gr.Button("Clear Decision Logs")
        logs_output = gr.JSON(label="Decision Logs")

        view_logs_button.click(
            fn=view_decision_logs,
            inputs=[],
            outputs=logs_output,
        )

        clear_logs_button.click(
            fn=clear_decision_logs,
            inputs=[],
            outputs=logs_output,
        )


# =========================
# 9. Launch
# =========================
if __name__ == "__main__":
    demo.launch()