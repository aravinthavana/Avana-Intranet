# Stage 1: Build the Vue.js frontend
FROM node:22-alpine AS build-stage
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend .
RUN chmod +x node_modules/.bin/vite
RUN npm run build

# Stage 2: Setup Python backend & serve frontend
FROM python:3.9-slim
WORKDIR /app

# Copy requirement files and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY backend ./backend

# Copy built frontend files from the build stage to where the backend expects them
COPY --from=build-stage /app/frontend/dist ./frontend/dist

# Ensure the data directory exists
RUN mkdir -p ./backend/data

# Setup environment variables for production
ENV FLASK_ENV=production
ENV FLASK_DEBUG=false

# Expose the Flask port
EXPOSE 5000

# Start Waitress server (production-ready WSGI server)
CMD ["python", "backend/app.py"]
