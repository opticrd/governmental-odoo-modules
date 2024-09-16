ARG IMAGE_LOCATION=gcr.io/iterativo/dockerdoo
ARG ODOO_VERSION=15.0
FROM ${IMAGE_LOCATION}:${ODOO_VERSION}

ARG ODOO_VERSION
ENV ODOO_EXTRA_ADDONS /mnt/extra-addons
ENV ODOO_VERSION ${ODOO_VERSION}

USER root
RUN sudo mkdir -p ${ODOO_EXTRA_ADDONS}

RUN git clone --depth 1 --branch master --single-branch https://github.com/camptocamp/anthem.git ${ODOO_EXTRA_ADDONS}/camptocamp/anthem \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/camptocamp/odoo-cloud-platform.git ${ODOO_EXTRA_ADDONS}/camptocamp/odoo-cloud-platform \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/partner-contact.git ${ODOO_EXTRA_ADDONS}/oca/partner-contact \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/sale-workflow.git ${ODOO_EXTRA_ADDONS}/oca/sale-workflow \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/purchase-workflow.git ${ODOO_EXTRA_ADDONS}/oca/purchase-workflow \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/stock-logistics-workflow.git ${ODOO_EXTRA_ADDONS}/oca/stock-logistics-workflow \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/stock-logistics-warehouse.git ${ODOO_EXTRA_ADDONS}/oca/stock-logistics-warehouse \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/wms.git ${ODOO_EXTRA_ADDONS}/oca/wms \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/account-payment.git ${ODOO_EXTRA_ADDONS}/oca/account-payment \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/account-analytic.git ${ODOO_EXTRA_ADDONS}/oca/account-analytic \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/operating-unit.git ${ODOO_EXTRA_ADDONS}/oca/operating-unit \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/product-attribute.git ${ODOO_EXTRA_ADDONS}/oca/product-attribute \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/web.git ${ODOO_EXTRA_ADDONS}/oca/web \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/server-tools.git ${ODOO_EXTRA_ADDONS}/oca/server-tools \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/server-env.git ${ODOO_EXTRA_ADDONS}/oca/server-env \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/server-ux.git ${ODOO_EXTRA_ADDONS}/oca/server-ux \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/server-auth.git ${ODOO_EXTRA_ADDONS}/oca/server-auth \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/connector.git ${ODOO_EXTRA_ADDONS}/oca/connector \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/OCA/rest-framework.git ${ODOO_EXTRA_ADDONS}/oca/rest-framework \
    && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/indexa-git/l10n-dominicana.git ${ODOO_EXTRA_ADDONS}/indexa/l10n-dominicana
    # && git clone --depth 1 --branch ${ODOO_VERSION} --single-branch https://github.com/indexa-git/external-service-addons.git ${ODOO_EXTRA_ADDONS}/indexa/external-service-addons

COPY . ${ODOO_EXTRA_ADDONS}

RUN apt-get -qq update && apt-get -qq install -y --no-install-recommends build-essential \
    && find ${ODOO_EXTRA_ADDONS} -name 'requirements.txt' -exec pip3 --no-cache-dir install -r {} \; \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 -qq install --prefix=/usr/local --no-cache-dir --upgrade ${ODOO_EXTRA_ADDONS}/camptocamp/anthem

# TODO: remove this after finding the correct fix for: `module 'lib' has no attribute 'X509_V_FLAG_CB_ISSUER_CHECK'`
# Use fixed requirements from odoo core
# Add specific boto3 the one in https://github.com/camptocamp/odoo-cloud-platform/blob/15.0/requirements.txt does not support python 3.10
RUN pip3 -qq install --prefix=/usr/local --no-cache-dir pyopenssl==19.0.0 cryptography==2.6.1 boto3==1.26.7

RUN sudo chown -R 1000:1000 ${ODOO_EXTRA_ADDONS}

# TODO we need to finish up this PR for acceptance into Odoo's core
# RUN if [ "${ODOO_VERSION}" = "15.0" ]; then \
#     cd /opt/odoo && \
#     curl https://patch-diff.githubusercontent.com/raw/odoo/odoo/pull/69429.patch | git apply - && \
#     git status; \
#     fi

# Odoo Configuration file variables
ARG ADMIN_PASSWORD
ENV ADMIN_PASSWORD ${ADMIN_PASSWORD}
ARG PGHOST
ENV PGHOST ${PGHOST}
ARG PGUSER
ENV PGUSER ${PGUSER}
ARG PGPORT
ENV PGPORT ${PGPORT}
ARG PGPASSWORD
ENV PGPASSWORD ${PGPASSWORD}
ARG HTTP_INTERFACE
ENV HTTP_INTERFACE ${HTTP_INTERFACE}
ARG HTTP_PORT
ENV HTTP_PORT ${HTTP_PORT}
ARG DBFILTER
ENV DBFILTER ${DBFILTER}
ARG DBNAME
ENV DBNAME ${DBNAME}
ARG SERVER_WIDE_MODULES
ENV SERVER_WIDE_MODULES ${SERVER_WIDE_MODULES}

# 
ARG EXTRA_MODULES
ENV EXTRA_MODULES ${EXTRA_MODULES}

# camptocamp variables!
ARG RUNNING_ENV
ENV RUNNING_ENV ${RUNNING_ENV}
ARG ODOO_SESSION_REDIS
ENV ODOO_SESSION_REDIS ${ODOO_SESSION_REDIS}
ARG ODOO_SESSION_REDIS_HOST
ARG ODOO_SESSION_REDIS_PREFIX
ENV ODOO_SESSION_REDIS_PREFIX ${ODOO_SESSION_REDIS_PREFIX}
ENV ODOO_SESSION_REDIS_HOST ${ODOO_SESSION_REDIS_HOST}
ARG ODOO_LOGGING_JSON
ENV ODOO_LOGGING_JSON ${ODOO_LOGGING_JSON}
ARG AWS_HOST
ENV AWS_HOST ${AWS_HOST}
ARG AWS_REGION
ENV AWS_REGION ${AWS_REGION}
ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID ${AWS_ACCESS_KEY_ID}
ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY ${AWS_SECRET_ACCESS_KEY}
ARG AWS_BUCKETNAME
ENV AWS_BUCKETNAME ${AWS_BUCKETNAME}
ARG AWS_BUCKETNAME_UNSTRUCTURED
ENV AWS_BUCKETNAME_UNSTRUCTURED ${AWS_BUCKETNAME_UNSTRUCTURED}

USER 1000
