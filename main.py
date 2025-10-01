import qrcode
from PIL import Image
from utils import to_three_digits, reset_all_codes
import os
import pandas as pd
import sys

# At the end of your main script, add:
if len(sys.argv) > 1 and sys.argv[1] == '--reset':
    reset_all_codes()
else:

    # Excel file path
    excel_file = "qr_codes.xlsx"

    # Load or create Excel file
    if os.path.exists(excel_file):
        df = pd.read_excel(excel_file)
        existing_codes = set(df['code'].tolist())
        print(f"Loaded existing Excel file with {len(df)} entries")
    else:
        df = pd.DataFrame(columns=['code', 'used'])
        existing_codes = set()
        print("Created new Excel file")

    new_rows = []

    for i in range(1, 161):
        code = f'E1LAG-GP{to_three_digits(i)}'
        output_path = f"qrs/{code}.png"

        # Check if QR code image already exists
        if os.path.exists(output_path):
            print(f"QR code {code} already exists")

            # Add to Excel if not already there
            if code not in existing_codes:
                new_rows.append({'code': code, 'used': 0})
                existing_codes.add(code)
                print(f"  -> Added {code} to Excel")

            continue  # Skip creating the QR code

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

        base_image = Image.open("base_image.jpg")
        qr_size = (600, 600)

        qr_img = qr_img.resize(qr_size)
        position = (2250, 4950)

        qr_img = qr_img.convert("RGBA")

        base_image.paste(qr_img, position, qr_img)
        base_image.save(output_path)

        print(f"Created QR code {code}")

        # Add to Excel if not already there
        if code not in existing_codes:
            new_rows.append({'code': code, 'used': 0})
            existing_codes.add(code)
            print(f"  -> Added {code} to Excel")

    # Save Excel file with all entries (existing + new)
    if new_rows:
        new_df = pd.DataFrame(new_rows)
        df = pd.concat([df, new_df], ignore_index=True)
        df.to_excel(excel_file, index=False)
        print(f"\nSaved {len(new_rows)} new entries to Excel")

    print(f'\nDone! Total entries in Excel: {len(df)}')
    print(f'Excel file location: {os.path.abspath(excel_file)}')
    pass