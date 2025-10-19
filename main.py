import streamlit as st
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import time
st.title("   Cause List Scraper")

try:
    import importlib
    uc = importlib.import_module("undetected_chromedriver")
    HAVE_UC = True
except Exception:
    uc = None
    HAVE_UC = False

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

@st.cache_resource
def get_driver():
    
    if HAVE_UC and uc is not None:
        options = uc.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = uc.Chrome(options=options)
        return driver
    else:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver


def get_dropdown_options(driver, element_id):
    select_elem = Select(driver.find_element(By.ID, element_id))
    options = [opt.text.strip() for opt in select_elem.options if opt.text.strip()]
    return options

def select_dropdown_option(driver, element_id, option_text):
    select_elem = Select(driver.find_element(By.ID, element_id))
    select_elem.select_by_visible_text(option_text)

def fetch_court_names(driver, timeout=15):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.ID, "CL_court_no"))
    )
    select_elem = driver.find_element(By.ID, "CL_court_no")
    select_obj = Select(select_elem)
    courts = [
        option.text.strip()
        for option in select_obj.options
        if option.text.strip() and "select" not in option.text.strip().lower() and not option.get_attribute('disabled')
    ]
    return courts


def save_all_cases_to_txt(html, filename="case_results.txt"):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", id="dispTable")

    if not table:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("No result table found!\n")
        st.warning(f"No result table found! A file has still been created: {filename}")
        return filename

    with open(filename, "w", encoding="utf-8") as f:
        # Extract headers
        thead = table.find("thead")
        if thead:
            headers = [th.get_text(strip=True) for th in thead.find("tr").find_all("th")]
            f.write(" | ".join(headers) + "\n")

        # Extract rows
        tbody = table.find("tbody")
        for row in tbody.find_all("tr"):
            cols = [td.get_text(separator=" ", strip=True) for td in row.find_all("td")]
            f.write(" | ".join(cols) + "\n")

    st.success(f"Results saved to {filename}")
    
    # ----------------- Download Button -----------------
    with open(filename, "rb") as f:
        st.download_button(
            label="📥 Download Results",
            data=f,
            file_name=filename,
            mime="text/plain"
        )
    
    return filename



if 'driver' not in st.session_state:
    st.session_state.driver = get_driver()

driver = st.session_state.driver
if 'page_loaded' not in st.session_state:
    driver.get("https://services.ecourts.gov.in/ecourtindia_v6/?p=cause_list/")
    time.sleep(3)
    st.session_state.page_loaded = True



states = get_dropdown_options(driver, "sess_state_code")
state_choice = st.selectbox("Select State", states)
select_dropdown_option(driver, "sess_state_code", state_choice)
time.sleep(2)


districts = get_dropdown_options(driver, "sess_dist_code")
district_choice = st.selectbox("Select District", districts)
select_dropdown_option(driver, "sess_dist_code", district_choice)
time.sleep(2)


complexes = get_dropdown_options(driver, "court_complex_code")
complex_choice = st.selectbox("Select Court Complex", complexes)
select_dropdown_option(driver, "court_complex_code", complex_choice)
time.sleep(3)


court_names = fetch_court_names(driver)
if court_names:
    court_choice = st.selectbox("Select Court", court_names)
    select_dropdown_option(driver, "CL_court_no", court_choice)



cause_list_date = st.text_input("Enter Cause List Date (dd-mm-yyyy)")
if cause_list_date:
    date_field = driver.find_element(By.ID, "causelist_date")
    date_field.clear()
    date_field.send_keys(cause_list_date)
    time.sleep(1)


st.write("Open the official eCourts that poped in your Browser.")
st.write("Look at the captcha displayed there and enter it below:")

captcha_val = st.text_input("Enter Captcha Value")




if captcha_val:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Civil"):
            
            captcha_input = driver.find_element(By.ID, "cause_list_captcha_code")
            captcha_input.clear()
            captcha_input.send_keys(captcha_val)

            
            driver.execute_script("submit_causelist('civ')")

            
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "dispTable"))
                )
                save_all_cases_to_txt(driver.page_source)
            except TimeoutException:
                st.error("Timeout: Result table did not appear.")

    with col2:
        if st.button("Criminal"):
            
            captcha_input = driver.find_element(By.ID, "cause_list_captcha_code")
            captcha_input.clear()
            captcha_input.send_keys(captcha_val)

           
            driver.execute_script("submit_causelist('cri')")

            
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.ID, "dispTable"))
                )
                save_all_cases_to_txt(driver.page_source)
            except TimeoutException:
                st.error("Timeout: Result table did not appear.")


    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "dispTable")))
        save_all_cases_to_txt(driver.page_source)
    except TimeoutException:
        st.error("Timeout: Result table did not appear.")
