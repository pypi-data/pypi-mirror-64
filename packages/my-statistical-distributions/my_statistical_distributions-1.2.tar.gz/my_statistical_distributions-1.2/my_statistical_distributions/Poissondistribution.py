import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution

class Poisson(Distribution):
    """ Poisson distribution class for calculating and 
    visualizing a Poisson distribution.
    
    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        lambda (float) the rate parameter       
    """
   
   
    def __init__(self, l=1):
        
        self.l = l
        
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
        
    def calculate_mean(self):
        """Function that returns the mean of the distribution
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """
        
        self.mean = self.l
        
        return self.mean
    
    def calculate_stdev(self):

        """Function that returns the standard deviation lambda of the distribution
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """
        
        self.stdev = math.sqrt(self.l)
     
        return self.stdev
    
    def replace_stats_with_data(self):
    
        """Function to calculate lambda from the data set
        
        Args: 
            None
        
        Returns: 
            float: the lambda value
    
        """
    
        self.l = sum(self.data) / len(self.data)
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        
        return self.l
    
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """
                
        plt.hist(self.data)
        plt.title('Bar Chart of Data')
        plt.xlabel('outcome')
        plt.ylabel('count')
        
    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """
        
        a = math.exp(- self.l)
        b = math.pow(self.l, k) / math.factorial(k)
        
        return a * b
    
    def plot_bar_pdf(self, n):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            n: maximum number of events to calculate pdf for
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
        
        x = []
        y = []
        
        # calculate the x values to visualize
        for i in range(n + 1):
            x.append(i)
            y.append(self.pdf(i))

        # make the plots
        plt.bar(x, y)
        plt.title('Probability of Events in One Interval')
        plt.ylabel('Probability')
        plt.xlabel('Events')

        plt.show()

        return x, y
    
    def __add__(self, other):
        
        """Function to add together two Poisson distributions
        
        Args:
            other (Poisson): Poisson instance
            
        Returns:
            Poisson: Poisson distribution
            
        """
        
        result = Poisson()
        result.l = self.l + other.l
        result.calculate_mean()
        result.calculate_stdev()
        
        return result
        
        
    def __repr__(self):
    
        """Function to output the characteristics of the Poisson instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Poisson
        
        """
        
        return "mean {}, standard deviation {}, lambda {}".\
        format(self.mean, self.stdev, self.l)