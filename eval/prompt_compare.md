# AQIExplainer – Prompt Comparison Evaluation

## 1. Objective

The objective of this evaluation is to compare two prompt versions used by AQIExplainer.

- **Prompt Version 1:** Basic instructions for answering AQI questions.
- **Prompt Version 2:** Detailed instructions with dataset grounding, missing-data handling, and confidence guidelines.

Both prompts are tested using the same 10 AQIExplainer user questions.

## 2. Evaluation Criteria

Each prompt is evaluated using these criteria:

1. **Accuracy:** Does the response provide correct information?
2. **Data Grounding:** Does it use the available AQI records?
3. **Hallucination Control:** Does it avoid inventing missing information?
4. **Clarity:** Is the answer easy to understand?
5. **Follow-up Quality:** Does it suggest a useful next question?

Score each criterion from 1 to 5.

## 3. Prompt Versions

### Version 1 – Basic Prompt

- Answer the user's AQI-related question.
- Use the supplied AQI records when relevant.
- Keep the answer short and simple.
- If information is unavailable, say so.
- Return answer, confidence, and follow-up in JSON.

### Version 2 – Improved Prompt

- Identify what information the user is requesting.
- Use actual AQI records for city-specific facts.
- Do not invent historical trends or missing values.
- Explain missing information clearly.
- Distinguish general AQI knowledge from dataset facts.
- Assign confidence based on the available evidence.
- Return valid JSON with the required fields.

## 4. Ten-Question Evaluation

Use the same questions for both prompt versions.

| No. | User Question | Expected Evaluation |
|---|---|---|
| Q1 | What is the AQI of Nagpur? | Check the value against the dataset. |
| Q2 | Which city has poor air quality? | Check category-based results. |
| Q3 | What is PM2.5? | Check whether the explanation is correct. |
| Q4 | What does Severe AQI mean? | Check whether the category is explained correctly. |
| Q5 | Which city has the highest AQI? | Check the highest value against the dataset. |
| Q6 | How has the AQI of Pune changed over the last 30 days? | Must identify that historical data is unavailable. |
| Q7 | Which cities have Moderate AQI? | Check the matching city records. |
| Q8 | What is the prominent pollutant reported in Mumbai? | Check the pollutant field. |
| Q9 | How many monitoring stations reported data for Pune? | Check the stations reporting field. |
| Q10 | Which city has the lowest AQI? | Check the lowest value against the dataset. |

## 5. Results Recording

Run each question twice:
- First with `prompt_version` set to `v1`.
- Then with `prompt_version` set to `v2`.

Record the results below.

| Question | V1 Score / 5 | V2 Score / 5 | Better Version |
|---|---:|---:|---|
| Q1 | ___ | ___ | ___ |
| Q2 | ___ | ___ | ___ |
| Q3 | ___ | ___ | ___ |
| Q4 | ___ | ___ | ___ |
| Q5 | ___ | ___ | ___ |
| Q6 | ___ | ___ | ___ |
| Q7 | ___ | ___ | ___ |
| Q8 | ___ | ___ | ___ |
| Q9 | ___ | ___ | ___ |
| Q10 | ___ | ___ | ___ |
| **Total** | **___ / 50** | **___ / 50** | **___** |

## 6. Comparison and Conclusion

Prompt Version 1 provides basic instructions and is useful as a baseline.

Prompt Version 2 provides more detailed instructions for using the dataset, handling missing information, and controlling unsupported answers.

The expected advantage of Version 2 is better data grounding and clearer handling of questions that cannot be answered using the available records.

The final conclusion should be written after testing both versions against all 10 questions and recording the actual scores.

## 7. Evaluation Limitation

The AQI dataset currently contains records from one daily bulletin. Therefore, questions requiring historical trends, such as Q6, cannot be answered using the current dataset.

A correct response should explain this limitation instead of inventing historical AQI values.