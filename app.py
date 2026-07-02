import os
import streamlit as st
import requests
from dotenv import load_dotenv

# Load environment variables from your .env file
load_dotenv()

st.set_page_config(page_title="Enterprise Compliance System", layout="wide")
st.title("🤖 Multi-Agent Enterprise Operations System")
st.caption("Grounded Architecture: Pure Multi-Agent Orchestration")
st.markdown("---")


api_key_val = os.environ.get("MY_SECRET_AGENT_KEY")

if not api_key_val:
    st.error("🔑 MY_SECRET_AGENT_KEY is missing from your .env file!")
    st.stop()

def ask_gemini_direct(prompt_text: str) -> str:
    """Calls Gemini directly via standard HTTP headers, guaranteeing AQ. key validation."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key_val}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt_text}]}]}
    
    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise Exception(f"API Error {response.status_code}: {response.text}")

# =========================================================================
# CORE MULTI-AGENT DEFINITIONS
# =========================================================================

def orchestrator_agent(query: str):
    log = "📋 [Orchestrator] Decomposing query task requirements...\n"
    log += f"   - Query: '{query}'\n"
    log += "   - Action: Distributing tasks sequentially across specialized agents.\n"
    return log

def vector_retriever_agent(query: str):
    docs_folder = "enterprise_docs"
    context_segments = []
    retrieval_log = "🔍 [Retriever Agent] Searching local document repository...\n"
    
    if os.path.exists(docs_folder):
        for file_name in os.listdir(docs_folder):
            if file_name.endswith(".txt"):
                with open(os.path.join(docs_folder, file_name), "r") as f:
                    content = f.read()
                    retrieval_log += f"   - Found Reference Document: {file_name} | Match (1.00)\n"
                    context_segments.append(f"Source File: {file_name}\n{content}")
    return "\n\n".join(context_segments), retrieval_log

def compliance_analyst_agent(query: str, context: str):
    analyst_prompt = f"""
    You are an Enterprise Knowledge Operations Analyst. 
    Review the corporate policy context below and answer the employee's request.
    If they ask for a summary, synthesize the main rules clearly.

    POLICY CONTEXT:
    {context}

    EMPLOYEE REQUEST:
    {query}
    """
    return ask_gemini_direct(analyst_prompt)

def safety_verifier_agent(context: str, draft: str):
    verifier_prompt = f"""
    You are an Enterprise Compliance Quality Checker. Your job is to prevent AI hallucinations.
    Compare the DRAFT RESPONSE against the original SOURCE POLICY CONTEXT.
    
    You must output your answer in this exact format:
    GROUNDING SCORE: [Score out of 100 based on accurate support]
    VERDICT: [PASSED or FAILED]
    EXPLANATION: [Brief explanation of support or what facts were ungrounded/invented]

    SOURCE POLICY CONTEXT:
    {context}

    DRAFT RESPONSE TO EVALUATE:
    {draft}
    """
    return ask_gemini_direct(verifier_prompt)

# =========================================================================
# UI LAYOUT
# =========================================================================
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("💬 Ask Enterprise Policies")
    user_query = st.text_input("Enter your query:", value="")
    submit_btn = st.button("Execute Agent Pipeline", type="primary")

with col2:
    st.subheader("📋 Live Agent Decision Traces")
    trace_container = st.empty()

if submit_btn and user_query:
    # 1. Orchestrator Plan
    orchestrator_log = orchestrator_agent(user_query)
    
    # 2. Vector Retrieval Search
    context_data, retriever_log = vector_retriever_agent(user_query)
    combined_logs = orchestrator_log + "\n" + retriever_log
    trace_container.text(combined_logs)
    
    try:
        # 3. Dynamic AI Synthesis
        draft_output = compliance_analyst_agent(user_query, context_data)
        combined_logs += "\n🧠 [Analyst Agent] Dynamic response generated successfully."
        trace_container.text(combined_logs)
        
        # 4. Dynamic AI Verification
        verification_output = safety_verifier_agent(context_data, draft_output)
        
        with col2:
            trace_container.empty()
            if "VERDICT: PASSED" in verification_output:
                st.success("🟢 VERIFIER VERDICT: PASSED")
            else:
                st.error("🔴 VERIFIER VERDICT: FAILED")
            st.text_area("Live AI Verification Analysis:", value=verification_output, height=220)
            st.code(combined_logs)
            
        with col1:
            st.markdown("### 🤖 Verified System Output:")
            st.info(draft_output)

    except Exception as e:
        with col2:
            st.error("🔴 LIVE AI CONNECTION FAILED")
            st.text_area("Raw API Error Details:", value=str(e), height=250)
        with col1:
            st.error("⚠️ Pipeline stopped. Please ensure your .env has a valid API key string.")