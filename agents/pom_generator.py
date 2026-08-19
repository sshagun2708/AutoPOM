import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import ServerError

load_dotenv()

class POMGenerator:
    def __init__(self):
        self.client = genai.Client()
        self.model_id = "gemini-3.5-flash"

    def generate_pom_code(self, page_name: str, analyzed_locators: str, framework: str = "playwright", is_healing: bool = False) -> str:
        healing_context = "Verify and ensure the locators are clean and functional." if is_healing else "Create a brand new class."
        
        print(f"[*] Generating Page Object Model code for '{page_name}' using {framework}...")

        prompt = f"""
        You are an expert Test Automation Architect.
        Based on the following analyzed locators and element data, generate a clean, production-ready Page Object Model (POM) class file in Java using {framework}.
        
        Page Name: {page_name}
        Framework Target: {framework}
        Context: {healing_context}
        
        Analyzed Locators / Elements Data:
        {analyzed_locators}
        
        Requirements:
        1. Must follow standard Java structure with package declarations (`package com.pages.{framework};`).
        2. Declare explicit locator variables (using CSS selectors or Playwright locators found in the data).
        3. Include a standard constructor accepting the page/driver instance.
        4. Include clean action methods corresponding to the page actions.
        5. Output ONLY the raw Java code wrapped inside a ```java markdown block. Do not include long conversational text or explanations outside the code block.
        """

        retries = 3
        for attempt in range(retries):
            try:
                response = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                )
                return response.text
            except ServerError as e:
                if attempt < retries - 1:
                    wait_time = (attempt + 1) * 3
                    print(f"[!] API Server busy (503). Retrying in {wait_time} seconds... (Attempt {attempt+1}/{retries})")
                    time.sleep(wait_time)
                else:
                    raise e