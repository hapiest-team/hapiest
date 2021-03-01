# hapiest v0.2-alpha
*hapiest* is a GUI that works with the HITRAN API, enabling access
to all sorts of spectrographic data without knowledge of python.

*hapiest* is still in it's alpha stage of development. 
## Manual
The most up to date version of the manual can be downloaded [here](https://github.com/hitranonline/hapiest/raw/master/docs/manual.pdf).

## License 
*hapiest* is licensed under the LGPL license.

## Download
You can download an executable for your system [here.](https://github.com/hitranonline/hapiest/releases/tag/v0.2-alpha)

Currently 32 bit (x86) Windows and Linux machines are not supported but they will be eventually.

## Usage
A manual that documents what hapiest can do can be found 
[here](https://github.com/hitranonline/hapiest/raw/master/doc/HAPIESTmanual.pdf) (this link will download the PDF file).

## How to Manually Install
Hapiest has a limited number of binary packages, but the program itself can be
downloaded and ran from its source code quite easily.

*You must have python 3.6 or later to install and use hapiest*.

For mac and linux you can run the following in the terminal, and on windows in the command line (you must have git
installed):
```bash
git clone https://github.com/hitranonline/hapiest
```

This will download the latest version of hapiest and put it in a folder named hapiest. In order to run *hapiest*, 
you must have all of the packages listen in requirements.txt installed. 

It is recommended you install these packages using a [virtual environment](https://docs.python.org/3/tutorial/venv.html).

To install these packages automatically, you can run the following command:
```bash
pip install -r requirements.txt
```
Note that your pip program may be called pip3.


Then, to run the program execute the following:
```bash
cd hapiest
python3.6 src
```
    
You may have to replace `python` in the above commands with `python3`, `python3.6`, `python3.x`, etc., depending on your specific
configuration.

## Troubleshooting
*hapiest* is still an immature piece of software. If you encounter any bugs, you're encouraged to open an issue with
your bug report.

# References
If you use data retreived using hapiest or hapi and use it in research, please use the following citation if you publish
it:

```
R.V. Kochanov, I.E. Gordon, L.S. Rothman, P. Wcislo, C. Hill, J.S. Wilzewski, HITRAN Application Programming Interface
(HAPI): A comprehensive approach to working with spectroscopic data, J. Quant. Spectrosc. Radiat. Transfer 177, 15-30
(2016) [http://www.sciencedirect.com/science/article/pii/S0022407315302466?via%3Dihub].
```
