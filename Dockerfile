FROM alpine:latest
MAINTAINER sudoii<sudoii@sudoii.com>

ENV NODE_ID=0                     \
    SPEEDTEST=0                   \
    CLOUDSAFE=1                   \
    AUTOEXEC=0                    \
    ANTISSATTACK=1                \
    MU_SUFFIX=cloudflare.com      \
    MU_REGEX=%5m%id.%suffix       \
    API_INTERFACE=modwebapi       \
    WEBAPI_URL=https://1.1.1.1    \
    WEBAPI_TOKEN=glzjin           \
    MYSQL_HOST=127.0.0.1          \
    MYSQL_PORT=3306               \
    MYSQL_USER=cloudflare         \
    MYSQL_PASS=cloudflare         \
    MYSQL_DB=cloudflare           \
    MYSQL_PUSH_DURATION=60        \
    REDIRECT=cloudflare.com       \
    FAST_OPEN=true                \
    NS_SYS_1=1.0.0.1              \
    NS_SYS_2=8.8.8.8              \
    NS_NETFLIX=null               \
    NS_HBO=null                   \
    NS_HULU=null                  \
    NS_BBC=null

COPY . /root/shadowsocks
WORKDIR /root/shadowsocks

RUN  apk --no-cache add \
                        curl \
                        libintl \
                        python3-dev \
                        libsodium-dev \
                        openssl-dev \
                        udns-dev \
                        mbedtls-dev \
                        pcre-dev \
                        libev-dev \
                        libtool \
                        libffi-dev                              && \
     apk --no-cache add --virtual .build-deps \
                        tar \
                        make \
                        gettext \
                        py3-pip \
                        autoconf \
                        automake \
                        build-base \
                        linux-headers                           && \
     iptables -I INPUT -p tcp --tcp-flags RST RST -j DROP       && \
     ln -s /usr/bin/python3 /usr/bin/python                     && \
     ln -s /usr/bin/pip3    /usr/bin/pip                        && \
     cp  /usr/bin/envsubst  /usr/local/bin/                     && \
     pip install --upgrade pip                                  && \
     pip install -r requirements.txt                            && \
     rm -rf ~/.cache && touch /etc/hosts.deny                   && \
     apk del --purge .build-deps

CMD envsubst < apiconfig.py > userapiconfig.py && \
    envsubst < config.json > user-config.json  && \
    echo -e "${NS_SYS_1}\n${NS_SYS_2}\n" > dns.conf  && \
    python server.py
