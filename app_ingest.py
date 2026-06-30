import os

def initialize_knowledge_base():
    docs_folder = "enterprise_docs"
    os.makedirs(docs_folder, exist_ok=True)
    
    with open(os.path.join(docs_folder, "hr_remote_policy.txt"), "w") as f:
        f.write(
            "POLICY-HR-101: Remote Work Regulations\n"
            "1. Standard Remote Work: Full-time employees are permitted to work remotely up to 3 days per week.\n"
            "2. Public Locations: Working from public spaces (cafes, libraries, hotels) is allowed, provided security protocols are followed.\n"
            "3. International Travel: Working remotely from an international country is strictly regulated. "
            "Employees must submit a formal request to HR at least 14 days prior to departure and obtain written approval from their department head."
        )
        
    with open(os.path.join(docs_folder, "it_security_policy.txt"), "w") as f:
        f.write(
            "SOP-IT-202: Data Protection and Asset Security\n"
            "1. Device Possession: All company-issued laptops must remain in the physical custody of the employee at all times.\n"
            "2. Network Encryption: When connecting to internet networks in public spaces, "
            "employees are strictly required to activate the corporate Always-On VPN before accessing any internal company portals.\n"
            "3. Hardware Export: Exporting corporate hardware outside the home country of employment for any reason requires "
            "explicit written authorization from the IT Security Team at least 7 days in advance."
        )
    print("📝 Step 1: Created Mock Enterprise Documents successfully!")

if __name__ == "__main__":
    initialize_knowledge_base()