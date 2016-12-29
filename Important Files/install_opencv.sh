#!/usr/bin/env bash

OPENCV_VERSION="3.1.0"

OPENCV_URL="https://github.com/Itseez/opencv/archive/${OPENCV_VERSION}.zip"
OPENCV_PACKAGE_NAME="opencv-${OPENCV_VERSION}"
OPENCV_CONTRIB_URL="https://github.com/Itseez/opencv_contrib/archive/${OPENCV_VERSION}.zip"
OPENCV_CONTRIB_PACKAGE_NAME="opencv_contrib-${OPENCV_VERSION}"

PREFIX="${PREFIX:-/usr/local}"
MAKEFLAGS="${MAKEFLAGS:--j 4}"

install_build_dependencies() {
    local build_packages="build-essential git cmake pkg-config"
    local image_io_packages="libjpeg-dev libtiff5-dev libjasper-dev \
                             libpng12-dev"
    local video_io_packages="libavcodec-dev libavformat-dev \
                             libswscale-dev libv4l-dev \
                             libxvidcore-dev libx264-dev"
    local gtk_packages="libgtk2.0-dev"
    local matrix_packages="libatlas-base-dev gfortran"
    local python_dev_packages="python2.7-dev python3-dev python-pip python3-pip"

    sudo apt-get install -y $build_packages $image_io_packages $gtk_packages \
                       $video_io_packages $matrix_packages $python_dev_packages
}

install_global_python_dependencies() {
    sudo pip install virtualenv virtualenvwrapper
}

install_local_python_dependences() {
    pip install numpy
    pip install imutils
}

download_packages() {
    wget -c -O "${OPENCV_PACKAGE_NAME}.zip" "$OPENCV_URL"
    wget -c -O "${OPENCV_CONTRIB_PACKAGE_NAME}.zip" "$OPENCV_CONTRIB_URL"
}

unpack_packages() {
    # unzip args:
    # -q = quiet
    # -n = never overwrite existing files
    unzip -q -n "${OPENCV_PACKAGE_NAME}.zip"
    unzip -q -n "${OPENCV_CONTRIB_PACKAGE_NAME}.zip"
}

setup_virtualenv() {
    echo -e "\n# virtualenv and virtualenvwrapper" >> ~/.profile
    echo "export WORKON_HOME=$HOME/.virtualenvs" >> ~/.profile
    echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.profile
    export WORKON_HOME="$HOME/.virtualenvs"
    source /usr/local/bin/virtualenvwrapper.sh
    mkvirtualenv -p python2 cv
    workon cv
    install_local_python_dependences
}

build() {
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX="$PREFIX" \
          -D INSTALL_PYTHON_EXAMPLES=ON \
          -D OPENCV_EXTRA_MODULES_PATH="$HOME/$OPENCV_CONTRIB_PACKAGE_NAME/modules" \
          -D BUILD_EXAMPLES=ON \
          ..
    make ${MAKEFLAGS}
}

install() {
    sudo make install
    sudo ldconfig
}

log() {
    local msg="$1"; shift
    local _color_bold_yellow='\e[1;33m'
    local _color_reset='\e[0m'
    echo -e "\[${_color_bold_yellow}\]${msg}\[${_color_reset}\]"
}

main() {
    log "Instalando as dependencias..."
    install_build_dependencies
    log "Baixando o OpenCV..."
    download_packages
    log "Descompactando o OpenCV..."
    unpack_packages
    log "Instalando as dependencias globais do Python..."
    install_global_python_dependencies
    log "Configurando o ambiente local Python..."
    setup_virtualenv
    #SECONDS = 0
    log "Construindo o OpenCV..."
    #duration = $SECONDS
    #echo "Tempo de instalação: $(($duration / 60)) minutos"
    cd "$OPENCV_PACKAGE_NAME"
    mkdir build
    cd build
    build
    echo "Instalando o OpenCV..."
    install
    ln -s /usr/local/lib/python2.7/site-packages/cv2.so ~/.virtualenvs/cv/lib/python2.7/site-packages/cv2.so
    cd /home/pi/
    chmod +x on_reboot.sh 
}

main
