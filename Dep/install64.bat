@echo off

SET py=C:\Python27\python.exe

%py% -m pip uninstall scipy
%py% -m pip uninstall scikit-learn
%py% -m pip uninstall numpy
%py% -m pip uninstall nltk
%py% -m pip uninstall jpype
%py% -m pip install wheel

rem py -m pip install Dep\scikit_learn-0.17-cp35-none-win32.whl
%py% -m pip install %~dp0\Dep\64\scikit_learn-0.15.1-cp27-none-win_amd64.whl
%py% -m pip install %~dp0\Dep\64\numpy-1.10.4+mkl-cp27-cp27m-win_amd64.whl

%py% -m pip install pyyaml nltk
%py% -m pip install %~dp0\Dep\64\scipy-0.17.0-cp27-none-win_amd64.whl

%py% -m pip install pyjnius

%py% -m pip install %~dp0\Dep\64\Cython-0.23.4-cp27-none-win_amd64

%py% -m pip install nose

%py% -c "import nltk; nltk.download(""punkt"")"

pause