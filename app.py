import os
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from PIL import Image
import zipfile
import io

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-12345')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Allowed extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def resize_single_image(image_file, width, height, output_format=None):
    """Resize a single image from file object"""
    try:
        with Image.open(image_file) as img:
            # Convert to RGB if necessary (for JPEG format)
            if output_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Resize image
            resized_img = img.resize((width, height), Image.LANCZOS)
            
            # Save to bytes
            img_bytes = io.BytesIO()
            if output_format:
                resized_img.save(img_bytes, format=output_format)
                extension = output_format.lower()
            else:
                # Keep original format
                format_map = {'JPEG': 'jpeg', 'PNG': 'png', 'GIF': 'gif', 'BMP': 'bmp', 'TIFF': 'tiff', 'WEBP': 'webp'}
                format_name = format_map.get(img.format, 'jpeg')
                resized_img.save(img_bytes, format=format_name)
                extension = format_name.lower()
            
            img_bytes.seek(0)
            return img_bytes, extension, True
            
    except Exception as e:
        print(f"Error processing image: {e}")
        return None, None, False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/resize', methods=['POST'])
def resize_images():
    if 'images' not in request.files:
        flash('❌ No files selected! Please choose some images.', 'error')
        return redirect(url_for('index'))
    
    files = request.files.getlist('images')
    width = int(request.form.get('width', 800))
    height = int(request.form.get('height', 600))
    output_format = request.form.get('format', '').upper() or None
    
    valid_files = [f for f in files if f and f.filename and allowed_file(f.filename)]
    
    if not valid_files:
        flash('❌ Please select at least one valid image file!', 'error')
        return redirect(url_for('index'))
    
    if len(valid_files) > 20:
        flash('❌ Too many files! Please select up to 20 images.', 'error')
        return redirect(url_for('index'))
    
    # Create in-memory zip file
    zip_buffer = io.BytesIO()
    success_count = 0
    
    try:
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for file in valid_files:
                try:
                    # Get original filename without extension
                    original_name = os.path.splitext(file.filename)[0]
                    
                    # Resize image
                    img_bytes, extension, success = resize_single_image(file, width, height, output_format)
                    
                    if success:
                        # Create output filename
                        output_filename = f"resized_{original_name}_{width}x{height}.{extension}"
                        
                        # Add to zip
                        zip_file.writestr(output_filename, img_bytes.getvalue())
                        success_count += 1
                        
                except Exception as e:
                    print(f"Error processing {file.filename}: {e}")
                    continue
        
        if success_count > 0:
            zip_buffer.seek(0)
            flash(f'🎉 Successfully resized {success_count} images!', 'success')
            return send_file(
                zip_buffer,
                as_attachment=True,
                download_name=f'resized_images_{width}x{height}.zip',
                mimetype='application/zip'
            )
        else:
            flash('❌ No images were processed successfully. Please try again.', 'error')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash('❌ Error creating ZIP file. Please try again.', 'error')
        return redirect(url_for('index'))

@app.route('/batch-info')
def batch_info():
    return render_template('batch_info.html')

@app.errorhandler(413)
def too_large(e):
    flash('❌ File too large! Please upload images smaller than 16MB.', 'error')
    return redirect(url_for('index'))

@app.errorhandler(500)
def internal_error(e):
    flash('❌ Server error occurred. Please try again.', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
