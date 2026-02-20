# 🖼️ Bulk Image Resizer

A powerful Python script to resize, rename, and convert images in bulk using Pillow.

## 🚀 Quick Start

### Install
```bash
pip install Pillow
```

### Run
```bash
python resizer.py
```

That's it! The interactive menu will guide you.

## ✨ Features

### Core Features
✅ **Bulk resize** - Process entire folders at once  
✅ **Multiple modes** - Fit, fill, stretch, or pad  
✅ **Smart aspect ratio** - Maintain proportions automatically  
✅ **Format conversion** - Convert between JPEG, PNG, WEBP, etc.  
✅ **Quality control** - Adjust compression for smaller files  
✅ **Presets** - Quick resize for common sizes  
✅ **Batch rename** - Add prefixes, suffixes, sequential numbers  
✅ **Progress tracking** - See what's happening in real-time  

### Advanced Features
✅ **Recursive processing** - Handle subdirectories  
✅ **EXIF preservation** - Keep photo metadata  
✅ **Smart cropping** - Intelligent fill mode  
✅ **Format optimization** - Automatic quality settings  
✅ **Error handling** - Skip broken images, report errors  
✅ **File size reporting** - See compression savings  

## 📐 Resize Modes

### 1. **Fit** (Default)
Resize to fit within dimensions, maintaining aspect ratio.
```
Original: 1920x1080  →  Target: 800x600
Result:   800x450 (fits width, maintains ratio)
```

### 2. **Fill**
Resize and crop to fill exact dimensions.
```
Original: 1920x1080  →  Target: 800x800
Result:   800x800 (cropped to square)
```

### 3. **Stretch**
Stretch to exact dimensions (may distort).
```
Original: 1920x1080  →  Target: 800x800
Result:   800x800 (stretched, distorted)
```

### 4. **Pad**
Resize to fit and add padding.
```
Original: 1920x1080  →  Target: 800x800
Result:   800x800 (with white bars top/bottom)
```

## 🎯 Common Use Cases

### Social Media
```python
# Instagram posts
Width: 1080, Height: 1080, Mode: fill

# Facebook cover
Width: 1200, Height: 630, Mode: fill

# Twitter header
Width: 1200, Height: 675, Mode: fill
```

### Thumbnails
```python
# Small thumbnails
Width: 150, Height: 150, Mode: fill

# Medium thumbnails
Width: 320, Height: 320, Mode: fit
```

### Web Optimization
```python
# Full width images
Width: 1920, Height: auto, Mode: fit, Quality: 80

# Hero images
Width: 1920, Height: 1080, Mode: fill, Quality: 85
```

### Print Preparation
```python
# 4x6 inches at 300 DPI
Width: 1800, Height: 1200, Mode: fit, Quality: 95
```

## 📋 Menu Options

### 1. Quick Resize (Presets)
Choose from common presets:
- Thumbnail (150x150)
- Small (320x320)
- Medium (640x640)
- Large (1024x1024)
- HD (1920x1080)
- Instagram (1080x1080)
- Facebook (1200x630)
- Twitter (1200x675)
- YouTube (1280x720)
- Profile (400x400)

**Example:**
```
Select: 6 (Instagram)
Input folder: /Users/john/Photos
✅ Processing 47 images to 1080x1080...
```

### 2. Custom Dimensions
Specify your own width and height.

**Example:**
```
Width: 1200
Height: 800
Mode: fit
Quality: 90
```

### 3. Batch Convert Format
Convert all images to a different format.

**Example:**
```
Input: Folder with PNG files
Output format: JPEG
Quality: 85
Result: All PNGs converted to JPEGs
```

### 4. Advanced Options
Full control over all settings:
- Custom output folder
- Filename prefixes/suffixes
- Sequential numbering
- Recursive subdirectories
- Overwrite settings

## 🎨 Quality Settings

### JPEG Quality Guide
- **60** - Low (small files, visible artifacts)
- **80** - Medium (good balance)
- **85** - High (recommended default)
- **95** - Maximum (large files, minimal compression)
- **100** - Lossless (very large files)

### WEBP Quality Guide
- **70** - Low (better than JPEG 60)
- **80** - Medium (better than JPEG 85)
- **90** - High (better than JPEG 95)
- **95** - Maximum (excellent quality)

## 📝 Example Workflows

### Workflow 1: Optimize Photos for Web
```
Input: Raw photos from camera (4000x3000, 5MB each)
Settings:
  - Width: 1920
  - Height: auto
  - Mode: fit
  - Quality: 85
  - Format: JPEG

Result: Web-optimized images (~300KB each)
```

### Workflow 2: Create Thumbnails
```
Input: Product photos
Settings:
  - Preset: thumbnail (150x150)
  - Mode: fill
  - Prefix: thumb_
  - Format: WEBP

Result: thumb_product1.webp, thumb_product2.webp...
```

### Workflow 3: Social Media Batch
```
Input: Event photos
Settings:
  - Width: 1080
  - Height: 1080
  - Mode: fill
  - Quality: 90
  - Sequential: yes

Result: Instagram-ready images with numbers
```

### Workflow 4: Format Conversion
```
Input: 100 PNG screenshots
Settings:
  - Convert to: JPEG
  - Quality: 90
  - Prefix: screenshot_

Result: All PNGs converted to JPEG, ~70% file size reduction
```

## 🔧 Advanced Usage

### Filename Patterns

**Prefix + Original + Suffix + Counter:**
```
Input: photo.jpg
Prefix: resized_
Suffix: _edited
Sequential: yes (counter 0001)

Output: resized_photo_edited_0001.jpg
```

### Recursive Processing
```
Input folder structure:
  /photos
    /vacation
      img1.jpg
      img2.jpg
    /family
      img3.jpg

Recursive: yes

Output maintains structure:
  /photos/resized
    /vacation
      img1.jpg
      img2.jpg
    /family
      img3.jpg
```

### Format Optimization

**PNG to JPEG (with transparency handling):**
```
Input: logo.png (with transparency)
Output format: JPEG
Result: White background added automatically
```

**JPEG to WEBP (smaller files):**
```
Input: photo.jpg (1MB)
Output format: WEBP
Quality: 85
Result: photo.webp (~400KB, same quality)
```

## 📊 Performance

**Example batch (100 photos):**
```
Original: 100 photos, 4000x3000px, 500MB total
Target: 1920x1080px, JPEG quality 85

Results:
✅ Processed: 100/100
📉 Total size: 500MB → 45MB (91% reduction)
⏱️  Time: ~25 seconds
```

## 🐛 Troubleshooting

### "No images found"
- Check the folder path is correct
- Ensure files have image extensions (.jpg, .png, etc.)
- Try absolute path instead of relative

### "Permission denied"
- Check folder write permissions
- Don't use system folders
- Try a different output folder

### "Image cannot be opened"
- File might be corrupted
- Check file is actually an image
- Script will skip and continue with others

### "Out of memory"
- Processing very large images (>10,000px)
- Reduce target dimensions
- Process in smaller batches

## 💡 Tips & Tricks

**1. Test on a few images first**
```
Create a test folder with 3-5 images
Run your settings
Check the results
Then process the full folder
```

**2. Keep originals safe**
```
Never overwrite original folder
Always use output folder
Or make a backup first
```

**3. Compare file sizes**
```
Script shows size reduction percentage
Higher compression = smaller files
But may reduce quality
```

**4. Use presets for speed**
```
Don't reinvent the wheel
Presets are optimized for common uses
Customize only when needed
```

**5. Batch by purpose**
```
Don't mix different needs
Thumbnails in one batch
Full-size in another
Social media separately
```

## 🧠 What You're Learning

### Python Concepts
- **File I/O** - Reading and writing files
- **Path handling** - Using pathlib for cross-platform paths
- **Iteration** - Looping through folders and files
- **Error handling** - Try/except for robust code
- **String formatting** - f-strings, padding, alignment
- **CLI menus** - Building interactive interfaces

### Pillow (PIL) Library
- **Image.open()** - Load images
- **img.thumbnail()** - Resize maintaining aspect ratio
- **img.resize()** - Resize to exact dimensions
- **img.crop()** - Crop images
- **ImageOps.pad()** - Add padding
- **img.save()** - Save with options
- **EXIF handling** - Preserve metadata
- **Format conversion** - JPEG, PNG, WEBP, etc.

### Image Processing Concepts
- **Aspect ratios** - Width to height proportions
- **Resampling** - LANCZOS for quality
- **Compression** - Quality vs file size
- **Color modes** - RGB, RGBA, transparency
- **File formats** - When to use each
- **Batch processing** - Handling multiple files

## 🎓 Progression

This project builds on Day 1 & 2:

**Day 1:** File operations (organizing files)  
**Day 2:** CSV data handling (expenses)  
**Day 3:** Image processing (this project)  

**Next steps:**
- **Day 4+:** Add GUI with tkinter
- **Week 2:** Batch watermarking
- **Week 3:** Face detection & auto-crop
- **Week 4:** AI-powered smart cropping

## 📦 Dependencies

```bash
pip install Pillow
```

That's it! Pure Python stdlib + Pillow.

## 🌟 Future Enhancements

Want to extend this? Ideas:
- Add watermarks
- Rotate images
- Auto-enhance (brightness, contrast)
- Face detection for smart cropping
- GUI with drag-and-drop
- Batch effects (filters, grayscale, etc.)
- Video thumbnail generation
- PDF to images conversion

## Day 3 of #30DaysOfPython 🐍

From basic file operations to image processing - you're leveling up!
