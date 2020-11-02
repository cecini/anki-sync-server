# use buildkit
# [Choice] Python version: 3, 3.9, 3.8, 3.7, 3.6
#FROM mcr.microsoft.com/vscode/devcontainers/python:${VARIANT}

FROM debian:stable-slim

# [Option] Install zsh
ARG INSTALL_ZSH="true"
# [Option] Upgrade OS packages to their latest versions
ARG UPGRADE_PACKAGES="true"

# Install needed packages and setup non-root user. Use a separate RUN statement to add your own dependencies.
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID
COPY .devcontainer/library-scripts/common-debian.sh /tmp/library-scripts/
#ENV HTTP_PROXY "http://192.168.1.1:8123"
#ENV HTTPS_PROXY "http://192.168.1.1:8123"
#ENV NO_PROXY "192.168.1.1,192.168.1.227,localhost,creativebaul.asuscomm.com"
# RUN cat /etc/apt/sources.list
# RUN git config --list

# use mirror not proxy 
#RUN echo 'Acquire::http::Proxy "http://192.168.1.1:8123/";' > /etc/apt/apt.conf.d/proxy.conf && \
#    echo 'Acquire::https::Proxy "http://192.168.1.1:8123/";' >> /etc/apt/apt.conf.d/proxy.conf

RUN echo "deb http://ftp2.cn.debian.org/debian stable main" > /etc/apt/sources.list && \
    echo "deb http://security.debian.org/debian-security stable/updates main" >> /etc/apt/sources.list  && \
    echo "deb http://ftp2.cn.debian.org/debian stable-updates main" >> /etc/apt/sources.list  
# RUN apt-get update && apt-get install git 

#RUN git config --global http.proxy  http://192.168.1.1:8123/ &&  \
#    git config --global https.proxy  http://192.168.1.1:8123/ && \
#    git config --global http.sslVerify false

RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    # Remove imagemagick due to https://security-tracker.debian.org/tracker/CVE-2019-10131
    && apt-get purge -y imagemagick imagemagick-6-common \ 
    && apt-get install -y git \
   # && git config --global http.proxy  http://192.168.1.1:8123/ \
    #&& git config --global https.proxy  http://192.168.1.1:8123/ \
    #&& git config --global http.sslVerify false \
    # Install common packages, non-root user
    && bash /tmp/library-scripts/common-debian.sh "${INSTALL_ZSH}" "${USERNAME}" "${USER_UID}" "${USER_GID}" "${UPGRADE_PACKAGES}" \
    && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts




ARG VARIANT=3.9.0
ARG PYTHON_PATH=/usr/local/python
ENV PIPX_HOME=/usr/local/py-utils \
    PIPX_BIN_DIR=/usr/local/py-utils/bin
ENV PATH=${PYTHON_PATH}/bin:${PATH}:${PIPX_BIN_DIR}
COPY .devcontainer/library-scripts/python-debian.sh /tmp/library-scripts/
# why not #9 4.591 /bin/sh: 1: VARIANT: not found
RUN apt-get update && bash /tmp/library-scripts/python-debian.sh "${VARIANT}" "${PYTHON_PATH}" "${PIPX_HOME}" \


# Setup default python tools in a venv via pipx to avoid conflicts
ENV PIPX_HOME=/usr/local/py-utils \
    PIPX_BIN_DIR=/usr/local/py-utils/bin
ENV PATH=${PATH}:${PIPX_BIN_DIR}
COPY .devcontainer/library-scripts/python-debian.sh /tmp/library-scripts/
RUN bash /tmp/library-scripts/python-debian.sh "none" "/usr/local" "${PIPX_HOME}" "${USERNAME}" "false" \ 
    && apt-get clean -y && rm -rf /tmp/library-scripts


# [Option] Install Node.js
ARG INSTALL_NODE="true"
#ARG NODE_VERSION="none"
ARG NODE_VERSION="lts/*"

ENV NVM_DIR=/usr/local/share/nvm
ENV NVM_SYMLINK_CURRENT=true \
    PATH=${NVM_DIR}/current/bin:${PATH}
COPY .devcontainer/library-scripts/node-debian.sh /tmp/library-scripts/
RUN if [ "$INSTALL_NODE" = "true" ]; then bash /tmp/library-scripts/node-debian.sh "${NVM_DIR}" "${NODE_VERSION}" "${USERNAME}"; fi \
    && apt-get clean -y && rm -rf /var/lib/apt/lists/* /tmp/library-scripts


### [Option] Install Node.js
##ARG INSTALL_NODE="true"
#RUN if [ "${INSTALL_NODE}" = "true" ]; then su vscode -c "source /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi


# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
# COPY requirements.txt /tmp/pip-tmp/
# RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
#    && rm -rf /tmp/pip-tmp

# [Optional] Uncomment this section to install additional OS packages.
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends vim gdb
## for anki 
#RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh 
#RUN source $HOME/.cargo/env
#wget https://github.com/protocolbuffers/protobuf/releases/download/v3.13.0/protoc-3.13.0-linux-x86_64.zip
#sudo unzip protoc-3.13.0-linux-x86_64.zip -d /usr/local/ -x readme.txt
#rustup update
#cargo install ripgrep
#RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
#    && apt-get -y install --no-install-recommends portaudio19-dev mpv lame npm rsync gcc gettext git curl python3-dev python3-venv libxcb-xinerama0
#    && apt-get -y install --no-install-recommends portaudio19-dev mpv lame rsync gcc gettext git curl libxcb-xinerama0


# [Optional] Uncomment this line to install global node packages.
# RUN su vscode -c "source /usr/local/share/nvm/nvm.sh && npm install -g <your-package-here>" 2>&1
