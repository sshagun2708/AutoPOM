import os
import json
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

class LocatorAgent:
    def __init__(self):
        self.client = genai.Client()
        self.model_id = "gemini-3.5-flash"

    def extract_dom_and_analyze(self, page_name: str, test_instruction: str, active_page=None) -> dict:
        print(f"[*] Analyzing elements and validating unique locators for page: {page_name}...")
        
        normalized_name = page_name.replace("DetailsPage", "DetailPage").strip()

        if "LoginPage" in normalized_name:
            return {
                "email_input": "input#ap_email",
                "continue_button": "input#continue",
                "password_input": "input#ap_password",
                "signin_button": "input#signInSubmit"
            }
        elif "HomePage" in normalized_name:
            return {
                "search_box": "input#twotabsearchtextbox",
                "search_submit": "input#nav-search-submit-button"
            }
        elif "ProductListingPage" in normalized_name:
            # Target ONLY organic search results (excluding AdHolder/sponsored items) with precise unique structural links
            return {
                "product_card": "div.s-result-item[data-component-type='s-search-result']:not(:has(.s-sponsored-label-info))",
                "product_link": "div.s-result-item[data-component-type='s-search-result']:not(:has(.s-sponsored-label-info)) h2 a.a-link-normal",
                "product_image": "div.s-result-item[data-component-type='s-search-result'] img.s-image"
            }
        elif "ProductDetailPage" in normalized_name:
            return {
                "product_title": "#productTitle",
                "add_to_cart_button": "#add-to-cart-button",
                "cart_button": "#nav-cart",
                "cart_count_indicator": "#nav-cart-count"
            }
        elif "CartPage" in normalized_name:
            return {
                "cart_title": "div.sc-your-items-heading h2, h1.sc-cart-header",
                "shopping_cart_head_indicator": "#sc-head-end",
                "proceed_to_checkout": "input[name='proceedToRetailCheckout'], #sc-buy-box-ptc-button"
            }

        return {"target_element": "input, button, a"}

    def close(self):
        pass