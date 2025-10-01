import qrcode
from PIL import Image
from utils import to_three_digits, reset_all_codes
import os
import pandas as pd
import sys

filepath = "../files/guest_list.csv"

# At the end of your main script, add:
if len(sys.argv) > 1 and sys.argv[1] == '--reset':
    reset_all_codes(filepath)
else:
    # CSV file path
    csv_file = filepath

    # Check if CSV exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found!")
        sys.exit(1)

    # Load CSV file
    df = pd.read_csv(csv_file)
    print(f"Loaded CSV file with {len(df)} entries")

    # Create qrs directory if it doesn't exist
    os.makedirs("qrs", exist_ok=True)

    created_count = 0
    skipped_count = 0

    # Process each row in the CSV
    for index, row in df.iterrows():
        name = row['NAME']
        code = row['CODE']
        output_path = f"qrs/{name}.jpg"

        # Check if QR code image already exists
        if os.path.exists(output_path):
            print(f"QR code for '{name}' already exists - skipping")
            skipped_count += 1
            continue

        # Create new QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )

        qr.add_data(code)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Open base image
        base_image = Image.open("base_image.jpg")
        qr_size = (600, 600)

        # Resize and position QR code
        qr_img = qr_img.resize(qr_size)
        position = (2250, 4950)

        qr_img = qr_img.convert("RGBA")

        # Paste QR code onto base image
        base_image.paste(qr_img, position, qr_img)

        # Save as JPG
        base_image = base_image.convert("RGB")  # Convert to RGB for JPG
        base_image.save(output_path, "JPEG")

        print(f"Created QR code for '{name}' ({code})")
        created_count += 1

    print(f'\nDone!')
    print(f'Created: {created_count} new QR codes')
    print(f'Skipped: {skipped_count} existing QR codes')
    print(f'QR codes location: {os.path.abspath("qrs")}')
