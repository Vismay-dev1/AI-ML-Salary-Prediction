# -*- coding: utf-8 -*-
from content_base import *

# ---- Program 6
prog("PROGRAM 6 — DATA PREPROCESSING", [code(13)],
     [(OUT["p6_map"], "Education mapping used for ordinal encoding (supplementary print of the notebook variable education_order)"),
      (OUT["p6"], "Preprocessed data – output of data.head() (12 columns shown in three parts)")],
     ["**Step by step:** (1) ID is dropped because it is only an identifier. (2) Education is mapped with the dictionary "
      "education_order. (3) Remote Work is one-hot encoded with pd.get_dummies. (4) The five remaining text columns are "
      "converted with LabelEncoder inside a loop, and each fitted encoder is saved in the dictionary encoders so that the "
      "same encoding can be applied to new data later.",
      "**Ordinal encoding (Education):** used when categories have a natural order. Bachelors < Masters < PhD are given 0, 1 "
      "and 2, so the order is preserved.",
      "**One-hot encoding (Remote Work):** each category becomes its own True/False (1/0) column: Remote_Hybrid, Remote_No "
      "and Remote_Yes. This suits unordered categories because no artificial order is created.",
      "**Label encoding:** LabelEncoder converts each distinct text value of a column into an integer label (0, 1, 2, …), "
      "assigned in alphabetical order of the values. For example, in the output the first row’s Job Title “Research Intern” "
      "became 14. LabelEncoder is neither frequency encoding nor target encoding: it does not use how often a value occurs or "
      "the salary values; it only gives each category a number.",
      "**Technical clarification about the notebook:** the Markdown text above this cell in the notebook describes the "
      "LabelEncoder step as “Frequency/Target-safe encoding”. That wording is not correct; the code simply performs label "
      "encoding, as explained above. The code is kept unchanged. A limitation of label encoding is that the numbers imply an "
      "order between categories that does not really exist; this matters more for Linear Regression than for tree-based models."])

prog("PROGRAM 7 — FEATURE AND TARGET SEPARATION", [code(14)],
     [(OUT["p7"], "Output of the feature and target separation")],
     ["**X = input features:** all columns of the preprocessed data except Salary (USD). The 11 feature columns are Job Title, "
      "Experience (Years), Education, Skill Count, Industry, Company, Location, Certification, Remote_Hybrid, Remote_No and Remote_Yes.",
      "**y = target/output:** the Salary (USD) column, the value the model must predict.",
      "**Shapes:** X has shape (500, 11) – 500 records and 11 features – and y has shape (500,) – 500 salary values."])

prog("PROGRAM 8 — TRAIN-TEST SPLIT", [code(16)],
     [(OUT["p8"], "Output of the train-test split (first line from the notebook; second line is a supplementary check)")],
     ["**What it does:** train_test_split randomly divides X and y into a training set and a testing set.",
      "**80% training / 20% testing:** test_size=0.2 reserves 20% of the data for testing, so 400 records are used for "
      "training and 100 records for testing (output: Train size: 400 | Test size: 100).",
      "**random_state=42:** the split is random but fixed by the seed 42, so the same records go to the same sets every time "
      "the code is run and the results can be reproduced. The number 42 itself has no special meaning.",
      "**Why splitting is needed:** a model must be tested on data it has not seen during training; otherwise the score "
      "would only show how well it memorised the training data."])

# ---- Program 9
H2("PROGRAM 9 — FEATURE SCALING", True)
H3("Program"); CODE(code(17)); H3("Output")
P("The notebook cell produces no printed output. The following snippet is a supplementary verification (not part of the "
  "notebook) that prints the mean and standard deviation of the scaled training data:")
CODE('print("Mean of scaled training features (rounded):", X_train_scaled.mean(axis=0).round(2))\n'
     'print("Std  of scaled training features (rounded):", X_train_scaled.std(axis=0).round(2))')
IMG(OUT["p9"], "Supplementary verification of StandardScaler (mean ≈ 0, standard deviation = 1 for each of the 11 features)")
H3("Explanation")
P("**Standardization:** StandardScaler transforms each feature as z = (x − mean) / standard deviation. After scaling, every "
  "feature has a mean of about 0 and a standard deviation of 1, as the output above confirms for all 11 features.")
P("**Mean and standard deviation:** the mean is the average value of a feature and the standard deviation shows how far "
  "values typically lie from the mean.")
P("**fit_transform and transform:** the scaler learns the mean and standard deviation from the training data only "
  "(fit_transform) and then applies the same values to the test data (transform). This avoids data leakage, i.e. the test "
  "data does not influence the scaling.")
P("**Why scaling is useful:** features measured on very different scales (for example experience 0–20 versus label "
  "codes 0–19) can affect algorithms that depend on feature magnitude. Tree-based models (Decision Tree, Random Forest, "
  "Gradient Boosting) split on thresholds and generally do not need standard scaling. In this workflow the scaled data is "
  "used only for Linear Regression; the tree models use the unscaled X_train and X_test.")

# ---- Program 10
H2("PROGRAM 10 — MODEL TRAINING", True)
cell19 = code(19)
head19, tail19 = cell19.split("# --- Linear Regression")
tail19 = "# --- Linear Regression" + tail19
imports19 = "\n".join(head19.split("\n")[:4])
evalpart = "\n".join(head19.split("\n")[3:]).strip("\n")
H3("Program")
P("The notebook trains and evaluates the models in one cell. Here the cell is shown in two parts: the imports with the model "
  "training code (this program) and the metric function (Program 11). The complete cell is also given in the Appendix.")
CODE(imports19); CODE(tail19)
H3("Output")
P("The training itself prints nothing; the printed lines are the evaluation results shown under Program 11. The following "
  "supplementary snippet (not part of the notebook) confirms that the models were fitted with the parameters in the code:")
CODE('print("Decision Tree  -> max_depth param:", dt.max_depth, "| fitted tree depth:", dt.get_depth(), "| leaves:", dt.get_n_leaves())\n'
     'print("Random Forest  -> n_estimators:", rf.n_estimators, "| max_depth param:", rf.max_depth, "| trees fitted:", len(rf.estimators_))\n'
     'print("Gradient Boost -> n_estimators:", gb.n_estimators, "| learning_rate:", gb.learning_rate, "| max_depth:", gb.max_depth, "| stages fitted:", gb.n_estimators_)')
IMG(OUT["p10"], "Supplementary verification of the trained models and their parameters")
H3("Explanation")
P("Four regression algorithms are trained on the same training data. The parameters are exactly those in the notebook.")
P("**1. Linear Regression** – LinearRegression() on the scaled features. It fits a straight-line (linear) equation "
  "salary = b0 + b1·x1 + b2·x2 + … by minimising the sum of squared errors. It is simple and fast and serves as the baseline, "
  "but it can only represent linear relationships.")
P("**2. Decision Tree Regressor** – DecisionTreeRegressor(max_depth=8, random_state=42). It splits the data again and again "
  "with yes/no questions on feature values and predicts the average salary of the training records in the final group "
  "(leaf). max_depth=8 limits the number of question levels to prevent a very deep, over-fitted tree.")
P("**3. Random Forest Regressor** – RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42, n_jobs=-1). It builds "
  "300 decision trees, each on a random sample of the data and with random feature choices, and averages their predictions. "
  "Averaging reduces over-fitting and makes it more stable than a single tree. n_jobs=-1 uses all CPU cores.")
P("**4. Gradient Boosting Regressor** – GradientBoostingRegressor(n_estimators=300, learning_rate=0.05, max_depth=3, "
  "random_state=42). It builds 300 small trees (depth 3) one after another; each new tree tries to correct the errors of the "
  "trees before it. learning_rate=0.05 makes each tree contribute only a small step.")

# ---- Program 11
H2("PROGRAM 11 — MODEL EVALUATION", True)
H3("Program")
P("This is the evaluation part of the same notebook cell. The function evaluate() is called after each model’s predict() in "
  "the code of Program 10.")
CODE(evalpart)
H3("Output")
IMG(OUT["p11"], "Output of the model evaluation (MAE, RMSE and R² on the test set)")
TBL(["Model", "MAE (USD)", "RMSE (USD)", "R²"],
    [[k, f"{m(k,'MAE'):,.2f}", f"{m(k,'RMSE'):,.2f}", f"{m(k,'R2'):.4f}"] for k in [LR, DT, RF, GB]],
    [5.6, 3.6, 3.6, 3.0], ["l", "r", "r", "r"], "Evaluation results on the 100-record test set (taken from the program output)")
H3("Explanation")
P("**Mean Absolute Error (MAE):** the average of the absolute differences between actual and predicted salaries. In simple "
  "words, it tells by how many dollars the prediction is wrong on average. Lower is better.")
P("**Root Mean Squared Error (RMSE):** the square root of the average of the squared errors. It is also in dollars, but because "
  "errors are squared first, large mistakes are penalised more. RMSE is always greater than or equal to MAE; a big gap between "
  "them means a few large errors. Lower is better.")
P("**R² score:** shows how much of the variation in salary is explained by the model. 1.0 is a perfect fit, 0 is no better than "
  "always predicting the average salary, and negative values mean worse than that. Higher is better.")
P("The notebook’s evaluate() function computes the three metrics with mean_absolute_error, mean_squared_error (followed by "
  "np.sqrt) and r2_score, stores them in the dictionary results and prints one formatted line per model.")

# ---- Program 12
H2("PROGRAM 12 — MODEL COMPARISON", True)
H3("Program")
CODE(code(21)); CODE(code(22))
H3("Output")
IMG(OUT["p12"], "Model comparison table – output of results_df (sorted by R², highest first)")
IMG(fig_of(22), "Model Performance Comparison (R² score and RMSE by model)", 16.2)
H3("Explanation")
P("The dictionary results is converted into a DataFrame with the models as rows (.T transposes it) and sorted by R² from "
  "highest to lowest. The two bar charts then show R² and RMSE for each model.")
P(f"**How the models are compared:** a model is better when its MAE and RMSE are lower and its R² is higher. On this test "
  f"set, {GB} has the lowest MAE ({m(GB,'MAE'):,.2f}) and RMSE ({m(GB,'RMSE'):,.2f}) and the highest R² ({m(GB,'R2'):.4f}); "
  f"{LR} has the highest errors and the lowest R² ({m(LR,'R2'):.4f}). {RF} and {DT} lie between them and are "
  f"close to each other (R² {m(RF,'R2'):.4f} and {m(DT,'R2'):.4f}). All three metrics give the same ranking in this run. "
  "Because only one random split with 100 test records was used, this ranking applies to this split; cross-validation would "
  "give a more reliable comparison.")

# ---- Program 13
prog("PROGRAM 13 — PREDICTED VS ACTUAL GRAPH", [code(24)],
     [(fig_of(24), "Predicted vs Actual Salary – Gradient Boosting", 11.0),
      (OUT["p13"], "Output of the best-model selection (printed line)")],
     [f"**What it does:** best_model_name = results_df['R2'].idxmax() selects the model with the highest R² (here "
      f"{F['best_model']}), takes its test predictions from preds_map and draws a scatter plot against the actual salaries.",
      "**X-axis** = actual salary; **Y-axis** = predicted salary; the **dashed diagonal line** = perfect prediction "
      "(predicted equals actual).",
      "**Reading the graph:** points closer to the diagonal are predictions closer to the actual value. In this graph most "
      "points lie near the line; the scatter is larger for some salaries above 100,000 USD, where a few points fall well "
      f"below the line. One prediction ({usd(F['best_pred_min'])}) is below zero, which is not a possible salary; Gradient "
      "Boosting can produce values outside the range of the training salaries."])

# ---- Program 14
prog("PROGRAM 14 — RESIDUAL ANALYSIS", [code(25)],
     [(fig_of(25), "Residual Distribution – Gradient Boosting", 14.0)],
     ["**Residual = Actual − Predicted.** The code computes it for the best model on the test set and plots its distribution "
      "as a histogram with a density curve. A positive residual means the model under-predicted; a negative residual means it over-predicted.",
      f"**Observation:** the residuals are centred close to zero: their mean is {F['resid_mean']:,.2f} USD and their standard deviation is "
      f"{F['resid_std']:,.2f} USD (calculated from the same residuals array). They range from {F['resid_min']:,.2f} to {F['resid_max']:,.2f} USD. "
      f"{F['abs_resid_gt_20k']} of the {F['n_test']} test records have an absolute error above 20,000 USD; the others are within that value.",
      "**Why residual analysis is used:** it checks whether errors are balanced around zero (no strong bias), shows how large "
      "the errors are and reveals unusual cases (outliers). A residual histogram that is roughly symmetric and centred on "
      "zero is a good sign."])

# ---- Program 15
prog("PROGRAM 15 — FEATURE IMPORTANCE", [code(27)],
     [(fig_of(27), "Random Forest Feature Importance", 13.5),
      (OUT["p15"], "Random Forest feature importance values – output of importances")],
     ["**What it does:** rf.feature_importances_ gives the importance of each feature in the trained Random Forest. The values add "
      "up to 1; a larger value means the feature was used more to reduce prediction error. The values are sorted and drawn as a horizontal bar chart.",
      f"**Result:** {IMPK[0]} has the highest importance ({IMP[IMPK[0]]:.4f}), followed by {IMPK[1]} ({IMP[IMPK[1]]:.4f}) and "
      f"{IMPK[2]} ({IMP[IMPK[2]]:.4f}). Together these three account for {IMP[IMPK[0]]+IMP[IMPK[1]]+IMP[IMPK[2]]:.1%} of the total importance. "
      f"Skill Count ({IMP['Skill Count']:.4f}), Company ({IMP['Company']:.4f}) and Industry ({IMP['Industry']:.4f}) have smaller values, "
      f"and Certification ({IMP['Certification']:.4f}), Education ({IMP['Education']:.4f}) and the three Remote Work columns "
      f"({IMP['Remote_Yes']:.4f}, {IMP['Remote_No']:.4f}, {IMP['Remote_Hybrid']:.4f}) have the lowest importance.",
      "**Note:** feature importance shows how the model used the features in this dataset; it does not prove a cause–effect "
      "relationship. Importance values of label-encoded columns with many distinct values (such as Location) can also be "
      "somewhat higher than those of columns with few values."])

# ---- Program 16
H2("PROGRAM 16 — NEW SALARY PREDICTION", True)
H3("Program")
CODE(code(29))
H3("Output")
IMG(OUT["p16"], "Output of the new salary prediction (Random Forest model)")
P("Supplementary verification (not part of the notebook) that displays what was passed to the model:")
CODE('print("Encoded new profile row sent to rf.predict():")\nprint(new_df.T.to_string(header=False))\nprint()\n'
     'print("Company \'Google\' in training classes?        ", \'Google\' in set(encoders[\'Company\'].classes_))\n'
     'print("Location \'Bengaluru, India\' in training classes?", \'Bengaluru, India\' in set(encoders[\'Location\'].classes_))\n'
     'print("Fallback class used for unseen values (classes_[0]):", encoders[\'Location\'].classes_[0])')
IMG(OUT["p16_supp"], "Supplementary check of the encoded new profile")
H3("Explanation")
P("**Profile:** the dictionary new_profile describes a Machine Learning Engineer with 5.0 years of experience, a Masters "
  "degree, 12 skills, in the Technology industry at Google, located in “Bengaluru, India”, working remotely (Yes) and "
  "holding an “AWS ML Specialty” certification.")
P("**Preprocessing of the new profile:** the profile is converted to a one-row DataFrame; Education is mapped with the same "
  "education_order; Remote Work is one-hot encoded; each label column is transformed with the encoder saved during training "
  "(encoders[col]); missing one-hot columns are added as 0 and the columns are re-ordered to match X.columns exactly. The "
  "model is then asked for a prediction with rf.predict(new_df)[0].")
P(f"**Result:** the program printed **Predicted Salary: {usd(F['predicted_salary'])}** using the Random Forest model.")
P("**Technical clarifications about the notebook code (code kept unchanged):**")
BUL(["The comment in the code says unseen categories fall back to “the most frequent known label”, but the code actually uses "
     "encoders[col].classes_[0], which is the **first label in alphabetical order**, not the most frequent one.",
     "The dataset contains the location “Bangalore, India”, but the profile uses “Bengaluru, India”, which is not in the "
     "training data. The supplementary check shows that this value was therefore replaced by the fallback “Austin, USA” "
     "(label 0) before prediction. The predicted salary above is hence for a profile whose Location was effectively "
     "“Austin, USA”. To predict for Bangalore, the spelling in new_profile should match the dataset (“Bangalore, India”).",
     "The prediction uses the Random Forest model (rf), as written in the notebook, although Gradient Boosting had the best "
     "scores in Program 12."])

# ================================ 8 WORKFLOW ===================================================
H1("8. PROJECT WORKFLOW")
P("The complete workflow of the project, from the dataset to the final prediction, is shown in the figure below.")
IMG("diagram_workflow.png", "Complete Project Workflow", 8.0)

# ================================ 9 RESULTS ====================================================
H1("9. RESULTS AND DISCUSSION")
P("All numbers in this chapter come from the program outputs of Chapter 7 (real execution), unless marked as a supplementary "
  "calculation from the dataset.")
H2("9.1 Dataset Observations")
BUL([f"The dataset has {DF.shape[0]} records and {DF.shape[1]} columns. A separate check found {int(DF.duplicated().sum())} duplicate rows, and "
     f"the {N_NAN} “missing” Certification entries are the text “None” (no certification).",
     f"Salary ranges from {usd0(sd['min'])} to {usd0(sd['max'])}, with mean {usd(sd['mean'])} and median {usd0(sd['50%'])}; the distribution has two groups (Program 5.2).",
     f"Experience and Skill Count have positive correlations with Salary ({corr['Salary (USD)']['Experience (Years)']:.2f} and {corr['Salary (USD)']['Skill Count']:.2f}).",
     "Median salary is lowest for Bachelors and highest for PhD; Remote Work type shows little difference."])
P("The two salary groups seen in Programs 5.2 and 5.5 can be explained by the Location column. The following table is a "
  "**supplementary calculation** (a Pandas groupby on the dataset, not a notebook cell). Each of the six Indian cities has a "
  "median salary well below that of the other locations, which matches the lower band of the scatter plot and the first "
  "peak of the histogram.")
g = DF.groupby("Location")["Salary (USD)"].agg(["count", "median", "mean"]).sort_values("median")
TBL(["Location", "Records", "Median salary (USD)", "Mean salary (USD)"],
    [[i, int(r["count"]), f"{r['median']:,.0f}", f"{r['mean']:,.0f}"] for i, r in g.iterrows()],
    [5.2, 2.6, 4.4, 4.2], ["l", "r", "r", "r"], "Salary by Location (supplementary groupby calculation on the dataset)", 11)
P(f"Consistent with this, Location has the highest feature importance in the Random Forest ({IMP['Location']:.4f}).")
H2("9.2 Model Performance")
TBL(["Model", "MAE (USD)", "RMSE (USD)", "R²"],
    [[k, f"{m(k,'MAE'):,.2f}", f"{m(k,'RMSE'):,.2f}", f"{m(k,'R2'):.4f}"] for k in [GB, RF, DT, LR]],
    [5.6, 3.6, 3.6, 3.0], ["l", "r", "r", "r"], "Model comparison (sorted by R²)")
BUL([f"**MAE:** {GB} {m(GB,'MAE'):,.2f} < {RF} {m(RF,'MAE'):,.2f} < {DT} {m(DT,'MAE'):,.2f} < {LR} {m(LR,'MAE'):,.2f}. "
     f"The Gradient Boosting MAE is about {m(GB,'MAE')/F['y_test_mean']:.1%} of the mean test salary ({usd0(F['y_test_mean'])}).",
     f"**RMSE:** {GB} {m(GB,'RMSE'):,.2f} < {RF} {m(RF,'RMSE'):,.2f} < {DT} {m(DT,'RMSE'):,.2f} < {LR} {m(LR,'RMSE'):,.2f}.",
     f"**R²:** {GB} {m(GB,'R2'):.4f} > {RF} {m(RF,'R2'):.4f} > {DT} {m(DT,'R2'):.4f} > {LR} {m(LR,'R2'):.4f}. "
     f"Gradient Boosting explains about {m(GB,'R2'):.1%} of the salary variation in the test set, Linear Regression about {m(LR,'R2'):.1%}."])
P(f"Since {GB} has the lowest MAE and RMSE and the highest R² on this test set, it is the best-performing of the four models "
  "**in this experiment**. The three tree-based models clearly outperform the Linear Regression baseline. A likely reason, "
  "not tested in the notebook, is that salary here depends on columns such as Location and Job Title in a non-linear way, "
  "while label-encoded numbers are arbitrary and a straight-line model cannot use them well; tree models can split on them.")
H2("9.3 Predicted vs Actual and Residuals")
P(f"For {GB}, most points lie near the perfect-prediction line (Program 13). The residuals have a mean of "
  f"{F['resid_mean']:,.2f} USD, which is small compared with the salary range, so the model shows little overall bias, and a "
  f"standard deviation of {F['resid_std']:,.2f} USD. {F['abs_resid_gt_20k']} of {F['n_test']} test predictions are more than 20,000 USD "
  "away from the actual salary, and one prediction is negative.")
H2("9.4 Feature Importance")
P(f"In the Random Forest, Location ({IMP['Location']:.4f}) and Experience (Years) ({IMP['Experience (Years)']:.4f}) are the most important features, "
  f"followed by Job Title ({IMP['Job Title']:.4f}). The Remote Work columns are the least important (each below 0.004). "
  "The notebook’s concluding Markdown cell says that Experience and Skill Count tend to be the strongest numeric predictors "
  "and that Job Title, Industry and Location contribute meaningfully. The actual run supports this for Experience (the most "
  f"important numeric feature), Job Title and Location. Skill Count ({IMP['Skill Count']:.4f}) is the second numeric feature but "
  f"much less important, and Industry has a low importance ({IMP['Industry']:.4f}). This shows why conclusions should be "
  "checked against the actual results.")
H2("9.5 New Salary Prediction")
P(f"For the sample profile, the Random Forest predicted **{usd(F['predicted_salary'])}**. Because the Location “Bengaluru, India” is "
  "not in the training data and was replaced by “Austin, USA”, this value should be read as a demonstration of the prediction "
  "pipeline rather than as a reliable estimate for Bengaluru.")
H2("9.6 Overall Discussion")
P("The project successfully runs a complete regression workflow. The results are specific to this dataset and to one "
  "80:20 split, and the best model was identified on the same test set that is used for reporting; therefore the "
  "numbers should be viewed as indicative of this experiment and not as a general claim about salaries.")

# ================================ 10-14 ========================================================
H1("10. ADVANTAGES", new=False)
BUL(["Automated salary estimation for a given job profile.", "Uses several job-related factors together.",
     "Multiple regression models can be trained and compared with the same metrics.",
     "Visualisation (histograms, box plots, heatmap, scatter plots) helps in understanding patterns in the data.",
     "Feature importance shows which variables were most influential in the model.",
     "The notebook is simple to run (Google Colab) and can be extended with larger datasets."])
H1("11. LIMITATIONS", new=False)
BUL([f"The dataset size is limited ({DF.shape[0]} records, 100 for testing), so results can change with a different split.",
     "Predictions depend on the quality and coverage of the dataset; the source and collection method of the data are not "
     "documented in the repository.",
     "Label encoding gives arbitrary numbers to categories and may not capture real-world relationships.",
     "Salary depends on many external factors (market conditions, negotiation, company policy) that are not in the data.",
     "Predictions must not be treated as guaranteed salary offers.",
     "Model performance depends on the training data; unseen categories (such as a differently spelt location) are replaced by a fallback label.",
     "Only one train-test split is used; there is no cross-validation or hyperparameter tuning."])
H1("12. FUTURE ENHANCEMENTS", new=False)
P("The following are suggestions for **future work**. They are **not implemented** in the current project.")
BUL(["Use larger, real-world datasets and more job-market data.",
     "Use better categorical encoding (for example one-hot encoding or carefully validated target encoding).",
     "Apply hyperparameter tuning (for example GridSearchCV) and cross-validation.",
     "Try more advanced regression algorithms, such as XGBoost or LightGBM.",
     "Build a web-based prediction interface and deploy it with Flask or Streamlit.",
     "Use real-time salary data and cloud deployment."])
H1("13. CONCLUSION", new=False)
P("In this project, a machine-learning system was developed to predict the salary of AI/ML-related jobs from the dataset "
  "ai_ml_job_analysis.csv. The data was inspected and explored with Pandas, Matplotlib and Seaborn, converted to numeric form "
  "using ordinal, one-hot and label encoding, split into training and testing sets and used to train four regression models.")
P(f"The models were evaluated with MAE, RMSE and R². In the actual run, Gradient Boosting gave the best scores on the test set "
  f"(R² = {m(GB,'R2'):.4f}), Random Forest and Decision Tree performed similarly to each other, and Linear Regression performed "
  f"the weakest (R² = {m(LR,'R2'):.4f}). Feature importance from the Random Forest showed Location and Experience as the most important features. "
  "A final cell shows how a new job profile is encoded in the same way as the training data and passed to the trained model for prediction.")
P("The project demonstrates the practical machine-learning workflow for a regression problem. It also showed the importance of "
  "careful data handling, for example matching category spellings for new inputs. The results are limited to the given dataset and are "
  "not a guarantee of real salaries.")
H1("14. LEARNING OUTCOMES", new=False)
BUL(["Python programming for data analysis.", "Using Pandas to load, inspect and transform datasets.", "Using NumPy for numerical operations.",
     "Data cleaning: checking missing values and understanding how they arise.", "Data preprocessing: ordinal, one-hot and label encoding, and scaling.",
     "Exploratory Data Analysis with statistics and graphs.", "Data visualisation with Matplotlib and Seaborn.",
     "Machine-learning concepts: supervised learning and regression.", "Training Linear Regression, Decision Tree, Random Forest and Gradient Boosting models.",
     "Model evaluation with MAE, RMSE and R², and model comparison.", "Interpreting feature importance and residuals.",
     "Working with Jupyter Notebook / Google Colab.", "Understanding the practical AI/ML workflow from data to prediction."])

# ================================ 15 VIVA ======================================================
H1("15. VIVA QUESTIONS AND ANSWERS")
QA = [
("What is Artificial Intelligence?", "AI is making computers perform tasks that normally need human intelligence, such as learning, reasoning and decision-making."),
("What is Machine Learning?", "Machine Learning is a part of AI in which computers learn patterns from data and make predictions without being explicitly programmed for every rule."),
("What is supervised learning?", "Learning from data that has known answers (labels). The model learns the relation between the inputs and the correct output."),
("What is regression?", "A supervised learning task in which the output is a continuous number, such as salary or price."),
("Why is this project a regression problem?", "Because it predicts salary, which is a continuous numeric value, not a category."),
("What is the target variable?", "The value we want to predict. Here it is Salary (USD)."),
("What are features?", "The input columns used for prediction, such as experience, education, skill count and location."),
("What is X?", "X is the set of input features: all columns except Salary (USD). Its shape is (500, 11)."),
("What is y?", "y is the target: the Salary (USD) column, with shape (500,)."),
("Why was train-test split used?", "To train the model on one part of the data and test it on unseen data, which shows how well it will work on new cases."),
("Why was random_state=42 used?", "To fix the random split so that the results are the same every time the code is run. 42 is just a commonly used seed."),
("What is Linear Regression?", "An algorithm that fits a straight-line equation between the features and the target by minimising squared errors."),
("What is a Decision Tree?", "A model that asks a series of yes/no questions on feature values to reach a prediction, like a flow chart."),
("What is Random Forest?", "An ensemble of many decision trees trained on random parts of the data; the final prediction is the average of all trees."),
("What is Gradient Boosting?", "An ensemble in which small trees are added one after another and each one corrects the errors of the previous ones."),
("What is MAE?", "Mean Absolute Error: the average size of the prediction error, in dollars here. Lower is better."),
("What is RMSE?", "Root Mean Squared Error: like MAE but large errors are punished more. Lower is better."),
("What is R²?", "A score that tells how much of the variation in the target the model explains. 1 is perfect; higher is better."),
("What is StandardScaler?", "A tool that rescales each feature to mean 0 and standard deviation 1."),
("What is LabelEncoder?", "A tool that converts each distinct category into an integer label (0, 1, 2 …)."),
("What is One-Hot Encoding?", "Converting a category into separate 0/1 columns, one for each category (for example Remote_Yes, Remote_No, Remote_Hybrid)."),
("Why is categorical data encoded?", "Machine-learning models work with numbers, so text categories must be converted to numeric form."),
("What is overfitting?", "When a model learns the training data too closely (including noise) and performs poorly on new data."),
("What is feature importance?", "A measure of how much each feature helped the model to make its predictions."),
("What is a residual?", "Residual = Actual value − Predicted value; it is the error of one prediction."),
("Why is salary the target variable?", "Because the aim of the project is to predict salary from the other job details."),
("Why are multiple models used?", "To compare their performance on the same data and see which works best."),
("What is n_estimators?", "The number of trees in a Random Forest, or the number of boosting stages in Gradient Boosting (300 in this project)."),
("What is max_depth?", "The maximum number of levels in a tree. It controls model complexity and helps limit overfitting."),
("What is learning_rate?", "In Gradient Boosting, it controls how much each new tree contributes. A small value (0.05) means small, careful steps."),
("What does fit() do?", "It trains the model (or scaler / encoder) by learning from the given data."),
("What does predict() do?", "It uses the trained model to give predicted outputs for new input data."),
("Why is Pandas used?", "To load the CSV file and to clean, inspect, encode and handle tabular data easily."),
("Why is NumPy used?", "For fast numerical and array operations; Pandas and Scikit-learn are built on it."),
("Why are Matplotlib and Seaborn used?", "To draw graphs such as histograms, heatmaps, box plots and scatter plots that help to understand the data and results."),
]
for i, (q, a) in enumerate(QA, 1):
    B.append(("qa", i, q, a))

# ================================ 16 REFERENCES ================================================
H1("16. REFERENCES")
REFS = [
 "Python Software Foundation. (n.d.). *Python 3 documentation*. https://docs.python.org/3/ (accessed 1 October 2026).",
 "The pandas development team. (n.d.). *pandas documentation*. https://pandas.pydata.org/docs/ (accessed 1 October 2026).",
 "NumPy Developers. (n.d.). *NumPy documentation*. https://numpy.org/doc/ (accessed 1 October 2026).",
 "Scikit-learn developers. (n.d.). *scikit-learn: Machine learning in Python – user guide and API reference*. https://scikit-learn.org/stable/ (accessed 1 October 2026).",
 "The Matplotlib development team. (n.d.). *Matplotlib documentation*. https://matplotlib.org/stable/ (accessed 1 October 2026).",
 "Waskom, M. L. (2021). seaborn: statistical data visualization. *Journal of Open Source Software, 6*(60), 3021. Documentation: https://seaborn.pydata.org/ (accessed 1 October 2026).",
 "Pedregosa, F., et al. (2011). Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research, 12*, 2825–2830.",
 "Breiman, L. (2001). Random forests. *Machine Learning, 45*(1), 5–32.",
 "Friedman, J. H. (2001). Greedy function approximation: A gradient boosting machine. *The Annals of Statistics, 29*(5), 1189–1232.",
 "Harris, C. R., et al. (2020). Array programming with NumPy. *Nature, 585*, 357–362.",
 "McKinney, W. (2010). Data structures for statistical computing in Python. In *Proceedings of the 9th Python in Science Conference* (pp. 56–61).",
 "Hunter, J. D. (2007). Matplotlib: A 2D graphics environment. *Computing in Science & Engineering, 9*(3), 90–95.",
 "Google. (n.d.). *Google Colaboratory*. https://colab.research.google.com/ (accessed 1 October 2026).",
 "Vinod, V. (n.d.). *AI-ML-Salary-Prediction* [GitHub repository]. https://github.com/Vismay-dev1/AI-ML-Salary-Prediction (notebook: AI_ML_Salary_Prediction.ipynb; dataset: ai_ml_job_analysis.csv).",
]
for i, r in enumerate(REFS, 1): B.append(("ref", i, r))

# ================================ 17 APPENDIX ==================================================
H1("17. APPENDIX — COMPLETE SOURCE CODE")
P("The complete code of the notebook AI_ML_Salary_Prediction.ipynb is given below in the notebook’s order, one block per "
  "code cell, without modification. Each block is labelled with its program number from Chapter 7.")
APP = [(2, "PROGRAM 1 — Load Dataset"), (3, "PROGRAM 2 — Load and Display Data"), (5, "PROGRAM 3 — Dataset Shape and Information"),
       (6, "PROGRAM 5.1 — Statistical Summary"), (7, "PROGRAM 4 — Check Missing Values"), (8, "PROGRAM 5.2 — Salary Distribution"),
       (9, "PROGRAM 5.3 — Correlation Analysis"), (10, "PROGRAM 5.4 — Salary by Categorical Features"),
       (11, "PROGRAM 5.5 — Experience vs Salary"), (13, "PROGRAM 6 — Data Preprocessing"),
       (14, "PROGRAM 7 — Feature and Target Separation"), (16, "PROGRAM 8 — Train-Test Split"), (17, "PROGRAM 9 — Feature Scaling"),
       (19, "PROGRAMS 10 & 11 — Model Training and Evaluation"), (21, "PROGRAM 12 — Model Comparison (table)"),
       (22, "PROGRAM 12 — Model Comparison (charts)"), (24, "PROGRAM 13 — Predicted vs Actual Graph"),
       (25, "PROGRAM 14 — Residual Analysis"), (27, "PROGRAM 15 — Feature Importance"), (29, "PROGRAM 16 — New Salary Prediction")]
for ci, t in APP:
    H3(t + f"  [notebook cell {ci}]")
    CODE(code(ci))
