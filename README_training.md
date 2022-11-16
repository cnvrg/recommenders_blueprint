Use this blueprint to train a custom model that can recommend similar items to customers according to their behaviors. For the model to learn each customer’s choices and predict recommendations on future items, the blueprint requires custom data in the form of a customer’s preferences on the current items.

The model predictions are based directly on the scores, which are essentially predicted ratings for all items rather than just the ones the customer has already viewed and rated. This blueprint also establishes an endpoint that can recommend similar items to customers according to their behavior based on the newly trained model.

Complete the following steps to train this recommenders model:
1. Click the **Use Blueprint** button. The cnvrg Blueprint Flow page displays.
2. In the flow, click the **S3 Connector** task to display its dialog.
   * Within the **Parameters** tab, provide the following Key-Value pair information:
     - Key: `bucketname` - Value: enter the data bucket name
     - Key: `prefix` - Value: provide the main path to the CSV file folder
   * Click the **Advanced** tab to change resources to run the blueprint, as required.
3. Return to the flow and click the **Data Validation** task to display its dialog.
   * Within the **Parameters** tab, provide the following Key-Value pair information:
     * Key: `input_path` – Value: provide the path to the ratings file including the S3 prefix
     * `/input/s3_connector/<prefix>/<csv file>` − ensure the CSV file path adheres this format
     NOTE: You can use prebuilt data examples paths already provided.
   * Click the **Advanced** tab to change resources to run the blueprint, as required.
4.	Click the **Run** button. The cnvrg software launches the training blueprint as set of experiments, generating a trained recommender model and deploying it as a new API endpoint.
5. Track the blueprint's real-time progress in its Experiments page, which displays artifacts such as logs, metrics, hyperparameters, and algorithms.
6. Click the **Serving** tab in the project, locate your endpoint, and complete one or both of the following options:
   * Use the Try it Live section with a relevant user ID to check the model's predictions.
   * Use the bottom integration panel to integrate your API with your code by copying in your code snippet.

A custom model and an API endpoint, which can recommend similar items to customers according to their behaviors, have now been trained and deployed. To learn how this blueprint was created, click [here](https://github.com/cnvrg/recommenders-blueprint).
