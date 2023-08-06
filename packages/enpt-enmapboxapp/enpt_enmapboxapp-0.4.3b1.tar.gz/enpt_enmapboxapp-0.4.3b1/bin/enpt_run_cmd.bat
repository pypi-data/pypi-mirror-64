:: enpt_enmapboxapp, A QGIS EnMAPBox plugin providing a GUI for the EnMAP processing tools (EnPT)
::
:: Copyright (C) 2019  Daniel Scheffler (GFZ Potsdam, daniel.scheffler@gfz-potsdam.de)
::
:: This software was developed within the context of the EnMAP project supported
:: by the DLR Space Administration with funds of the German Federal Ministry of
:: Economic Affairs and Energy (on the basis of a decision by the German Bundestag:
:: 50 EE 1529) and contributions from DLR, GFZ and OHB System AG.
::
:: This program is free software: you can redistribute it and/or modify it under
:: the terms of the GNU Lesser General Public License as published by the Free
:: Software Foundation, either version 3 of the License, or (at your option) any
:: later version.
::
:: This program is distributed in the hope that it will be useful, but WITHOUT
:: ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
:: FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
:: details.
::
:: You should have received a copy of the GNU Lesser General Public License along
:: with this program.  If not, see <http://www.gnu.org/licenses/>.

@echo off

:: activate the EnPT Anaconda environment located at %ENPT_PYENV_ACTIVATION%
:: echo %PATH%
call %ENPT_PYENV_ACTIVATION% enpt
:: echo %PATH%

:: check the path from where Python is loaded
:: where python

:: check if the enpt package is available
:: python -c "import enpt; print(enpt)"

:: print the user provided EnPT arguments
:: echo %*

:: run enpt_cli.py with the provided arguments
FOR /F %%i IN ('where enpt_cli.py') do (SET PATH_ENPT_CLI=%%i)

echo.
echo _______________________________________
python %PATH_ENPT_CLI% %*
echo _______________________________________
echo.

