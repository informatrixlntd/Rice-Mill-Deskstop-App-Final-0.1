const { exec } = require('child_process');
const fs = require('fs');
const path = require('path');
const { google } = require('googleapis');
const { BrowserWindow } = require('electron');

const BACKUP_DIR = path.join(process.env.USERPROFILE || process.env.HOME, 'PurchaseSlipBackups');

// Ensure backup directory exists
if (!fs.existsSync(BACKUP_DIR)) {
    fs.mkdirSync(BACKUP_DIR, { recursive: true });
}

function createMySQLBackup(dbConfig) {
    return new Promise((resolve, reject) => {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        const backupFileName = `purchase_slips_backup_${timestamp}.sql`;
        const backupFilePath = path.join(BACKUP_DIR, backupFileName);

        const command = `mysqldump -h ${dbConfig.host} -u ${dbConfig.user} -p${dbConfig.password} ${dbConfig.database} > "${backupFilePath}"`;

        exec(command, (error, stdout, stderr) => {
            if (error) {
                console.error('Backup error:', error);
                reject(error);
                return;
            }
            if (stderr) {
                console.error('Backup stderr:', stderr);
            }
            console.log('Backup created:', backupFilePath);
            resolve(backupFilePath);
        });
    });
}

async function authenticateGoogleDrive() {
    return new Promise((resolve, reject) => {
        const oauth2Client = new google.auth.OAuth2(
            'YOUR_CLIENT_ID', // User will need to set this
            'YOUR_CLIENT_SECRET', // User will need to set this
            'http://localhost:3000/oauth2callback'
        );

        const authUrl = oauth2Client.generateAuthUrl({
            access_type: 'offline',
            scope: ['https://www.googleapis.com/auth/drive.file']
        });

        // Open browser for authentication
        const authWindow = new BrowserWindow({
            width: 800,
            height: 600,
            webPreferences: {
                nodeIntegration: false
            }
        });

        authWindow.loadURL(authUrl);

        // Listen for redirect with code
        authWindow.webContents.on('will-redirect', async (event, url) => {
            if (url.startsWith('http://localhost:3000/oauth2callback')) {
                const code = new URL(url).searchParams.get('code');
                authWindow.close();

                try {
                    const { tokens } = await oauth2Client.getToken(code);
                    oauth2Client.setCredentials(tokens);
                    resolve(oauth2Client);
                } catch (error) {
                    reject(error);
                }
            }
        });

        authWindow.on('closed', () => {
            reject(new Error('Authentication window closed'));
        });
    });
}

async function uploadToGoogleDrive(filePath, auth) {
    const drive = google.drive({ version: 'v3', auth });

    const fileMetadata = {
        name: path.basename(filePath),
        mimeType: 'application/sql'
    };

    const media = {
        mimeType: 'application/sql',
        body: fs.createReadStream(filePath)
    };

    try {
        const response = await drive.files.create({
            requestBody: fileMetadata,
            media: media,
            fields: 'id,name'
        });

        console.log('File uploaded to Google Drive:', response.data);
        return response.data;
    } catch (error) {
        console.error('Error uploading to Google Drive:', error);
        throw error;
    }
}

async function performBackupAndUpload(dbConfig, mainWindow) {
    try {
        mainWindow.webContents.send('backup-status', 'Creating database backup...');

        // Create MySQL backup
        const backupFilePath = await createMySQLBackup(dbConfig);

        mainWindow.webContents.send('backup-status', 'Authenticating with Google Drive...');

        // Authenticate with Google Drive
        const auth = await authenticateGoogleDrive();

        mainWindow.webContents.send('backup-status', 'Uploading to Google Drive...');

        // Upload to Google Drive
        await uploadToGoogleDrive(backupFilePath, auth);

        mainWindow.webContents.send('backup-status', 'Backup completed successfully!');

        return true;
    } catch (error) {
        console.error('Backup failed:', error);
        mainWindow.webContents.send('backup-error', error.message);
        return false;
    }
}

module.exports = {
    performBackupAndUpload,
    BACKUP_DIR
};
