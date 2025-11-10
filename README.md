# okra
Classification of Okra  Maturity Using Thermal Images and Deep Learning                                                                                                                 
This project aims to automate the **classification of okra pods** based on their **maturity level** using **thermal imaging** and **deep learning models** such as **EfficientNet**, **MobileNet**, and **VGG19**.  
The proposed system offers a **non-destructive, accurate, and efficient solution** for post-harvest grading and quality control, helping farmers and distributors improve product quality and reduce waste.
Okra maturity directly affects its edibility and market value —
immature pods are tender and desirable,while over-mature pods become fibrous.
Traditional manual grading is subjective and time-consuming, which makes **AI-based thermal analysis** a powerful alternative.

okra-maturity-classification/
│
├── Okra_Dataset/
│ ├── adequate_matured_Okra/
│ ├── over_matured_Okra/
│   
│
├── models/
│ ├── okra.ipynb
│
├── utils/
│ ├── run.py
│ └── test.py
│ └── app.py
├── results/
│ ├── accuracy_curve.png/
│ ├── gradcam_results
│ └──gradcam_report
│
└── README.md
