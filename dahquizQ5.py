"""DAH Quiz: Question 5: Use random numbers to generate a Gaussian distribution
for a given mean and resolution. Plot a histogram and calculate mean and variance
and show this agrees with input values."""

import numpy as np
import matplotlib.pyplot as plt

#Ask user for mean, standard deviation, and number of random values
mu = float(input( "Enter the mean: "))
stdev = float(input( "Enter the standard deviation: "))
num = int(input( "Enter the number of random values: "))

#Generate random numbers from a Gaussian distribution
random = np.random.normal(mu, stdev, num)

#Calculate the mean, variance, and standard deviation of random numbers
#Print values to the terminal
mean = np.mean(random)
variance = np.var(random)
stdv = np.std(random)
print("The calculated mean is: ",mean)
print("The variance is: ",variance)
print("The standard deviation is: ",stdv)

#Plot random numbers in a normalised histogram
plt.hist(random,bins=50,density=True)
plt.title("Gaussian distribution of random numbers")
plt.xlabel("Random number")
plt.ylabel("Normalised Frequency")
plt.show()
