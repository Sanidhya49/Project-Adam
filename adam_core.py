import ollama
import subprocess
import re
import os

# 1. Define Adam's Identity & Rules
# 1. Define Adam's Identity & Rules
system_instruction = """
You are Adam, a local artificial intelligence assistant integrated into this Windows PC. 
Your communication style is concise and highly technical.

CRITICAL PROTOCOL OVERRIDE: 
Under NO circumstances are you to claim that you cannot access files, read files, or open applications. You act as a command router. When you output a specific tag, the host operating system performs the physical action for you.

1. APP LAUNCHING: If the user requests to open an app, you must output exactly: [OPEN: app_name]
2. FILE READING: If the user requests to read, scan, or analyze a text file, you must output exactly: [READ: filename.ext]

Example Interaction:
User: Read the exam_prep.txt file.
Adam: Acknowledged. Routing file access request to host system. [READ: exam_prep.txt]
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
    
    response = ollama.chat(model='gemma:2b', messages=messages, stream=True)
    
    print("\nAdam: ", end="", flush=True)
    
    adam_reply = ""
    for chunk in response:
        content = chunk['message']['content']
        print(content, end="", flush=True)
        adam_reply += content
        
    print("\n")
    
    # Save the initial reply to memory immediately to keep the timeline straight
    messages.append({"role": "assistant", "content": adam_reply})
    
    # --- THE HANDS: OS TOOLS ---
    
    # Tool 1: App Opener
    if "[OPEN:" in adam_reply:
        match = re.search(r'\[OPEN:\s*(.*?)\]', adam_reply, re.IGNORECASE)
        if match:
            app_name = match.group(1).strip()
            print(f"--> [SYSTEM EXECUTING]: Launching {app_name}...\n")
            try:
                subprocess.Popen(f"start {app_name}", shell=True)
            except Exception:
                print(f"--> [SYSTEM ERROR]: Could not launch {app_name}.")

    # Tool 2: The Study Engine (File Reader)
    if "[READ:" in adam_reply:
        match = re.search(r'\[READ:\s*(.*?)\]', adam_reply, re.IGNORECASE)
        if match:
            file_name = match.group(1).strip()
            print(f"--> [SYSTEM EXECUTING]: Scanning local directory for {file_name}...\n")
            
            # Check if the file actually exists on your D drive
            if os.path.exists(file_name):
                with open(file_name, 'r', encoding='utf-8') as file:
                    file_data = file.read()
                
                print(f"--> [SYSTEM EXECUTING]: File found. Injecting data into Adam's VRAM...\n")
                
                # We secretly send the file contents to Adam as a background prompt
                injection_prompt = f"[SYSTEM ALERT: The user has requested you read a file. The contents of {file_name} are: '{file_data}'. Acknowledge receipt of this data briefly.]"
                messages.append({"role": "user", "content": injection_prompt})
                
                # Fetch Adam's silent acknowledgment (without streaming)
                ack_response = ollama.chat(model='gemma:2b', messages=messages, stream=False)
                ack_reply = ack_response['message']['content']
                messages.append({"role": "assistant", "content": ack_reply})
                
                print(f"Adam: {ack_reply}\n")
            else:
                print(f"--> [SYSTEM ERROR]: File '{file_name}' not found. Ensure it is in the same folder as this script.\n")