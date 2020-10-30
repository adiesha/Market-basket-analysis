# Market-basket-analysis
# HW1 CSCI-550 Advanced Data Mining

# Team Members: 
Adiesha Liyanage

Kaveen Liyanage

Siddat Nesar

# How to run the system
First we need to clean the data and create necessary csv files. You need to run cleandata.py script. We have already run it and created the necessary csv files that we need, if # you like you can run it again.

    $command$ : python cleanData.py 

Now you can run our system. All the necessary code is in associationRulesAssesment.py script. When you run it you need to provide 3 command line arguments: minsup, minconf and krules. minsup is the minimum support value, minconf is the minimum confidence level which is a float and krules which is the number of k interesting rules that you want to output.
if aruguments that you want is: minsup = 15, minconf = 0.1 , krules = 25

    $command$ : python associationRulesAssesment.py 15 0.1 25

Then python script will run the data and output you the k number of interesting rules that you want
# Market_Basket_Analysis
