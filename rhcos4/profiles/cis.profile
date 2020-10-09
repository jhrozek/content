documentation_complete: true

title: 'CIS Red Hat OpenShift Container Platform 4 Benchmark'

description: |-
    This profile defines a baseline that aligns to the Center for Internet Security®
    Red Hat OpenShift Container Platform 4 Benchmark™, V0.3, currently unreleased.

    This profile includes Center for Internet Security®
    Red Hat OpenShift Container Platform 4 CIS Benchmarks™ content.

    Note that this part of the profile is meant to run on the Nodes that
    Red Hat OpenShift Container Platform 4 runs on top of.

selections:
  ### 2 etcd
  # 2.1 Ensure that the --cert-file and --key-file arguments are set as appropriate
    - etcd_config_cert_file

  ### 4 Worker Nodes
  #### 4.1 Worker node configuration
  # 4.1.1 Ensure that the kubelet service file permissions are set to 644 or more restrictive
    - file_permissions_kubelet_service
  # 4.1.2 Ensure that the kubelet service file ownership is set to root:root
    - file_ownership_kubelet_service
  # 4.1.5 Ensure that the --kubeconfig kubelet.conf file permissions are set to 644 or more restrictive (Automated)
    # - create a rule based on file_permissions_kubelet_service that checks the perms of /etc/kubernetes/kubelet.conf
  # 4.1.6 Ensure that the --kubeconfig kubelet.conf file ownership is set to root:root
    # - create a rule based on file_ownership_kubelet_service that checks the ownership of /etc/kubernetes/kubelet.conf
  # 4.1.7 Ensure that the certificate authorities file permissions are set to 644 or more restrictive
    # - create a rule based on file_permissions_kubelet_service that checks the perms of /etc/kubernetes/kubelet-ca.crt
  # 4.1.8 Ensure that the client certificate authorities file ownership is set to root:root
    # - create a rule based on file_ownership_kubelet_service that checks the ownership of /etc/kubernetes/kubelet-ca.crt
  # 4.1.9 Ensure that the kubelet --config configuration file has permissions set to 644 or more restrictive
    # - create a rule based on file_permissions_kubelet_service that checks the perms of /var/lib/kubelet/kubeconfig
  # 4.1.10 Ensure that the kubelet configuration file ownership is set to root:root
    # - create a rule based on file_ownership_kubelet_service that checks the ownership of /var/lib/kubelet/kubeconfig
  ###
  #### 4.2 Kubelet
  # 4.2.1 Ensure that the --anonymous-auth argument is set to false
    - kubelet_anonymous_auth_disabled
  # 4.2.2 Ensure that the --authorization-mode argument is not set to AlwaysAllow
    # - this seems to be the default in the code, so the rule should verify that authorization.
  # 4.2.3 Ensure that the --client-ca-file argument is set as appropriate
    # - like kubelet_anonymous_auth_disabled but check for authentication.x509.clientCAFile=/etc/kubernetes/kubelet-ca.crt
  # 4.2.11 Ensure that the --rotate-certificates argument is not set to false
    # - like kubelet_anonymous_auth_disabled but check for rotateCertificates=true
  # 4.2.12 Verify that the RotateKubeletServerCertificate argument is set to true (Automated)
    # - like kubelet_anonymous_auth_disabled but check for featureGates.RotateKubeletServerCertificate=true
