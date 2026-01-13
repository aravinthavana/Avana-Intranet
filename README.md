# Office Intranet Dashboard

A lightweight, scalable intranet dashboard for viewing Intercom, Announcements, Events, and Hall Bookings.
Includes an Admin Interface with Outlook Email Notification integration.

## Architecture
- **Frontend**: Vue 3 + Vite (Static Build)
- **Backend**: Python Flask (Static File Serving + API)
- **Data**: JSON files in `backend/data/`

## Prerequisites
- **Python 3.8+** (Required for Backend)
- **Node.js** (Only for development/building frontend)
- **Microsoft Outlook** (Required on Admin machine for Email Notifications)

## Setup & Run (Windows)

1. **Install Python**
   Ensure Python is installed and added to your PATH.

2. **Setup Backend**
   ```bat
   cd backend
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Build Frontend** (If modifying code)
   ```bat
   cd frontend
   npm install
   npm run build
   ```
   *The build output is automatically placed in `frontend/dist` which the backend serves.*

4. **Run Application**
   Double click `run_server.bat` in the root folder.
   Access at `http://localhost:5000`

## Admin Access
- Go to `/admin`
- Default Password: `admin123`
- **Email Notifications**: specific to Admin Dashboard. When publishing, check "Send email". This will trigger the local Outlook client to open a draft.

## Deployment on Windows Server 2012
1. Copy the entire `office-intranet` folder to the server.
2. Install Python on the server.
3. Run `run_server.bat`.
4. Alternatively, configure **IIS** with `HttpPlatformHandler` to run the Flask app, or serve `frontend/dist` as a static site and run Flask on a port for API.

## Project Structure
- `backend/app.py`: Main server logic.
- `backend/data/`: JSON database.
- `frontend/src/`: Vue source code.
