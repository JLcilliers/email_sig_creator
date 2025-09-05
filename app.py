from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename
import os
import base64
import io
from PIL import Image
from html2image import Html2Image
import tempfile
import shutil

# Import real base64 encoded images
try:
    from image_data import PHONE_ICON, LINKEDIN_ICON, GOOGLE_PARTNER, META_PARTNER, MAILCHIMP, BING, FSE_DIGITAL, FREELANCE_SEO
except ImportError:
    # Fallback to placeholders if image_data.py doesn't exist
    PHONE_ICON = "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNui8sowAAAAWdEVYdENyZWF0aW9uIFRpbWUAMDEvMDEvMDAg0AAAACB0RVh0Q29weXJpZ2h0AENvcHlyaWdodCAoQykgMjAwMCDRAAAAJ0lEQVQ4jWP8//8/AzUBEwOVwajBowaPGjxq8KjBowaPGjxq8NAEAAB2AwR5bkG9AAAAAElFTkSuQmCC"
    LINKEDIN_ICON = "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNui8sowAAAAWdEVYdENyZWF0aW9uIFRpbWUAMDEvMDEvMDAg0AAAACB0RVh0Q29weXJpZ2h0AENvcHlyaWdodCAoQykgMjAwMCDRAAAAJ0lEQVQ4jWP8//8/AzUBEwOVwajBowaPGjxq8KjBowaPGjxq8NAEAAB2AwR5bkG9AAAAAElFTkSuQmCC"
    GOOGLE_PARTNER = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAeCAYAAABuUU38AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNui8sowAAAAWdEVYdENyZWF0aW9uIFRpbWUAMDEvMDEvMDAg0AAAACB0RVh0Q29weXJpZ2h0AENvcHlyaWdodCAoQykgMjAwMCDRAAAAJ0lEQVRYhe3OMQ0AAAgDMPybjUcEhRMkCqDRAAAAAAAAAAAAAPy0AxYgAAG0L9PdAAAAAElFTkSuQmCC"
    META_PARTNER = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAeCAYAAABuUU38AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNui8sowAAAAWdEVYdENyZWF0aW9uIFRpbWUAMDEvMDEvMDAg0AAAACB0RVh0Q29weXJpZ2h0AENvcHlyaWdodCAoQykgMjAwMCDRAAAAJ0lEQVRYhe3OMQ0AAAgDMPybjUcEhRMkCqDRAAAAAAAAAAAAAPy0AxYgAAG0L9PdAAAAAElFTkSuQmCC"
    MAILCHIMP = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAeCAYAAABuUU38AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNui8sowAAAAWdEVYdENyZWF0aW9uIFRpbWUAMDEvMDEvMDAg0AAAACB0RVh0Q29weXJpZ2h0AENvcHlyaWdodCAoQykgMjAwMCDRAAAAJ0lEQVRYhe3OMQ0AAAgDMPybjUcEhRMkCqDRAAAAAAAAAAAAAPy0AxYgAAG0L9PdAAAAAElFTkSuQmCC"
    BING = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAeCAYAAABuUU38AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNui8sowAAAAWdEVYdENyZWF0aW9uIFRpbWUAMDEvMDEvMDAg0AAAACB0RVh0Q29weXJpZ2h0AENvcHlyaWdodCAoQykgMjAwMCDRAAAAJ0lEQVRYhe3OMQ0AAAgDMPybjUcEhRMkCqDRAAAAAAAAAAAAAPy0AxYgAAG0L9PdAAAAAElFTkSuQmCC"
    FSE_DIGITAL = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAeCAYAAABuUU38AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNui8sowAAAAWdEVYdENyZWF0aW9uIFRpbWUAMDEvMDEvMDAg0AAAACB0RVh0Q29weXJpZ2h0AENvcHlyaWdodCAoQykgMjAwMCDRAAAAJ0lEQVRYhe3OMQ0AAAgDMPybjUcEhRMkCqDRAAAAAAAAAAAAAPy0AxYgAAG0L9PdAAAAAElFTkSuQmCC"
    FREELANCE_SEO = "iVBORw0KGgoAAAANSUhEUgAAADIAAAAeCAYAAABuUU38AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAABx0RVh0U29mdHdhcmUAQWRvYmUgRmlyZXdvcmtzIENTNui8sowAAAAWdEVYdENyZWF0aW9uIFRpbWUAMDEvMDEvMDAg0AAAACB0RVh0Q29weXJpZ2h0AENvcHlyaWdodCAoQykgMjAwMCDRAAAAJ0lEQVRYhe3OMQ0AAAgDMPybjUcEhRMkCqDRAAAAAAAAAAAAAPy0AxYgAAG0L9PdAAAAAElFTkSuQmCC"

app = Flask(__name__)
app.secret_key = 'your-secret-key-here-change-in-production'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max file size
app.config['UPLOAD_FOLDER'] = 'temp'

# Create temp directory if it doesn't exist
if not os.path.exists('temp'):
    os.makedirs('temp')

# Allowed image extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image(image_file):
    """Process uploaded image: resize and convert to base64"""
    img = Image.open(image_file)
    
    # Convert to RGB if necessary (for PNG with transparency)
    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Create circular crop - matching the example size
    size = (90, 90)
    img.thumbnail(size, Image.Resampling.LANCZOS)
    
    # Create a square image
    square_img = Image.new('RGB', size, (255, 255, 255))
    img_pos = ((size[0] - img.width) // 2, (size[1] - img.height) // 2)
    square_img.paste(img, img_pos)
    
    # Convert to base64
    buffer = io.BytesIO()
    square_img.save(buffer, format='PNG')
    img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return img_base64


def generate_html_signature(name, title, phone, linkedin_url, photo_base64):
    """Generate HTML email signature"""
    # Extract just the username from LinkedIn URL for display
    linkedin_username = linkedin_url.split('/')[-1] if '/' in linkedin_url else linkedin_url
    
    html_template = f'''<table cellpadding="0" cellspacing="0" border="0" style="border-collapse: collapse; font-family: Arial, sans-serif; width: 500px; background: white;">
  <tr>
    <td style="vertical-align: top; padding-right: 15px; position: relative;">
      <!-- Orange circular border around photo -->
      <div style="position: relative; width: 100px; height: 100px;">
        <div style="position: absolute; top: -5px; left: -5px; width: 110px; height: 110px; border-radius: 50%; background: #FF6B35;"></div>
        <img src="data:image/png;base64,{photo_base64}" style="position: relative; width: 90px; height: 90px; border-radius: 50%; display: block; margin: 5px; border: 3px solid white;">
      </div>
    </td>
    <td style="vertical-align: top; padding-top: 8px;">
      <div style="font-size: 22px; font-weight: bold; color: #1a1a1a; margin: 0 0 3px 0;">{name}</div>
      <div style="font-size: 13px; color: #666666; margin: 0 0 8px 0;">{title}</div>
      
      <!-- Company logos -->
      <div style="margin: 0 0 10px 0;">
        <img src="data:image/png;base64,{FSE_DIGITAL}" style="height: 20px; margin-right: 5px; vertical-align: middle;">
        <img src="data:image/png;base64,{FREELANCE_SEO}" style="height: 20px; vertical-align: middle;">
      </div>
      
      <div style="border-top: 2px solid #0066CC; margin: 10px 0 10px 0; width: 280px;"></div>
      
      <!-- Phone -->
      <div style="margin: 8px 0;">
        <img src="data:image/png;base64,{PHONE_ICON}" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;">
        <span style="font-size: 13px; color: #333333; vertical-align: middle;">{phone}</span>
      </div>
      
      <!-- LinkedIn -->
      <div style="margin: 8px 0;">
        <img src="data:image/png;base64,{LINKEDIN_ICON}" style="width: 18px; height: 18px; vertical-align: middle; margin-right: 8px;">
        <a href="{linkedin_url}" style="color: #0077B5; text-decoration: none; font-size: 13px; vertical-align: middle;">LinkedIn</a>
      </div>
    </td>
  </tr>
  <tr>
    <td colspan="2" style="padding-top: 12px;">
      <table cellpadding="0" cellspacing="0" border="0">
        <tr>
          <td style="padding-right: 10px;">
            <img src="data:image/png;base64,{GOOGLE_PARTNER}" style="height: 35px;">
          </td>
          <td style="padding-right: 10px;">
            <img src="data:image/png;base64,{BING}" style="height: 35px;">
          </td>
          <td style="padding-right: 10px;">
            <img src="data:image/png;base64,{META_PARTNER}" style="height: 35px;">
          </td>
          <td style="padding-right: 10px;">
            <div style="background: #7C4DFF; padding: 5px 8px; border-radius: 3px; display: inline-block;">
              <span style="color: white; font-size: 12px; font-weight: bold;">Partner<br>Academy</span>
            </div>
          </td>
          <td>
            <img src="data:image/png;base64,{MAILCHIMP}" style="height: 35px;">
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>'''
    return html_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    # Validate form inputs
    if 'name' not in request.form or not request.form['name']:
        flash('Name is required')
        return redirect(url_for('index'))
    
    if 'title' not in request.form or not request.form['title']:
        flash('Title is required')
        return redirect(url_for('index'))
    
    if 'phone' not in request.form or not request.form['phone']:
        flash('Phone number is required')
        return redirect(url_for('index'))
    
    if 'linkedin' not in request.form or not request.form['linkedin']:
        flash('LinkedIn URL is required')
        return redirect(url_for('index'))
    
    if 'photo' not in request.files:
        flash('No photo uploaded')
        return redirect(url_for('index'))
    
    photo = request.files['photo']
    if photo.filename == '':
        flash('No photo selected')
        return redirect(url_for('index'))
    
    if not allowed_file(photo.filename):
        flash('Invalid file type. Please upload an image file.')
        return redirect(url_for('index'))
    
    # Get form data
    name = request.form['name']
    title = request.form['title']
    phone = request.form['phone']
    linkedin_url = request.form['linkedin']
    
    # Process the uploaded photo
    try:
        photo_base64 = process_image(photo)
    except Exception as e:
        flash(f'Error processing image: {str(e)}')
        return redirect(url_for('index'))
    
    # Generate HTML signature
    html_signature = generate_html_signature(name, title, phone, linkedin_url, photo_base64)
    
    # Generate PNG image
    try:
        # Create a temporary directory for html2image
        temp_dir = tempfile.mkdtemp()
        
        # Initialize Html2Image with temp directory - increased size for full signature
        hti = Html2Image(output_path=temp_dir, size=(500, 300))
        
        # Add CSS to make background white and add padding
        full_html = f'''
        <html>
        <head>
            <style>
                body {{
                    background-color: white;
                    margin: 0;
                    padding: 20px;
                    font-family: Arial, sans-serif;
                }}
            </style>
        </head>
        <body>
            {html_signature}
        </body>
        </html>
        '''
        
        # Generate the image
        files = hti.screenshot(html_str=full_html, save_as='signature.png')
        
        # Read the generated image
        png_path = os.path.join(temp_dir, 'signature.png')
        with open(png_path, 'rb') as f:
            png_data = f.read()
        
        # Clean up temp directory
        shutil.rmtree(temp_dir)
        
        # Save PNG to static folder for display
        static_dir = os.path.join(app.root_path, 'static')
        if not os.path.exists(static_dir):
            os.makedirs(static_dir)
        
        png_output_path = os.path.join(static_dir, 'signature.png')
        with open(png_output_path, 'wb') as f:
            f.write(png_data)
        
        png_generated = True
    except Exception as e:
        print(f"Error generating PNG: {str(e)}")
        png_generated = False
        flash('PNG generation requires Chrome to be installed. HTML signature is still available.')
    
    return render_template('result.html', 
                         html_code=html_signature,
                         png_generated=png_generated)

@app.route('/download/png')
def download_png():
    png_path = os.path.join(app.root_path, 'static', 'signature.png')
    if os.path.exists(png_path):
        return send_file(png_path, as_attachment=True, download_name='email_signature.png')
    else:
        flash('PNG file not found')
        return redirect(url_for('index'))

@app.route('/download/html')
def download_html():
    # Get the signature from session or regenerate
    # For simplicity, we'll redirect to home
    flash('Please regenerate the signature to download HTML')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)