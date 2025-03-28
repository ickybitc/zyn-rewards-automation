# ZYN Rewards Code Automation

A web application that automatically submits ZYN Rewards codes. Built with Flask and Selenium, featuring OCR capabilities for code extraction from images.

## Features

- Manual code entry
- Image upload with OCR (Optical Character Recognition)
- Automated login and code submission
- Modern, responsive UI
- Real-time feedback on submission status

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- pip (Python package manager)
- Tesseract OCR

### Installing Tesseract OCR

#### macOS
```bash
brew install tesseract
```

#### Ubuntu/Debian
```bash
sudo apt-get install tesseract-ocr
```

#### Windows
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## Setup

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/zyn-rewards-automation.git
   cd zyn-rewards-automation
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://localhost:5000`

## Usage

### Manual Code Entry
1. Enter your ZYN Rewards code in the text field
2. Enter your ZYN Rewards account email
3. Enter your ZYN Rewards account password
4. Click "Submit Code"

### Image Upload
1. Take a clear photo of your ZYN Rewards code
2. Upload the image using the file upload button
3. Enter your ZYN Rewards account email
4. Enter your ZYN Rewards account password
5. Click "Submit Code"

## Tips for Best Results

- When using image upload:
  - Take a clear, well-lit photo of the code
  - Ensure the code is in focus
  - Minimize glare and shadows
  - If OCR fails, you can still enter the code manually

## Security Considerations

- This tool should only be used on websites where you have permission to automate actions
- Do not use this tool for malicious purposes or to bypass security measures
- Be aware that some websites may detect and block automated access
- Your credentials are only used for this specific automation and are not stored

## Troubleshooting

If you encounter any issues:
1. Make sure all dependencies are installed correctly
2. Check that Chrome is installed and up to date
3. Verify that Tesseract OCR is installed and accessible
4. Check the browser console for any error messages
5. Ensure your internet connection is stable

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Make sure to comply with ZYN's terms of service when using this application. 