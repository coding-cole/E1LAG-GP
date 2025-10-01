let html5QrcodeScanner;
let isProcessing = false;

function startScanner() {
    document.getElementById('startBtn').disabled = true;
    document.getElementById('startBtn').textContent = 'Scanner Active';

    html5QrcodeScanner = new Html5QrcodeScanner(
        "reader",
        {
            fps: 10,
            qrbox: { width: 250, height: 250 },
            aspectRatio: 1.0
        },
        false
    );

    html5QrcodeScanner.render(onScanSuccess, onScanError);
}

async function onScanSuccess(decodedText, decodedResult) {
    if (isProcessing) return;

    isProcessing = true;

    // Stop scanning temporarily
    html5QrcodeScanner.pause();

    // Show loading
    document.getElementById('spinner').style.display = 'block';
    document.getElementById('message').style.display = 'none';

    try {
        const response = await fetch('/validate_qr', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ qr_code: decodedText })
        });

        const data = await response.json();

        // Hide loading
        document.getElementById('spinner').style.display = 'none';

        // Show message
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = data.message;
        messageDiv.className = 'message ' + (data.success ? 'success' : 'error');
        messageDiv.style.display = 'block';

        // Resume scanning after 3 seconds
        setTimeout(() => {
            html5QrcodeScanner.resume();
            isProcessing = false;
        }, 3000);

    } catch (error) {
        document.getElementById('spinner').style.display = 'none';
        const messageDiv = document.getElementById('message');
        messageDiv.textContent = 'Error connecting to server';
        messageDiv.className = 'message error';
        messageDiv.style.display = 'block';

        setTimeout(() => {
            html5QrcodeScanner.resume();
            isProcessing = false;
        }, 3000);
    }
}

function onScanError(errorMessage) {
    // Ignore scan errors (happens while searching for QR code)
}

// Auto-start scanner on page load
window.addEventListener('load', () => {
    setTimeout(startScanner, 500);
});
