from flask import Flask, render_template, request, jsonify
import pandas as pd
import os

app = Flask(__name__)

# Excel file path
EXCEL_FILE = 'qr_codes.xlsx'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/validate_qr', methods=['POST'])
def validate_qr():
    try:
        data = request.get_json()
        qr_code = data.get('qr_code', '').strip()

        if not qr_code:
            return jsonify({'success': False, 'message': 'No QR code provided'})

        # Read Excel file
        if not os.path.exists(EXCEL_FILE):
            return jsonify({'success': False, 'message': 'Excel file not found'})

        df = pd.read_excel(EXCEL_FILE)

        # Check if code exists
        code_row = df[df['code'] == qr_code]

        if code_row.empty:
            return jsonify({'success': False, 'message': 'QR code does not exist in database'})

        # Get the index of the code
        idx = code_row.index[0]

        # Check if already used
        if df.loc[idx, 'used'] == 1:
            return jsonify({'success': False, 'message': 'QR code has already been used'})

        # Mark as used
        df.loc[idx, 'used'] = 1

        # Save back to Excel
        df.to_excel(EXCEL_FILE, index=False)

        return jsonify({
            'success': True,
            'message': f'QR code {qr_code} is valid and has been marked as used!'
        })

    except Exception as e:
        return jsonify({'success': False, 'message': f'Error: {str(e)}'})


if __name__ == '__main__':
    app.run(debug=True)
