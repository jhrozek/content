FROM fedora:35 as builder

RUN dnf -y install cmake make git /usr/bin/python3 python3-pyyaml python3-jinja2 openscap-utils
RUN git clone --depth 1 https://github.com/ComplianceAsCode/content
WORKDIR /content
RUN ./build_product --datastream-only --debug ocp4 rhcos4 eks

FROM registry.access.redhat.com/ubi8/ubi-minimal
WORKDIR /
COPY --from=builder /content/build/ssg-ocp4-ds.xml .
COPY --from=builder /content/build/ssg-rhcos4-ds.xml .
COPY --from=builder /content/build/ssg-eks-ds.xml .
