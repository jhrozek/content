documentation_complete: true

metadata:
    SMEs:
        - jhrozek

reference: https://github.com/finos/compliant-financial-infrastructure/blob/dev/accelerators/kubernetes/ocp/sat_rh_ocp.adoc

title: 'CFI Service Approval Accelerators - OCP platform'

platform: ocp4

description: |-
    Compliant Financial Infrastructure (CFI) accelerates the development,
    deployment and adoption of services provided for AWS, Azure, Google
    Cloud, and IBM Cloud in a way that meets existing regulatory and
    internal security controls.

filter_rules: '"ocp4-node" not in platforms and "ocp4-master-node" not in platforms and "ocp4-on-sdn" not in platforms and "ocp4-node-on-sdn" not in platforms and "ocp4-node-on-ovn" not in platforms'

# includes all CIS rules
extends: cis

selections:
    - finos_ocp4:all
