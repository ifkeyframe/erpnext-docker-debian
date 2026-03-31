#!/bin/bash
# Railway entrypoint — uses external MariaDB and Redis, not built-in ones

cd /home/frappe/bench

# Fix volume permissions
sudo chown -R frappe:frappe /home/frappe/bench/sites

# Restore apps.txt if volume wiped it
if [ ! -f sites/apps.txt ]; then
    echo "frappe" > sites/apps.txt
    echo "erpnext" >> sites/apps.txt
    if [ -d apps/printbiz_custom ]; then
        echo "printbiz_custom" >> sites/apps.txt
    fi
    echo "[OK] apps.txt restored"
fi

# Restore assets if missing
if [ ! -d "sites/assets/frappe" ]; then
    echo "[INFO] Linking assets..."
    su frappe -c "bench setup assets" 2>&1 || true
fi

# Start bench (without built-in MariaDB/Redis — they are external on Railway)
exec su frappe -c "bench start"
