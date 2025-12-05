FROM python:3.10-slim

WORKDIR /

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy backend code as a package
COPY backend/ /app/

# Copy flow_engine directory to multiple locations for compatibility
# /flow_engine - absolute path (primary)
# /app/flow_engine - relative to backend (fallback)
COPY flow_engine/ /flow_engine/
COPY flow_engine/ /app/flow_engine/

# Copy start script and make it executable
COPY backend/start.sh /start.sh
RUN chmod +x /start.sh

# Create directories with proper permissions
RUN mkdir -p /app/data /app/logs /app/.deepeval /app/.cache \
    /flow_engine/templates /app/flow_engine/templates && \
    chmod 755 /app/data /app/logs /app/.deepeval /app/.cache \
    /flow_engine /flow_engine/templates \
    /app/flow_engine /app/flow_engine/templates

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app /flow_engine
USER appuser

# Set environment variables for cache directories
ENV HOME=/app \
    XDG_CACHE_HOME=/app/.cache \
    XDG_DATA_HOME=/app/.cache

# Set working directory to /app (writable by appuser)
WORKDIR /app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["/start.sh"]