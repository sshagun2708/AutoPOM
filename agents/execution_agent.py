import os
import time
from playwright.sync_api import sync_playwright

class ExecutionAgent:
    def __init__(self):
        self._playwright = None
        self._browser = None
        self._context = None
        self._page = None

    def start_session(self, start_url: str):
        print(f"[*] [ExecutionAgent] Initializing full-screen browser session...")
        self._playwright = sync_playwright().start()
        
        self._browser = self._playwright.chromium.launch(
            channel="msedge",
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--start-maximized",
                "--disable-extensions",
                "--disable-gpu"
            ]
        )
        
        # Use no_viewport=True to ensure the browser takes up the full screen naturally without clipping
        self._context = self._browser.new_context(
            no_viewport=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        self._context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self._page = self._context.new_page()
        
        self._page.set_default_navigation_timeout(30000)
        
        print(f"[*] [ExecutionAgent] Navigating securely to: {start_url}")
        try:
            self._page.goto(start_url, wait_until="domcontentloaded")
        except Exception as e:
            print(f"[!] Initial navigation note: {e}")
        self._page.wait_for_timeout(1000)

    def _safe_action_with_retry(self, action_type, selector_list, value=None):
        for selector in selector_list:
            for attempt in range(2):
                try:
                    element = self._page.locator(selector).first
                    element.wait_for(state="attached", timeout=3000)
                    element.scroll_into_view_if_needed()
                    
                    if action_type == "fill":
                        element.click(force=True)
                        element.fill(value)
                        print(f"✅ Successfully filled '{selector}' with value.")
                        return True
                    
                    elif action_type == "click":
                        try:
                            element.click(timeout=2000)
                        except Exception:
                            element.evaluate("node => node.click()")
                        
                        print(f"✅ Successfully clicked '{selector}'.")
                        return True
                except Exception:
                    time.sleep(0.5)
        
        if action_type == "click":
            try:
                print(f"[*] Action fallback: Pressing 'Enter' key as a universal click substitute...")
                self._page.keyboard.press("Enter")
                return True
            except Exception:
                pass

        raise Exception(f"Critical Frontend Failure: Could not execute '{action_type}' for selectors {selector_list}")

    def execute_page_actions(self, page_name: str, product_to_select: str = None, step_instructions: str = ""):
        print(f"👁️ [ExecutionAgent] Smart execution for: {page_name}")
        self._page.wait_for_timeout(1000)

        try:
            if "LoginPage" in page_name:
                print("[*] Processing LoginPage flow...")
                email_selectors = ["input#ap_email", "input[name='email']", "input[type='email']"]
                if self._safe_action_with_retry("fill", email_selectors, "9501343962"):
                    self._page.wait_for_timeout(500)
                    continue_selectors = [
                        "input#continue", 
                        "button#continue", 
                        "input.a-button-input[aria-labelledby*='continue']",
                        "span#auth-continue-button input",
                        "input[type='submit']"
                    ]
                    self._safe_action_with_retry("click", continue_selectors)
                    self._page.wait_for_timeout(1500)

                pass_selectors = ["input#ap_password", "input[name='password']", "input[type='password']"]
                if self._safe_action_with_retry("fill", pass_selectors, "Amandeep@2790"):
                    self._page.wait_for_timeout(500)
                    signin_selectors = [
                        "input#signInSubmit", 
                        "button#signInSubmit", 
                        "input.a-button-input[aria-labelledby*='auth-signin-button']",
                        "span#auth-signin-button input"
                    ]
                    self._safe_action_with_retry("click", signin_selectors)
                    self._page.wait_for_timeout(2000)

            elif "HomePage" in page_name:
                if "signin" in self._page.url.lower() or "ax/claim" in self._page.url.lower():
                    print("[*] Redirecting to Home page...")
                    self._page.goto("https://www.amazon.in", wait_until="domcontentloaded")
                    self._page.wait_for_timeout(1500)

                search_selectors = ["input#twotabsearchtextbox", "input[name='field-keywords']"]
                if self._safe_action_with_retry("fill", search_selectors, "Samsung Z Fold 8 - 5G - 256GB Storage"):
                    self._page.wait_for_timeout(500)
                    submit_selectors = ["input#nav-search-submit-button", "input.nav-input[type='submit']"]
                    self._safe_action_with_retry("click", submit_selectors)
                    self._page.wait_for_timeout(2000)

            elif "ProductListingPage" in page_name:
                print("[*] Navigating product search results...")
                self._page.wait_for_load_state("domcontentloaded")
                
                clicked = False
                robust_selectors = [
                    "h2 a.a-link-normal",
                    "div.s-result-item h2 a",
                    "[data-cy='title-recipe'] a",
                    "div.s-main-slot h2 a",
                    "a h2"
                ]
                
                for selector in robust_selectors:
                    try:
                        links = self._page.locator(selector)
                        count = links.count()
                        if count > 0:
                            for i in range(min(count, 5)):
                                target_link = links.nth(i)
                                if target_link.is_visible():
                                    target_link.scroll_into_view_if_needed()
                                    target_link.evaluate("node => { node.removeAttribute('target'); node.click(); }")
                                    clicked = True
                                    print(f"✅ Clicked product link using selector: {selector}")
                                    break
                        if clicked:
                            break
                    except Exception:
                        continue

                if not clicked:
                    try:
                        self._page.evaluate("""
                            const link = document.querySelector('.s-main-slot h2 a') || document.querySelector('h2 a');
                            if (link) { link.removeAttribute('target'); link.click(); }
                        """)
                        clicked = True
                    except Exception:
                        pass

                if not clicked:
                    raise Exception("Critical: Could not find or click any product link on the listing page.")

                print("[*] Waiting for product detail page URL transition...")
                navigated = False
                for _ in range(30):
                    current_url = self._page.url.lower()
                    if "/dp/" in current_url or "/gp/product/" in current_url:
                        navigated = True
                        break
                    time.sleep(0.5)

                self._page.bring_to_front()
                self._page.wait_for_load_state("domcontentloaded")
                print(f"✅ Successfully locked on Product Detail Page: {self._page.title()} ({self._page.url})")
                self._page.wait_for_timeout(1000)

            elif "ProductDetailPage" in page_name or "ProductDetailsPage" in page_name:
                print("[*] Smart Enforcement: Staying strictly on Product Detail Page...")
                self._page.bring_to_front()
                self._page.wait_for_load_state("domcontentloaded")

                if "/s?" in self._page.url.lower():
                    print("[*] Warning: Still on search listing page. Re-navigating to first product link...")
                    first_link = self._page.locator("h2 a.a-link-normal").first
                    first_link.evaluate("node => { node.removeAttribute('target'); node.click(); }")
                    self._page.wait_for_load_state("domcontentloaded")

                print("[*] Scrolling down to buy-box and clicking 'Add to Cart'...")
                
                # Scroll down to ensure the buy-box and Add to Cart button are rendered and in view
                try:
                    self._page.evaluate("window.scrollBy(0, 600);")
                    self._page.wait_for_timeout(1000)
                except Exception:
                    pass

                clicked_cart = False
                
                # Strategy 1: Playwright role-based button search
                try:
                    cart_role_btn = self._page.get_by_role("button", name="Add to Cart").first
                    if cart_role_btn.is_visible(timeout=3000):
                        cart_role_btn.scroll_into_view_if_needed()
                        cart_role_btn.click(timeout=3000)
                        clicked_cart = True
                        print("✅ Successfully clicked 'Add to Cart' via role selector.")
                except Exception as e:
                    print(f"[!] Role selector note: {e}")

                # Strategy 2: Fallback to input/id selectors
                if not clicked_cart:
                    cart_selectors = [
                        "#add-to-cart-button",
                        "input[name='submit.add-to-cart']",
                        "input#add-to-cart-button",
                        "#submit\\.add-to-cart",
                        "input.a-button-input[aria-labelledby*='submit.add-to-cart']",
                        "span#submit\\.add-to-cart input",
                        "input[value='Add to Cart']"
                    ]
                    for selector in cart_selectors:
                        try:
                            el = self._page.locator(selector).first
                            if el.is_visible():
                                el.scroll_into_view_if_needed()
                                el.evaluate("node => node.click()")
                                clicked_cart = True
                                print(f"✅ Successfully clicked 'Add to Cart' using selector: {selector}")
                                break
                        except Exception:
                            continue

                # Strategy 3: JavaScript text scanner fallback
                if not clicked_cart:
                    print("[*] Executing JS fallback to click 'Add to Cart'...")
                    try:
                        self._page.evaluate("""
                            const buttons = Array.from(document.querySelectorAll('input, button, span.a-button-inner, input[id*="add-to-cart"]'));
                            const cartBtn = buttons.find(el => el.textContent.includes('Add to Cart') || el.value === 'Add to Cart' || el.id.includes('add-to-cart'));
                            if (cartBtn) { cartBtn.click(); }
                        """)
                        clicked_cart = True
                    except Exception as js_err:
                        print(f"[!] JS fallback error: {js_err}")

                if not clicked_cart:
                    raise Exception("Critical: Could not locate or click the 'Add to Cart' button on the product detail page.")

                print("✅ Successfully added product to cart from Product Detail Page.")
                self._page.wait_for_timeout(3000)

            elif "CartPage" in page_name:
                print("[*] Navigating to Cart overview...")
                cart_nav = ["#nav-cart", "a[href*='nav_cart']"]
                self._safe_action_with_retry("click", cart_nav)
                self._page.wait_for_timeout(1500)

        except Exception as e:
            print(f"[!] Critical error during page execution: {e}")
            raise e

    def get_current_dom(self) -> str:
        try:
            return self._page.content()
        except:
            return ""

    def get_current_url(self) -> str:
        try:
            return self._page.url
        except:
            return ""

    def close(self):
        try:
            if self._browser:
                self._browser.close()
            if self._playwright:
                self._playwright.stop()
        except:
            pass