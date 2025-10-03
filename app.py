from dotenv import load_dotenv
import os

load_dotenv()

from flask import Flask, render_template, request, jsonify
import pandas as pd
import logging


app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('qr_validation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# CSV file path
CSV_FILE = 'files/guest_list.csv'

logger.info("=" * 50)
logger.info("Flask QR Validation App Starting")
logger.info(f"CSV File: {CSV_FILE}")
logger.info("=" * 50)


@app.route('/')
def index():
    logger.info("Index page accessed")
    return render_template('index.html')


@app.route('/validate_qr', methods=['POST'])
def validate_qr():
    logger.info("-" * 50)
    logger.info("NEW QR VALIDATION REQUEST")

    try:
        # Get request data
        data = request.get_json()
        qr_code = data.get('qr_code', '').strip()
        logger.info(f"Received QR code: '{qr_code}'")

        if not qr_code:
            logger.warning("Empty QR code provided")
            return jsonify({'success': False, 'message': 'No QR code provided'})

        # Check if CSV exists
        if not os.path.exists(CSV_FILE):
            logger.error(f"CSV file not found: {CSV_FILE}")
            return jsonify({'success': False, 'message': 'CSV file not found'})

        # Read CSV file
        logger.info(f"Reading CSV file: {CSV_FILE}")
        df = pd.read_csv(CSV_FILE)
        logger.info(f"CSV loaded successfully. Total entries: {len(df)}")

        # Check if code exists
        code_row = df[df['CODE'] == qr_code]

        if code_row.empty:
            logger.warning(f"QR code not found in database: {qr_code}")
            return jsonify({'success': False, 'message': 'QR code does not exist in database'})

        # Get the index of the code
        idx = code_row.index[0]
        name = df.loc[idx, 'NAME']
        used_status = df.loc[idx, 'USED']

        logger.info(f"QR code found - Name: {name}, Used: {used_status}")

        # Check if already used
        if used_status == 1:
            logger.warning(
                f"QR code already used - Name: {name}, Code: {qr_code}")
            return jsonify({'success': False, 'message': f'QR code for {name} has already been used'})

        # Mark as used
        logger.info(f"Marking QR code as used - Name: {name}, Code: {qr_code}")
        df.loc[idx, 'USED'] = 1

        # Save back to CSV
        df.to_csv(CSV_FILE, index=False)
        logger.info(f"CSV updated successfully")

        logger.info(f"✓ VALIDATION SUCCESSFUL - Name: {name}, Code: {qr_code}")
        return jsonify({
            'success': True,
            'message': f'Welcome {name}! QR code has been marked as used.',
            'name': name,
            'code': qr_code
        })

    except Exception as e:
        logger.error(f"ERROR during validation: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})
    finally:
        logger.info("-" * 50)


if __name__ == '__main__':
    logger.info("Starting Flask development server...")
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
