# Email Signature Generator

A simple, elegant HTML email signature generator that runs entirely in your browser. No backend, no dependencies - just download and use!

## Features

- **Client-side only** - No server needed, runs entirely in your browser
- **Zero dependencies** - Single HTML file with everything included
- **Auto-save** - Form data saved to localStorage automatically
- **Live preview** - See your signature as you build it
- **Copy to clipboard** - One-click copy functionality
- **Responsive design** - Works on desktop, tablet, and mobile
- **Form validation** - Ensures required fields are filled
- **Professional styling** - Clean, modern interface
- **Email-compatible HTML** - Generated signatures work across all major email clients

## Quick Start

1. **Download** the `index.html` file from this repository
2. **Open** the file in any modern web browser
3. **Fill in** your information in the form
4. **Click** "Generate Signature" to create your HTML signature
5. **Copy** the generated HTML using the "Copy to Clipboard" button
6. **Paste** into your email client's signature settings

## How to Add Your Signature to Email Clients

### Gmail
1. Open Gmail and click the gear icon → "See all settings"
2. Scroll down to the "Signature" section
3. Click "Create new" and name your signature
4. In the signature editor, click the "Insert HTML" button (looks like `<>`)
5. Paste your generated HTML signature
6. Click "Save Changes" at the bottom

### Outlook (Web)
1. Click the gear icon → "View all Outlook settings"
2. Go to Mail → Compose and reply
3. Under "Email signature", click "New signature"
4. Name your signature and paste the HTML in the editor
5. Select when to use the signature and save

### Apple Mail
1. Open Mail → Preferences → Signatures
2. Click the "+" button to create a new signature
3. Uncheck "Always match my default font"
4. Paste your HTML signature
5. Drag the signature to the desired email account

### Thunderbird
1. Go to Account Settings → Select your account
2. Check "Attach the signature from a file"
3. Save your HTML signature as a `.html` file
4. Browse and select the file
5. Click OK to save

## Form Fields

- **Full Name** (required) - Your display name
- **Job Title** (required) - Your professional title
- **Primary Phone** - Main contact number
- **Secondary Phone** - Alternative contact number
- **LinkedIn URL** - Your LinkedIn profile link
- **LinkedIn Link Text** - Custom text for the LinkedIn link (default: "Connect on LinkedIn")

## Browser Compatibility

Works on all modern browsers:
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+
- Opera 47+

## Customization Tips

The generated HTML signature includes inline styles for maximum email client compatibility. If you want to customize the appearance:

1. **Colors**: Edit the `color` values in the generated HTML
2. **Font Size**: Adjust the `font-size` values
3. **Spacing**: Modify the `<br>` tags or add padding/margin styles
4. **Font Family**: Change the `font-family` value (stick to web-safe fonts)

## Privacy

This tool runs entirely in your browser. No data is sent to any server. Your information is only stored locally in your browser's localStorage for convenience.

## License

MIT License - feel free to use, modify, and distribute as needed.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Support

If you encounter any issues or have suggestions, please [open an issue](https://github.com/yourusername/email-signature-generator/issues) on GitHub.

---

Made with HTML, CSS, and JavaScript - Keep it simple!