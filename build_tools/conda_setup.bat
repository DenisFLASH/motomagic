REM to run from Windows command line: cd into build_tools folder and type conda_setup.bat
REM to run from files explorer: double-click conda_setup.bat

call deactivate
conda env remove -y -n motomagic-env
conda create -y -n motomagic-env python=3.5 --yes --file requirements_conda.txt
call activate motomagic-env
cd ..
REM pip install -r build_tools/requirements_pip.txt

python setup.py develop
python -c "import motomagic.tests as mt; mt.run()"
