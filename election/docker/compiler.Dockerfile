FROM alpine AS build

RUN apk add git

WORKDIR /opt

RUN git clone --recursive https://github.com/ethereum/solidity.git

WORKDIR /opt/solidity

RUN git checkout v0.5.3 && git checkout -b v0.5.3

# Build dependencies
ADD /scripts/install_deps.sh /opt/solidity/scripts/install_deps.sh
RUN ./scripts/install_deps.sh

#Copy working directory on travis to the image
#COPY / $WORKDIR

# Number of parallel jobs during build
# or 0 for auto-computing (max(1, CPU_core_count * 2/3), a greedy value)
ARG BUILD_CONCURRENCY="0"

#Install dependencies, eliminate annoying warnings
RUN sed -i -E -e 's/include <sys\/poll.h>/include <poll.h>/' /usr/include/boost/asio/detail/socket_types.hpp
RUN cmake -DCMAKE_BUILD_TYPE=Release -DTESTS=0 -DSOLC_LINK_STATIC=1
RUN make solc \
    -j$(awk "BEGIN {                                       \
        if (${BUILD_CONCURRENCY} != 0) {                   \
            print(${BUILD_CONCURRENCY});                   \
        } else {                                           \
            x=($(grep -c ^processor /proc/cpuinfo) * 2/3); \
            if (x > 1) {                                   \
                printf(\"%d\n\", x);                       \
            } else {                                       \
                print(1);                                  \
            }                                              \
        }                                                  \
    }")
RUN strip solc/solc

FROM python:3.6
COPY --from=build /opt/solidity/solc/solc /usr/bin/solc
#ENTRYPOINT ["/usr/bin/solc"]
