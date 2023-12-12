### API Change:
1. we decided to add a data query module which includes the load_data function we already have in data_preprocessing module but also with additional functions to query the data via other ways (e.g. fits file). Details in API draft data query module. We will work on completing this module in milestone 6 and we already completed 3 modules in milestone 5 (metadata extraction, wavelegnth alignment, data augmentation)  
2. we changed certain function arguments in data_preprocessing module to make it offer more flexibility to the user. 
* updated outlier_removal function argument to take in a list of columns user wants to remove outliers for instead of removing outliers for all columns before
* updated correct_redshift function argument to take in column name for wavelength given it could be named differently across data, so we let user define that 
