#!/usr/bin/env python3
# Copyright 2020 Oliver Smith
# SPDX-License-Identifier: GPL-3.0-or-later

"""
This file uses pmb.helper.pkgrel_bump to check if the aports need a pkgrel bump
for any package, caused by a soname bump. Example: A new libressl/openssl
version was released, which increased the soname version, and now all packages
that link against it, need to be rebuilt.
"""

import os
import pytest
import sys

import add_pmbootstrap_to_import_path
import pmb.helpers.pkgrel_bump
import pmb.helpers.logging
import pmb.parse


@pytest.fixture
def args(request):
    # Initialize args
    sys.argv = ["pmbootstrap",
                "--aports", os.path.dirname(__file__) + "/../..",
                "--log", "$WORK/log_testsuite_pmaports.txt"
                "chroot"]
    args = pmb.parse.arguments()

    # Initialize logging
    pmb.helpers.logging.init(args)
    request.addfinalizer(args.logfd.close)
    return args


@pytest.mark.pmaports_upstream_compat
def test_soname_bump(args):
    # Temporarily disabled, because the postmarketOS binary repository has
    # armhf packages for various kde related packages depending on
    # qt5-qtwebengine-dev, although qt5-qtwebengine-dev isn't available for
    # armhf anymore. All related pmaports were disabled for armhf, however
    # currently the binary repository does not delete binary packages yet,
    # after the corresponding pmaport was deleted/disabled for a given arch.
    # I'll work on this with high priority, so we can enable the test again.
    # Related: https://gitlab.com/postmarketOS/build.postmarketos.org/issues/38
    # - ollieparanoid
    return True

    if pmb.helpers.pkgrel_bump.auto(args, True):
        raise RuntimeError("One or more packages need to be rebuilt, because"
                           " a library they link against had an incompatible"
                           " upgrade (soname bump). Run 'pmbootstrap"
                           " pkgrel_bump --auto' to automatically increase the"
                           " pkgrel in order to trigger a rebuild. If this"
                           " test case failed during a pull request, the issue"
                           " needs to be fixed on the 'master' branch first,"
                           " then rebase your PR on 'master' afterwards.")
