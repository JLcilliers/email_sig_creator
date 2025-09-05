# Email Signature Generator

A Flask web application that generates professional email signatures with both HTML code and PNG image outputs.

## Features

- Upload profile picture (automatically cropped to circle)
- Input personal details (name, title, phone, LinkedIn)
- Generate HTML email signature compatible with major email clients
- Export signature as PNG image
- Partner badges included (Google Partner, SEMrush, Meta Business Partner, Mailchimp)

## Installation

1. Install Python 3.x if not already installed

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Install Google Chrome (required for PNG generation):
   - Download from: https://www.google.com/chrome/
   - The html2image library uses Chrome for rendering

## Usage

1. Run the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://127.0.0.1:5000
```

3. Fill in the form:
   - Full Name
   - Job Title
   - Cell Phone Number
   - LinkedIn Profile URL
   - Upload Profile Picture (square images work best)

4. Click "Generate Signature"

5. Copy the HTML code or download the PNG image

## How to Add the Signature to Email Clients

### Gmail
1. Go to Settings → See all settings
2. Navigate to General → Signature
3. Click "Create new"
4. Paste the HTML code
5. Save changes

### Outlook
1. Go to Settings → View all Outlook settings
2. Navigate to Mail → Compose and reply
3. Under Email signature, paste the HTML code
4. Save

### Apple Mail
1. Go to Preferences → Signatures
2. Click "+" to add new signature
3. Paste the HTML code
4. Uncheck "Match my default message font"

### Thunderbird
1. Go to Account Settings
2. Under your account, find "Signature text"
3. Check "Use HTML"
4. Paste the HTML code

## Customization

To update the partner logos or company branding:
1. Replace the images in the `Images/` folder
2. Run `python convert_images.py` to regenerate base64 encodings
3. The app will automatically use the new images

## Troubleshooting

- **PNG not generating**: Make sure Google Chrome is installed
- **Image upload errors**: Ensure image is under 2MB and in JPG/PNG format
- **Signature not displaying correctly**: Use the HTML code option for best compatibility

## Company Branding

The signature displays:
- **Company**: fseDigital freelanceSEO (with orange accent)
- **Partner Badges**: Google Partner, SEMrush, Meta Business Partner, Mailchimp
