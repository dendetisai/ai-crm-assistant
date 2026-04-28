import json
from agent import run_agent


# -----------------------------
# 🔧 Helper: Clean LLM Output
# -----------------------------
def clean_json_response(response):
    try:
        cleaned = response.replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned)
    except:
        return {
            "error": "Invalid JSON from LLM",
            "raw_output": response
        }


# -----------------------------
# 1. Log Interaction Tool
# -----------------------------
def log_interaction_tool(user_input):
    prompt = f"""
You are an AI assistant for a pharmaceutical CRM system.

Extract structured data from this interaction:

{user_input}

STRICT RULE:
- Return ONLY valid JSON
- Do NOT change field names

Format:

{{
    "hcp_name": "",
    "product_discussed": "",
    "interaction_notes": "",
    "interaction_summary": "",
    "next_action": ""
}}
"""

    result = run_agent(prompt)
    return clean_json_response(result)


# -----------------------------
# 2. Edit Interaction Tool
# -----------------------------
def edit_interaction_tool(existing_data, user_request):
    prompt = f"""
You are an AI assistant for editing CRM interaction data.

Existing Data:
{existing_data}

User Request:
{user_request}

STRICT RULE:
- Return ONLY valid JSON
- Do NOT change field names

Format:

{{
    "hcp_name": "",
    "product_discussed": "",
    "interaction_notes": "",
    "interaction_summary": "",
    "next_action": ""
}}
"""

    result = run_agent(prompt)
    return clean_json_response(result)


# -----------------------------
# 3. Summarize Interaction Tool
# -----------------------------
def summarize_interaction_tool(text):
    prompt = f"""
Summarize this doctor interaction in 1 line:

{text}
"""
    return run_agent(prompt)


# -----------------------------
# 4. Next Best Action Tool
# -----------------------------
def next_best_action_tool(text):
    prompt = f"""
Based on this interaction, suggest the next best action:

{text}
"""
    return run_agent(prompt)


# -----------------------------
# 5. Extract Insights Tool
# -----------------------------
def extract_insights_tool(text):
    prompt = f"""
Extract key insights:
- Doctor interest level
- Opportunity
- Risk

{text}
"""
    return run_agent(prompt)


# -----------------------------
# 🔥 TEST BLOCK
# -----------------------------
if __name__ == "__main__":
    text = "Met Dr. Sharma. Discussed insulin. He is interested."

    print("\n🔹 Log Interaction:\n", log_interaction_tool(text))

    edit_request = "Change next_action to Monday and add send brochure"
    print("\n🔹 Edit Interaction:\n", edit_interaction_tool(text, edit_request))

    print("\n🔹 Summary:\n", summarize_interaction_tool(text))
    print("\n🔹 Next Action:\n", next_best_action_tool(text))
    print("\n🔹 Insights:\n", extract_insights_tool(text))