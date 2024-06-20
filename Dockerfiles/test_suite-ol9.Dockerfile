# This Dockerfile is a minimal example for an OL9-based SSG test suite target container.
FROM index.docker.io/library/oraclelinux:9@sha256:1bc1fc7f5e0fec6fd1e47db5f63b9b35c3f734a5344ea3db81b4a43f116dd443

ENV AUTH_KEYS=/root/.ssh/authorized_keys

ARG CLIENT_PUBLIC_KEY
ARG ADDITIONAL_PACKAGES

# Install Python so Ansible remediations can work
# Don't clean all, as the test scenario may require package install.
RUN true \
        && dnf install -y openssh-clients openssh-server openscap-scanner \
        python3 tar \
        $ADDITIONAL_PACKAGES \
        && true

RUN true \
        && for key_type in rsa ecdsa; do ssh-keygen -N '' -t $key_type -f /etc/ssh/ssh_host_${key_type}_key; done \
        && mkdir -p /root/.ssh \
        && printf "%s\n" "$CLIENT_PUBLIC_KEY" >> "$AUTH_KEYS" \
        && chmod og-rw /root/.ssh "$AUTH_KEYS" \
        && sed -i '/session\s\+required\s\+pam_loginuid.so/d' /etc/pam.d/sshd \
&& true
