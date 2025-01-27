# Segmentation Fault Report: Nuitka Compilation of SP_Management_Console.py

## Overview

This report details the segmentation fault encountered during the compilation of the `SP_Management_Console.py` script using Nuitka. The error appears to be related to reference counting in the compiled code, which may be caused by Nuitka itself or the dependencies used in the script.

## Command Used

The following command was used to compile the script with Nuitka:

```sh
py -m nuitka --standalone --plugin-enable=pyqt6 --plugin-enable=numpy --plugin-enable=pylint-warnings --follow-imports --include-data-dir=resources=resources --output-dir=dist --show-progress --show-scons --no-debug-immortal-assumptions --windows-icon-from-ico=resources/app.ico '.\Management Console.py'