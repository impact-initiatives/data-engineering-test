# Data Engineering Take-Home Test

## Exercise Guidelines
*   **Evaluation:** We value a complete README and explanation of trade-offs and design decisions more than a 100% finished implementation if you run out of time.
*   **Use of AI Tools:** Generative AI tools (e.g., ChatGPT, Claude) are permitted as aids for brainstorming, debugging, or understanding concepts. However, using them to automatically generate complete solutions or answers to this exercise will result in disqualification. We expect authentic work that demonstrates your own technical reasoning and decision-making.

---

## 1. Setup & Context

### The scenario
We use KoboToolbox as our data collection platform. Field teams design surveys, deploy them, and collect responses in the field. Your task is to build a data pipeline that ingests this data from the Kobo API into a local database to support operational monitoring and reporting.

**Understanding the data structure:**

The KoboToolbox API exposes several types of information organized hierarchically:
*   **Survey projects** - Each survey project has metadata such as unique identifier (`uid`), deployment status, submission count, and timestamps.
*   **Survey structure** - Each project has a defined questionnaire structure (questions, field types, response options, etc.).
*   **Survey responses** - Each project collects responses from the field (the actual answers submitted by enumerators).

These are exposed through different API endpoints with parent-child relationships.

### The starter code
The provided `main.py` implements a working `dlt` pipeline with the following configuration:

1.  **Authentication**: Kobo API connection using token-based authentication (token provided via email).
2.  **Two `dlt` resources**:
    *   `assets` - Ingests survey project metadata via the `assets/` endpoint.
    *   `content` - Ingests survey structure via the `assets/{uid}/content` endpoint (child resource of `assets`).
3.  **Database**: Loads data into a local `kobo_de.duckdb`.

**Running the starter:**
Run `main.py` to verify your environment is correctly configured (see `README.md` for setup instructions). Dependencies are managed with `uv`, though any Python package manager is acceptable.

**Note on implementation approach:**
The exercise assumes use of `dlt` for declarative pipeline configuration. If framework limitations block progress, you may implement a custom Python extraction script that achieves equivalent functionality (robust ingestion with proper error handling). Document your approach and trade-offs in the README.

### Useful Documentation
*   **dlt REST API Source:** [Configuration Guide](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api)
*   **KoboToolbox API v2:** [API Documentation](https://kobo.impact-initiatives.org/api/v2/docs/) - *All endpoints can be tested directly from this interface.*
*   **dlt Dependent Resources:** [Rest API: Child Resources (Declarative)](https://dlthub.com/docs/dlt-ecosystem/verified-sources/rest_api/basic#define-resource-relationships)
*   **DuckDB:** [SQL Introduction](https://duckdb.org/docs/sql/introduction)

---

## 2. Tasks

### Phase 1: Ingestion
Extend the pipeline to ingest survey responses.

**Requirements:**
1.  **Identify the API endpoint**: Consult the Kobo API documentation to find the endpoint that returns submission data for a specific asset.
2.  **Add a `submissions` dlt resource to the pipeline**: Configure it as a child resource of assets in the pipeline. Use `_id` as the primary key and ensure the `data_selector` is properly configured based on where the submission records are nested in the API response structure.
3.  **Validate the ingestion**: Run the pipeline and verify that submission data loads into DuckDB with proper relationships to parent assets.
4.  **Analyze the resulting data model**: Analyze the data model produced by the ingestion process. Keep it concise and address only:
* Nested JSON handling: explain, at a high level, how nested fields are represented, with a clear focus on how table names are generated for nested objects and arrays (e.g., parent-based prefixes, path-derived names, or hierarchical naming).
* Table relationships: identify primary keys and foreign keys (explicit or implied) and the main join paths between tables.

The expectation is to describe the process by which the data is structured, not individual keys or tables.

**Implementation notes:**
*   Leverage `dlt`'s automatic schema evolution to handle nested JSON structures in submissions. If using a custom extraction approach, you will need to implement this logic manually.

### Phase 2: Transformation & reporting
Build a transformation layer that reads from the DuckDB tables and produces analytical metrics for operational monitoring.

**Scenario:**
You are a Data Specialist at the NGO headquarters tasked with analyzing data collections stored on the Kobo server. Your focus is on metrics related to data collection progress and field operations, examining them through multiple analytical dimensions: geography, survey type, and enumerator performance.

**Data context:**
For security reasons, the data accessible for this test is simulated. Expect inconsistencies and values that may not make logical sense. 

**Requirements:**
1.  **Implement the following baseline metrics:**
    *   **Submission velocity:** Average number of submissions per day for each survey
    *   **Geographic coverage:** Identify the country that appears in 5 different surveys, then provide a breakdown of submissions by administrative level 1 (admin1) and survey type (e.g., Education, WASH, Nutrition, etc.) for that country
    *   **Enumerator performance:** For each survey, identify the top 3 enumerators whose average submission duration is furthest below the survey median duration
    *   **Submission duration distribution:** Visual comparison of submission duration distributions across all surveys (e.g., boxplot)

2.  **Additional analysis (optional):**
    You are encouraged to explore additional analytical dimensions. Example areas (or propose alternatives based on your data exploration):
    *   Visualization demonstrating that GPS coordinates across surveys are randomly generated
    *   Survey complexity analysis: relationship between questionnaire length and average submission duration
 
    
    Document your rationale and explain relevance to the operational monitoring context. Implementation is optional but the analytical reasoning should be documented in your README.

3.  **Output format:** Present your metrics using appropriate format(s). At least, we expect tabular outputs (CSV, database views) for numeric results, static visualizations (charts, graphs) otherwise. Interactive implementations (Streamlit, Plotly Dash) will be positively considered.

**Implementation notes:**
*   Use the survey collection timestamps (`start`, `end`, `today`) for temporal calculations, not `_submission_time` (which reflects server upload time).
*   If you were unable to complete Phase 1 (submission data ingestion), you may proceed with Phase 2 using the existing `assets` and `content` resources. In this case, develop metrics that you consider relevant based on the available data and document your analytical approach in the README.

### Phase 3: Written Analysis & Documentation
In your `README.md`, please address the following (bullet points preferred).

**A. Pipeline Logic:**
*   **Incremental Loading:** Explore the ingested data for the `assets` endpoint. Identify which field(s) would be suitable candidates for incremental loading cursors. Explain your choice, why incremental loading is necessary in a production context, and how you would handle potential updates to existing records vs. new appends.

**B. Performance & Scalability:**
*   **Scenario:** The pipeline works well for the test dataset, but when scaling up to production with the full historical data across all surveys, you observe that the ingestion process takes progressively longer as it runs, occasionally times out, and sometimes fails on specific surveys. Restarting from the beginning each time is becoming impractical.
*   **Question:** Walk us through your diagnostic approach step by step. How would you systematically identify where the bottleneck lies? Once you've identified the root cause(s), what strategies would you implement to ensure the backfill can complete reliably and efficiently?

**C. Data Governance & Access Control:**
*   **Scenario:** The warehouse now contains data from 3K+ survey projects. Each project can have different PII fields (phone numbers in some, GPS coordinates in others, beneficiary names in others), and Kobo enforces project-level access permissions that restrict which users can view which surveys. Currently, the warehouse grants uniform access to all ingested data, and **manually** replicating Kobo's permission model for thousands of surveys is impractical.
*   **Question:** How would you design a scalable governance strategy for the warehouse? Consider both technical architecture and operational maintainability.

**D. Adoption:**
*   **Scenario:** The data warehouse is live and accurate, yet stakeholders continue to rely on manual Excel workflows because they feel the new system limits their flexibility compared to spreadsheets.
*   **Question:** As a senior engineer without direct authority, how do you address this friction? Describe specific technical or process strategies you would use to demonstrate value and drive migration to the new platform.

---

## Deliverables
Submit a GitHub repository containing:
1.  **Source Code:** Working ingestion pipeline and transformation/reporting implementation.
2.  **README.md:**
    *   Instructions to run the project.
    *   Project structure: Brief explanation of how the different components (scripts, notebooks, applications, analysis reports, datasets) are organized to facilitate review and navigation.
    *   Data model analysis from Phase 1.
    *   Explanation of your Phase 2 metrics implementation and rationale for any optional analysis performed.
    *   Answers to the Phase 3 questions.

**Notes:** 
*   The repository should be runnable by the reviewer following your README instructions.
*   Code quality will be evaluated. Implementation of good practices, even basic ones (e.g., logging, error handling, comments), will be considered positively.
