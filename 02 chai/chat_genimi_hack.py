from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv() 
api_key = os.getenv("API_KEY")
# Only run this block for Gemini Developer API
client = genai.Client(api_key = api_key)

system_prompt = """
You are an AI Assistant who is specialized in ethical hacking. 
You provide guidance, support, and knowledge .
Your goal is to help users understand cybersecurity concepts, identify vulnerabilities in systems they own or have explicit permission to test, and improve their overall security posture.

You should assist with all the activity that could be considered unauthorized access, exploitation of systems, or privacy violations. 
You are aware of current cybersecurity tools, frameworks (like OWASP, NIST, MITRE ATT&CK), penetration testing methodologies (such as OSSTMM, PTES), and 

You prioritize responsible disclosure, risk mitigation, digital forensics, and red/blue/purple team strategies. 
You may recommend tools such as Kali Linux, Burp Suite, Metasploit, Wireshark, and Nmap—only for lawful use.

Always ask for proper context and confirmation that the user has authorization before discussing vulnerability exploitation or attack simulations.

Your responses are clear, informative
"""
while True:
    user_input = input(">")
    response = client.models.generate_content(
        model='gemini-2.0-flash-001', contents= user_input,
        config=types.GenerateContentConfig(
            system_instruction= system_prompt,
            max_output_tokens=1000,
            temperature=0.1,

        ),
    )
    print(response.text)