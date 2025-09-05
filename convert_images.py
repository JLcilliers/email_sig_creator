"""
Utility script to convert images to base64 strings for embedding in HTML
"""

import base64
import os
from PIL import Image
import io

def convert_image_to_base64(image_path, resize=None):
    """Convert an image file to base64 string"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            elif img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Resize if needed
            if resize:
                img.thumbnail(resize, Image.Resampling.LANCZOS)
            
            # Save to buffer
            buffer = io.BytesIO()
            img.save(buffer, format='PNG', optimize=True)
            
            # Convert to base64
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            return img_base64
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
        return None

def create_phone_icon():
    """Create an orange circle with phone icon"""
    from PIL import Image, ImageDraw
    
    # Create a new image with transparent background
    size = (40, 40)
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw orange circle
    circle_color = (255, 102, 0, 255)  # #FF6600 - matching the original orange
    draw.ellipse([0, 0, 39, 39], fill=circle_color)
    
    # Draw phone icon (simple phone shape in white)
    phone_color = (255, 255, 255, 255)
    # Create a simple phone path
    draw.arc([10, 10, 30, 30], start=225, end=45, fill=phone_color, width=3)
    draw.ellipse([8, 8, 14, 14], fill=phone_color)
    draw.ellipse([26, 26, 32, 32], fill=phone_color)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

def create_linkedin_icon():
    """Create a LinkedIn icon"""
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a new image
    size = (40, 40)
    img = Image.new('RGBA', size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw blue square with rounded corners
    linkedin_color = (0, 119, 181, 255)  # LinkedIn blue
    draw.rounded_rectangle([2, 2, 38, 38], radius=4, fill=linkedin_color)
    
    # Draw "in" text
    try:
        # Try to use a font, fallback to default if not available
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    
    draw.text((10, 5), "in", fill=(255, 255, 255, 255), font=font)
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    return base64.b64encode(buffer.getvalue()).decode('utf-8')

if __name__ == "__main__":
    print("Converting images to base64...")
    
    # Process partner logos and company logos
    image_mappings = {
        "GOOGLE_PARTNER": "Images/images.png",  # Google Partner badge
        "META_PARTNER": "Images/Met-Business-Partners.png",  # Meta Business Partner
        "MAILCHIMP": "Images/MC-Partner-Horizontal-Final_1.png",  # Mailchimp
        "BING": "Images/images.png",  # Using as Bing placeholder
        "FSE_DIGITAL": "Images/FSE-Digital-Logo (1).jpg",  # FSE Digital logo
        "FREELANCE_SEO": "Images/Freenlance-SEO-Logo-RGB.png",  # Freelance SEO logo
    }
    
    results = {}
    
    # Convert partner logos
    for name, path in image_mappings.items():
        if os.path.exists(path):
            print(f"Converting {name}...")
            base64_str = convert_image_to_base64(path, resize=(150, 50))
            if base64_str:
                results[name] = base64_str[:100] + "..." if len(base64_str) > 100 else base64_str
                print(f"  [OK] {name} converted (length: {len(base64_str)})")
        else:
            print(f"  [X] {path} not found")
    
    # Create icons
    print("\nCreating icons...")
    phone_icon = create_phone_icon()
    linkedin_icon = create_linkedin_icon()
    
    print(f"  [OK] Phone icon created (length: {len(phone_icon)})")
    print(f"  [OK] LinkedIn icon created (length: {len(linkedin_icon)})")
    
    # Save to a Python file for easy import
    with open('image_data.py', 'w') as f:
        f.write('"""\nBase64 encoded images for email signature\n"""\n\n')
        f.write(f'PHONE_ICON = "{phone_icon}"\n\n')
        f.write(f'LINKEDIN_ICON = "{linkedin_icon}"\n\n')
        
        for name, data in results.items():
            full_path = image_mappings[name]
            if os.path.exists(full_path):
                full_base64 = convert_image_to_base64(full_path, resize=(150, 50))
                if full_base64:
                    f.write(f'{name} = "{full_base64}"\n\n')
    
    print("\n[OK] Image data saved to image_data.py")
    print("\nYou can now import these in your app.py file:")
    print("from image_data import PHONE_ICON, LINKEDIN_ICON, GOOGLE_PARTNER, META_PARTNER, MAILCHIMP, SEMRUSH")