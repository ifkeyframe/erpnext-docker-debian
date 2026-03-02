###############################################
# Base Image
###############################################
# https://github.com/frappe/frappe_docker/blob/main/images/production/Containerfile
# `frappe/base` is built from `python:slim-bookworm` and includes:
#   Python (system), Node (nvm), bench (pip3), nginx, wkhtmltopdf,
#   mariadb-client, weasytprint deps, frappe user.
# Default USER in this image is root.
FROM frappe/base:version-16


###############################################
# Args
###############################################
ARG APP_BRANCH=version-16
ARG FRAPPE_REPO="https://github.com/frappe/frappe"
ARG ERPNEXT_REPO="https://github.com/frappe/erpnext"
# These are just development default value,
# it won't be used in production.
ARG ADMIN_PASS=12345
ARG MARIADB_PASS=12345
ARG SITE_NAME=site1.local


###############################################
# ENV
###############################################
# https://docs.frappe.io/framework/user/en/installation
# ---
# https://github.com/frappe/frappe_docker/blob/bc254c2b4ceb9d01dbdd598ace2053326120d27f/overrides/compose.mariadb.yaml#L11
# https://github.com/frappe/frappe_docker/blob/bc254c2b4ceb9d01dbdd598ace2053326120d27f/docs/02-setup/05-overrides.md?plain=1#L9-L13
ENV MARIADB_VERSION=11.8


###############################################
# Config File
###############################################
# MariaDB config
COPY --chown=frappe ./mariadb.cnf /home/frappe/mariadb.cnf
# image entrypoint
COPY --chown=frappe --chmod=0755 ./entrypoint.sh /usr/local/bin/entrypoint.sh


###############################################
# Install Dependencies
###############################################
RUN apt-get update \
    && apt-get install -y -q \
    # [fix] "debconf: delaying package configuration, since apt-utils is not installed"
    apt-utils \
    # [fix] "debconf: unable to initialize frontend: Dialog"
    # https://github.com/moby/moby/issues/27988
    && echo "debconf debconf/frontend select Noninteractive" | debconf-set-selections \
    ###############################################
    # sudo (required by entrypoint.sh at runtime)
    ###############################################
    && apt-get install -y -q sudo \
    && echo "frappe ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers \
    ###############################################
    # Build dependencies (needed for bench init to compile Python packages)
    # These are in frappe/bench but NOT in frappe/base
    ###############################################
    && apt-get install -y -q \
    build-essential \
    gcc \
    cron \
    libffi-dev \
    liblcms2-dev \
    libldap2-dev \
    libmariadb-dev \
    libsasl2-dev \
    libtiff5-dev \
    libwebp-dev \
    pkg-config \
    libbz2-dev \
    ###############################################
    # Install dependencies: MariaDB server
    # (mariadb-client is already in frappe/base)
    ###############################################
    && apt-get install -y -q apt-transport-https \
    && mkdir -p /etc/apt/keyrings \
    && curl -o /etc/apt/keyrings/mariadb-keyring.pgp "https://mariadb.org/mariadb_release_signing_key.pgp" \
    && echo "deb [signed-by=/etc/apt/keyrings/mariadb-keyring.pgp] https://mirror.kku.ac.th/mariadb/repo/${MARIADB_VERSION}/debian bookworm main" | tee /etc/apt/sources.list.d/mariadb.list \
    && apt-get update \
    && apt-get install -y -q \
    mariadb-server \
    python3-mysqldb \
    ###############################################
    # Install dependencies: Redis
    ###############################################
    && apt-get install -y -q \
    redis-server \
    ###############################################
    # Install dependencies: supervisor
    ###############################################
    && apt-get install -y -q \
    supervisor \
    ###############################################
    # clean-up
    ###############################################
    && apt-get autoremove --purge -y \
    && apt-get clean -y \
    ###############################################
    # Init Bench & Setup Site
    ###############################################
    # copy MariaDB Config
    && cp /home/frappe/mariadb.cnf /etc/mysql/mariadb.cnf \
    && service mariadb start \
    # root uses unix socket auth — no password needed to set the password
    && mariadb --user="root" --execute="ALTER USER 'root'@'localhost' IDENTIFIED BY '${MARIADB_PASS}';" \
    # start redis service
    && redis-server --port 11000 --daemonize yes \
    ###############################################
    # Symlink node/yarn into /usr/local/bin so bench subprocesses can find them
    # regardless of PATH restrictions (e.g. sudo secure_path)
    ###############################################
    && ln -sf "$(ls -d ${NVM_DIR}/versions/node/v*/bin/node | head -1)" /usr/local/bin/node \
    && ln -sf "$(ls -d ${NVM_DIR}/versions/node/v*/bin/yarn | head -1)" /usr/local/bin/yarn \
    ###############################################
    # Init Bench (run as frappe user — bench creates files in /home/frappe)
    ###############################################
    && sudo -EH -u frappe bash -c " \
        bench init /home/frappe/frappe-bench \
            --frappe-path ${FRAPPE_REPO} \
            --frappe-branch ${APP_BRANCH} \
        && cd /home/frappe/frappe-bench \
        && bench get-app erpnext ${ERPNEXT_REPO} --branch ${APP_BRANCH}" \
    # delete temp files
    && rm -rf /tmp/* \
    # create site (run as frappe user)
    && sudo -EH -u frappe bash -c " \
        cd /home/frappe/frappe-bench \
        && bench new-site ${SITE_NAME} \
            --mariadb-root-password ${MARIADB_PASS} \
            --admin-password ${ADMIN_PASS} \
        && bench --site ${SITE_NAME} install-app erpnext \
        && bench use ${SITE_NAME}"


###############################################
# WORKDIR
###############################################
WORKDIR /home/frappe/frappe-bench


###############################################
# FINALIZED
###############################################
USER frappe

# image entrypoint script
CMD ["/usr/local/bin/entrypoint.sh"]

# expose port
EXPOSE 8000 9000 3306
