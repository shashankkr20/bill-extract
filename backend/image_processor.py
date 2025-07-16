from PIL import Image, ImageEnhance, ImageFilter
import cv2
import numpy as np
from pathlib import Path
import asyncio
from typing import Optional

class ImageProcessor:
    def __init__(self):
        pass
    
    async def enhance_image(self, image_path: Path) -> Path:
        """Enhance image for better text extraction"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Apply enhancements
            enhanced_image = await self._apply_enhancements(image)
            
            # Save enhanced image
            enhanced_path = image_path.parent / f"enhanced_{image_path.name}"
            enhanced_image.save(enhanced_path, quality=95)
            
            return enhanced_path
            
        except Exception as e:
            # If enhancement fails, return original image path
            print(f"Image enhancement failed: {str(e)}")
            return image_path
    
    async def _apply_enhancements(self, image: Image.Image) -> Image.Image:
        """Apply various image enhancements"""
        try:
            # Convert PIL image to OpenCV format
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            
            # Convert to grayscale
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            
            # Apply noise reduction
            denoised = cv2.fastNlMeansDenoising(gray)
            
            # Apply contrast enhancement
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            enhanced = clahe.apply(denoised)
            
            # Apply slight blur to reduce noise
            blurred = cv2.GaussianBlur(enhanced, (1, 1), 0)
            
            # Convert back to PIL
            enhanced_pil = Image.fromarray(blurred)
            
            # Apply additional PIL enhancements
            # Contrast enhancement
            contrast_enhancer = ImageEnhance.Contrast(enhanced_pil)
            enhanced_pil = contrast_enhancer.enhance(1.2)
            
            # Sharpness enhancement
            sharpness_enhancer = ImageEnhance.Sharpness(enhanced_pil)
            enhanced_pil = sharpness_enhancer.enhance(1.1)
            
            return enhanced_pil
            
        except Exception as e:
            print(f"Enhancement error: {str(e)}")
            return image
    
    async def correct_rotation(self, image_path: Path) -> Path:
        """Correct image rotation if needed"""
        try:
            # Load image
            image = Image.open(image_path)
            
            # Try to get EXIF orientation
            try:
                exif = image._getexif()
                if exif:
                    orientation = exif.get(274)  # 274 is the orientation tag
                    if orientation:
                        # Apply rotation based on EXIF data
                        rotations = {3: 180, 6: 270, 8: 90}
                        if orientation in rotations:
                            image = image.rotate(rotations[orientation], expand=True)
            except:
                pass
            
            # Save corrected image
            corrected_path = image_path.parent / f"corrected_{image_path.name}"
            image.save(corrected_path, quality=95)
            
            return corrected_path
            
        except Exception as e:
            print(f"Rotation correction failed: {str(e)}")
            return image_path
    
    async def resize_image(self, image_path: Path, max_size: int = 2048) -> Path:
        """Resize image if it's too large"""
        try:
            image = Image.open(image_path)
            
            # Check if resizing is needed
            if max(image.size) <= max_size:
                return image_path
            
            # Calculate new size maintaining aspect ratio
            ratio = max_size / max(image.size)
            new_size = tuple(int(dim * ratio) for dim in image.size)
            
            # Resize image
            resized_image = image.resize(new_size, Image.Resampling.LANCZOS)
            
            # Save resized image
            resized_path = image_path.parent / f"resized_{image_path.name}"
            resized_image.save(resized_path, quality=95)
            
            return resized_path
            
        except Exception as e:
            print(f"Image resizing failed: {str(e)}")
            return image_path 