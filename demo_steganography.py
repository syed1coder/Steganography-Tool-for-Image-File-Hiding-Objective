#!/usr/bin/env python3
"""
Demo script to test steganography functionality
Creates sample images and demonstrates embedding/extraction
"""

from PIL import Image
import os

def text_to_binary(text):
    """Convert text to binary string"""
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    """Convert binary string to text"""
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def create_sample_image():
    """Create a colorful sample image for testing"""
    width, height = 400, 300
    img = Image.new('RGB', (width, height))
    pixels = []
    
    for y in range(height):
        for x in range(width):
            # Create a gradient pattern
            r = int((x / width) * 255)
            g = int((y / height) * 255)
            b = int(((x + y) / (width + height)) * 255)
            pixels.append((r, g, b))
    
    img.putdata(pixels)
    return img

def embed_message(image, message):
    """Embed secret message in image using LSB"""
    # Add delimiter
    message = message + "<<<END>>>"
    binary_message = text_to_binary(message)
    
    # Get pixel data
    pixels = list(image.getdata())
    
    # Check capacity
    max_bits = len(pixels) * 3
    if len(binary_message) > max_bits:
        raise ValueError(f"Message too large! Max: {max_bits // 8} bytes")
    
    # Embed data
    data_index = 0
    new_pixels = []
    
    for pixel in pixels:
        r, g, b = pixel
        
        # Modify LSB of each color channel
        if data_index < len(binary_message):
            r = (r & 0xFE) | int(binary_message[data_index])
            data_index += 1
        
        if data_index < len(binary_message):
            g = (g & 0xFE) | int(binary_message[data_index])
            data_index += 1
        
        if data_index < len(binary_message):
            b = (b & 0xFE) | int(binary_message[data_index])
            data_index += 1
        
        new_pixels.append((r, g, b))
    
    # Create new image
    stego_img = Image.new('RGB', image.size)
    stego_img.putdata(new_pixels)
    
    return stego_img

def extract_message(image):
    """Extract hidden message from stego image"""
    pixels = list(image.getdata())
    
    # Extract LSBs
    binary_data = ""
    for pixel in pixels:
        r, g, b = pixel
        binary_data += str(r & 1)
        binary_data += str(g & 1)
        binary_data += str(b & 1)
    
    # Convert to text
    extracted_text = binary_to_text(binary_data)
    
    # Find delimiter
    if "<<<END>>>" in extracted_text:
        return extracted_text.split("<<<END>>>")[0]
    else:
        return extracted_text

def main():
    print("=" * 60)
    print("STEGANOGRAPHY DEMO - LSB TECHNIQUE")
    print("=" * 60)
    
    # Create sample image
    print("\n1. Creating sample cover image...")
    cover_img = create_sample_image()
    cover_img.save('/home/claude/sample_cover.png')
    print(f"   ✓ Cover image created: sample_cover.png (400x300)")
    
    # Secret message
    secret_message = """This is a secret message hidden inside the image!
    
Steganography is the art of hiding information in plain sight.
Nobody looking at this image would suspect it contains hidden data.

- Confidential data can be transmitted securely
- The image looks completely normal
- Only those who know can extract the message"""
    
    print(f"\n2. Secret message to hide:")
    print(f"   Length: {len(secret_message)} characters")
    print(f"   Preview: {secret_message[:50]}...")
    
    # Embed message
    print("\n3. Embedding message using LSB technique...")
    stego_img = embed_message(cover_img, secret_message)
    stego_img.save('/home/claude/sample_stego.png')
    print("   ✓ Message embedded successfully!")
    print("   ✓ Stego image saved: sample_stego.png")
    
    # Calculate image sizes
    original_size = os.path.getsize('/home/claude/sample_cover.png')
    stego_size = os.path.getsize('/home/claude/sample_stego.png')
    
    print(f"\n4. Image comparison:")
    print(f"   Original size: {original_size:,} bytes")
    print(f"   Stego size:    {stego_size:,} bytes")
    print(f"   Difference:    {abs(stego_size - original_size):,} bytes")
    
    # Extract message
    print("\n5. Extracting hidden message from stego image...")
    extracted = extract_message(stego_img)
    print("   ✓ Message extracted successfully!")
    
    # Verify
    print("\n6. Verification:")
    if extracted == secret_message:
        print("   ✅ SUCCESS! Extracted message matches original perfectly!")
    else:
        print("   ❌ ERROR! Messages don't match!")
    
    print(f"\n7. Extracted message:")
    print("   " + "-" * 56)
    for line in extracted.split('\n'):
        print(f"   {line}")
    print("   " + "-" * 56)
    
    # Calculate capacity
    max_capacity = (400 * 300 * 3) // 8
    print(f"\n8. Image capacity:")
    print(f"   Maximum data: {max_capacity:,} bytes ({max_capacity / 1024:.1f} KB)")
    print(f"   Used: {len(secret_message)} bytes ({len(secret_message) / max_capacity * 100:.2f}%)")
    print(f"   Available: {max_capacity - len(secret_message):,} bytes")
    
    print("\n" + "=" * 60)
    print("DEMO COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("\nFiles created:")
    print("  • sample_cover.png  - Original cover image")
    print("  • sample_stego.png  - Image with hidden message")
    print("\nYou can now run steganography_tool.py for the GUI version!")

if __name__ == "__main__":
    main()
