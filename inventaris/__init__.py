"""Package inventaris: pengolahan data inventaris toko berbasis CLI.

Alur dependensi antar-module (panah = "mengimpor"):

    main.py -> cli -> loader    -> validator -> exceptions
                   -> processor
                   -> report
"""

__version__ = "1.0.0"