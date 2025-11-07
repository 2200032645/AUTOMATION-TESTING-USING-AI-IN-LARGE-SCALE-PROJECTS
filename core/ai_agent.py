# ai_testing_app/core/ai_agent.py
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.options import Options # NEW: For stability settings
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

from google import genai
from google.genai import types

# --- Configuration ---
GEMINI_MODEL = "gemini-2.5-flash" 

class AITestingAgent:
    """The core AI-powered agent to autonomously test a website."""

    def __init__(self, start_url: str):
        
        # 1. Initialize Gemini Client (securely gets key from environment)
        api_key = os.getenv("GEMINI_API_KEY")
        self.client = genai.Client(api_key=api_key) 
        
        # 2. Initialize WebDriver with Stability Fix
        chrome_options = Options()
        # Recommended arguments to fix common session errors and stabilize the browser
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--start-maximized") # Start maximized for better visual context
        # chrome_options.add_argument("--headless") # Uncomment if you want it to run in the background
        
        self.driver = webdriver.Chrome(options=chrome_options) # Pass the options here
        
        # 3. Test State Variables
        self.start_url = start_url
        self.test_report = {"url": start_url, "actions": [], "summary": ""}
        self.history = ""
        self.max_steps = 7 # Limit actions for demonstration purposes

    def get_page_state(self) -> str:
        """Extracts key information from the current page for the AI to analyze."""
        url = self.driver.current_url
        title = self.driver.title
        
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        interactable_elements = []
        
        for tag in soup.find_all(['a', 'button', 'input']):
            label = tag.get('aria-label') or tag.text or tag.get('placeholder') or tag.get('name')
            if label and len(label) < 50: 
                 interactable_elements.append(f"<{tag.name}> Text: '{label.strip()}' ID: '{tag.get('id', 'N/A')}'")
        
        state = (
            f"Current URL: {url}\n"
            f"Page Title: {title}\n"
            f"Visible Interactable Elements (Top 10):\n"
            + "\n".join(interactable_elements[:10])
        )
        return state

    def generate_action(self, page_state: str) -> str:
        """Uses the LLM to decide the next action based on the page state and history."""
        
        system_prompt = (
            "You are a sophisticated Web Testing Agent. Your goal is to explore the website, "
            "perform functional tests, and look for bugs. "
            "You must respond ONLY with a single, valid Python function call from the list: "
            "1. click_element(By.LINK_TEXT, 'About')"
            "2. type_text(By.ID, 'search-input', 'test query')"
            "3. navigate_to('contact')"
            "4. finish_testing('Your final quality assessment and summary')"
            "Analyze the page state and testing history to decide the best action. Prefer locators by visible text (LINK_TEXT) or unique ID (ID)."
        )

        prompt = (
            f"TESTING HISTORY (last 200 chars):\n{self.history[-200:]}\n\n"
            f"CURRENT PAGE STATE:\n{page_state}\n\n"
            "What is the single, best Python action to take next? Respond ONLY with the function call."
        )

        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt, 
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt
                )
            ).text.strip()
            
            return response
        except Exception as e:
            self.report_action(f"Error calling Gemini: {e}", "FATAL_ERROR")
            return "finish_testing('AI communication failed.')"
    
    # --- Action Functions (Callable by the LLM) ---
    def click_element(self, by_type: By, locator: str):
        """Clicks an element."""
        try:
            WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(by_type, locator)
            ).click()
            self.report_action(f"Clicked element found by {by_type}='{locator}'.", "PASS")
        except (TimeoutException, NoSuchElementException):
            self.report_action(f"Failed to click element {locator}. Element not found or timed out.", "ERROR")
            
    def type_text(self, by_type: By, locator: str, text: str):
        """Types text into an input field."""
        try:
            element = WebDriverWait(self.driver, 10).until(
                lambda d: d.find_element(by_type, locator)
            )
            element.clear()
            element.send_keys(text)
            self.report_action(f"Typed text into field {locator}.", "PASS")
        except (TimeoutException, NoSuchElementException):
            self.report_action(f"Failed to type text into {locator}. Element not found.", "ERROR")

    def navigate_to(self, path: str):
        """Navigates to a new path relative to the base URL."""
        new_url = urljoin(self.start_url, path)
        self.driver.get(new_url)
        self.report_action(f"Navigated to: {new_url}", "PASS")

    def finish_testing(self, summary: str):
        """Terminates the testing loop and captures the final summary."""
        self.test_report['summary'] = summary
        self.report_action(summary, "FINISH")
        
    # --- Execution & Reporting ---
    
    def report_action(self, description: str, status: str):
        """Logs the action for the final report and updates history."""
        log = {"step": len(self.test_report['actions']) + 1, "action": description, "status": status, "url_after": self.driver.current_url}
        self.test_report['actions'].append(log)
        self.history += f"Step {log['step']} ({status}): {description}\n"
        print(f"[{status}] Step {log['step']}: {description}")

    def run_tests(self):
        """Main loop for autonomous testing."""
        self.driver.get(self.start_url)
        self.report_action(f"Initial navigation to: {self.start_url}", "PASS")
        
        for step in range(self.max_steps):
            if self.test_report['actions'] and self.test_report['actions'][-1]['status'] == "FINISH":
                break

            page_state = self.get_page_state()
            action_code = self.generate_action(page_state)
            
            try:
                # Execution of the AI's generated Python code
                eval(f"self.{action_code}") 
                time.sleep(3) 
            except Exception as e:
                self.report_action(f"CRITICAL ERROR executing AI code '{action_code}': {e}", "FATAL_ERROR")
                break
        
        self.driver.quit()
        return self.test_report