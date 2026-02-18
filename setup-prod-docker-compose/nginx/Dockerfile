FROM frappe-image AS assets
FROM nginx:1.29

COPY --from=assets /home/frappe/frappe-bench/sites/assets /usr/share/nginx/sites/assets