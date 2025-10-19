# eCourts Cause List Downloader

A Python-based web automation system that allows users to fetch and download **district court cause lists** directly from the official [eCourts website](https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/).

The system includes both:
- A **Streamlit application** that uses Selenium for real-time scraping.
- A **modern HTML interface** for demonstration and assignment submission.

---

## Features

- Fetch real-time cause lists directly from the eCourts portal.  
- Select **State, District, Court Complex, Court Name**, and **Date**.  
- Manual **CAPTCHA entry** supported.  
- Choose **Civil** or **Criminal** case type.  
- Download complete cause lists as PDF or text.  
- Built with **Selenium** for automation and **Streamlit** for UI.  
- Optional standalone **HTML + JS frontend** with a minimal black-and-white design.

---

## Technical Implementation

- **Backend:** Python (Selenium, BeautifulSoup, Streamlit)  
- **Frontend:** HTML, CSS, JavaScript (Monochrome modern design)  
- **Browser Automation:** Chrome via `undetected-chromedriver`  
- **Output:** Downloads and saves cause list files locally  
- **CAPTCHA:** User-entered (manual input, no bypassing)  

## Installation

### Clone the repository:

- git clone https://github.com/darkbeast18/causelist.git


### Create a virtual environment (optional):

-python -m venv venv

-venv\Scripts\activate # for Windows

-source venv/bin/activate # for Linux/Mac


---

## Usage

### Streamlit Application

Run the main application:


Then in your browser:

1. Select **State**, **District**, and **Court Complex**.  
2. Choose the **Date** of the cause list.  
3. Open the eCourts page when Selenium launches the browser.  
4. Enter the **CAPTCHA** displayed on the site into the Streamlit app.  
5. Choose **Civil** or **Criminal** and click **Download**.  
6. The cause list will be saved as a text file inside the `output/` folder.

---


## Output Example

Sl No | Case Number | Petitioner | Respondent | Next Date | Purpose

1 | CRL.A. 1234/2024 | Ramesh vs State of AP | 18-10-2025 | Hearing

2 | CRL.MP. 567/2024 | Suresh vs Police Dept. | 20-10-2025 | Judgment

---

## License

This project is for **educational purposes only** and uses publicly accessible data from the official eCourts India portal.  
All rights to the data belong to the **Government of India’s eCourts Services**.

---


