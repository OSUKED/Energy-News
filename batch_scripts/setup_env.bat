call cd ..
call conda env create -f environment.yml
call conda activate EnergyNews
call ipython kernel install --user --name=EnergyNews
pause