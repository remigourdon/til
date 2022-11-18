#!/usr/bin/env bash
set -Eueo pipefail

BUILD_DIR=".build"
rm -rf "${BUILD_DIR}"

CONFIG_FILE="hugo_config.toml"

THEME_VERSION="v1.1"
THEME_URL="https://github.com/luizdepra/hugo-coder/archive/refs/tags/${THEME_VERSION}.tar.gz"
THEME_DIR="themes/hugo-coder"

hugo new site "${BUILD_DIR}"
cp "${CONFIG_FILE}" "${BUILD_DIR}/config.toml"

CONTENT_DIR="${BUILD_DIR}/content/posts"
mkdir -p "${CONTENT_DIR}"
./process_markdown.py "${CONTENT_DIR}"

pushd "${BUILD_DIR}"

mkdir -p "${THEME_DIR}"
wget -qO- "${THEME_URL}" | tar xvz -C "${THEME_DIR}" --strip-components 1
hugo

popd