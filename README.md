# Image Steganography Tool 🔐

A powerful GUI application for hiding text messages and files inside images using the LSB (Least Significant Bit) steganography technique.

## Features

✨ **Key Capabilities:**
- Hide secret text messages inside images
- Embed complete files (any format) within images
- Extract hidden data from stego images
- Drag-and-drop support for easy file handling
- Support for PNG and BMP image formats
- Imperceptible image modifications
- User-friendly tabbed interface

## Installation

### Prerequisites
- Python 3.x
- pip package manager

### Install Dependencies

```bash
pip install pillow tkinterdnd2 --break-system-packages
```

## Usage

### Running the Application

```bash
python3 steganography_tool.py
```

### How to Hide Data

1. **Select Cover Image**
   - Click "Choose Image (PNG/BMP)" or drag-and-drop an image
   - Supported formats: PNG, BMP

2. **Enter Secret Data**
   - **Option A:** Type your secret message in the text area
   - **Option B:** Click "Choose File to Hide" to embed a complete file

3. **Embed the Data**
   - Click "🔒 Embed Data"
   - Choose where to save the stego image
   - The output image will look identical to the original!

### How to Extract Data

1. **Select Stego Image**
   - Click "Choose Stego Image" or drag-and-drop the image with hidden data

2. **Extract the Data**
   - Click "🔓 Extract Data"
   - If it's a text message, it will appear in the text area
   - If it's a file, you'll be prompted to save it

## Technical Details

### LSB Steganography Method

The tool uses the Least Significant Bit (LSB) technique:

1. **Embedding Process:**
   - Converts secret message/file to binary
   - Modifies the last bit of each RGB color component
   - Changes are imperceptible to the human eye
   - Adds delimiter to mark data end

2. **Extraction Process:**
   - Reads LSB from each pixel's RGB values
   - Reconstructs binary data
   - Converts back to original format

### Capacity Calculation

Maximum data capacity = (Image Width × Image Height × 3) ÷ 8 bytes

Example: A 1000×1000 pixel image can hide approximately 375 KB of data.

## File Structure

```
steganography_tool/
│
├── steganography_tool.py       # Main GUI application
├── generate_report.py          # PDF report generator
├── Steganography_Project_Report.pdf  # Project documentation
└── README.md                   # This file
```

## Supported Image Formats

| Format | Extension | Notes |
|--------|-----------|-------|
| PNG    | .png      | Recommended (lossless) |
| BMP    | .bmp      | Lossless, larger files |

**Note:** JPEG is NOT supported as it uses lossy compression which destroys hidden data.

## Examples

### Example 1: Hide Text Message
```
1. Load image: vacation_photo.png
2. Enter message: "Meet me at the old oak tree at midnight"
3. Save as: vacation_photo_stego.png
4. Share the stego image - nobody will know it contains a message!
```

### Example 2: Hide PDF File
```
1. Load image: beach.png
2. Click "Choose File to Hide"
3. Select: confidential_report.pdf
4. Save stego image
5. Recipient extracts and recovers the original PDF!
```

## Security Considerations

⚠️ **Important Notes:**
- LSB steganography provides **obscurity**, not encryption
- Hidden data is NOT encrypted by default
- For sensitive data, encrypt before embedding
- Stego images should not be re-compressed (avoid JPEG conversion)
- Original and stego images should not be compared publicly

## Troubleshooting

**Issue:** "Message too large" error
- **Solution:** Use a larger image or reduce message size

**Issue:** Extraction shows garbage text
- **Solution:** Ensure you're extracting from the correct stego image

**Issue:** Drag-and-drop not working
- **Solution:** Ensure tkinterdnd2 is properly installed

## Future Enhancements

- [ ] Password-based encryption
- [ ] Multiple LSB layers for higher capacity
- [ ] JPEG support with F5 algorithm
- [ ] Batch processing
- [ ] Image quality analysis

## Project Report

A detailed 2-page PDF report is included covering:
- Abstract and Introduction
- Tools and Technologies Used
- Implementation Steps
- Key Features
- Conclusion

File: `Steganography_Project_Report.pdf`

## License

This project is created for educational purposes.

## Author

Created as a demonstration of steganography techniques in information security.

---

**⚠️ Disclaimer:** This tool is for educational and legitimate security purposes only. Users are responsible for compliance with applicable laws and regulations.
