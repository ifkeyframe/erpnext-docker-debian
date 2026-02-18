# ------------------------------------------
# - Stage: 01 - builder
# ------------------------------------------

# This image is also based on frappe/bench which we use for production
# https://github.com/pipech/erpnext-docker-debian/blob/master/Dockerfile
FROM pipech/erpnext-docker-debian:version-15-latest AS builder

# These variable has been set from base image
# frappe, frappe-bench
USER frappe
WORKDIR /home/frappe/frappe-bench

RUN echo "-> Start builder" \
    ### remove unused sites, created by base image
    && rm -rf /home/frappe/frappe-bench/sites/site1.local \
    ### [HOTFIX] Railway used IPv6 (Does not support IPv4),  https://docs.railway.com/guides/private-networking#caveats
    ### https://github.com/frappe/frappe/issues/33981
    && sed -i 's/socket\.AF_INET, socket\.SOCK_STREAM/socket.AF_INET6, socket.SOCK_STREAM/g' /home/frappe/bench/apps/frappe/frappe/utils/connections.py \
    ### install your custom apps here
    # && bench get-app https://github.com/your-repo/custom_app
    && echo "-> Builder done!"


# ------------------------------------------
# - Stage: 02 - production
# ------------------------------------------

# Image version should also match with stage 01
# (Check pipech/erpnext-docker-debian Dockerfile)
# https://github.com/frappe/frappe_docker/blob/main/images/bench/Dockerfile
FROM frappe/bench:v5.22.9

# this env should match stage 01
# (Check pipech/erpnext-docker-debian Dockerfile)
ENV SYSTEM_USER=frappe
ENV BENCH_FOLDER_NAME=bench

# Copied bench folder from build stage
COPY --from=builder --chown=frappe /home/frappe/frappe-bench /home/frappe/frappe-bench

# Copy template
COPY /railway/temp_nginx.conf /home/frappe/temp_nginx.conf
COPY /railway/temp_supervisor.conf /home/frappe/temp_supervisor.conf

USER root
WORKDIR /home/frappe/frappe-bench

# [fix] "debconf: unable to initialize frontend: Dialog"
# https://github.com/moby/moby/issues/27988
ARG DEBIAN_FRONTEND=noninteractive

RUN echo "-> Install nginx & supervisor" \
    # apt-get update
    && apt-get update \
    && apt-get install -y \
    # nginx for serving files
    nginx \
    # supervisor to run multiple server per container
    supervisor \
    && echo "-> Cleaning installation" \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && echo "-> Remove nginx default site" \
    && rm /etc/nginx/sites-enabled/default \
    && echo "-> Rebuilding bench" \
    && su frappe -c "bench build" \
    && su frappe -c "cp -r /home/frappe/frappe-bench/sites /home/frappe/frappe-bench/built_sites"

COPY --chown=frappe --chmod=0755 /railway/railway-setup.sh /home/frappe/frappe-bench/railway-setup.sh
COPY --chown=frappe --chmod=0755 /railway/railway-entrypoint.sh /usr/local/bin/railway-entrypoint.sh
COPY --chown=frappe --chmod=0755 /railway/railway-cmd.sh /usr/local/bin/railway-cmd.sh

ENTRYPOINT ["/usr/local/bin/railway-entrypoint.sh"]
CMD ["/usr/local/bin/railway-cmd.sh"]

EXPOSE 80
