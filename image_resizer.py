import os
from PIL import Image
import argparse

def resize_image(input_path, output_path, size, format=None):
    """
    Resize an image to the specified size and save it.
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGB if necessary (for JPEG format)
            if format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Resize image - use LANCZOS for Pillow 9.5.0
            resized_img = img.resize(size, Image.LANCZOS)
            
            # Save image
            if format:
                resized_img.save(output_path, format=format)
            else:
                resized_img.save(output_path)
            
            print(f"✓ Resized: {os.path.basename(input_path)} -> {size[0]}x{size[1]}")
            return True
            
    except Exception as e:
        print(f"✗ Error processing {input_path}: {str(e)}")
        return False

def batch_resize_images(input_folder, output_folder, size, output_format=None):
    """
    Resize all images in a folder.
    """
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Supported image formats
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp')
    
    # Process all images in input folder
    processed_count = 0
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(supported_formats)]
    
    if not image_files:
        print("❌ No image files found in input folder!")
        return
    
    for filename in image_files:
        input_path = os.path.join(input_folder, filename)
        
        # Determine output filename and format
        name, ext = os.path.splitext(filename)
        if output_format:
            output_filename = f"{name}.{output_format.lower()}"
        else:
            output_filename = f"resized_{filename}"
        
        output_path = os.path.join(output_folder, output_filename)
        
        # Resize image
        if resize_image(input_path, output_path, size, output_format):
            processed_count += 1
    
    print(f"\n🎉 Resizing complete! Processed {processed_count} images.")
    print(f"📁 Output folder: {output_folder}")

def main():
    parser = argparse.ArgumentParser(description='🎨 Batch Image Resizer Tool')
    parser.add_argument('--input', '-i', default='input_images', 
                       help='Input folder path (default: input_images)')
    parser.add_argument('--output', '-o', default='resized_images', 
                       help='Output folder path (default: resized_images)')
    parser.add_argument('--width', '-w', type=int, default=800, 
                       help='Target width (default: 800)')
    parser.add_argument('--height', '-ht', type=int, default=600, 
                       help='Target height (default: 600)')
    parser.add_argument('--format', '-f', choices=['JPEG', 'PNG', 'WEBP'], 
                       help='Output format (optional)')
    
    args = parser.parse_args()
    
    print("🖼️  Image Resizer Tool")
    print("=" * 40)
    
    # Check if input folder exists
    if not os.path.exists(args.input):
        print(f"❌ Input folder '{args.input}' not found!")
        print("💡 Please create an 'input_images' folder and add your images.")
        print("   Or specify a different folder with: --input YOUR_FOLDER")
        return
    
    target_size = (args.width, args.height)
    
    print(f"📂 Input: {args.input}")
    print(f"📁 Output: {args.output}")
    print(f"📐 Size: {args.width}x{args.height}")
    if args.format:
        print(f"🎨 Format: {args.format}")
    print("=" * 40)
    print("Processing images...\n")
    
    batch_resize_images(args.input, args.output, target_size, args.format)

if __name__ == "__main__":
    main()
