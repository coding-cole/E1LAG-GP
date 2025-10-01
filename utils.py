import os

import pandas as pd


def to_three_digits(num):
    """
    Convert a number to a 3-digit string with zero-padding.

    Args:
        num: Integer or string number to convert

    Returns:
        String representation with 3 digits
    """
    return str(num).zfill(3)


def reset_all_codes(excel_file="qr_codes.xlsx"):
    """Reset all 'used' values to 0 in the Excel file"""
    if not os.path.exists(excel_file):
        print(f"Error: {excel_file} not found!")
        return False

    df = pd.read_excel(excel_file)
    print(f"Resetting {len(df)} codes...")

    df['used'] = 0
    df.to_excel(excel_file, index=False)

    print(f"✓ All codes reset to used=0")
    return True
