#!/bin/bash

#0. Set up the directory for creating source
export INSTALL_BASEDIR=/usr/local/src

#In case we dont have permissions to add a folder there
sudo chmod a+rwx $INSTALL_BASEDIR

#1. Clone the official emacs repo (SPECIFICIALLY with the most recent changes)
cd $INSTALL_BASEDIR

git clone --depth=1 git://git.savannah.gnu.org/emacs.git

#2. Install the required Dependencies
#Taken from https://harryrschwartz.com/2022/12/08/how-i-build-emacs-from-source-on-debian
sudo apt install \
	make \
	build-essential \
	libgtk-3-dev \
	libgnutls28-dev \
	libtiff5-dev \
	libgif-dev \
	libjpeg-dev \
	libpng-dev \
	libxpm-dev \
	libncurses-dev \
	texinfo \
	libjansson4 \
	libjansson-dev \
	libgccjit0 \
	libgccjit-10-dev \
	gcc-10 \
	g++-10 \
	libmagickcore-dev \
	libmagick++-dev \
	libtree-sitter-dev \
	libwebkit2gtk-4.0-dev

#3. Set up Config options and then Build Emacs
cd $INSTALL_BASEDIR/emacs

export CC=/usr/bin/gcc-10 CXX=/usr/bin/gcc-10
./autogen.sh
./configure \
	--with-native-compilation \
	--with-json \
	--with-tree-sitter \
	--with-imagemagick \
	--with-xwidgets \
	--with-cairo \
	--with-x-toolkit=gtk3
make --jobs=$(nproc)
sudo make install
