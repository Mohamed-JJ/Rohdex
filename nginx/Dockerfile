# Use the official Nginx image
FROM nginx:latest

# Install Certbot and Nginx plugin
RUN apt-get update && \
    apt-get install -y certbot python3-certbot-nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the Nginx configuration
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy the renewal script
COPY renew_cert.sh /usr/local/bin/renew_cert.sh
RUN chmod +x /usr/local/bin/renew_cert.sh

# Install cron and set up the cron job
RUN apt-get update && apt-get install -y cron && \
    echo "0 0 * * * /usr/local/bin/renew_cert.sh" >> /etc/crontab && \
    service cron start

# Expose HTTP and HTTPS ports
EXPOSE 80 443

# Start cron and nginx
CMD ["sh", "-c", "cron && nginx -g 'daemon off;'"]