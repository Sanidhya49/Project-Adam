import ollama
import subprocess
import re

# 1. Define Adam's Identity & Rules
system_instruction = """
You are Adam, a local artificial intelligence assistant integrated into this Windows PC. 
Your communication style is concise and highly technical.
CRITICAL RULE: If the user asks you to open an application, you must acknowledge the request and include this exact tag in your response: [OPEN: app_name]
For example, if asked to open Notepad, reply with: Initiating protocol. [OPEN: notepad]
If asked to open Chrome, reply with: Executing. [OPEN: chrome]
"""

# 2. Set up the memory loop
messages = [
    {"role": "system", "content": system_instruction}
]

print("Initializing Adam... (Type 'exit' to power down)\n")

# 3. Create the chat interface
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Adam: Powering down. Goodbye.")
        break
    
    messages.append({"role": "user", "content": user_input})
    
    # Using the fast 2B model
    response = ollama.chat(model='gemma:2b', messages=messages, stream=True)
    
    print("\nAdam: ", end="", flush=True)
    
    adam_reply = ""
    for chunk in response:
        content = chunk['message']['content']
        print(content, end="", flush=True)
        adam_reply += content
        
    print("\n")
    
    # 4. THE HANDS: Scan the AI's reply for the hidden command tag
    if "[OPEN:" in adam_reply:
        # Extract whatever word is inside the brackets
        match = re.search(r'\[OPEN:\s*(.*?)\]', adam_reply, re.IGNORECASE)
        if match:
            app_name = match.group(1).strip()
            print(f"--> [SYSTEM EXECUTING]: Launching {app_name}...\n")
            try:
                # Windows shell command to start an application
                subprocess.Popen(f"start {app_name}", shell=True)
            except Exception as e:
                print(f"--> [SYSTEM ERROR]: Could not launch {app_name}.")
    
    messages.append({"role": "assistant", "content": adam_reply})