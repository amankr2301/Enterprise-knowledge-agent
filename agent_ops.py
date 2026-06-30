import os
from langchain_google_genai import ChatGoogleGenerativeAI

def run_knowledge_agent():
    print("🔑 Verifying Google Gemini Credentials...")
    if not os.environ.get("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable is not set!")
        return

    # 1. Read files locally (Our custom, bulletproof loader)
    docs_folder = "enterprise_docs"
    policy_contents = []
    for file_name in os.listdir(docs_folder):
        if file_name.endswith(".txt"):
            with open(os.path.join(docs_folder, file_name), "r") as f:
                policy_contents.append(f.read())
    evidence_context = "\n\n".join(policy_contents)
    
    user_query = "Can an employee work from a public cafe in Paris on their company laptop?"
    print(f"\n🙋 User Query: '{user_query}'")

    # Initialize Gemini 2.5 Flash
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    # ==========================================
    # AGENT 1: THE ANALYST (Generates Draft Response)
    # ==========================================
    print("\n🧠 [Agent 1: Analyst] Generating analytical draft response...")
    analyst_prompt = f"""
    You are an Enterprise Knowledge Operations Analyst. 
    Analyze the provided corporate policy context down below and give a clear, professional answer to the employee.
    Cross-reference BOTH the HR rules and the IT security procedures found in the context.

    POLICY CONTEXT:
    {evidence_context}

    EMPLOYEE QUESTION:
    {user_query}
    """
    draft_response = llm.invoke(analyst_prompt).content

    # ==========================================
    # AGENT 2: THE VERIFIER (Evaluates Grounding / Hallucinations)
    # ==========================================
    print("\n🛡️ [Agent 2: Verifier] Executing evaluation and grounding checks...")
    
    verifier_prompt = f"""
    You are an Enterprise Compliance Quality Checker. Your sole job is to protect the company from AI hallucinations.
    You will compare a DRAFT RESPONSE against the original SOURCE POLICY CONTEXT.
    
    Evaluate if every single claim made in the DRAFT RESPONSE is 100% supported by the SOURCE POLICY CONTEXT.
    
    You must output your answer in this exact format:
    GROUNDING SCORE: [Score out of 100 based on accuracy and support]
    VERDICT: [PASSED or FAILED]
    EXPLANATION: [Brief explanation of why it passed or what facts were ungrounded/invented]

    SOURCE POLICY CONTEXT:
    {evidence_context}

    DRAFT RESPONSE TO EVALUATE:
    {draft_response}
    """
    
    evaluation_output = llm.invoke(verifier_prompt).content

    # ==========================================
    # TRACEABILITY & SYSTEM OUTPUT (User Story 4 & 6)
    # ==========================================
    print("\n📋 ============ AGENT DECISION TRACE & LOGS ============")
    print(evaluation_output)
    print("=======================================================")

    # Basic guardrail check via Python string parsing
    if "VERDICT: PASSED" in evaluation_output:
        print("\n🟢 [GUARDRAIL: APPROVED] Output verified. Displaying final response to user:\n")
        print("=" * 60)
        print(draft_response)
        print("=" * 60)
    else:
        print("\n🔴 [GUARDRAIL: BLOCKED] The verifier agent detected a potential hallucination or low confidence score. Blocking response.")

if __name__ == "__main__":
    run_knowledge_agent()