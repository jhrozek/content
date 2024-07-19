FROM index.docker.io/library/ubuntu:22.04@sha256:340d9b015b194dc6e2a13938944e0d016e57b9679963fdeb9ce021daac430221

ENV OSCAP_USERNAME oscap
ENV OSCAP_DIR content
ENV BUILD_JOBS 4

RUN true \
	&& apt-get -qq update \
	&& apt-get -qq install cmake ninja-build libopenscap8 libxml2-utils expat xsltproc python3-jinja2 python3-yaml \
	&& mkdir -p /home/$OSCAP_USERNAME \
	&& rm -rf /usr/share/doc /usr/share/doc-base \
		/usr/share/man /usr/share/locale /usr/share/zoneinfo \
	&& true

WORKDIR /home/$OSCAP_USERNAME

COPY . $OSCAP_DIR/

# clean the build dir in case the user is also building SSG locally
RUN rm -rf $OSCAP_DIR/build/*

WORKDIR /home/$OSCAP_USERNAME/$OSCAP_DIR/build

CMD true \
	&& cmake -G Ninja .. \
	&& ninja -j $BUILD_JOBS \
	&& ctest --output-on-failure -j $BUILD_JOBS \
	&& true
