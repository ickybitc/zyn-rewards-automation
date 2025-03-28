from flask import Flask, render_template, request, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pytesseract
import cv2
import numpy as np
from PIL import Image
import io
import time
import os

app = Flask(__name__)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Use ChromeDriverManager with specific path for PythonAnywhere
    service = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def process_image(image_data):
    # Convert image data to numpy array
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to preprocess the image
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    
    # Apply dilation to connect text components
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    gray = cv2.dilate(gray, kernel, iterations=1)
    
    # Convert to PIL Image for Tesseract
    pil_image = Image.fromarray(gray)
    
    # Extract text using Tesseract
    text = pytesseract.image_to_string(pil_image)
    
    # Clean up the extracted text
    text = ''.join(c for c in text if c.isalnum())
    
    return text

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/automate', methods=['POST'])
def automate():
    try:
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([email, password]):
            return jsonify({'error': 'Missing required parameters'}), 400
        
        # Handle image upload
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename:
                image_data = image_file.read()
                code = process_image(image_data)
                if not code:
                    return jsonify({'error': 'Could not extract code from image. Please try again or enter code manually.'}), 400
        else:
            code = request.form.get('code')
            if not code:
                return jsonify({'error': 'Please provide either an image or a code'}), 400
        
        driver = setup_driver()
        
        # Navigate to ZYN Rewards
        driver.get('https://us.zyn.com/ZYNRewards/')
        
        # Wait for and click the login button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='login-button']"))
        )
        login_button.click()
        
        # Wait for and fill in email
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
        )
        email_input.send_keys(email)
        
        # Fill in password
        password_input = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
        password_input.send_keys(password)
        
        # Click login submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        
        # Wait for the rewards input field
        rewards_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[placeholder*='code']"))
        )
        
        # Input the rewards code
        rewards_input.send_keys(code)
        
        # Find and click the submit button
        submit_code_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_code_button.click()
        
        # Wait a moment to ensure the submission is processed
        time.sleep(3)
        
        # Check for success message or error
        try:
            success_message = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div[role='alert']"))
            )
            message = success_message.text
        except:
            message = "Code submitted successfully"
        
        driver.quit()
        return jsonify({'success': True, 'message': message})
        
    except Exception as e:
        if 'driver' in locals():
            driver.quit()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0') 