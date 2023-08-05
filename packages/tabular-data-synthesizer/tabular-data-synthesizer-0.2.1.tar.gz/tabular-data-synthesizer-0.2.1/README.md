# TabularDataSynthesizer
The tabular data synthezier project has as a primary goal to support the general synthesis of tabular data, whatever its shape or form. Currently, the synthesizer supports the following data types:
 - Nominal
 - Ordinal
 - Continuous
 - Dates (approached as continous data)

 TODO:
  - Datetime
  - Free text




The tabular data synthetization process consists of several steps:
1. Tokenizing the data for the relevant columns. The 'relevant' columns in this case are determined by the columns with dtypes category and object. These values are tokenized using the pd.factorize class, which maps each value to an integer. We save this and the inverse mapping. This tokenization step allows us to input everyday data, that has textual columns as well. 
2. The second step consists of a numerical representation to a representation that can be used by a neural network. In short, this means getting all values in the range [-1, 1]. There are several implementations of this. For continues values, there is three ways at the moment. 
    1. **Gaussian Mixture Models.** A combination of several gaussians are fit to the data of a single column and can represent the data when it does not follow a typical gaussian shape, which is the assumption of more neural networks.
    2. **Bayesian Gaussian Mixture Models.** The BGMM is an adaptation of the Gaussian Mixture Models, that, in short, allows for a varying number of components to be learned. This method takes quite a bit longer to fix, but should typically give a bit better results. 
    3. **Scaler**. Futhermore, we can use normalizations and standardization to get the data in the required ranges. However, this often has caveats for the neural network, since the resulting distributions are not typically Gaussians. 


