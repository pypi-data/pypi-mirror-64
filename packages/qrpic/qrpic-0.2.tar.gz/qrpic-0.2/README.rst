qrpic
=====

A command-line tool to create beautiful QR-codes with perfectly fitting logos!

Usage
-----

qrpic takes (for the moment) only SVG images and produces an output SVG.
You invoke it simply with

.. code-block:: bash

    qrpic "data text or link you want in your qr code" path-to-logo.svg

qrpic computes the exact shape of the SVG and removes QR-code pixels that are
in the way, so they don't disturb your logo.

qrpic offers various options to control the logo size, adding shells and buffer
areas around your logo so it looks proper with just the right amount of spacing.
For more info, query ``qrpic --help``::

    usage: main.py [-h] [--out FILE] [--shell {none,viewbox,convex,boundary-box}]
                   [--ppi VALUE] [--svg-area VALUE] [--border VALUE]
                   [--error-correction {high,medium,low}] [--buffer VALUE]
                   [--shape-resolution VALUE]
                   TEXT SVG-FILE

    Generates QR-codes with centered logo images from SVGs in a beautiful manner,
    by not just overlaying them but also removing QR-code pixels properly so they
    do not interfere with the logo. Note that this tool does not (yet) check
    whether the generated QR-code is actually valid.

    positional arguments:
      TEXT                  The QR-code text.
      SVG-FILE              Logo SVG to center inside the QR code to be generated.

    optional arguments:
      -h, --help            show this help message and exit
      --out FILE            Output filename. If none specified, uses out.svg as
                            default.
      --shell {none,viewbox,convex,boundary-box}
                            Different types of shells to enclose the given SVG
                            shape where to remove QR-code pixels. none (default):
                            No shell geometry is applied. Removes pixels as per
                            geometry inside the given svg. viewbox: Assume the SVG
                            defined viewbox to be the shell. convex: Applies a
                            convex hull. boundary-box: Applies a minimal boundary
                            box around the SVG geometry.
      --ppi VALUE           Pixels per inch. Can be used to override the default
                            value of 96 for SVGs as defined per standard.
      --svg-area VALUE      Relative area of the SVG image to occupy inside the
                            QR-code (default 0.2).
      --border VALUE        Amount of border pixels around the final QR-code.
                            Default is 1.
      --error-correction {high,medium,low}
                            QR-code error correction level. By default "high" for
                            maximum tolerance.
      --buffer VALUE        A round buffer around the SVG shape/shell to add
                            (default is 0.04). The buffer is a relative measure.
                            To deactivate the buffer, just pass 0 as value.
      --shape-resolution VALUE
                            The interpolation resolution of circular geometry such
                            as SVG circles or buffers (default 32).

.. note::

    qrpic is currently very much a prototype. It works, but the SVG parsing and
    shape extraction capabilities are in the moment limited.
    If you encounter such a limitation or ugly output, please
    `file an issue <https://gitlab.com/Makman2/qrpic/issues>`_!

Roadmap
-------

- Better SVG parsing and shape extraction
- Support non-vector graphics such as PNG, JPG, etc. Properly handle
  image transparency
- QR-code verification step
- Use minimally necessary QR-code error correction level
