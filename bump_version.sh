#!/bin/bash
# -*- coding: utf-8 -*-
#
#  This file is part of the python-semetric project.
#
#  Copyright (C) 2013  Matt Jeffery <matt@clan.se>
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

# default location for the version file for this project
TOP_LEVEL_DIR=$(git rev-parse --show-toplevel 2> /dev/null) # will default to empty string ie. current directory
MODULE_DIR="semetric/apiclient"
DEFAULT_VERSION_FILE="${TOP_LEVEL_DIR}/${MODULE_DIR}/VERSION.txt"

print_usage()
{
    cat  >&2 << EOF
usage: $(basename $0) [version] [version-file]

positional arguments:
version             version to bump to, if the version is not
                    given the new version will be guessed based
                    on the current git branch using git flow
                    convention
version-file        version file to write the version to

optional arguments:
-h, --help          show this help message and exit
EOF

    exit 1;
}

# decide if to print the help
while [ $# -gt 0 ] ; do
    case "$1" in
        -h | --help)            print_usage
                                ;;
        -*)                     echo "bad option '$1'" >&2
                                print_usage
                                ;;
        *)                      args=("${args[@]}" "$1")
                                shift
                                ;;
         esac
done
# If the number of arguments provided is less then >= 2 then print usage and exit
[ ${#args[@]} -lt 3 ] || print_usage

# Get the symbolic reference for HEAD, if we are on a git flow release branch
# this will return refs/heads/release/<version>
GIT_REF_HEAD=$(git symbolic-ref HEAD 2> /dev/null)
GIT_REF_HEAD_ARRAY=(${GIT_REF_HEAD//\// })

# Extract the version number from the release branch name
VERSION_GUESS=
if [ ${GIT_REF_HEAD_ARRAY[2]} == "release" ]; then
    VERSION_GUESS=${GIT_REF_HEAD_ARRAY[3]}
fi

NEW_VERSION="${1-$VERSION_GUESS}"
VERSION_FILE="${2-$DEFAULT_VERSION_FILE}"

# If the version number was not found print an error
if [ -z "${NEW_VERSION}" ]; then
    echo "error: cannot determin the release version" >&2
    print_usage
fi

# If the version cannot be found print and error
if [ ! -f "$VERSION_FILE" ]; then
    echo "error: cannot open version file \`${VERSION_FILE}'" >&2
    print_usage
fi

# Get the current version
CURRENT_VERSION=$(cat $VERSION_FILE)
BUMP_MESSAGE="Bumping version from ${CURRENT_VERSION} to ${NEW_VERSION}"

echo "${NEW_VERSION}" > "${VERSION_FILE}"
echo "${BUMP_MESSAGE}"

git commit "${VERSION_FILE}" -m "${BUMP_MESSAGE}" 2> /dev/null
