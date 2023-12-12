### API Change:
1. we decided to add a data query module (?)
2. we changed certain function arguments in data_preprocessing module to make it offer more flexibility to the user. 
* updated outlier_removal function argument to take in a list of columns user wants to remove outliers for instead of removing outliers for all columns before
* updated correct_redshift function argument to take in column name for wavelength given it could be named differently across data, so we let user define that 
