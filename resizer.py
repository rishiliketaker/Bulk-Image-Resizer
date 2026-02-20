#!/usr/bin/env python3
"""
Bulk Image Resizer
Resize, rename, and convert images in bulk using Pillow
Usage: python resizer.py
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageOps
from datetime import datetime
from config import *

class ImageResizer:
    """Bulk image resizer with multiple modes and options."""
    
    def __init__(self):
        self.processed = 0
        self.failed = 0
        self.errors = []
    
    def resize_image(self, input_path, output_path, width=None, height=None, 
                     mode='fit', quality=85, output_format=None, maintain_exif=True):
        """
        Resize a single image with various options.
        
        Args:
            input_path: Path to input image
            output_path: Path to save resized image
            width: Target width (None to maintain aspect ratio)
            height: Target height (None to maintain aspect ratio)
            mode: Resize mode ('fit', 'fill', 'stretch', 'pad')
            quality: JPEG/WEBP quality (1-100)
            output_format: Output format (None to keep original)
            maintain_exif: Whether to preserve EXIF data
        """
        try:
            # Open image
            img = Image.open(input_path)
            original_size = img.size
            
            # Convert RGBA to RGB if saving as JPEG
            if output_format == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                # Create white background
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Calculate target size
            if width and height:
                target_size = (width, height)
            elif width:
                # Maintain aspect ratio based on width
                ratio = width / img.width
                target_size = (width, int(img.height * ratio))
            elif height:
                # Maintain aspect ratio based on height
                ratio = height / img.height
                target_size = (int(img.width * ratio), height)
            else:
                # No resize needed
                target_size = img.size
            
            # Apply resize mode
            if mode == 'fit':
                # Resize to fit within dimensions (thumbnail with aspect ratio)
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                resized = img
            
            elif mode == 'fill':
                # Resize and crop to fill exact dimensions
                img_ratio = img.width / img.height
                target_ratio = target_size[0] / target_size[1]
                
                if img_ratio > target_ratio:
                    # Image is wider, crop width
                    new_width = int(img.height * target_ratio)
                    offset = (img.width - new_width) // 2
                    img = img.crop((offset, 0, offset + new_width, img.height))
                else:
                    # Image is taller, crop height
                    new_height = int(img.width / target_ratio)
                    offset = (img.height - new_height) // 2
                    img = img.crop((0, offset, img.width, offset + new_height))
                
                resized = img.resize(target_size, Image.Resampling.LANCZOS)
            
            elif mode == 'stretch':
                # Stretch to exact dimensions (may distort)
                resized = img.resize(target_size, Image.Resampling.LANCZOS)
            
            elif mode == 'pad':
                # Fit and add padding to reach exact dimensions
                img.thumbnail(target_size, Image.Resampling.LANCZOS)
                resized = ImageOps.pad(img, target_size, Image.Resampling.LANCZOS, color='white')
            
            else:
                raise ValueError(f"Unknown mode: {mode}")
            
            # Prepare save options
            save_kwargs = {}
            
            # Preserve EXIF data if requested and available
            if maintain_exif and hasattr(img, 'info'):
                exif = img.info.get('exif')
                if exif:
                    save_kwargs['exif'] = exif
            
            # Set quality for JPEG/WEBP
            if output_format in ('JPEG', 'WEBP') or (not output_format and input_path.suffix.upper() in ('.JPG', '.JPEG', '.WEBP')):
                save_kwargs['quality'] = quality
                save_kwargs['optimize'] = True
            
            # Save image
            if output_format:
                save_kwargs['format'] = output_format
            
            resized.save(output_path, **save_kwargs)
            
            return {
                'success': True,
                'original_size': original_size,
                'new_size': resized.size,
                'file_size_before': os.path.getsize(input_path),
                'file_size_after': os.path.getsize(output_path)
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_output_filename(self, input_path, output_dir, prefix='', suffix='', 
                                 counter=None, output_format=None):
        """
        Generate output filename with various naming options.
        
        Args:
            input_path: Original file path
            output_dir: Output directory
            prefix: Prefix to add
            suffix: Suffix to add (before extension)
            counter: Number to add (for sequential naming)
            output_format: Output format (changes extension)
        """
        input_path = Path(input_path)
        stem = input_path.stem
        
        # Build new filename
        parts = []
        if prefix:
            parts.append(prefix)
        parts.append(stem)
        if suffix:
            parts.append(suffix)
        if counter is not None:
            parts.append(f"_{counter:04d}")
        
        new_stem = ''.join(parts)
        
        # Determine extension
        if output_format:
            ext = OUTPUT_FORMATS.get(output_format, '.jpg')
        else:
            ext = input_path.suffix.lower()
        
        return Path(output_dir) / f"{new_stem}{ext}"
    
    def process_folder(self, input_folder, output_folder=None, width=None, height=None,
                      mode='fit', quality=85, output_format=None, recursive=False,
                      prefix='', suffix='', sequential=False, overwrite=False):
        """
        Process all images in a folder.
        
        Args:
            input_folder: Source folder
            output_folder: Destination folder (None = create 'resized' subfolder)
            width, height, mode, quality, output_format: Resize options
            recursive: Process subdirectories
            prefix: Filename prefix
            suffix: Filename suffix
            sequential: Add sequential numbers to filenames
            overwrite: Overwrite existing files
        """
        input_folder = Path(input_folder)
        
        # Setup output folder
        if output_folder is None:
            output_folder = input_folder / 'resized'
        else:
            output_folder = Path(output_folder)
        
        output_folder.mkdir(parents=True, exist_ok=True)
        
        # Find all images
        if recursive:
            image_files = []
            for ext in SUPPORTED_FORMATS:
                image_files.extend(input_folder.rglob(f'*{ext}'))
                image_files.extend(input_folder.rglob(f'*{ext.upper()}'))
        else:
            image_files = []
            for ext in SUPPORTED_FORMATS:
                image_files.extend(input_folder.glob(f'*{ext}'))
                image_files.extend(input_folder.glob(f'*{ext.upper()}'))
        
        if not image_files:
            print(f"\n❌ No images found in {input_folder}")
            return
        
        print(f"\n📁 Found {len(image_files)} images")
        print(f"📂 Output: {output_folder}")
        print(f"🎯 Settings: {width or 'auto'}x{height or 'auto'}, {mode} mode, quality {quality}")
        print()
        
        # Process images
        counter = 1
        for idx, img_path in enumerate(image_files, 1):
            # Generate output path
            if recursive:
                # Maintain folder structure
                rel_path = img_path.relative_to(input_folder)
                out_path = output_folder / rel_path
                out_path.parent.mkdir(parents=True, exist_ok=True)
                output_path = self.generate_output_filename(
                    img_path, out_path.parent, prefix, suffix, 
                    counter if sequential else None, output_format
                )
            else:
                output_path = self.generate_output_filename(
                    img_path, output_folder, prefix, suffix,
                    counter if sequential else None, output_format
                )
            
            # Skip if exists and not overwriting
            if output_path.exists() and not overwrite:
                print(f"⏭️  Skipping {img_path.name} (already exists)")
                continue
            
            # Resize image
            print(f"[{idx}/{len(image_files)}] Processing {img_path.name}...", end=' ')
            
            result = self.resize_image(
                img_path, output_path, width, height, mode, quality, output_format
            )
            
            if result['success']:
                original = result['original_size']
                new = result['new_size']
                size_before = result['file_size_before'] / 1024  # KB
                size_after = result['file_size_after'] / 1024   # KB
                reduction = ((size_before - size_after) / size_before) * 100 if size_before > 0 else 0
                
                print(f"✅ {original[0]}x{original[1]} → {new[0]}x{new[1]} "
                      f"({size_before:.1f}KB → {size_after:.1f}KB, {reduction:+.1f}%)")
                
                self.processed += 1
                counter += 1
            else:
                print(f"❌ Failed: {result['error']}")
                self.failed += 1
                self.errors.append((img_path.name, result['error']))
        
        # Summary
        print(f"\n{'='*60}")
        print(f"✅ Processed: {self.processed}")
        print(f"❌ Failed: {self.failed}")
        if self.errors:
            print(f"\nErrors:")
            for filename, error in self.errors:
                print(f"  • {filename}: {error}")
        print(f"{'='*60}\n")


def show_menu():
    """Show interactive menu."""
    print("\n" + "="*60)
    print("🖼️  BULK IMAGE RESIZER")
    print("="*60)
    print("\nOptions:")
    print("1. Quick resize (choose preset)")
    print("2. Custom dimensions")
    print("3. Batch convert format")
    print("4. Advanced options")
    print("5. Exit")
    print()
    
    choice = input("Select option (1-5): ").strip()
    return choice


def quick_resize():
    """Quick resize using presets."""
    print("\n📐 Available Presets:")
    print()
    for i, (name, (w, h)) in enumerate(PRESETS.items(), 1):
        print(f"{i:2}. {name:15} → {w}x{h}px")
    
    print(f"\n{len(PRESETS)+1}. Custom size")
    
    preset_choice = input(f"\nSelect preset (1-{len(PRESETS)+1}): ").strip()
    
    try:
        idx = int(preset_choice) - 1
        if idx < len(PRESETS):
            preset_name = list(PRESETS.keys())[idx]
            width, height = PRESETS[preset_name]
            print(f"✅ Using {preset_name}: {width}x{height}px")
        else:
            width = int(input("Width (px): "))
            height = int(input("Height (px): "))
    except:
        print("❌ Invalid choice")
        return
    
    input_folder = input("\n📁 Input folder path: ").strip()
    
    if not os.path.exists(input_folder):
        print("❌ Folder not found")
        return
    
    resizer = ImageResizer()
    resizer.process_folder(
        input_folder,
        width=width,
        height=height,
        mode='fit',
        quality=85
    )


def custom_resize():
    """Custom resize with full options."""
    input_folder = input("\n📁 Input folder path: ").strip()
    
    if not os.path.exists(input_folder):
        print("❌ Folder not found")
        return
    
    print("\n🎯 Resize Settings:")
    width = input("Width (px, blank to auto): ").strip()
    height = input("Height (px, blank to auto): ").strip()
    
    width = int(width) if width else None
    height = int(height) if height else None
    
    if not width and not height:
        print("❌ Must specify at least width or height")
        return
    
    print("\n📐 Aspect Ratio Mode:")
    for i, (mode, desc) in enumerate(ASPECT_MODES.items(), 1):
        print(f"{i}. {mode:8} - {desc}")
    
    mode_choice = input(f"Select mode (1-{len(ASPECT_MODES)}): ").strip()
    try:
        mode = list(ASPECT_MODES.keys())[int(mode_choice) - 1]
    except:
        mode = 'fit'
    
    quality = input("\n🎨 Quality (1-100, default 85): ").strip()
    quality = int(quality) if quality else 85
    
    output_folder = input("\n📂 Output folder (blank for 'resized' subfolder): ").strip()
    output_folder = output_folder if output_folder else None
    
    resizer = ImageResizer()
    resizer.process_folder(
        input_folder,
        output_folder=output_folder,
        width=width,
        height=height,
        mode=mode,
        quality=quality
    )


def batch_convert():
    """Convert images to different format."""
    input_folder = input("\n📁 Input folder path: ").strip()
    
    if not os.path.exists(input_folder):
        print("❌ Folder not found")
        return
    
    print("\n🔄 Output Format:")
    for i, fmt in enumerate(OUTPUT_FORMATS.keys(), 1):
        print(f"{i}. {fmt}")
    
    fmt_choice = input(f"Select format (1-{len(OUTPUT_FORMATS)}): ").strip()
    try:
        output_format = list(OUTPUT_FORMATS.keys())[int(fmt_choice) - 1]
    except:
        print("❌ Invalid choice")
        return
    
    quality = 85 if output_format in ('JPEG', 'WEBP') else None
    
    resizer = ImageResizer()
    resizer.process_folder(
        input_folder,
        output_format=output_format,
        quality=quality
    )


def advanced_options():
    """Advanced resize with all options."""
    input_folder = input("\n📁 Input folder path: ").strip()
    
    if not os.path.exists(input_folder):
        print("❌ Folder not found")
        return
    
    output_folder = input("📂 Output folder (blank for 'resized' subfolder): ").strip() or None
    
    width = input("Width (px, blank to auto): ").strip()
    height = input("Height (px, blank to auto): ").strip()
    width = int(width) if width else None
    height = int(height) if height else None
    
    print("\nAspect mode:")
    for i, mode in enumerate(ASPECT_MODES.keys(), 1):
        print(f"{i}. {mode}")
    mode_choice = input("Select: ").strip()
    mode = list(ASPECT_MODES.keys())[int(mode_choice) - 1] if mode_choice.isdigit() else 'fit'
    
    quality = input("Quality (1-100, default 85): ").strip()
    quality = int(quality) if quality else 85
    
    print("\nOutput format:")
    print("0. Keep original")
    for i, fmt in enumerate(OUTPUT_FORMATS.keys(), 1):
        print(f"{i}. {fmt}")
    fmt_choice = input("Select: ").strip()
    if fmt_choice and fmt_choice != '0':
        output_format = list(OUTPUT_FORMATS.keys())[int(fmt_choice) - 1]
    else:
        output_format = None
    
    prefix = input("\nFilename prefix (blank for none): ").strip()
    suffix = input("Filename suffix (blank for none): ").strip()
    
    sequential = input("Add sequential numbers? (y/n): ").strip().lower() == 'y'
    recursive = input("Process subdirectories? (y/n): ").strip().lower() == 'y'
    overwrite = input("Overwrite existing files? (y/n): ").strip().lower() == 'y'
    
    resizer = ImageResizer()
    resizer.process_folder(
        input_folder,
        output_folder=output_folder,
        width=width,
        height=height,
        mode=mode,
        quality=quality,
        output_format=output_format,
        recursive=recursive,
        prefix=prefix,
        suffix=suffix,
        sequential=sequential,
        overwrite=overwrite
    )


def main():
    """Main entry point."""
    print("\n🖼️  Welcome to Bulk Image Resizer!")
    
    while True:
        choice = show_menu()
        
        if choice == '1':
            quick_resize()
        elif choice == '2':
            custom_resize()
        elif choice == '3':
            batch_convert()
        elif choice == '4':
            advanced_options()
        elif choice == '5':
            print("\n👋 Thanks for using Bulk Image Resizer!")
            break
        else:
            print("\n❌ Invalid choice")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
