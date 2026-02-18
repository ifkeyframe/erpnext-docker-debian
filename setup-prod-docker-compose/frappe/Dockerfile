# ------------------------------------------
# - Stage: 01 - builder
# ------------------------------------------

# This image is also based on frappe/bench which we use for production
# https://github.com/pipech/erpnext-docker-debian/blob/master/Dockerfile
FROM pipech/erpnext-docker-debian:version-16-latest AS builder

RUN echo "-> Start builder" \
    ### install your custom apps here
    # && bench get-app https://github.com/your-repo/custom_app
    ### remove unused sites
    && rm -rf /home/frappe/frappe-bench/sites/$SITE_NAME \
    && echo "-> Builder done!"


# ------------------------------------------
# - Stage: 02 - production
# ------------------------------------------

# Image version should also match with stage 01
# (Check pipech/erpnext-docker-debian Dockerfile)
# https://github.com/frappe/frappe_docker/blob/main/images/bench/Dockerfile
FROM frappe/bench:latest

# Copied bench folder from build stage
COPY --from=builder --chown=frappe:frappe /home/frappe/frappe-bench /home/frappe/frappe-bench

ENTRYPOINT ["/usr/local/bin/railway-entrypoint.sh"]

EXPOSE 80
