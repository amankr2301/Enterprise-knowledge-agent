import os
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma

def initialize_knowledge_base():
    # 1. Create a folder for our corporate policies
    docs_folder = "enterprise_docs"
    os.makedirs(docs_folder, exist_ok=True)
    
    # 2. Document A: The HR Leave & Remote Work Policy
    hr_policy_path = os.path.join(docs_folder, "hr_remote_policy.txt")
    with open(hr_policy_path, "w") as f:
        f.write(
            "POLICY-HR-101: Remote Work Regulations\n"
            "1. Standard Remote Work: Full-time employees are permitted to work remotely up to 3 days per week.\n"
            "2. Public Locations: Working from public spaces (cafes, libraries, hotels) is allowed, provided security protocols are followed.\n"
            "3. International Travel: Working remotely from an international country is strictly regulated. "
            "Employees must submit a formal request to HR at least 14 days prior to departure and obtain written approval from their department head."
        )
        
    # 3. Document B: The IT Security & Asset Management SOP
    it_policy_path = os.path.join(docs_folder, "it_security_policy.txt")
    with open(it_policy_path, "w") as f:
        f.write(
            "SOP-IT-202: Data Protection and Asset Security\n"
            "1. Device Possession: All company-issued laptops must remain in the physical custody of the employee at all times.\n"
            "2. Network Encryption: When connecting to internet networks in public spaces (e.g., coffee shops, airport Wi-Fi), "
            "employees are strictly required to activate the corporate Always-On VPN before accessing any internal company portals.\n"
            "3. Hardware Export: Exporting corporate hardware outside the home country of employment for any reason requires "
            "explicit written authorization from the IT Security Team at least 7 days in advance."
        )
        
    print("📝 Step 1: Created Mock Enterprise Documents successfully!")

    # 4. Verify API Key exists before calling Google
    if not os.environ.get("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable is not set. Please set it in your repository secrets.")
        return

    # 5. Load the files into our Python script
    print("📦 Loading documents into memory...")
    documents = []
    for file_name in os.listdir(docs_folder):
        if file_name.endswith(".txt"):
            loader = TextLoader(os.path.join(docs_folder, file_name))
            documents.extend(loader.load())

    # 6. Initialize Google's Text Embedding Model
    print("🧠 Connecting to Google Gemini Text Embedding API...")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

    # 7. Create and persist our Chroma Vector Database
    print("🗄️ Creating Chroma Vector Database folder...")
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    print("💾 Success! Your Vector DB is compiled and saved locally in the './chroma_db' folder.")

if __name__ == "__main__":
    initialize_knowledge_base()