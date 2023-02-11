FROM registry.access.redhat.com/ubi8/ubi-minimal

ENV PATH=/usr/pgsql-14/bin:${PATH}

RUN rpm -ivh https://download.postgresql.org/pub/repos/yum/reporpms/EL-8-x86_64/pgdg-redhat-repo-latest.noarch.rpm && \
    microdnf install --nodocs cpio && \
    cd /tmp && microdnf download postgresql14 postgresql14-libs && \
    rpm2cpio postgresql14-14.6-1PGDG.rhel8.x86_64.rpm | cpio -idmv && \
    rpm2cpio postgresql14-libs-14.6-1PGDG.rhel8.x86_64.rpm | cpio -idmv && \
    rm -rf /tmp/usr/share/doc/postgresql14 /tmp/usr/pgsql-14/share/man /tmp/usr/lib/.build && \
    cp -r /tmp/usr / && \
    rm -rf /tmp/usr postgresql14* && \
    microdnf install --nodocs python39 && \
    microdnf remove cpio pgdg-redhat-repo && microdnf clean all

WORKDIR /app

COPY ./requirements.txt /app

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 25432

ENTRYPOINT "python"

CMD "pgsqlcheck.py"
