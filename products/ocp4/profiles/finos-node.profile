documentation_complete: true

title: 'CFI Service Approval Accelerators - OCP platform - node'

platform: ocp4-node

metadata:
    SMEs:
        - jhrozek

description: |-
    Compliant Financial Infrastructure (CFI) accelerates the development,
    deployment and adoption of services provided for AWS, Azure, Google
    Cloud, and IBM Cloud in a way that meets existing regulatory and
    internal security controls.

extends: cis-node

filter_rules: '"ocp4-node" in platforms or "ocp4-master-node" in platforms or "ocp4-node-on-ovn" in platforms'

selections:
    - finos_ocp4:all
