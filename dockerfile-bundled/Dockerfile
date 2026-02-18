###############################################
# Base Image
###############################################
# https://github.com/frappe/frappe_docker/blob/main/images/bench/Dockerfile
# `frappe/bench` use `debian:bookworm-slim` as a base image
# then it install dependencies for bench (python, nodejs).
FROM frappe/bench:latest


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
RUN sudo apt-get update \
    && sudo apt-get install -y -q \
    # [fix] "debconf: delaying package configuration, since apt-utils is not installed"
    apt-utils \
    # [fix] "debconf: unable to initialize frontend: Dialog"
    # https://github.com/moby/moby/issues/27988
    && echo "debconf debconf/frontend select Noninteractive" | sudo debconf-set-selections \
    ###############################################
    # Install dependencies: MariaDB
    ###############################################
    && sudo apt-get install -y -q apt-transport-https curl \
    && sudo mkdir -p /etc/apt/keyrings \
    && sudo curl -o /etc/apt/keyrings/mariadb-keyring.pgp "https://mariadb.org/mariadb_release_signing_key.pgp" \
    && echo "deb [signed-by=/etc/apt/keyrings/mariadb-keyring.pgp] https://mirror.kku.ac.th/mariadb/repo/${MARIADB_VERSION}/debian bookworm main" | sudo tee /etc/apt/sources.list.d/mariadb.list \
    && sudo apt-get update \
    && sudo apt-get install -y -q \
    mariadb-server \
    mariadb-client \
    mariadb-common \
    libmariadb3 \
    python3-mysqldb \
    ###############################################
    # Install dependencies: Redis
    ###############################################
    && sudo apt-get install -y -q \
    redis-server \
    ###############################################
    # Install dependencies: supervisor
    ###############################################
    && sudo apt-get install -y -q \
    supervisor \
    ###############################################
    # Install dependencies: nginx
    ###############################################
    && sudo apt-get install -y -q \
    nginx \
    ###############################################
    # clean-up
    ###############################################
    && sudo apt-get autoremove --purge -y \
    && sudo apt-get clean -y \
    ###############################################
    # Init Bench & Setup Site
    ###############################################
    # copy MariaDB Config
    && sudo cp /home/frappe/mariadb.cnf /etc/mysql/mariadb.cnf \
    && sudo service mariadb start \
    && sudo mariadb --user="root" --password="${MARIADB_PASS}" --execute="ALTER USER 'root'@'localhost' IDENTIFIED BY '${MARIADB_PASS}';" \
    # start redis service
    && sudo redis-server --port 11000 --daemonize yes \
    ###############################################
    # Init Bench
    ###############################################
    && bench init frappe-bench --frappe-path $FRAPPE_REPO --frappe-branch $APP_BRANCH \
    # cd into bench folder
    && cd frappe-bench \
    # install erpnext
    && bench get-app erpnext $ERPNEXT_REPO --branch $APP_BRANCH \
    # delete temp file
    && sudo rm -rf /tmp/* \
    # start new site
    && bench new-site $SITE_NAME \
    --mariadb-root-password $MARIADB_PASS  \
    --admin-password $ADMIN_PASS \
    && bench --site $SITE_NAME install-app erpnext \
    # use site
    && bench use $SITE_NAME


###############################################
# WORKDIR
###############################################
WORKDIR /home/frappe/frappe-bench


###############################################
# FINALIZED
###############################################
# image entrypoint script
CMD ["/usr/local/bin/entrypoint.sh"]

# expose port
EXPOSE 8000 9000 3306
