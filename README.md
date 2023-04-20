# Crop-Recommendation-and-Soil-Analysis

India is the homeland to a variety of crops and the second populous country. The major percentage of the population are dependent on Agriculture for a living.The growing need of demand for food urges the young ML engineers like us to develop sophisticated systems for a more efficient farming and make it more profitable too. This project has a wide vision of implementing this crop recommendation system to the country's benefit.


The analysis of a soil sample reveals the soil type based on the image given as input. The model is built using five convolution layers with max pooling.

The crop recommendation system takes the state,district,season,year,crop and total area as input from which it processes and compares the production yield for that area with all the crops and recommends the best one to sow.



Dataset is taken from Kaggle. Link : https://www.kaggle.com/datasets/srinivas1/agricuture-crops-production-in-india


Algorithm :

Accuracy of the model using Linear Regression is 95%.

Accuracy of the model using Decision Tree Regressor is 96%.

Accuracy of the model using Random Forest Regressor is 97%.





Out of these three Algorithms, Random Forest Regressor has better Performance.

After Cross Validation of Random Forest Regressor the Accuracy is 99% and it is used for development of model.

Deployment :

We have used  flask to create the application.

# Output :

Crop Recommendation :-
![Screenshot 2023-01-01 at 12 18 04 PM](https://user-images.githubusercontent.com/113231945/210163072-44f95ee0-c0c8-4cea-9d2a-9beee166a293.png)

Soil Analysis :-
![Screenshot 2023-01-01 at 12 19 53 PM](https://user-images.githubusercontent.com/113231945/210163092-55b69315-cf75-470a-b147-7fed0fe78837.png)
