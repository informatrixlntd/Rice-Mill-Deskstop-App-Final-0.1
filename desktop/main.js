const { app, BrowserWindow, ipcMain, dialog } = require('electron');
const path = require('path');
const { spawn, exec } = require('child_process');
const fs = require('fs');
const dotenv = require('dotenv');

let mainWindow;
let pythonProcess;
let isBackupInProgress = false;
let canCloseApp = false;

// Load environment variables
dotenv.config({ path: path.join(__dirname, '..', '.env') });

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1400,
        height: 900,
        icon: path.join(__dirname, 'assets', 'icon.png'),
        webPreferences: {
            nodeIntegration: true,
            contextIsolation: false,
            enableRemoteModule: true
        },
        autoHideMenuBar: true,
        resizable: true
    });

    mainWindow.loadFile(path.join(__dirname, 'login.html'));

    mainWindow.on('close', async (event) => {
        if (!canCloseApp && !isBackupInProgress) {
            event.preventDefault();
            await showBackupDialog();
        }
    });

    mainWindow.on('closed', function() {
        mainWindow = null;
    });
}

async function showBackupDialog() {
    if (isBackupInProgress) return;

    const result = await dialog.showMessageBox(mainWindow, {
        type: 'warning',
        title: 'Backup Required Before Exit',
        message: 'Database backup is required before closing the application.',
        detail: 'Click "Start Backup" to create a backup and upload it to Google Drive.',
        buttons: ['Start Backup', 'Cancel'],
        defaultId: 0,
        cancelId: 1
    });

    if (result.response === 0) {
        await performBackup();
    }
}

async function performBackup() {
    isBackupInProgress = true;

    try {
        const progressDialog = dialog.showMessageBox(mainWindow, {
            type: 'info',
            title: 'Backup in Progress',
            message: 'Creating database backup...',
            detail: 'Please wait. This may take a few moments.',
            buttons: []
        });

        const dbConfig = {
            host: process.env.DB_HOST || 'localhost',
            user: process.env.DB_USER || 'root',
            password: process.env.DB_PASSWORD || '',
            database: process.env.DB_NAME || 'purchase_slips'
        };

        // Try to use backup module if available
        let backupSuccess = false;
        try {
            const backup = require('./backup');
            backupSuccess = await backup.performBackupAndUpload(dbConfig, mainWindow);
        } catch (error) {
            console.error('Backup module error:', error);
            // Fallback: just create local backup without Google Drive
            backupSuccess = await createLocalBackupOnly(dbConfig);
        }

        isBackupInProgress = false;

        if (backupSuccess) {
            await dialog.showMessageBox(mainWindow, {
                type: 'info',
                title: 'Backup Completed',
                message: 'Database backup completed successfully!',
                detail: 'The application will now close.',
                buttons: ['OK']
            });

            canCloseApp = true;
            mainWindow.close();
        } else {
            await dialog.showMessageBox(mainWindow, {
                type: 'error',
                title: 'Backup Failed',
                message: 'Database backup failed.',
                detail: 'Please try again or contact support.',
                buttons: ['OK']
            });
        }
    } catch (error) {
        isBackupInProgress = false;
        console.error('Backup error:', error);
        await dialog.showMessageBox(mainWindow, {
            type: 'error',
            title: 'Backup Error',
            message: 'An error occurred during backup.',
            detail: error.message,
            buttons: ['OK']
        });
    }
}

function createLocalBackupOnly(dbConfig) {
    return new Promise((resolve) => {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const backupDir = path.join(process.env.USERPROFILE || process.env.HOME, 'PurchaseSlipBackups');

        if (!fs.existsSync(backupDir)) {
            fs.mkdirSync(backupDir, { recursive: true });
        }

        const backupFileName = `purchase_slips_backup_${timestamp}.sql`;
        const backupFilePath = path.join(backupDir, backupFileName);

        const command = `mysqldump -h ${dbConfig.host} -u ${dbConfig.user} -p${dbConfig.password} ${dbConfig.database} > "${backupFilePath}"`;

        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error('Local backup error:', error);
                resolve(false);
                return;
            }
            console.log('Local backup created:', backupFilePath);
            resolve(true);
        });
    });
}

function startPythonBackend() {
    const pythonScript = path.join(__dirname, '..', 'backend', 'app.py');
    pythonProcess = spawn('python', [pythonScript], {
        cwd: path.join(__dirname, '..')
    });

    pythonProcess.stdout.on('data', (data) => {
        console.log(`Backend: ${data}`);
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Backend Error: ${data}`);
    });

    setTimeout(() => {
        console.log('Backend started successfully');
    }, 3000);
}

app.on('ready', () => {
    startPythonBackend();
    createWindow();
});

app.on('window-all-closed', function() {
    if (pythonProcess) {
        pythonProcess.kill();
    }
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', function() {
    if (mainWindow === null) {
        createWindow();
    }
});

ipcMain.on('login-success', () => {
    mainWindow.loadFile(path.join(__dirname, 'app.html'));
});

ipcMain.on('logout', () => {
    mainWindow.loadFile(path.join(__dirname, 'login.html'));
});

/**
 * Print slip handler with PDF preview
 * Generates PDF using printToPDF and displays in custom viewer
 * User can print or download from the viewer
 */
ipcMain.on('print-slip', async (event, slipId) => {
    const { dialog } = require('electron');
    let printWindow = null;

    try {
        // Create hidden window to load slip content
        printWindow = new BrowserWindow({
            width: 800,
            height: 1100,
            show: false,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true
            }
        });

        // Load slip HTML from Flask server
        await printWindow.loadURL(`http://localhost:5000/print/${slipId}`);

        // Wait for content to fully render
        await new Promise(resolve => setTimeout(resolve, 1500));

        // Generate PDF using Electron's built-in printToPDF
        const pdfData = await printWindow.webContents.printToPDF({
            marginsType: 0,
            pageSize: 'A4',
            printBackground: true,
            printSelectionOnly: false,
            landscape: false
        });

        // Close the temporary window
        printWindow.close();
        printWindow = null;

        // Convert PDF to base64 for embedding
        const pdfBase64 = pdfData.toString('base64');

        // Create PDF viewer window with toolbar
        const viewerWindow = new BrowserWindow({
            width: 900,
            height: 1200,
            webPreferences: {
                nodeIntegration: false,
                contextIsolation: true
            },
            title: `Purchase Slip ${slipId}`
        });

        // Create HTML with embedded PDF viewer
        const viewerHTML = `
<!DOCTYPE html>
<html>
<head>
    <title>Purchase Slip ${slipId}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #525252;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            overflow: hidden;
        }
        #toolbar {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            background: #323639;
            padding: 12px 20px;
            display: flex;
            gap: 12px;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            box-shadow: 0 2px 8px rgba(0,0,0,0.3);
        }
        button {
            background: #4a90e2;
            color: white;
            border: none;
            padding: 10px 24px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        button:hover {
            background: #357abd;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        button:active {
            transform: translateY(0);
        }
        button.download {
            background: #4caf50;
        }
        button.download:hover {
            background: #45a049;
        }
        #pdf-container {
            width: 100%;
            height: calc(100vh - 50px);
            border: none;
            margin-top: 50px;
            background: #525252;
        }
    </style>
</head>
<body>
    <div id="toolbar">
        <button onclick="printPDF()">
            <span>🖨️</span>
            <span>Print</span>
        </button>
        <button class="download" onclick="downloadPDF()">
            <span>⬇️</span>
            <span>Download PDF</span>
        </button>
    </div>
    <iframe id="pdf-container" src="data:application/pdf;base64,${pdfBase64}"></iframe>

    <script>
        function printPDF() {
            window.print();
        }

        function downloadPDF() {
            const link = document.createElement('a');
            link.href = 'data:application/pdf;base64,${pdfBase64}';
            link.download = 'purchase_slip_${slipId}.pdf';
            link.click();
        }

        // Add keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'p') {
                e.preventDefault();
                printPDF();
            }
        });
    </script>
</body>
</html>
        `;

        // Load the viewer with embedded PDF
        viewerWindow.loadURL('data:text/html;charset=utf-8,' + encodeURIComponent(viewerHTML));

    } catch (error) {
        console.error('Error generating PDF:', error);

        // Clean up print window if it exists
        if (printWindow && !printWindow.isDestroyed()) {
            printWindow.close();
        }

        // Show error dialog to user
        dialog.showErrorBox(
            'Print Error',
            `Failed to generate PDF:\n\n${error.message}\n\nPlease ensure the Flask server is running.`
        );
    }
});
