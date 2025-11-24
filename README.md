# 🖼️ Cute Image Resizer Tool

A beautiful and efficient batch image resizer with both web interface and command-line options.

## 🌟 Live Demo
**Live App:**  image-resizer-tool-production.up.railway.app
## ✨ Features

- 🎨 **Beautiful Web Interface** - Cute and responsive design
- ⚡ **Batch Processing** - Resize multiple images at once
- 📱 **Mobile Friendly** - Works perfectly on mobile devices
- 🖥️ **CLI Version** - Command-line tool for automation
- 🔄 **Format Conversion** - Convert between JPEG, PNG, WebP
- 📦 **ZIP Download** - Download all resized images as a single ZIP file

## 🚀 Quick Start

### Web Version (Recommended for Mobile)

1. **Visit the live website** (after deploying to Render)
2. **Upload your images** - Select multiple images from your device
3. **Set dimensions** - Choose width and height
4. **Choose format** - Optional format conversion
5. **Download** - Get all resized images as ZIP file

### Command Line Version

```bash
# Basic usage
python image_resizer.py

# Custom size and format
python image_resizer.py --width 1024 --height 768 --format PNG

# Custom folders
python image_resizer.py --input my_photos --output results --width 400 --height 300
