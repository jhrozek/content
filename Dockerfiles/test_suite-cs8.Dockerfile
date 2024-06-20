# This Dockerfile is a minimal example for a Centos Stream 8 SSG test suite target container.
FROM quay.io/centos/centos:stream8@sha256:20da069d4f8126c4517ee563e6e723d4cbe79ff62f6c4597f753478af91a09a3

ENV AUTH_KEYS=/root/.ssh/authorized_keys

ARG CLIENT_PUBLIC_KEY
ARG ADDITIONAL_PACKAGES

# Install Python so Ansible remediations can work
# Don't clean all, as the test scenario may require package install.
RUN true \
        && yum install -y openssh-clients openssh-server openscap-scanner \
		python39 \
		$ADDITIONAL_PACKAGES \
        && true

RUN true \
        && for key_type in rsa ecdsa; do ssh-keygen -N '' -t $key_type -f /etc/ssh/ssh_host_${key_type}_key; done \
        && mkdir -p /root/.ssh \
        && printf "%s\n" "$CLIENT_PUBLIC_KEY" >> "$AUTH_KEYS" \
        && chmod og-rw /root/.ssh "$AUTH_KEYS" \
        && sed -i '/session\s\+required\s\+pam_loginuid.so/d' /etc/pam.d/sshd \
&& true

