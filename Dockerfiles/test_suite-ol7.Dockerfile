# This Dockerfile is a minimal example for a OL7-based SSG test suite target container.
FROM index.docker.io/library/oraclelinux:7.9@sha256:797cf11329609b009eb092397144ffc1fbe5650494d2b9d0c46d26b6f26fcc92

ENV AUTH_KEYS=/root/.ssh/authorized_keys

ARG CLIENT_PUBLIC_KEY
ARG ADDITIONAL_PACKAGES

# Install Python so Ansible remediations can work
# Don't clean all, as the test scenario may require package install.
RUN true \
        && yum install -y openssh-clients openssh-server openscap-scanner \
        python tar \
        $ADDITIONAL_PACKAGES \
        && true

RUN true \
        && for key_type in rsa ecdsa; do ssh-keygen -N '' -t $key_type -f /etc/ssh/ssh_host_${key_type}_key; done \
        && mkdir -p /root/.ssh \
        && printf "%s\n" "$CLIENT_PUBLIC_KEY" >> "$AUTH_KEYS" \
        && chmod og-rw /root/.ssh "$AUTH_KEYS" \
        && sed -i '/session\s\+required\s\+pam_loginuid.so/d' /etc/pam.d/sshd \
&& true
