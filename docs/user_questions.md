# AQIExplainer – 10 Real User Questions

These questions represent the kind of questions a user may ask while exploring Maharashtra's air quality information.

1. What is the AQI of Aurangabad?
2. Which city has poor air quality?
3. What is PM2.5?
4. What does Severe AQI mean?
5. Which city has the highest AQI in the available records?
6. How has the AQI of Pune changed over the last 30 days?
7. Which cities have Moderate AQI?
8. What is the prominent pollutant reported in Mumbai?
9. How many monitoring stations reported data for Pune?
10. Which city has the lowest AQI in the available records?

## Question Support Check

| Question | Can current dataset answer it? |
|---|---|
| Q1 | Yes – city AQI lookup |
| Q2 | Yes – AQI category lookup |
| Q3 | No – pollutant definition is not stored in the dataset |
| Q4 | No – category explanation is not stored in the dataset |
| Q5 | Yes – highest AQI calculation |
| Q6 | **No – historical data for the last 30 days is unavailable** |
| Q7 | Yes – category search |
| Q8 | Yes – prominent pollutant field |
| Q9 | Yes – stations reporting field |
| Q10 | Yes – lowest AQI calculation |

**Important:** Q6 is intentionally unanswerable using the current dataset because AQIExplainer contains records from one daily bulletin, not 30 days of historical records.

The current `/questions` endpoint may not understand every question above. The table describes whether the underlying data contains the information, not whether the current question-answering logic already supports every wording.