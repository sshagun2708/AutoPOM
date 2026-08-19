import os
import json
import sys
import time
from dotenv import load_dotenv
from agents.locator_agent import LocatorAgent
from agents.pom_generator import POMGenerator
from agents.execution_agent import ExecutionAgent

# Force unbuffered output for real-time terminal feedback
sys.stdout.reconfigure(line_buffering=True)
os.environ["PYTHONUNBUFFERED"] = "1"

load_dotenv()

STORE_FILE = "locators_store.json"

def load_locator_store():
    if os.path.exists(STORE_FILE):
        with open(STORE_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_locator_store(store):
    with open(STORE_FILE, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=4)

def parse_plain_text_inputs(file_path="inputs.txt"):
    if not os.path.exists(file_path):
        return "", [], ""
    url, steps, product = "", [], ""
    with open(file_path, "r", encoding="utf-8") as f:
        reading_steps = False
        for line in f:
            line_clean = line.strip()
            if not line_clean or line_clean.startswith("#"):
                continue
            if line_clean.lower().startswith("target url:") or line_clean.lower().startswith("url:"):
                url = line_clean.split(":", 1)[1].strip()
            elif line_clean.lower().startswith("product name:"):
                product = line_clean.split(":", 1)[1].strip()
            elif line_clean.lower().startswith("test steps:") or line_clean.lower().startswith("steps:"):
                reading_steps = True
            elif reading_steps:
                steps.append(line_clean)
    return url, steps, product

def main():
    print("=" * 60)
    print("🤖 AutoPOM Synchronized Execution & Generation Agent")
    print("=" * 60)

    url, steps, target_product = parse_plain_text_inputs("inputs.txt")
    if not url or not steps:
        print("[!] Error: 'inputs.txt' missing or incorrectly formatted.")
        return

    formatted_instructions = "\n".join(steps)
    framework = "playwright"
    target_pages_dir = os.path.join("demo", "src", "main", "java", "com", "pages", framework)
    os.makedirs(target_pages_dir, exist_ok=True)

    locator_agent = LocatorAgent()
    pom_generator = POMGenerator()
    execution_agent = ExecutionAgent()
    locator_store = load_locator_store()

    print(f"\n[*] Analyzing workflow to determine page breakdown...")

    routing_prompt = f"""
    You are an expert QA Test Automation Architect.
    Analyze the following user test steps and split them into logical Page Object Model (POM) page classes.
    
    Test Steps:
    {formatted_instructions}
    
    Return your answer STRICTLY as a valid JSON list of objects:
    [
      {{"page_name": "LoginPage", "steps": ["Step 1 text", "Step 2 text"]}},
      {{"page_name": "HomePage", "steps": ["Step 3 text", "Step 4 text"]}}
    ]
    """

    # Auto-retry loop to handle temporary 503 high demand errors gracefully
    routing_response = None
    for attempt in range(3):
        try:
            routing_response = locator_agent.client.models.generate_content(
                model=locator_agent.model_id,
                contents=routing_prompt,
            )
            break
        except Exception as e:
            if attempt < 2:
                print(f"[!] Model experiencing high demand (503). Retrying in {(attempt + 1) * 3} seconds...")
                time.sleep((attempt + 1) * 3)
            else:
                print(f"[!] Error: Could not connect to Gemini API after 3 attempts: {e}")
                return

    response_text = routing_response.text
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0].strip()
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0].strip()

    try:
        page_mappings = json.loads(response_text)
    except Exception as e:
        print(f"[!] Error parsing page breakdown: {e}")
        return

    any_existing = any(os.path.exists(os.path.join(target_pages_dir, f"{p['page_name']}.java")) for p in page_mappings)
    global_overwrite = True
    
    if any_existing:
        choice = input("\n[Notice] ⚠️ POM files exist. Overwrite? (y/n): ").strip().lower()
        global_overwrite = (choice == 'y')

    # 1. Start browser session
    execution_agent.start_session(url)

    # 2. Synchronized Loop
    for page_info in page_mappings:
        page_name = page_info["page_name"]
        page_steps = page_info["steps"]
        step_text_block = "\n".join([f"- {s}" for s in page_steps])

        file_path = os.path.join(target_pages_dir, f"{page_name}.java")
        if os.path.exists(file_path) and not global_overwrite:
            continue

        print(f"\n------------------------------------------------------------")
        print(f"🚀 Processing Page: {page_name}")
        print(f"------------------------------------------------------------")

        # Frontend Sync: Perform visual action, passing step instructions for smart context enforcement
        execution_agent.execute_page_actions(page_name, product_to_select=target_product, step_instructions=step_text_block)

        # Backend Sync: Analyze settled DOM and generate code
        analyzed_elements = locator_agent.extract_dom_and_analyze(
            page_name, step_text_block, active_page=execution_agent._page
        )
        
        locator_store[page_name] = analyzed_elements
        save_locator_store(locator_store)

        raw_code = pom_generator.generate_pom_code(
            page_name, json.dumps(analyzed_elements), framework, os.path.exists(file_path)
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(raw_code.replace("```java", "").replace("```", "").strip())

        print(f"🎉 [Generated] Saved POM to: {file_path}")
        time.sleep(0.5)

    print("\n" + "=" * 60)
    print("✨ Workflow completed successfully!")
    print("=" * 60)

    # Keep browser window open until user presses Enter in terminal
    input("\n[📌 Execution Complete] The browser is remaining open for review. Press Enter here to close and exit...")

    execution_agent.close()

if __name__ == "__main__":
    main()