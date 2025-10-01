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


def reset_all_codes(csv_file="qr_codes.csv"):
    """Reset all 'USED' values to 0 in the CSV file"""
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return False

    df = pd.read_csv(csv_file)
    print(f"Resetting {len(df)} codes...")

    df['USED'] = 0
    df.to_csv(csv_file, index=False)

    print(f"✓ All codes reset to USED=0")
    return True
