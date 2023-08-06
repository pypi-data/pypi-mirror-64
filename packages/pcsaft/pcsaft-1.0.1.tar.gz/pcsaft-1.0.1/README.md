# PC-SAFT

These functions implement the PC-SAFT equation of state. In addition to the hard chain and dispersion terms, these functions also include dipole, association and ion terms for use with these types of compounds. When the ion term is included it is also called electrolyte PC-SAFT (ePC-SAFT).

## Dependencies

The Numpy and Scipy packages are required. The core functions have been written in C++ to improve calculation speed, so [Cython](http://cython.org/) is needed, along with the [Eigen](https://github.com/eigenteam/eigen-git-mirror) package for linear algebra. For unit testing pytest is used.

## Python package

To make it easier to use this code, it has been added as a package to PyPi ([pcsaft](https://pypi.org/project/pcsaft/)), which means it can be installed using pip. This allows you to use the code without needing to compile the Cython code yourself. Binaries for Linux and Windows have been added, but MacOS is currently not supported.

## Compiling with Cython

To speed up the original Python code the core functions have been rewritten in C++. These are then connected with the remaining Python code using Cython. This gave a significant improvement in speed. The Cython code needs to be compiled before use, and for instructions on how to do this see the [Cython documentation](http://docs.cython.org/en/latest/src/quickstart/build.html).

The original Python-only code has been removed from the repository. If you still want to use the original Python-only functions, go back to an [earlier version](https://github.com/zmeri/PC-SAFT/tree/b43bf568c4dc1907316422d5c3f7b809e9725848) of the repository. Note that the Python-only code is no longer maintained, so it may not be as reliable as the Cython code.

## Author

* **Zach Baird** - [zmeri](https://github.com/zmeri)

## License

This project is licensed under the GNU General Public License v3.0 License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

When developing these functions the code from two other groups was used as references:
* Code from Joachim Gross (https://www.th.bci.tu-dortmund.de/cms/de/Forschung/PC-SAFT/Download/index.html)
* The MATLAB/Octave program written by Angel Martin and others (http://hpp.uva.es/open-source-software-eos/) 

