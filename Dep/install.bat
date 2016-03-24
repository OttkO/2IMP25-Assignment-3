@echo off

SET py=C:\Python27\python.exe

%py% -m pip uninstall scipy
%py% -m pip uninstall scikit-learn
%py% -m pip uninstall numpy
%py% -m pip uninstall nltk
%py% -m pip uninstall py4j
%py% -m pip uninstall python_dateutil
%py% -m pip uninstall beautifulsoup4
%py% -m pip uninstall lxml
%py% -m pip install wheel

%py% -m pip install python_dateutil

rem py -m pip install Dep\scikit_learn-0.17-cp35-none-win32.whl
%py% -m pip install %~dp0\Dep\scikit_learn-0.15.1-cp27-none-win32.whl

rem py -m pip install Dep\numpy-1.10.4+mkl-cp35-cp35m-win32.whl
rem %py% -m pip install Dep\numpy-1.10.4-cp27-none-win32.whl
%~dp0\Dep\numpy-1.9.0-win32-superpack-python2.7.exe

%~dp0\Dep\nltk-3.2.win32.exe
%~dp0\Dep\scipy-0.12.0-win32-superpack-python2.7.exe
%py% -m pip install py4j

%py% -m pip install nose
%py% -m pip install beautifulsoup4
%py% -m pip install lxml

%py% -c "import nltk; nltk.download(""punkt"")"

pause