This is a short instruction on how to run integration test and unit test for this package locally 

#### Clone the repo 
First please clone the repo https://code.harvard.edu/CS107/team16_2023/tree/main 

#### Run docker 
If you wish to run the tests in docker
docker pull iacs/cs107_ubuntu
bash run_cs107_docker.sh ./

#### Install dependency 
run pip install -r tests/requirements.txt at the root of the repo to install necessary dependencies 

#### Run integration test 
copy file test_integration.py and spectrum.fits into root directory and run pytest test_integration.py.
Note we tested the whole flow in test_data_processing_pipeline(). You will see 1 pass if everything works 

#### Run unit test 
copy the specific unit test file into root directory and run pytest <unit_test>.py Replace unit test with the specific test file name  
