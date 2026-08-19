# AutoPOM
AutoPOM agent is an intelligent assistant that automatically reads your plain-text test instructions and generates ready-to-use software automation code (Page Object Model classes) while keeping track of all your webpage elements.

Here is a clear, step-by-step installation and environment setup guide for anyone wanting to run and use **AutoPOM** on their local system. You can include this directly in your repository's `README.md` file!

---

# 🚀 AutoPOM: Installation & Environment Setup Guide

Follow these instructions to clone, install, and configure **AutoPOM** on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

* **Python** (Version 3.10 or higher recommended)
* **Node.js & npm** (Required if working with generated frontend frameworks/Playwright dependencies)
* **Java Development Kit (JDK)** (Required for executing or compiling Java-based Page Object Model files)
* **Git**

---

## Step 1: Clone the Repository

Open your terminal or command prompt and clone your repository from GitHub:

```bash
git clone https://github.com/sshagun2708/AutoPOM.git
cd AutoPOM

```

---

## Step 2: Set Up a Python Virtual Environment

It is best practice to run the project inside an isolated virtual environment:

* **On Windows:**
```bash
python -m venv venv
venv\Scripts\activate

```


* **On macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate

```



---

## Step 3: Install Python Dependencies

Install the required packages (including Playwright and Google GenAI dependencies) using `pip`:

```bash
pip install -r requirements.txt

```

After installing Playwright, ensure the necessary browser binaries are installed:

```bash
playwright install

```

---

## Step 4: Configure Environment Variables (.env)

AutoPOM relies on the **Google Gemini API** to analyze test steps, map pages, and generate intelligent locators.

1. Create a file named `.env` in the root directory of the project (`C:\AutoPOM\.env`).
2. Add your Gemini API key inside the `.env` file like this:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here

```


*(Note: Never commit your `.env` file to GitHub. It is already included in `.gitignore` to keep your credentials secure).*

---

## Step 5: Configure Your Test Inputs (`inputs.txt`)

Create or update your `inputs.txt` file in the root directory to define your target URL, product name, and test steps.

Example format:

```text
Target URL: https://www.amazon.in
Product Name: Samsung Z Fold 8 - 5G - 256GB Storage

Test Steps:
1. Login to application with credentials
2. Search for the product on home page
3. Select an organic product from the search listing page
4. Add the product to cart from the product detail page
5. Navigate to the cart overview

```

---

## Step 6: Run AutoPOM

Once your environment and inputs are configured, run the main orchestration script:

```bash
python main.py

```

AutoPOM will automatically launch the browser, execute the frontend actions step-by-step, extract and analyze the DOM layout, and generate clean, structured Page Object Model (POM) classes inside your project directory!
