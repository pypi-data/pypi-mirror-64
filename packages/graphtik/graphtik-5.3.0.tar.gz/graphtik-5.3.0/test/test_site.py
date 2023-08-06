# Copyright 2016, Yahoo Inc.
# Licensed under the terms of the Apache License, Version 2.0. See the LICENSE file associated with the project for terms.
import importlib
import logging
import os
import os.path as osp
import subprocess
import sys

proj_path = osp.join(osp.dirname(__file__), "..")


def test_README_as_PyPi_landing_page(monkeypatch):
    from docutils import core as dcore

    long_desc = subprocess.check_output(
        "python setup.py --long-description".split(), cwd=proj_path
    )
    assert long_desc

    # See `docutils.frontend`
    dcore.publish_string(
        long_desc,
        enable_exit_status=False,
        # The specific options are a selective copy of:
        # https://github.com/pypa/readme_renderer/blob/master/readme_renderer/rst.py
        settings_overrides={
            "halt_level": 2,  # 2=WARN, 1=INFO
            "output_encoding": "unicode",
            "raw_enabled": False,
        },
    )


def test_sphinx_html(monkeypatch):
    # Fail on warnings, but don't rebuild all files (no `-a`),
    # rm -r ./build/sphinx/ # to fully test site.
    site_args = list("setup.py build_sphinx -W".split())
    if logging.getLogger(__name__).isEnabledFor(logging.INFO):
        site_args.append("-v")
    monkeypatch.setattr(sys, "argv", site_args)
    monkeypatch.chdir(proj_path)
    importlib.import_module("setup")
