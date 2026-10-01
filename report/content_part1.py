# -*- coding: utf-8 -*-
from content_base import *

# ================================ COVER ========================================================
B.append(("cover",))

# ================================ CERTIFICATE ==================================================
H1("CERTIFICATE", center=True)
P("This is to certify that **Vismay Vinod**, a student of **Bachelor of Computer Applications (BCA)** at "
  "**[College Name]**, **[University Name]**, has carried out the internship project entitled "
  "**“AI/ML Job Salary Prediction”** as part of the **Artificial Intelligence and Machine Learning** internship at "
  "**[Internship Organization]** for a duration of **[Internship Duration]**, under the guidance of **[Guide Name]**.")
P("The work reported in this document is based on the student’s own Jupyter Notebook "
  "(AI_ML_Salary_Prediction.ipynb) and the dataset ai_ml_job_analysis.csv. To the best of my knowledge, the project "
  "has been completed satisfactorily and is submitted for evaluation.")
TBL(["Item", "Details"],
    [["Student Name", "Vismay Vinod"], ["Course", "Bachelor of Computer Applications (BCA)"], ["College", "[College Name]"],
     ["Internship Organization", "[Internship Organization]"], ["Project Title", "AI/ML Job Salary Prediction"],
     ["Internship Duration", "[Internship Duration]"], ["Guide Name", "[Guide Name]"]],
    [5.4, 11.0], ["l", "l"], None, 13)
SP(30)
B.append(("sig", ["Faculty / Project Guide\n[Guide Name]", "Head of Department\n[Department Name]",
                  "Internship Organization\n[Authorised Signatory]"]))
LINE("Date: [DD / MM / YYYY]          Place: [Place]          Official Seal: [Seal]", False, 13, False, 8)
NOTE("Note: This page is a certificate format with placeholders. It becomes valid only after it is completed, signed and "
     "sealed by the authorised persons of the college and the internship organization.")

# ================================ DECLARATION ==================================================
H1("DECLARATION", center=True)
P("I, **Vismay Vinod**, a student of Bachelor of Computer Applications (BCA) at [College Name], hereby declare that the "
  "project work entitled **“AI/ML Job Salary Prediction”** submitted in this report is a record of work carried out by me "
  "as part of the internship / project requirements of the BCA programme, in the area of Artificial Intelligence and "
  "Machine Learning.")
P("The programs, outputs and graphs presented in this report were produced by running my project code "
  "(AI_ML_Salary_Prediction.ipynb) on the dataset ai_ml_job_analysis.csv. Standard open-source libraries and their public "
  "documentation have been used and are acknowledged in the references. This work has not been submitted to any other "
  "university or institution for the award of any degree or diploma.")
SP(40)
B.append(("sig", ["Signature of the Student\nVismay Vinod"]))
LINE("Date: [DD / MM / YYYY]          Place: [Place]", False, 14, False, 4)

# ================================ ACKNOWLEDGEMENT ==============================================
H1("ACKNOWLEDGEMENT", center=True)
P("I express my sincere gratitude to **[College Name]** and the **Department of [Department Name]** for providing the "
  "academic environment and facilities required to complete this internship project.")
P("I am thankful to my faculty / project guide, **[Guide Name]**, for the guidance, suggestions and encouragement "
  "given during the work. I also thank **[Internship Organization / Training Provider]** for the opportunity to learn the "
  "practical workflow of Artificial Intelligence and Machine Learning through this internship.")
P("I am grateful to my teachers, classmates and friends who supported me with discussions and feedback, and to my "
  "family for their constant motivation. I also acknowledge the open-source communities behind Python, NumPy, Pandas, "
  "Matplotlib, Seaborn and Scikit-learn, whose tools and documentation made this project possible.")
SP(18)
LINE("Vismay Vinod", True, 14, False, 2)

# ================================ ABSTRACT =====================================================
H1("ABSTRACT", center=True)
P("This project, **AI/ML Job Salary Prediction**, applies supervised machine learning to estimate the annual salary "
  "(in USD) of an AI/ML-related job from its characteristics. Salary estimates help job seekers, students and recruiters "
  "form realistic expectations, and the project shows how data-driven models can handle many job factors together.")
P(f"The project uses the dataset **ai_ml_job_analysis.csv**, which contains **{DF.shape[0]} records and {DF.shape[1]} columns**: "
  "job title, years of experience, education, skill count, industry, company, location, remote-work type, certification "
  "and salary. The work follows a standard workflow in Python: data loading and inspection, exploratory data analysis "
  "with Pandas, Matplotlib and Seaborn, preprocessing, an 80:20 train-test split, feature scaling and model training.")
P("In preprocessing, Education is ordinal-encoded, Remote Work is one-hot encoded, and Job Title, Industry, Company, "
  "Location and Certification are converted to numeric labels with LabelEncoder. Four regression models from "
  "Scikit-learn are trained and compared: Linear Regression, Decision Tree Regressor, Random Forest Regressor and "
  "Gradient Boosting Regressor. They are evaluated with Mean Absolute Error (MAE), Root Mean Squared Error (RMSE) and the "
  "R² score, and further analysed with a predicted-versus-actual plot, residual analysis and Random Forest feature "
  "importance.")
P(f"On the 100-record test set used in this project, the measured R² values were {m(GB,'R2'):.4f} (Gradient Boosting), "
  f"{m(RF,'R2'):.4f} (Random Forest), {m(DT,'R2'):.4f} (Decision Tree) and {m(LR,'R2'):.4f} (Linear Regression). "
  "A final prediction cell estimates the salary for a new job profile entered as a Python dictionary. The purpose of the "
  "project is educational: to demonstrate the complete practical machine-learning workflow for a regression problem. "
  "The predictions are estimates for this dataset and are not salary guarantees.")
B.append(("toc",))

# ================================ 1 INTRODUCTION ===============================================
H1("1. INTRODUCTION")
H2("1.1 Introduction to Artificial Intelligence")
P("Artificial Intelligence (AI) is the branch of computer science that builds systems able to perform tasks that normally "
  "need human intelligence, such as learning from experience, recognising patterns, understanding language, making "
  "decisions and solving problems. Modern AI is used in search engines, recommendation systems, voice assistants, medical "
  "diagnosis support, fraud detection and many other applications.")
H2("1.2 Introduction to Machine Learning")
P("Machine Learning (ML) is a part of AI in which a computer learns patterns from data instead of being programmed with "
  "fixed rules. A learning algorithm is given example data, finds relationships in it and builds a model, which can then "
  "make predictions for new data. ML is commonly divided into supervised learning (data with known answers), unsupervised "
  "learning (data without answers) and reinforcement learning (learning from rewards). This project uses **supervised "
  "learning**, specifically **regression**, because the target (salary) is a continuous number.")
H2("1.3 Machine Learning in Salary Prediction")
P("A salary depends on several factors at the same time: the role, experience, education, skills, industry, employer, "
  "location and working arrangement. A machine-learning model can learn from past records how these factors are related "
  "to salary and then estimate the salary of a new profile. Because it uses many features together and applies the same "
  "learned rules every time, it gives consistent estimates, which can support salary benchmarking and career planning.")
H2("1.4 Problem Statement")
P("To develop a machine learning system that predicts the salary of an AI/ML-related job based on job characteristics "
  "such as experience, education, skills, industry, company, location, remote-work type and certification.")
H2("1.5 Objectives")
NUM(["Load and understand the dataset.", "Perform exploratory data analysis.",
     "Preprocess categorical and numerical data.", "Prepare features and target variables.",
     "Split the dataset into training and testing sets.", "Train multiple regression algorithms.",
     "Evaluate the models using MAE, RMSE and R².", "Compare model performance.",
     "Analyse feature importance.", "Predict salary for a new job profile."])

# ================================ 2 EXISTING SYSTEM ============================================
H1("2. EXISTING SYSTEM", new=False)
P("In the traditional approach, salary expectations are formed manually: by asking colleagues, reading job advertisements, "
  "browsing salary web sites or relying on a recruiter’s experience. This approach has several limitations:")
BUL(["**Manual estimation:** the estimate depends on a person’s judgement and on the few examples that person has seen.",
     "**Difficulty handling many factors:** it is hard to weigh experience, education, skills, location, industry and "
     "company together in one’s head.",
     "**Lack of consistent prediction:** two people can give different estimates for the same profile, and the same person "
     "may give different estimates at different times.",
     "**Difficulty in identifying relationships:** manual methods cannot easily measure how strongly each factor is related "
     "to salary or whether the relationship is linear or non-linear.",
     "**Time-consuming:** collecting and comparing many records by hand is slow."])
P("Simple rules of thumb (for example, “salary rises with experience”) are useful, but they cannot capture interactions "
  "between several factors. This does not mean manual methods are useless; they remain a good source of context. The "
  "proposed system adds a data-driven, repeatable estimate on top of them.")

# ================================ 3 PROPOSED SYSTEM ============================================
H1("3. PROPOSED SYSTEM")
P("The proposed system is a machine-learning pipeline built in a Jupyter / Google Colab notebook. It reads the job dataset, "
  "inspects and visualises it, converts all columns into numeric form, splits the data into training and testing parts, "
  "trains four regression models, evaluates them with standard metrics, compares them and finally predicts the salary of "
  "a new job profile. The workflow is shown in the figure below.")
IMG("diagram_proposed.png", "Workflow of the Proposed System", 7.2)
P("Each stage of the workflow is implemented as one or more cells in the notebook, and each is explained with its "
  "program and output in Chapter 7.")

# ================================ 4 SYSTEM REQUIREMENTS ========================================
H1("4. SYSTEM REQUIREMENTS")
H2("4.1 Hardware Requirements")
P("The dataset is small (about 50 KB) and the models train in a few seconds, so the requirements are modest. The "
  "figures below are typical estimates for running the notebook; they were not obtained from a formal benchmark.")
TBL(["Component", "Minimum (to run the notebook)", "Recommended (comfortable use)"],
    [["Computer", "Laptop / desktop PC", "Laptop / desktop PC"],
     ["Processor", "Dual-core, 64-bit CPU", "Quad-core CPU (Intel i5 / Ryzen 5 or better)"],
     ["RAM", "4 GB", "8 GB or more"],
     ["Storage", "1 GB free disk space", "5 GB free (SSD preferred)"],
     ["Display", "1366 × 768", "Full HD (1920 × 1080)"],
     ["Network", "Not needed after set-up (Colab needs internet)", "Broadband (for Google Colab / package install)"]],
    [3.2, 6.6, 6.6], ["l", "l", "l"], "Hardware requirements")
H2("4.2 Software Requirements")
TBL(["Software", "Purpose", "Version used for the outputs in this report"],
    [["Python 3", "Programming language", ENV["python"]],
     ["Jupyter Notebook / Google Colab", "Environment to run the notebook", "The README recommends Colab; the outputs here were produced by running the notebook code with Python"],
     ["NumPy", "Numerical computing", ENV["numpy"]], ["Pandas", "Data handling and preprocessing", ENV["pandas"]],
     ["Matplotlib", "Plotting", ENV["matplotlib"]], ["Seaborn", "Statistical visualisation", ENV["seaborn"]],
     ["Scikit-learn", "Machine learning", ENV["sklearn"]]],
    [4.6, 4.6, 7.2], ["l", "l", "l"], "Software requirements")
NOTE("Operating system: Windows, Linux or macOS (any system that can run Python 3 and Jupyter). Results may differ slightly "
     "if other library versions are used.")

# ================================ 5 TECHNOLOGIES ===============================================
H1("5. TECHNOLOGIES AND LIBRARIES USED", new=False)
H2("5.1 Python")
P("Python is a high-level, general-purpose programming language with simple, readable syntax. It is widely used for data "
  "science and machine learning because it has a large ecosystem of libraries, an active community and works well with "
  "notebooks.")
H2("5.2 NumPy")
P("NumPy provides the n-dimensional array and fast mathematical operations on whole arrays. In this project it is used "
  "for numeric work such as selecting numeric columns (np.number) and computing the square root for RMSE (np.sqrt). "
  "Pandas and Scikit-learn are built on NumPy arrays.")
H2("5.3 Pandas")
P("Pandas provides the DataFrame, a table-like structure for loading CSV files, inspecting data (head, info, describe), "
  "finding missing values (isnull), mapping and encoding columns (map, get_dummies) and separating features from the "
  "target. All dataset handling and preprocessing in this project is done with Pandas.")
H2("5.4 Matplotlib")
P("Matplotlib is the basic plotting library of Python. It is used to create and control figures, axes, titles, labels and "
  "scatter plots, for example the predicted-versus-actual plot and the model-comparison bar charts.")
H2("5.5 Seaborn")
P("Seaborn is built on Matplotlib and gives attractive statistical plots with little code. In this project it is used for "
  "the histograms with density curve, the correlation heatmap, box plots, the experience–salary scatter plot and the "
  "feature-importance bar chart.")
H2("5.6 Scikit-learn")
P("Scikit-learn is the main machine-learning library of the project. It provides preprocessing tools (LabelEncoder, "
  "StandardScaler), data splitting (train_test_split), regression algorithms (LinearRegression, DecisionTreeRegressor, "
  "RandomForestRegressor, GradientBoostingRegressor) and evaluation metrics (mean_absolute_error, mean_squared_error, "
  "r2_score), all with a uniform fit() / predict() interface.")

# ================================ 6 DATASET ====================================================
H1("6. DATASET DESCRIPTION")
P(f"The dataset **ai_ml_job_analysis.csv** (stored in the project repository) was inspected directly. It contains "
  f"**{DF.shape[0]} rows (records)** and **{DF.shape[1]} columns**, which agrees with the repository README. Each row is one "
  f"AI/ML job record and the column **Salary (USD)** is the target to be predicted.")
def rng(c):
    return f"{DF[c].min():.1f} – {DF[c].max():.1f}" if c == "Experience (Years)" else f"{DF[c].min():,} – {DF[c].max():,}"
TBL(["Column", "Description", "Type", "Values observed"],
    [["ID", "Unique record identifier", "Numeric", f"{rng('ID')} ({DF['ID'].nunique()} unique)"],
     ["Job Title", "Job position / role", "Categorical", f"{DF['Job Title'].nunique()} different titles"],
     ["Experience (Years)", "Years of professional experience", "Numeric", rng("Experience (Years)")],
     ["Education", "Education level", "Categorical", "Bachelors, Masters, PhD"],
     ["Skill Count", "Number of technical skills listed", "Numeric", rng("Skill Count")],
     ["Industry", "Industry sector of the job", "Categorical", f"{DF['Industry'].nunique()} sectors"],
     ["Company", "Employer name", "Categorical", f"{DF['Company'].nunique()} companies"],
     ["Location", "Job location (city, country, or “Remote”)", "Categorical", f"{DF['Location'].nunique()} locations"],
     ["Remote Work", "Remote / Hybrid / No status", "Categorical", "Yes, No, Hybrid"],
     ["Certification", "Professional certification held", "Categorical",
      f"{DF['Certification'].nunique()} certificates + “None” ({N_NONE} rows)"],
     ["Salary (USD)", "Salary in US dollars (target variable)", "Numeric", rng("Salary (USD)")]],
    [3.4, 5.0, 2.5, 5.5], ["l", "l", "l", "l"], "Structure of ai_ml_job_analysis.csv", 11)
P("The column types were verified by running df.info() (see Program 3). Seven columns are text (object) columns and four "
  "are numeric: ID, Experience (Years), Skill Count and Salary (USD).")
NOTE("Important observation: in the Certification column, the text “None” (meaning no certification) appears in "
     f"{N_NONE} rows. Pandas read_csv treats the string “None” as a missing value by default, so df.isnull() reports "
     f"{N_NAN} missing values in Certification (Program 4). These are records without a certification, not data-entry errors. "
     "In the notebook, astype(str) turns them into the label “nan”, which LabelEncoder then encodes like any other category.")

# ================================ 7 PROGRAMS (intro) ===========================================
H1("7. IMPLEMENTATION: PROGRAMS AND OUTPUTS")
P("This chapter presents the actual programs from the notebook AI_ML_Salary_Prediction.ipynb, each followed by its output "
  "and a short explanation. The code is copied from the notebook without modification.")
H3("How the outputs were obtained")
P("The notebook file in the repository was saved without cell outputs. Therefore the code cells were executed, unchanged and "
  "in order, on the real dataset, and the printed results and graphs were captured. Printed text and tables are shown as "
  "images rendered from those captured results; graphs are the actual figures drawn by the notebook code. No result in this "
  f"report was typed in manually. Environment: Python {ENV['python']}, pandas {ENV['pandas']}, NumPy {ENV['numpy']}, "
  f"scikit-learn {ENV['sklearn']}, Matplotlib {ENV['matplotlib']}, Seaborn {ENV['seaborn']}. Results in another environment "
  "(for example Google Colab with other library versions) may differ slightly.")
NOTE("Where the notebook itself prints nothing (for example, feature scaling), a short “supplementary verification” snippet "
     "is shown separately and clearly marked. Such snippets are not part of the notebook; they only display the state "
     "created by the notebook code.")

prog("PROGRAM 1 — LOAD DATASET", [code(2)],
     [(OUT["p1"], "Output of the Dataset Availability Check")],
     ["**What it does:** the program checks whether the file ai_ml_job_analysis.csv is present in the working directory. "
      "If it is missing and the notebook is running in Google Colab, it opens the Colab file-upload dialog; outside Colab the "
      "ImportError is ignored. The assert statement stops the notebook with a clear message if the file is still not found, "
      "and finally the message “Dataset ready” (with a green tick) is printed.",
      "**Why it is required:** every later cell reads this file. Checking early gives a clear error message instead of a "
      "confusing failure later. In this run the file was already present, so no upload was needed."])

prog("PROGRAM 2 — LOAD AND DISPLAY DATA", [code(3)],
     [(OUT["p2"], "Dataset Preview – output of df.head() (11 columns shown in three parts for readability)")],
     ["**What it does:** the cell imports NumPy, Pandas, Matplotlib and Seaborn, sets the Seaborn style to “whitegrid” "
      "and the default figure size to 10 × 6 inches. pd.read_csv('ai_ml_job_analysis.csv') reads the CSV file into a "
      "DataFrame named df. df.head() displays the first five rows (index 0 to 4).",
      "**What head() does:** it returns the first n rows of a DataFrame (n = 5 by default). It is used for a quick look at the "
      "column names, the kind of values and the format of the data.",
      "In the notebook, df.head() is shown as one wide table. Here it is split into three parts only so that the text stays "
      "readable on an A4 page; the rows and values are exactly the same."])

prog("PROGRAM 3 — DATASET SHAPE AND INFORMATION", [code(5)],
     [(OUT["p3"], "Output of df.shape and df.info()")],
     ["**Number of rows and columns:** df.shape returned (500, 11), i.e. 500 rows and 11 columns.",
      "**Data types:** df.info() lists each column with its non-null count and data type: ID, Skill Count and Salary (USD) are "
      "int64, Experience (Years) is float64 and the other seven columns are object (text).",
      "**Non-null counts:** all columns have 500 non-null values except Certification, which has 334 (explained in Program 4).",
      "**Memory information:** df.info() reported “memory usage: 43.1+ KB”, the approximate memory used by the DataFrame "
      "(the “+” means the memory of the text values is a lower estimate).",
      "This step confirms that the file was read correctly and shows which columns need encoding."])

prog("PROGRAM 4 — CHECK MISSING VALUES", [code(7)],
     [(OUT["p4"], "Output of df.isnull().sum()")],
     ["**What it does:** df.isnull() marks every missing cell as True; .sum() adds up the True values of each column and so "
      "gives the number of missing values per column.",
      f"**Result:** ten columns have 0 missing values. Certification shows {N_NAN} missing values (334 non-null + {N_NAN} = 500).",
      f"**Interpretation:** the original CSV contains the word “None” in {N_NONE} Certification cells, meaning the "
      "person has no certification. read_csv automatically treats “None” as missing, hence the count. These are therefore "
      "not real data gaps.",
      "**Why checking is important:** most machine-learning algorithms cannot handle missing values, and missing values can "
      "bias results. Checking them before training shows whether cleaning (dropping or filling) is needed. In this project "
      "the notebook converts the column to text with astype(str) during label encoding, so these entries become the "
      "category “nan” and no row is lost."])

# ---- Program 5: EDA
H2("PROGRAM 5 — EXPLORATORY DATA ANALYSIS", True)
P("Exploratory Data Analysis (EDA) means studying the data with statistics and graphs before building a model. The notebook "
  "performs five EDA steps, shown below as Programs 5.1 to 5.5. (In the notebook, the statistical summary, Program 5.1, "
  "comes before the missing-value check of Program 4.)")
sub("PROGRAM 5.1 — Statistical Summary", code(6),
    [(OUT["p5_desc"], "Output of df.describe(include='all').T (shown in three parts)")],
    ["**What it does:** describe(include='all') summarises every column: count, unique, top and freq for text columns and "
     "count, mean, std, min, quartiles and max for numeric columns. .T transposes the table so that each column of the dataset "
     "is one row.",
     f"**Key observations:** Salary (USD) ranges from {usd0(sd['min'])} to {usd0(sd['max'])} with a mean of {usd(sd['mean'])}, a "
     f"median of {usd0(sd['50%'])} and a standard deviation of {usd(sd['std'])}. Experience (Years) ranges from "
     f"{DF['Experience (Years)'].min():.1f} to {DF['Experience (Years)'].max():.1f} years (mean {DF['Experience (Years)'].mean():.2f}) and Skill Count from "
     f"{DF['Skill Count'].min()} to {DF['Skill Count'].max()} (mean {DF['Skill Count'].mean():.2f}). The text columns have "
     f"{DF['Job Title'].nunique()} job titles, {DF['Industry'].nunique()} industries, {DF['Company'].nunique()} companies and "
     f"{DF['Location'].nunique()} locations."], new=False)
sub("PROGRAM 5.2 — Salary Distribution", code(8),
    [(fig_of(8), "Salary Distribution (histogram with density curve)", 14.5)],
    ["**What it does:** sns.histplot draws a histogram of the target variable with 30 bins and a smooth KDE (density) curve.",
     "**Observation:** the distribution does not have a single bell shape. There is a high peak between roughly 30,000 and "
     "55,000 USD and a second, broader group between roughly 85,000 and 190,000 USD, with few salaries above 200,000 USD. It "
     "is therefore a two-group (bimodal) distribution. Program 5.5 and Section 9.1 show what separates the groups."])
sub("PROGRAM 5.3 — Correlation Analysis", code(9),
    [(fig_of(9), "Correlation Heatmap (numeric features)", 10.5)],
    ["**What it does:** the numeric columns (without ID) are selected, their correlation matrix is calculated and shown as an "
     "annotated heatmap. Correlation ranges from −1 (perfect negative) through 0 (none) to +1 (perfect positive) and measures "
     "linear association only.",
     f"**Observation:** Experience (Years) has a correlation of {corr['Salary (USD)']['Experience (Years)']:.2f} with Salary and Skill Count "
     f"has {corr['Salary (USD)']['Skill Count']:.2f}. Experience and Skill Count are almost uncorrelated with each other "
     f"({corr['Skill Count']['Experience (Years)']:.2f}). Both numeric features therefore have a positive linear relationship with "
     "salary, moderate for Experience and weak for Skill Count. The other factors are categorical and are not part of this matrix."])
sub("PROGRAM 5.4 — Salary by Categorical Features", code(10),
    [(fig_of(10), "Salary by Education, Remote Work, Job Title and Industry (box plots)", 16.2)],
    ["**What it does:** four box plots compare the salary distribution across Education, Remote Work type, Job Title (ordered "
     "by how often each title occurs) and Industry. Each box shows the middle 50% of salaries, the line inside is the median, "
     "and the whiskers show the range.",
     "**Observations:** the median salary is lowest for Bachelors and highest for PhD, with Masters in between. The three "
     "Remote Work groups have similar medians and spreads. “Research Intern” has clearly lower salaries than all other job "
     "titles. Industries differ in their medians, but their boxes overlap a lot. In every group the salaries spread widely, "
     "which shows that no single one of these four columns explains salary alone."])
sub("PROGRAM 5.5 — Experience vs Salary", code(11),
    [(fig_of(11), "Experience vs Salary (coloured by Education)", 14.5)],
    ["**What it does:** a scatter plot of Experience (Years) against Salary (USD), with each point coloured by Education.",
     "**Observation:** salary tends to rise with experience, which agrees with the positive correlation. The points form two "
     "separate bands: a lower band (roughly 10,000–65,000 USD) that rises slowly with experience and an upper band (roughly "
     "60,000–215,000 USD) that is wider and rises more strongly. The Education colours are mixed inside both bands, so "
     "Education is not what separates them. Section 9.1 checks the Location column for the cause."])
