from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
from werkzeug.utils import secure_filename
from PIL import Image
import zipfile
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_single_image(image_path, output_path, width, height, format=None):
    """Resize a single image"""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Resize image
            resized_img = img.resize((width, height), Image.LANCZOS)
            
            # Save image
            if format:
                resized_img.save(output_path, format=format)
            else:
                resized_img.save(output_path)
            
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resize', methods=['POST'])
def resize_images():
    if 'images' not in request.files:
        flash('❌ No files selected!', 'error')
        return redirect(url_for('index'))
    
    files = request.files.getlist('images')
    width = int(request.form.get('width', 800))
    height = int(request.form.get('height', 600))
    output_format = request.form.get('format', '').upper() or None
    
    if not files or files[0].filename == '':
        flash('❌ Please select at least one image!', 'error')
        return redirect(url_for('index'))
    
    # Create temporary directory
    temp_dir = 'temp_resized'
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    
    processed_files = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_path = os.path.join(temp_dir, f"temp_{filename}")
            file.save(input_path)
            
            # Determine output filename
            name, ext = os.path.splitext(filename)
            if output_format:
                output_filename = f"resized_{name}.{output_format.lower()}"
            else:
                output_filename = f"resized_{filename}"
            
            output_path = os.path.join(temp_dir, output_filename)
            
            if resize_single_image(input_path, output_path, width, height, output_format):
                processed_files.append(output_filename)
            
            # Clean up temporary input file
            if os.path.exists(input_path):
                os.remove(input_path)
    
    if processed_files:
        # Create zip file
        zip_filename = 'resized_images.zip'
        zip_path = os.path.join(temp_dir, zip_filename)
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in processed_files:
                file_path = os.path.join(temp_dir, file)
                zipf.write(file_path, file)
        
        flash(f'🎉 Successfully resized {len(processed_files)} images!', 'success')
        return send_file(zip_path, as_attachment=True, download_name=zip_filename)
    else:
        flash('❌ No images were processed successfully.', 'error')
        return redirect(url_for('index'))

@app.route('/batch-info')
def batch_info():
    return render_template('batch_info.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
