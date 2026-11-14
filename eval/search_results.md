# Day 7 - Semantic Search Evaluation

Retrieval evaluation using the AQIExplainer ChromaDB collection.

Top 3 results are recorded for each question.

## Question 1: What is the AQI of Nagpur?

### Result 1
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-17
- **Similarity:** 0.719
- **Retrieved text:** city: Nagpur | bulletin_date: 2026-11-06 | aqi_value: 153 | aqi_category: Moderate | prominent_pollutant: PM2.5 | stations_reporting: 4/4

### Result 2
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-20
- **Similarity:** 0.4934
- **Retrieved text:** city: Pune | bulletin_date: 2026-11-06 | aqi_value: 134 | aqi_category: Moderate | prominent_pollutant: PM2.5, PM10 | stations_reporting: 7/9

### Result 3
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-19
- **Similarity:** 0.469
- **Retrieved text:** city: Navi Mumbai | bulletin_date: 2026-11-06 | aqi_value: 128 | aqi_category: Moderate | prominent_pollutant: PM2.5, PM10 | stations_reporting: 6/8

**Manual relevance assessment:** To be reviewed.

## Question 2: Which city has poor air quality?

### Result 1
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 15
- **Similarity:** 0.5985
- **Retrieved text:** Air Quality Index on Nov 06, 2026 @ 4 PM (Average of past 24 hours) * Cities absent in AQI Bulletin due to insufficient data: 1) Ariyalur, 2) Bathinda, 3) Bidar, 4) Bihar Sharif, 5) Chamarajanagar, 6) Chengalpattu, 7) Coimbatore, 8) Dhanbad, 9) Dindigul, 10) Ernakulam, 11) Fatehpur Sikri, 12) Gadag, 13) Guntur, 14) Hapur, 15) Hassan, 16) Haveri, 17) Hosur, 18) Imphal, 19) Kaithal, 20) Kanchipuram, 21) Karur, 22) Karwar, 23) Kashipur, 24) Katihar, 25) Kishanganj, 26) Kochi, 27) Kollam, 28) Kozhik

### Result 2
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 15
- **Similarity:** 0.5437
- **Retrieved text:** , 46) Sri Vijaya Puram, 47) Thanjavur, 48) Tiruchirappalli, 49) Tirunelveli, 50) Tirupur, 51) Tumakuru, 52) Vellore, 53) Virudhunagar Notes: * In case of a city with multiple monitoring locations, average value is used to indicate air quality. Air quality may show variations across locations, and averaging is not a scientifically sound approach. However, for the sake of simplicity this method is being followed. For AQI of monitoring locations, website (http://cpcb.gov.in) may be referred. * The 

### Result 3
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 6
- **Similarity:** 0.5114
- **Retrieved text:** Air Quality Index on Nov 06, 2026 @ 4 PM (Average of past 24 hours) S.No City Air Quality Index Value Prominent Pollutant No. of Stations Participated/ Total Stations 101 Gaya Moderate 166 PM2.5, PM10 3/3 102 Ghaziabad Poor 257 PM2.5 7/8 103 Gopalganj Poor 240 PM2.5 1/1 104 Gorakhpur Satisfactory 94 PM10 1/1 105 Greater noida Very Poor 316 PM2.5 5/5 106 Gummidipoondi Moderate 158 PM2.5 1/1 107 Gurugram Very Poor 368 PM2.5 4/4 108 Guwahati Moderate 101 PM2.5, SO2 3/4 109 Gwalior Poor 247 PM2.5, P

**Manual relevance assessment:** To be reviewed.

## Question 3: What is PM2.5?

### Result 1
- **Title:** About AQI
- **Source:** `data\raw\About_AQI.pdf`
- **Page/row:** 1
- **Similarity:** 0.3812
- **Retrieved text:** cribed. 3. Based on the measured ambient concentrations of a pollutant, sub-index is calculated, which is a linear function of concentration (e.g. the sub-index for PM2.5 will be 51 at concentration 31 µg/m3, 100 at concentration 60 µg/m3, and 75 at concentration of 45 µg/m3). The worst sub-index determines the overall AQI. AQI categories and health breakpoints for the eight pollutants are as follow: AQI Category AQI Concentration Range* PM10 PM2.5 NO2 O3 CO SO2 NH3 Pb Good 0-50 0-50 0-30 0–40 0

### Result 2
- **Title:** About AQI
- **Source:** `data\raw\About_AQI.pdf`
- **Page/row:** 1
- **Similarity:** 0.3654
- **Retrieved text:** 800 801-1200 2.1-3.0 Very Poor 301–400 351-430 121-250 281-400 209-748* 17-34 801-1600 1200-1800 3.1-3.5 Severe 401-500 430+ 250+ 400+ 748+* 34+ 1600+ 1800+ 3.5+ * CO in mg/m3 and other pollutants in µg/m3; 24-hourly average values for PM10, PM2.5, NO2, SO2, NH3, and Pb, and 8-hourly values for CO and O3.

### Result 3
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-18
- **Similarity:** 0.3574
- **Retrieved text:** city: Nashik | bulletin_date: 2026-11-06 | aqi_value: 158 | aqi_category: Moderate | prominent_pollutant: PM2.5, PM10 | stations_reporting: 4/4

**Manual relevance assessment:** To be reviewed.

## Question 4: What does Severe AQI mean?

### Result 1
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 15
- **Similarity:** 0.5329
- **Retrieved text:** or AQI Categories AQI Category Color Code Possible Health Impacts 0-50 Good Minimal Impact 51-100 Satisfactory Minor breathing discomfort to sensitive people 101-200 Moderate Breathing discomfort to the people with lungs, asthma and heart diseases 201-300 Poor Breathing discomfort to most people on prolonged exposure 301-400 Very Poor Respiratory illness on prolonged exposure 401-500 Severe Affects healthy people and seriously impacts those with existing diseases

### Result 2
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 15
- **Similarity:** 0.4819
- **Retrieved text:** , 46) Sri Vijaya Puram, 47) Thanjavur, 48) Tiruchirappalli, 49) Tirunelveli, 50) Tirupur, 51) Tumakuru, 52) Vellore, 53) Virudhunagar Notes: * In case of a city with multiple monitoring locations, average value is used to indicate air quality. Air quality may show variations across locations, and averaging is not a scientifically sound approach. However, for the sake of simplicity this method is being followed. For AQI of monitoring locations, website (http://cpcb.gov.in) may be referred. * The 

### Result 3
- **Title:** About AQI
- **Source:** `data\raw\About_AQI.pdf`
- **Page/row:** 1
- **Similarity:** 0.4352
- **Retrieved text:** cribed. 3. Based on the measured ambient concentrations of a pollutant, sub-index is calculated, which is a linear function of concentration (e.g. the sub-index for PM2.5 will be 51 at concentration 31 µg/m3, 100 at concentration 60 µg/m3, and 75 at concentration of 45 µg/m3). The worst sub-index determines the overall AQI. AQI categories and health breakpoints for the eight pollutants are as follow: AQI Category AQI Concentration Range* PM10 PM2.5 NO2 O3 CO SO2 NH3 Pb Good 0-50 0-50 0-30 0–40 0

**Manual relevance assessment:** To be reviewed.

## Question 5: Which city has the highest AQI?

### Result 1
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 15
- **Similarity:** 0.5174
- **Retrieved text:** , 46) Sri Vijaya Puram, 47) Thanjavur, 48) Tiruchirappalli, 49) Tirunelveli, 50) Tirupur, 51) Tumakuru, 52) Vellore, 53) Virudhunagar Notes: * In case of a city with multiple monitoring locations, average value is used to indicate air quality. Air quality may show variations across locations, and averaging is not a scientifically sound approach. However, for the sake of simplicity this method is being followed. For AQI of monitoring locations, website (http://cpcb.gov.in) may be referred. * The 

### Result 2
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-8
- **Similarity:** 0.5138
- **Retrieved text:** city: Bhiwandi | bulletin_date: 2026-11-06 | aqi_value: 126 | aqi_category: Moderate | prominent_pollutant: PM10 | stations_reporting: 1/1

### Result 3
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-10
- **Similarity:** 0.4785
- **Retrieved text:** city: Chandrapur | bulletin_date: 2026-11-06 | aqi_value: 134 | aqi_category: Moderate | prominent_pollutant: PM10 | stations_reporting: 2/2

**Manual relevance assessment:** To be reviewed.

## Question 6: How has AQI of Pune changed over the last 30 days?

### Result 1
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-20
- **Similarity:** 0.6206
- **Retrieved text:** city: Pune | bulletin_date: 2026-11-06 | aqi_value: 134 | aqi_category: Moderate | prominent_pollutant: PM2.5, PM10 | stations_reporting: 7/9

### Result 2
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-5
- **Similarity:** 0.4713
- **Retrieved text:** city: Aurangabad (Maharashtra) | bulletin_date: 2026-11-06 | aqi_value: 91 | aqi_category: Satisfactory | prominent_pollutant: O3, PM10, PM2.5 | stations_reporting: 3/3

### Result 3
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 6
- **Similarity:** 0.451
- **Retrieved text:** 1/2 117 Hyderabad Satisfactory 60 PM10 14/14 118 Indore Moderate 124 PM10, PM2.5 5/6 119 Jabalpur Moderate 106 PM10, O3 3/4 120 Jaipur Poor 207 PM2.5, PM10 6/6

**Manual relevance assessment:** To be reviewed.

## Question 7: Which cities have Moderate AQI?

### Result 1
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-8
- **Similarity:** 0.5973
- **Retrieved text:** city: Bhiwandi | bulletin_date: 2026-11-06 | aqi_value: 126 | aqi_category: Moderate | prominent_pollutant: PM10 | stations_reporting: 1/1

### Result 2
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 15
- **Similarity:** 0.5806
- **Retrieved text:** , 46) Sri Vijaya Puram, 47) Thanjavur, 48) Tiruchirappalli, 49) Tirunelveli, 50) Tirupur, 51) Tumakuru, 52) Vellore, 53) Virudhunagar Notes: * In case of a city with multiple monitoring locations, average value is used to indicate air quality. Air quality may show variations across locations, and averaging is not a scientifically sound approach. However, for the sake of simplicity this method is being followed. For AQI of monitoring locations, website (http://cpcb.gov.in) may be referred. * The 

### Result 3
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-13
- **Similarity:** 0.5454
- **Retrieved text:** city: Jalgaon | bulletin_date: 2026-11-06 | aqi_value: 118 | aqi_category: Moderate | prominent_pollutant: PM10 | stations_reporting: 1/1

**Manual relevance assessment:** To be reviewed.

## Question 8: What is the prominent pollutant in Mumbai?

### Result 1
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-16
- **Similarity:** 0.6554
- **Retrieved text:** city: Mumbai | bulletin_date: 2026-11-06 | aqi_value: 102 | aqi_category: Moderate | prominent_pollutant: PM10, PM2.5 | stations_reporting: 24/26

### Result 2
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-19
- **Similarity:** 0.5948
- **Retrieved text:** city: Navi Mumbai | bulletin_date: 2026-11-06 | aqi_value: 128 | aqi_category: Moderate | prominent_pollutant: PM2.5, PM10 | stations_reporting: 6/8

### Result 3
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-20
- **Similarity:** 0.5359
- **Retrieved text:** city: Pune | bulletin_date: 2026-11-06 | aqi_value: 134 | aqi_category: Moderate | prominent_pollutant: PM2.5, PM10 | stations_reporting: 7/9

**Manual relevance assessment:** To be reviewed.

## Question 9: How many monitoring stations reported data for Pune?

### Result 1
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-20
- **Similarity:** 0.6871
- **Retrieved text:** city: Pune | bulletin_date: 2026-11-06 | aqi_value: 134 | aqi_category: Moderate | prominent_pollutant: PM2.5, PM10 | stations_reporting: 7/9

### Result 2
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-17
- **Similarity:** 0.5397
- **Retrieved text:** city: Nagpur | bulletin_date: 2026-11-06 | aqi_value: 153 | aqi_category: Moderate | prominent_pollutant: PM2.5 | stations_reporting: 4/4

### Result 3
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-18
- **Similarity:** 0.5295
- **Retrieved text:** city: Nashik | bulletin_date: 2026-11-06 | aqi_value: 158 | aqi_category: Moderate | prominent_pollutant: PM2.5, PM10 | stations_reporting: 4/4

**Manual relevance assessment:** To be reviewed.

## Question 10: Which city has the lowest AQI?

### Result 1
- **Title:** AQI Bulletin 20261106
- **Source:** `data\raw\AQI_Bulletin_20261106.pdf`
- **Page/row:** 15
- **Similarity:** 0.4917
- **Retrieved text:** , 46) Sri Vijaya Puram, 47) Thanjavur, 48) Tiruchirappalli, 49) Tirunelveli, 50) Tirupur, 51) Tumakuru, 52) Vellore, 53) Virudhunagar Notes: * In case of a city with multiple monitoring locations, average value is used to indicate air quality. Air quality may show variations across locations, and averaging is not a scientifically sound approach. However, for the sake of simplicity this method is being followed. For AQI of monitoring locations, website (http://cpcb.gov.in) may be referred. * The 

### Result 2
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-8
- **Similarity:** 0.4904
- **Retrieved text:** city: Bhiwandi | bulletin_date: 2026-11-06 | aqi_value: 126 | aqi_category: Moderate | prominent_pollutant: PM10 | stations_reporting: 1/1

### Result 3
- **Title:** aqi data
- **Source:** `data\raw\aqi_data.csv`
- **Page/row:** row-15
- **Similarity:** 0.4547
- **Retrieved text:** city: Latur | bulletin_date: 2026-11-06 | aqi_value: 50 | aqi_category: Good | prominent_pollutant: PM10 | stations_reporting: 1/1

**Manual relevance assessment:** To be reviewed.
