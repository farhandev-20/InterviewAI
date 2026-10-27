"""
Full Question Bank Builder for InterviewAI - Part 3
Roles 7-9 + All Roles:
7. Data Analyst
8. Machine Learning Engineer
9. HR Interview
10. All Roles (Universal questions)
5+ curated questions per focus type across Easy, Medium, Hard.
"""

PART3_ENTRIES = []

def q(role, focus, diff, topic, question, answer):
    PART3_ENTRIES.append({
        "role": role,
        "type": focus,
        "difficulty": diff,
        "topic": topic,
        "question": question,
        "sample_answer": answer
    })

# ==============================================================================
# 7. DATA ANALYST
# ==============================================================================
# Technical (8 questions)
q("Data Analyst", "Technical Interview", "Easy", "SQL Aggregation & Filtering",
  "Explain the difference between WHERE and HAVING clauses in SQL, and when each must be used.",
  "WHERE filters individual rows before any grouping or aggregation takes place; it cannot reference aggregate functions like SUM() or AVG(). HAVING filters grouped summary rows after the GROUP BY clause has executed and is used specifically to filter on aggregate calculations (e.g. HAVING COUNT(*) > 5).")
q("Data Analyst", "Technical Interview", "Easy", "Data Cleaning with Pandas",
  "How do you handle missing (NaN) values and deduplicate data in Pandas, and what are the trade-offs between imputation and dropping rows?",
  "In Pandas, identify missing data using isna().sum(). Rows can be dropped with dropna(), or imputed using fillna() with mean, median, mode, or forward-fill (ffill). Dropping rows loses sample size and can introduce selection bias if data is not missing completely at random. Imputation preserves row counts but can artificially reduce variance or distort correlations.")
q("Data Analyst", "Technical Interview", "Easy", "Data Visualization Choices",
  "How do you decide between using a bar chart, line chart, scatter plot, and heatmap when communicating data insights?",
  "Use bar charts to compare discrete categorical metrics across groups. Use line charts to display continuous trends and seasonal patterns over time. Use scatter plots to investigate correlations between two continuous numerical variables. Use heatmaps to visualize high-dimensional matrices, correlation grids, or activity patterns across hours and days.")
q("Data Analyst", "Technical Interview", "Medium", "SQL Window Functions",
  "Explain how SQL Window Functions (ROW_NUMBER, RANK, DENSE_RANK, LEAD, LAG) work and how the OVER(PARTITION BY ... ORDER BY ...) clause operates.",
  "Window functions perform calculations across a set of table rows related to the current row without collapsing the rows into a single group like GROUP BY does. ROW_NUMBER assigns a unique sequential integer. RANK assigns ranks with gaps for ties. DENSE_RANK ranks ties without skipping numbers. LEAD and LAG access data from following or preceding rows, ideal for calculating period-over-period growth rates.")
q("Data Analyst", "Technical Interview", "Medium", "A/B Testing & Statistical Significance",
  "How do you determine statistical significance in an A/B test, and what is the difference between p-value and statistical power?",
  "Statistical significance evaluates whether the difference in conversion between variant and control is unlikely to be due to random chance. The p-value is the probability of observing results at least as extreme assuming the null hypothesis is true (typically compared against alpha = 0.05). Statistical power (1 - beta, typically 0.80) is the probability of detecting a true effect when one exists, dictated by sample size and minimum detectable effect.")
q("Data Analyst", "Technical Interview", "Medium", "Data Warehouse Modeling",
  "Compare Star Schema versus Snowflake Schema in dimensional data modeling for business intelligence data marts.",
  "A Star Schema features a centralized fact table containing quantitative metrics surrounded by denormalized dimension tables, optimizing for fast query execution and simple BI tool joins. A Snowflake Schema normalizes dimension tables into sub-dimensions (e.g. splitting product category and brand), reducing data redundancy and storage at the cost of more complex multi-table joins in queries.")
q("Data Analyst", "Technical Interview", "Hard", "Query Optimization on Big Data Warehouses",
  "How do you diagnose and optimize expensive, slow-running analytical queries in BigQuery or Snowflake using partitioning and clustering?",
  "Inspect query execution graphs to detect full table scans, data shuffling spills, and join skew. In BigQuery or Snowflake, implement date or timestamp partitioning to prune scanned data volumes dramatically, reducing cost and latency. Apply clustering on high-cardinality filter and join columns (e.g. user_id, status) so query engines scan only relevant physical micro-partitions.")
q("Data Analyst", "Technical Interview", "Hard", "Attribution Modeling",
  "How do multi-touch attribution models (e.g. First-Touch, Last-Touch, Linear, Time-Decay, Data-Driven) influence marketing budget allocation?",
  "First-touch attributes 100% of conversion credit to top-of-funnel discovery channels, while last-touch credits the closing channel (often overvaluing branded search). Linear spreads credit evenly across all touchpoints. Time-decay gives progressive weight to interactions closer to conversion. Data-driven attribution uses algorithmic game theory (Shapley values) to objectively quantify the incremental lift contributed by each channel.")

# Behavioral (5 questions)
q("Data Analyst", "Behavioral Interview", "Easy", "Explaining Insights to Non-Technical Leaders",
  "Tell me about a time when you had to present complex analytical data to a non-technical executive. How did you structure your presentation?",
  "I was presenting churn analysis to the Chief Marketing Officer. Instead of diving into statistical formulas, I led with the executive bottom line: 'We are losing 14% of customers on month 2 due to onboarding drop-off, costing $120k ARR.' I used three clean charts, provided three actionable recommendations, and reserved technical methodology for the appendix.")
q("Data Analyst", "Behavioral Interview", "Easy", "Data Integrity Advocacy",
  "Tell me about a time when you had to push back on a team that was misinterpreting a metric to claim an unearned success.",
  "A growth team claimed a 50% spike in engagement by counting page refreshes as distinct sessions. I showed the raw session durations, explained the skew, and guided them to adopt unique daily active users as the true benchmark, protecting our executive reporting credibility.")
q("Data Analyst", "Behavioral Interview", "Medium", "Presenting Uncomfortable Findings",
  "Describe a situation where your data analysis revealed a conclusion that contradicted what business leadership wanted to hear. How did you present your findings?",
  "Leadership believed an expensive influencer campaign drove a spike in sales. My cohort analysis proved the spike was driven by an organic holiday discount, and the influencer traffic had a 90% bounce rate. I presented the findings objectively with side-by-side cohort retention graphs, framing it as an opportunity to reallocate budget into high-retention channels.")
q("Data Analyst", "Behavioral Interview", "Medium", "Collaborating with Data Engineers",
  "Tell me about a time when you worked with data engineers to fix an unreliable data pipeline. How did you coordinate the resolution?",
  "Our daily sales dashboard frequently lagged by 4 hours due to slow ETL transformations. I analyzed the upstream query bottlenecks, shared query profiling plans with the data engineering team, and helped redesign the aggregation table to use incremental materialized rollups.")
q("Data Analyst", "Behavioral Interview", "Hard", "Catching Critical Data Pipeline Bugs",
  "Tell me about a time when you discovered a critical bug in an upstream data pipeline that invalidated historical reports. How did you handle the situation?",
  "I noticed a sudden 20% discrepancy between our payment gateway settlement reports and internal database dashboards. I traced the issue to an upstream ETL job that was dropping timezone offsets. I immediately alerted the data engineering lead and CFO, documented the historical error margin, assisted in rebuilding the backfill pipeline, and established automated daily reconciliation tests.")

# Scenario Based (5 questions)
q("Data Analyst", "Scenario Based Interview", "Easy", "Daily Active Users Triage",
  "A product manager notices that daily active users (DAU) dropped 12% over the weekend. What is your immediate data triage checklist to investigate why?",
  "First, check if the drop is real or an instrumentation logging failure. Second, segment the drop by geography, platform (iOS, Android, Web), and user tier (new vs returning) to isolate the pocket of decline. Third, check external factors (holidays, server outages, app store release rollouts) against historical seasonal baselines.")
q("Data Analyst", "Scenario Based Interview", "Easy", "Sudden Data Spike Anomaly",
  "Your analytics dashboard reports an unprecedented 400% surge in user signups from a single geographic region overnight. How do you verify if this is authentic growth or bot spam?",
  "Inspect IP address ranges, email domain distribution (looking for disposable domains), and time-to-complete form metrics. If thousands of registrations occur from the same subnet with identical browser user-agents and zero subsequent engagement, it is automated spam; alert the security team immediately.")
q("Data Analyst", "Scenario Based Interview", "Medium", "Reconciling Conversion Discrepancies",
  "Marketing reports 2,500 campaign signups in Google Analytics, but your production database only shows 1,800 registered accounts. How do you reconcile the discrepancy?",
  "Audit definition discrepancies: Google Analytics may count client-side button click events or repeated attempts from the same visitor, while the database records unique, verified account activations. Check for drop-offs between form submission and email confirmation, bot traffic inflating GA hits, and client-side ad-blockers preventing analytics beacons.")
q("Data Analyst", "Scenario Based Interview", "Medium", "Data Drift in Scheduled Reports",
  "A scheduled weekly executive dashboard suddenly displays blank charts for two key product lines. What steps do you take to diagnose and communicate the issue?",
  "Check whether an upstream schema change altered column names or table partitions. Post an immediate notification to the executive channel acknowledging the display bug with an ETA, run the query manually in SQL with updated column mappings, and schedule automated schema-validation alerts in your pipeline.")
q("Data Analyst", "Scenario Based Interview", "Hard", "A/B Test Metric Trade-Off",
  "An A/B test for a new checkout flow shows a 6% increase in conversion rate, but average order value (AOV) dropped by 10%, reducing overall revenue. What is your recommendation?",
  "Do not launch the variant immediately despite the positive conversion headline. Analyze customer baskets to determine if the new flow promoted lower-priced impulse items while cannibalizing premium upsells. Recommend iterating on the variant to preserve checkout speed while restoring upsell visibility, running a follow-up test with statistical power focused on total revenue per visitor.")

# Problem Solving (5 questions)
q("Data Analyst", "Problem Solving Interview", "Easy", "Top N Customers by Region in SQL",
  "How would you write a SQL query to identify the top 3 highest spending customers in each geographic region from an orders table?",
  "Use a Common Table Expression (CTE) with DENSE_RANK() OVER (PARTITION BY region ORDER BY SUM(order_total) DESC) as rank_num, grouping by region and customer_id. In the outer query, filter WHERE rank_num <= 3, returning region, customer_id, and total spend in descending order.")
q("Data Analyst", "Problem Solving Interview", "Easy", "Calculating Month-over-Month Growth",
  "How would you calculate month-over-month (MoM) revenue growth percentage in SQL using the LAG() window function?",
  "Aggregate monthly revenue in a CTE using DATE_TRUNC('month', order_date). In the outer query, use LAG(revenue, 1) OVER (ORDER BY month) to fetch previous month's revenue, and compute: ROUND(100.0 * (revenue - prev_revenue) / prev_revenue, 2) AS mom_growth_pct.")
q("Data Analyst", "Problem Solving Interview", "Medium", "Executive KPI Dashboard Design",
  "How would you design an executive dashboard tracking company-wide KPIs (MRR, CAC, LTV, Net Retention) to ensure it provides actionable insights rather than visual clutter?",
  "Structure the dashboard top-down: Tier 1 shows four high-level KPI cards with current values, percentage changes vs previous period, and color-coded status indicators. Tier 2 provides trend line charts showing 12-month rolling trajectories. Tier 3 offers interactive drill-down filters (by product line, customer segment). Avoid clutter by omitting raw tables from the main view.")
q("Data Analyst", "Problem Solving Interview", "Medium", "Cohort Retention Matrix Analysis",
  "How would you build a cohort retention matrix in SQL and Python to track what percentage of users return 1, 2, 3, and 6 months after signup?",
  "Assign each user to a signup cohort month (DATE_TRUNC('month', created_at)). For each subsequent activity record, compute months_since_signup. Group by cohort_month and months_since_signup, counting distinct active users divided by cohort size. Pivot into a heatmap matrix visualizing retention decay curves.")
q("Data Analyst", "Problem Solving Interview", "Hard", "Customer Churn Prediction Framework",
  "How would you build an automated customer churn prediction framework using historical transaction logs, product usage telemetry, and customer support tickets?",
  "Extract feature vectors per customer: days since last login, feature usage frequency slope over 30 days, count of unresolved support tickets, and billing plan tier. Train a gradient-boosted classifier (XGBoost) evaluated using PR-AUC due to class imbalance. Schedule a weekly batch inference pipeline writing risk scores into the CRM, triggering automated customer success retention workflows for high-risk accounts.")

# HR (5 questions)
q("Data Analyst", "HR Interview", "Easy", "Analytics Motivation",
  "What drew you to data analytics, and what business domains do you find most interesting to analyze?",
  "I love uncovering patterns hidden within raw numbers and turning noisy datasets into clear, strategic decisions. I find product usage analytics and customer behavior particularly fascinating because small data-driven optimizations create immediate, measurable business growth.")
q("Data Analyst", "HR Interview", "Easy", "Attention to Detail",
  "How do you maintain rigorous attention to detail and sanity-check your SQL queries before sharing figures with leadership?",
  "I always verify row counts, check for duplicate keys before and after joins, cross-reference summary totals against known audited financial benchmarks, and write automated sanity assertions (e.g. ensuring percentages sum to 100%).")
q("Data Analyst", "HR Interview", "Medium", "Prioritizing Ad-Hoc vs Strategic Analytics",
  "How do you manage ad-hoc urgent data pull requests from multiple teams while still making progress on long-term analytical projects?",
  "I establish an analytics triage ticketing queue with agreed SLAs. I categorize requests by business impact and urgency, build self-service Metabase/Tableau dashboards for recurring requests so business users can pull standard data independently, and protect dedicated focus blocks for strategic projects.")
q("Data Analyst", "HR Interview", "Medium", "Continuous Learning in Data Tools",
  "How do you stay updated with the evolving data stack (e.g. dbt, DuckDB, modern cloud warehouses) without losing focus on business impact?",
  "I follow data engineering communities and participate in open data competitions. I evaluate new tools based strictly on whether they reduce analytical turnaround time or improve query cost efficiency for our specific business use cases.")
q("Data Analyst", "HR Interview", "Hard", "Analytics vs Machine Learning",
  "Where do you see the boundary between traditional business intelligence and modern predictive machine learning in your daily work?",
  "Business intelligence explains 'what happened' and 'why it happened' through clean descriptive metrics and diagnostics. Machine learning extends this into 'what will happen next' and 'how should we act' through predictive scoring. A strong data analyst bridges both: validating data integrity and business framing before applying predictive models.")

# ==============================================================================
# 8. MACHINE LEARNING ENGINEER
# ==============================================================================
# Technical (8 questions)
q("Machine Learning Engineer", "Technical Interview", "Easy", "Evaluation Metrics Trade-offs",
  "Explain Precision, Recall, and F1-score, and give an example of when Recall must be prioritized over Precision.",
  "Precision is the proportion of positive identifications that were correct (TP / (TP + FP)). Recall is the proportion of actual positives correctly identified (TP / (TP + FN)). F1-score is their harmonic mean. Recall must be prioritized in critical medical diagnosis or fraud screening, where missing a true positive (False Negative) has catastrophic consequences compared to reviewing a false alarm.")
q("Machine Learning Engineer", "Technical Interview", "Easy", "Overfitting vs Underfitting",
  "What is the difference between overfitting and underfitting, and what are three standard techniques to prevent overfitting in deep neural networks?",
  "Underfitting occurs when a model is too simple to capture underlying data patterns (high bias, poor train and validation accuracy). Overfitting occurs when a model memorizes training noise and fails to generalize (low train loss, high validation loss). Overfitting is mitigated using Dropout, L1/L2 weight regularization, Early Stopping, and data augmentation.")
q("Machine Learning Engineer", "Technical Interview", "Easy", "Train/Validation/Test Splits",
  "Why is it essential to maintain a strict separation between train, validation, and test datasets, and what causes data leakage?",
  "The training set fits model weights; the validation set tunes hyperparameters and guides early stopping; the test set provides an unbiased final evaluation of generalization on unseen data. Data leakage occurs when information from outside the training dataset (such as test set statistics during normalization, or future time-series values) contaminates the training pipeline.")
q("Machine Learning Engineer", "Technical Interview", "Medium", "Handling Imbalanced Datasets",
  "How do you handle severe class imbalance (e.g. 99:1 ratio in fraud detection) during model training and evaluation?",
  "During evaluation, never use accuracy; use Precision-Recall AUC (PR-AUC) and Cost-Matrix analysis. During training, use algorithmic techniques like Focal Loss or class-weighted cross-entropy. For data-level rebalancing, use SMOTE (Synthetic Minority Over-sampling Technique) or targeted undersampling on majority classes, ensuring resampling occurs strictly within cross-validation folds.")
q("Machine Learning Engineer", "Technical Interview", "Medium", "Transformers & Self-Attention",
  "Explain the mechanics of Scaled Dot-Product Self-Attention in Transformers (Query, Key, Value) and why scaling by sqrt(d_k) is necessary.",
  "Self-attention computes Attention(Q, K, V) = softmax((Q * K^T) / sqrt(d_k)) * V. Queries and Keys represent vector projections of tokens; their dot product measures pairwise token relevance. Scaling by sqrt(d_k) prevents dot products from growing excessively large for high vector dimensions, which would push softmax into regions with vanishingly small gradients.")
q("Machine Learning Engineer", "Technical Interview", "Medium", "Gradient Descent & Optimizers",
  "How does AdamW optimizer improve upon standard Adam and Stochastic Gradient Descent (SGD) with momentum?",
  "SGD with momentum accelerates gradient vectors in persistent directions, dampening oscillations. Standard Adam combines momentum with per-parameter adaptive learning rates based on second-moment gradient estimates. However, standard Adam applies L2 regularization incorrectly when combined with adaptive gradients. AdamW decouples weight decay from gradient updates, ensuring proper regularization and superior generalization.")
q("Machine Learning Engineer", "Technical Interview", "Hard", "Model Quantization & Inference Optimization",
  "Explain post-training quantization (FP16, INT8) and describe how TensorRT or ONNX Runtime optimizes inference latency on GPUs.",
  "Quantization converts model weights and activations from 32-bit floating point (FP32) to 16-bit (FP16) or 8-bit integers (INT8), shrinking memory footprint by 50-75% and leveraging Tensor Cores for higher throughput. TensorRT and ONNX optimize inference graphs by fusing adjacent layers (e.g. Conv + BatchNorm + ReLU), pruning unused operations, and tuning memory kernel allocations for target hardware.")
q("Machine Learning Engineer", "Technical Interview", "Hard", "Distributed Training & Data Drift",
  "Explain the difference between Data Parallelism (DDP) and Pipeline Parallelism (FSDP/ZeRO) in distributed LLM training, and how you detect feature drift in production.",
  "Distributed Data Parallel (DDP) replicates model weights across GPUs and synchronizes gradients via AllReduce. When models exceed single-GPU VRAM, Fully Sharded Data Parallel (FSDP / ZeRO) shards optimizer states, gradients, and model parameters across nodes. In production, feature drift is detected by monitoring statistical distance (Population Stability Index [PSI], Wasserstein Distance, or KS-Test) between training baseline distributions and incoming inference features.")

# Behavioral (5 questions)
q("Machine Learning Engineer", "Behavioral Interview", "Easy", "Preprocessing vs Modeling Realities",
  "Tell me about an ML project where data cleaning and preprocessing took significantly longer than model training. What did you learn?",
  "While building an NLP customer sentiment model, 80% of our effort was spent handling multilingual typos, HTML entity artifacts, and duplicate bot submissions. Clean data with simple logistic regression outperformed a complex Transformer trained on raw noise, teaching me that data quality always trumps model complexity.")
q("Machine Learning Engineer", "Behavioral Interview", "Easy", "Reproducibility in Machine Learning",
  "Tell me about a time when you struggled to reproduce experimental ML results. How did you introduce scientific rigor to your workflow?",
  "Early in my career, training runs gave varying results due to unseeded random initializations and non-deterministic GPU operations. I established strict seed configurations, integrated MLflow experiment tracking logging all hyperparameters and dataset SHA-256 hashes, ensuring 100% reproducible experiments.")
q("Machine Learning Engineer", "Behavioral Interview", "Medium", "Production Generalization Failure",
  "Describe a situation where a model achieved high validation accuracy in development but degraded severely when deployed to production. How did you diagnose the issue?",
  "A document classification model achieved 97% validation accuracy but dropped to 65% in production. I inspected production inference logs and found a data leakage bug: the training pipeline included an internal routing tag that was stripped before documents reached the production endpoint. I re-trained without the leakage feature, restoring robust performance.")
q("Machine Learning Engineer", "Behavioral Interview", "Medium", "Cross-Functional Collaboration with Software Engineers",
  "Tell me about a time when you collaborated with backend engineers to integrate an ML model into an existing microservices architecture.",
  "Backend engineers were concerned about model latency and memory usage. I packaged the model into a lightweight Triton container using ONNX runtime, established a gRPC contract, and agreed on strict 50ms latency budgets, achieving seamless production integration.")
q("Machine Learning Engineer", "Behavioral Interview", "Hard", "Simplicity vs Deep Learning Complexities",
  "Tell me about a time when business stakeholders wanted to deploy a complex deep learning model when a simpler heuristic or linear model was more appropriate. How did you handle it?",
  "Stakeholders wanted to deploy a multi-layer Transformer for lead scoring. I benchmarked a fine-tuned Transformer against an XGBoost classifier with domain features. XGBoost achieved 94% of the Transformer's accuracy with 10x lower inference latency, 85% lower compute costs, and full feature-importance explainability, winning unanimous stakeholder approval.")

# Scenario Based (5 questions)
q("Machine Learning Engineer", "Scenario Based Interview", "Easy", "Misleading Accuracy in Fraud Detection",
  "A fraud detection model has a 99.5% raw accuracy score, but fraudulent transactions are still getting through. What metric is misleading here and how do you fix it?",
  "With fraud representing only 0.5% of total transactions, a dummy model that predicts 'Not Fraud' every time achieves 99.5% accuracy while catching 0% of fraud. Replace accuracy with Recall at high precision thresholds, False Positive Rate, and the PR-AUC metric, calibrating the classification probability threshold to the business cost of fraud.")
q("Machine Learning Engineer", "Scenario Based Interview", "Easy", "Training Loss Exploding to NaN",
  "During deep neural network training with PyTorch, your training loss suddenly explodes to NaN after epoch 12. What are the common causes and immediate remedies?",
  "Common causes include exploding gradients, division by zero in custom loss functions, or unnormalized input features with large outliers. Immediate remedies include adding gradient clipping (torch.nn.utils.clip_grad_norm_), applying learning rate warm-up schedules, verifying input normalization, and inspecting for zero or negative values inside log operations.")
q("Machine Learning Engineer", "Scenario Based Interview", "Medium", "Inference Latency SLA Breach",
  "Your deep learning inference API is experiencing 750ms latency per request under peak traffic, but the client SLA requires under 150ms. Walk me through your latency optimization playbook.",
  "First, profile request latency: separate network transfer, tokenization/preprocessing, and model inference. Second, convert the model to ONNX/TensorRT format and apply FP16 quantization. Third, implement dynamic batching on the inference server (Triton Inference Server) and cache common query embeddings in Redis to achieve sub-50ms responses.")
q("Machine Learning Engineer", "Scenario Based Interview", "Medium", "Production Model Performance Degradation",
  "Three months after deploying a customer lifetime value model, accuracy drops by 25%. What data and concept drift checks do you perform?",
  "Calculate Population Stability Index (PSI) and Kolmogorov-Smirnov statistics across input features between the training baseline and current inference data to identify which features drifted (e.g. macro inflation altering spending amounts). Re-train the model on recent sliding-window data and automate scheduled weekly drift retraining triggers.")
q("Machine Learning Engineer", "Scenario Based Interview", "Hard", "Recommendation Feedback Loop Drift",
  "You deploy a recommendation model, and within two weeks, user engagement begins falling because the model repeatedly recommends the same viral items, creating an echo chamber. How do you redesign it?",
  "The model is suffering from a feedback loop: it only collects engagement data on items it recommends, starving other items of exposure. Redesign using an Multi-Armed Bandit framework (Epsilon-Greedy or Thompson Sampling) to enforce an exploration vs exploitation balance, injecting diversity heuristics and novelty penalties to break echo chambers.")

# Problem Solving (5 questions)
q("Machine Learning Engineer", "Problem Solving Interview", "Easy", "Ticket Auto-Categorization System",
  "How would you frame, prepare data, and select baseline models for a customer support ticket auto-categorization system?",
  "Frame as a multi-class text classification problem. Preprocess ticket text by stripping PII and signatures, tokenizing, and generating TF-IDF features or lightweight embeddings (Sentence-Transformers). Train a fast baseline model (Logistic Regression or LightGBM). Evaluate using micro and macro F1-score across ticket categories before experimenting with fine-tuned LLMs.")
q("Machine Learning Engineer", "Problem Solving Interview", "Easy", "Feature Selection for High-Dimensional Data",
  "How would you select the most informative 50 features from a tabular dataset containing 2,000 candidate features without overfitting?",
  "Remove zero-variance and highly collinear features using variance thresholds and Pearson/Spearman correlation matrices. Apply model-based feature importance using Random Forests or LightGBM, and use L1 Lasso regularization to drive uninformative feature coefficients to zero. Cross-validate selected subsets to prevent selection bias.")
q("Machine Learning Engineer", "Problem Solving Interview", "Medium", "End-to-End MLOps Churn Pipeline",
  "How would you architect an end-to-end Machine Learning pipeline (from data ingestion to automated retraining and canary model deployment) for a real-time churn prediction system?",
  "Ingest event streams via Kafka into a feature store (Feast). Schedule automated training pipelines using Airflow or Kubeflow, evaluating candidates against the production model on a holdout test split. If candidate performance exceeds production by >2% PR-AUC, register in MLflow Model Registry, deploy via canary rollout (10% traffic), and monitor feature drift with Evidently AI.")
q("Machine Learning Engineer", "Problem Solving Interview", "Medium", "Image Similarity Search Engine",
  "How would you build an image similarity search engine capable of finding visually matching products across a catalog of 5 million items?",
  "Pass images through a pre-trained Vision Transformer or ResNet backbone to extract 512-dimensional feature embedding vectors. Normalize embeddings and index them into an approximate nearest neighbor (ANN) vector database like FAISS or Milvus using an HNSW index. Query incoming images in under 15ms using cosine distance.")
q("Machine Learning Engineer", "Problem Solving Interview", "Hard", "Enterprise RAG Pipeline Design",
  "How would you design a scalable semantic search and question-answering system using LLMs, embedding models, and vector stores that can search across 10 million technical support articles with sub-second retrieval?",
  "Chunk documents into semantically coherent segments (512 tokens with 50-token overlap). Generate embeddings using a dedicated embedding model (e.g. text-embedding-3-small) and index into a vector database (Milvus or Pinecone) using HNSW indexing. For queries, perform hybrid search (BM25 keyword search + vector cosine similarity), rerank top 25 results using a cross-encoder model, and feed top 5 into an LLM with strict context grounding prompts.")

# HR (5 questions)
q("Machine Learning Engineer", "HR Interview", "Easy", "ML Specialization Motivation",
  "What motivated you to specialize in machine learning engineering rather than general software engineering?",
  "I was captivated by the transition from deterministic rule-based software to probabilistic models that learn complex patterns from real-world data. Combining rigorous software engineering with empirical machine learning experimentation is where I find the greatest impact.")
q("Machine Learning Engineer", "HR Interview", "Easy", "Collaboration with Business Stakeholders",
  "How do you manage expectations with business stakeholders who believe machine learning can solve every problem with 100% accuracy?",
  "I establish probabilistic expectations early: explaining that models make statistical predictions with confidence intervals rather than absolute guarantees. I define clear baseline benchmarks and frame project success around business metrics (e.g. reducing manual triage time by 40%) rather than unrealistic perfection.")
q("Machine Learning Engineer", "HR Interview", "Medium", "Keeping Up with AI Research",
  "How do you keep up with the rapid pace of AI research (new architectures, open-source models, paper releases) while staying focused on company deliverables?",
  "I filter the noise by following trusted curation sources: Papers with Code, Hugging Face daily papers, and top conference proceedings (NeurIPS, ICML). Rather than chasing every paper, I prioritize papers that solve practical engineering bottlenecks relevant to our business stack (quantization, latency, context caching).")
q("Machine Learning Engineer", "HR Interview", "Medium", "Handling Model Rollback Decisions",
  "Describe how you handle the psychological challenge of deciding to roll back a machine learning model that you spent months training and tuning.",
  "I maintain emotional detachment from models: production health and customer trust always come first. If production metrics or unintended bias emerge after deployment, I roll back without hesitation, analyze the telemetry, and use the failure as empirical data to build a better model.")
q("Machine Learning Engineer", "HR Interview", "Hard", "AI Ethics & Algorithmic Fairness",
  "How do you address ethical considerations, algorithmic fairness, and data privacy when designing automated machine learning models?",
  "I conduct pre-training audits on dataset demographic parity and remove protected attributes to prevent proxy bias. I run slice-based evaluation to ensure model accuracy does not degrade on underrepresented sub-populations, adhere to GDPR/HIPAA privacy guardrails, and document model limitations in standard Model Cards.")

# ==============================================================================
# 9. HR INTERVIEW (ROLE & FUNCTIONAL HR PRACTICE)
# ==============================================================================
# Technical / Functional HR (8 questions)
q("HR Interview", "Technical Interview", "Easy", "Employee Lifecycle Stages",
  "Walk me through the core stages of the employee lifecycle from recruitment to offboarding, and identify the primary HR objective in each stage.",
  "The stages are: Attract (employer branding), Hire (unbiased structured recruitment), Onboard (equipping and cultural integration), Develop (performance reviews, career ladders, training), Retain (compensation benchmarking, culture, engagement surveys), and Offboard (compliant exit interviews, knowledge transfer, alumni relations).")
q("HR Interview", "Technical Interview", "Easy", "Structured Interviewing & Bias Mitigation",
  "How do structured job descriptions and rubric-based scorecards eliminate unconscious bias in talent acquisition?",
  "Unstructured interviews often rely on subjective 'gut feel' or affinity bias (favoring candidates with shared backgrounds). Structured scorecards define standardized competency rubrics with concrete scoring criteria before interviews begin, ensuring every candidate answers identical role-relevant questions evaluated against measurable benchmarks.")
q("HR Interview", "Technical Interview", "Easy", "Core HR Analytics Metrics",
  "Explain the significance of Time-to-Hire, Cost-per-Hire, and Quality-of-Hire in evaluating recruitment efficiency.",
  "Time-to-Hire measures days from job posting to offer acceptance, highlighting bottlenecks in interview loops. Cost-per-Hire aggregates advertising, agency fees, and recruiter compensation divided by total hires. Quality-of-Hire tracks 1-year retention rates, performance appraisal scores, and ramp-up velocity to evaluate recruitment ROI.")
q("HR Interview", "Technical Interview", "Medium", "Compensation & Equity Benchmarking",
  "How do you design and maintain competitive compensation bands and equity allocations across junior to staff engineering levels?",
  "Aggregate industry salary data from benchmarking providers (e.g. Radford, Pave, Levels.fyi) normalized by geographic tier and funding stage. Establish distinct career bands with defined base salary ranges (minimum, midpoint, maximum) and equity grants. Review compensation bands semi-annually against market inflation and turnover data to maintain internal equity and external competitiveness.")
q("HR Interview", "Technical Interview", "Medium", "Performance Management & PIPs",
  "What are the essential elements of an effective Performance Improvement Plan (PIP) that is both legally compliant and genuinely supportive?",
  "A compliant PIP clearly specifies the performance deficiencies with documented objective examples, outlines measurable 30/60/90-day improvement objectives, details the exact coaching and resources provided by management, and establishes scheduled weekly check-ins. It transparently communicates consequences while providing a fair, achievable pathway to success.")
q("HR Interview", "Technical Interview", "Medium", "Employment Law & FLSA Compliance",
  "What is the difference between Exempt and Non-Exempt employee classifications under the Fair Labor Standards Act (FLSA)?",
  "Non-exempt employees are entitled to minimum wage and overtime pay (1.5x regular rate) for hours worked beyond 40 per week, requiring accurate time tracking. Exempt employees are excluded from overtime pay based on meeting the salary threshold test and specific job duties tests (Executive, Administrative, Professional, or Computer Employee exemptions).")
q("HR Interview", "Technical Interview", "Hard", "Scaling Engineering Talent Acquisition",
  "How would you design a talent acquisition strategy to scale an engineering department from 50 to 150 developers across multiple hubs within 12 months?",
  "Establish a predictable recruiting capacity model: calculate hiring funnel conversion rates (outreach to phone screen to onsite to offer accept). Build standardized competency interview loops with trained interviewer panels to avoid burnout. Partner with engineering leadership on employer branding (technical blogs, open-source sponsorships), and implement ATS automation to streamline candidate velocity.")
q("HR Interview", "Technical Interview", "Hard", "Workplace Investigations & Compliance",
  "What are the mandatory procedural steps when investigating a sensitive complaint of workplace harassment or discrimination involving leadership?",
  "Immediately acknowledge the complaint with confidentiality assurances and protection against retaliation. Create an investigation plan, collect documentary evidence (emails, chat logs), and conduct separate, objective interviews with the complainant, witnesses, and the accused. Document findings with legal counsel, determine policy violation findings, and enact consistent corrective actions.")

# Behavioral (5 questions)
q("HR Interview", "Behavioral Interview", "Easy", "Delivering Difficult Feedback",
  "Tell me about a time when you had to deliver difficult feedback to a hiring manager or executive. How did you ensure a constructive outcome?",
  "A senior manager was rejecting qualified candidates based on vague 'culture fit' reasons. I met with the manager privately, shared scorecard data showing their inconsistency, explained the hiring velocity cost, and partnered with them to clarify concrete, competency-based evaluation criteria, improving candidate pass-through by 35%.")
q("HR Interview", "Behavioral Interview", "Easy", "Navigating Policy Exceptions",
  "Tell me about a time when an employee requested an exception to a standard company policy. How did you handle it?",
  "An employee requested an extended leave policy exception due to sudden family illness. I reviewed the legal guidelines, consulted with their manager on team coverage, balanced compassion with organizational precedent, and structured a temporary flexible remote arrangement that supported the employee while maintaining policy fairness.")
q("HR Interview", "Behavioral Interview", "Medium", "Mediating Workplace Conflict",
  "Describe a situation where you had to mediate a serious workplace conflict between two team members. What was your process and outcome?",
  "An engineering lead and product manager had reached an impasse over sprint priorities that stalled team velocity. I held individual listening sessions to understand their underlying concerns, facilitated a joint mediation session focused on shared OKRs, and co-created an explicit decision-making RACI framework that restored healthy collaboration.")
q("HR Interview", "Behavioral Interview", "Medium", "Improving Low Engagement Scores",
  "Tell me about a time when an annual engagement survey revealed declining morale in an engineering division. What action plan did you execute?",
  "Engagement scores dropped 18% in engineering due to perceived lack of career progression. I conducted listening focus groups, collaborated with engineering VPs to publish transparent career ladders with competency matrices, introduced biannual promotion cycles, and saw engagement bounce back by 24% the following survey.")
q("HR Interview", "Behavioral Interview", "Hard", "Managing Organizational Restructuring",
  "Tell me about a time when you managed an organizational restructuring or layoff. How did you support affected employees while maintaining team morale?",
  "During a corporate restructuring, I prepared empathetic severance packages and comprehensive outplacement resources for departing staff, trained managers on delivering exit notifications respectfully, and conducted transparent all-hands meetings with remaining employees to address concerns and reaffirm future company trajectory.")

# Scenario Based (5 questions)
q("HR Interview", "Scenario Based Interview", "Easy", "Candidate Verbal Acceptance Delay",
  "A top candidate verbally accepts a job offer but delays signing the formal agreement for two weeks. How do you handle this professionally?",
  "I schedule a check-in call with the candidate to understand their hesitation empathetically. I explore whether they have competing offers, questions about compensation or benefits, or concerns about role scope. I coordinate a quick call with their future manager or executive sponsor to reinforce our enthusiasm while setting a respectful, firm deadline for a decision.")
q("HR Interview", "Scenario Based Interview", "Easy", "Sudden Resignation of Key Contributor",
  "A critical senior engineer submits a sudden 2-week notice right before a major project launch. What is your immediate retention and transition plan?",
  "Conduct an immediate, empathetic stay conversation to understand root causes (compensation, burnout, leadership conflict). If retention is possible, explore counter-offers or role adjustments. If departure is final, shift immediately to comprehensive knowledge transfer, document key architecture with teammates, and conduct an honest exit interview.")
q("HR Interview", "Scenario Based Interview", "Medium", "Department Headcount Deadlock",
  "Two department vice presidents are in a deadlock over allocating a single remaining headcount for the upcoming fiscal quarter. How do you facilitate an objective resolution?",
  "I facilitate an objective review based on company-wide OKRs and revenue impact rather than executive influence. I evaluate historical team capacity, burnout metrics, and project business cases. I present the comparative analysis to the executive committee with options for contracting or phasing, driving an aligned consensus.")
q("HR Interview", "Scenario Based Interview", "Medium", "Sudden Hiring Freeze Communication",
  "Leadership suddenly institutes a company-wide hiring freeze while you have 15 candidates in final interview stages. How do you handle candidate communications?",
  "Act with speed and transparency: immediately pause interview scheduling. Reach out personally via phone or individualized email to all active candidates, explaining the corporate change honestly with gratitude for their time. Document strong candidates in your CRM talent pool to reactivate outreach as soon as headcount opens.")
q("HR Interview", "Scenario Based Interview", "Hard", "Executive Misconduct Allegation",
  "An anonymous whistleblower report alleges that a top-revenue-producing executive is creating a toxic work environment and violating company code of conduct. What are your immediate actions?",
  "Immediately notify the Head of People and General Counsel to open a confidential formal inquiry. Ensure zero retaliation measures are enacted. Review objective electronic communications and conduct structured, confidential interviews. Treat the investigation with impartiality regardless of the executive's revenue contributions, ensuring company values and legal obligations are upheld.")

# Problem Solving (5 questions)
q("HR Interview", "Problem Solving Interview", "Easy", "Remote Onboarding Checklist",
  "How would you design a 30-60-90 day onboarding framework for remote employees that accelerates productivity and cultural integration?",
  "Days 1-30: Hardware and system access ready on Day 1, paired with an onboarding 'Buddy', 1:1 check-ins with team members, and a 'starter task' deployed within week two. Days 31-60: Ownership of core deliverables and first independent sprint feature. Days 61-90: Autonomy in cross-functional collaboration and first quarterly performance sync.")
q("HR Interview", "Problem Solving Interview", "Easy", "Overcoming Unconscious Interviewer Bias",
  "How would you design an interviewer training curriculum to train hiring managers on eliminating affinity bias and halo effect during candidate evaluations?",
  "Design an interactive 2-hour workshop covering the 5 common cognitive biases (halo, affinity, confirmation, contrast, intuition). Mandate rubric-based scorecards with concrete behavior evidence requirements ('Candidate explained X using STAR framework'), and establish interview debrief protocols where recruiters challenge non-evidence claims.")
q("HR Interview", "Problem Solving Interview", "Medium", "Fixing Offer Rejection Rates",
  "If 60% of candidates who pass the final technical interview decline your company's offers, how do you diagnose and fix the breakdown?",
  "Survey declining candidates to gather honest, anonymized data: analyze whether rejections stem from below-market compensation, prolonged time-to-offer latency (where candidates accept competitors first), or negative interview loop impressions. Adjust compensation bands, streamline hiring loops to under 14 days, and introduce personalized welcome videos from the team.")
q("HR Interview", "Problem Solving Interview", "Medium", "Diversity & Inclusion Sourcing Strategy",
  "How would you build a sustainable sourcing strategy to increase the representation of underrepresented groups in your technical hiring pipeline?",
  "Audit job description language for exclusionary masculine phrasing using augmented writing tools. Partner with organizations like Women Who Code and AfroTech. Introduce blind resume review stages where candidate names and universities are masked, and enforce diverse interview panels on all final-round interview loops.")
q("HR Interview", "Problem Solving Interview", "Hard", "Engineering Retention & Career Ladders",
  "How would you design a retention strategy and engineering career ladder for an organization experiencing high attrition among mid-level engineers?",
  "Conduct stay interviews to understand pain points (often lack of growth and ambiguous promotion criteria). Build a transparent dual-track career matrix (Individual Contributor vs Management) defining explicit competency milestones for Staff/Principal levels. Introduce annual learning stipends, internal mobility policies, and quarterly compensation parity audits.")

# HR (5 questions)
q("HR Interview", "HR Interview", "Easy", "Human Resources Passion",
  "What inspired you to build a career in Human Resources, and what workplace culture do you personally thrive in?",
  "I was inspired by the profound impact workplace culture has on human happiness and company success. I thrive in environments built on psychological safety, high standards, transparency, and empathy where people can do the best work of their lives.")
q("HR Interview", "HR Interview", "Easy", "Professional Discretion & Confidentiality",
  "How do you maintain strict confidentiality and professional boundaries when managing sensitive employee grievances or compensation data?",
  "I treat confidentiality as foundational to trust: sensitive conversations occur in private, records are secured with strict access controls, and information is shared exclusively on a need-to-know basis with authorized legal and leadership stakeholders.")
q("HR Interview", "HR Interview", "Medium", "Employee Advocate vs Business Partner",
  "How do you balance being an empathetic advocate for employees while also representing business objectives and executive leadership?",
  "I view employee advocacy and business success as mutually reinforcing rather than conflicting. High-performing companies require engaged, supported, and fairly treated employees. By presenting people initiatives in terms of business ROI (retention, productivity, reduced legal risk), I serve both the workforce and leadership.")
q("HR Interview", "HR Interview", "Medium", "Handling Difficult Conversations Calmly",
  "Describe your strategy for remaining calm, composed, and empathetic when conducting emotionally charged terminations or performance discussions.",
  "I prepare thoroughly: scripting key points clearly, practicing active listening without becoming defensive, focusing on documented behaviors rather than character, and maintaining a calm, respectful tone that honors the dignity of the individual.")
q("HR Interview", "HR Interview", "Hard", "Building Trust with Skeptical Teams",
  "How do you build trust with cynical or disengaged engineering teams who view HR primarily as bureaucratic overhead?",
  "I build trust through competence and humility: I take the time to learn their engineering rhythms, avoid introducing unnecessary meetings or jargon, solve tangible administrative friction quickly (payroll, tooling, benefits), and show through actions that HR is a strategic partner committed to unblocking their work.")

# ==============================================================================
# 10. ALL ROLES (UNIVERSAL QUESTIONS FOR BEHAVIORAL & HR)
# ==============================================================================
q("All Roles", "Behavioral Interview", "Easy", "Time Management & Competing Deadlines",
  "Tell me about a time when you had to manage multiple competing deadlines. How did you prioritize your work?",
  "I categorized tasks by urgency and business impact using an Eisenhower matrix, aligned priorities with my manager during our morning standup, set expectations with stakeholders early on timeline trade-offs, and delivered the critical deliverables on schedule.")
q("All Roles", "Behavioral Interview", "Easy", "Cross-Functional Collaboration",
  "Tell me about a time when you worked closely with cross-functional team members (designers, product managers, engineers) to launch a feature.",
  "I organized a weekly alignment sync, defined shared success metrics, maintained open communication in a dedicated Slack channel, and resolved edge-case misunderstandings early, ensuring an on-time and cohesive feature launch.")
q("All Roles", "Behavioral Interview", "Medium", "Adaptability to Changing Requirements",
  "Describe a time when project specifications or requirements changed drastically right in the middle of development.",
  "When a client shifted core features one week prior to release, I stayed calm, assessed the delta, decoupled the affected modules, and worked with the team to reprioritize the sprint backlog, successfully shipping the modified scope without burnout.")
q("All Roles", "Behavioral Interview", "Medium", "Navigating Workplace Disagreements",
  "Describe a situation where you had a constructive disagreement with a teammate regarding project strategy. How did you resolve it?",
  "We disagreed on whether to build a custom solution or integrate a third-party tool. I proposed listing evaluation criteria (cost, maintenance, delivery timeline), gathered objective data on both options, and we aligned on the third-party tool for our MVP to validate user demand.")
q("All Roles", "Behavioral Interview", "Hard", "Handling Failure in Production",
  "Tell me about a significant mistake or failure you experienced in production. How did you take ownership and what was the outcome?",
  "I deployed a query that lacked an index, causing database CPU spikes. I owned the error, rolled back the change within minutes, applied the missing index in staging, and added an automated query EXPLAIN check to our CI validation pipeline.")

q("All Roles", "HR Interview", "Easy", "Continuous Learning & Curiosity",
  "How do you stay updated with emerging technology trends and best practices in your field?",
  "I follow engineering blogs from top tech companies, experiment with personal side projects, contribute to open source, and read foundational software architecture books to continually sharpen my technical craft.")
q("All Roles", "HR Interview", "Easy", "Receiving Constructive Feedback",
  "Tell me about a time when you received constructive feedback that was difficult to hear. What action did you take?",
  "A manager noted that my pull requests were too large and difficult for peers to review thoroughly. I took the feedback constructively, adopted an atomic commit discipline, and began breaking features into small, reviewable PRs under 300 lines of code.")
q("All Roles", "HR Interview", "Medium", "Collaboration & Healthy Team Dynamics",
  "What team culture and communication norms bring out your highest productivity and creativity?",
  "I thrive in teams that practice blameless post-mortems, transparent feedback, intellectual curiosity, and clear ownership. When team members feel safe to ask questions and challenge ideas respectfully, great software is created.")
q("All Roles", "HR Interview", "Medium", "Work-Life Integration & Burnout Prevention",
  "How do you manage stress and maintain a sustainable pace during high-intensity project crunch periods?",
  "I maintain strict daily boundaries, protect regular exercise and rest, prioritize ruthlessly with my manager, and communicate early when workload risks outpacing team capacity.")
q("All Roles", "HR Interview", "Hard", "Handling Ambiguity",
  "How do you approach a situation when leadership hands you a vague, high-stakes objective with minimal direction?",
  "I embrace ambiguity by breaking the objective into key questions, interviewing stakeholders to document assumptions, drafting an initial Request For Comments (RFC) proposal with measurable success metrics, and gathering alignment before deep implementation.")

print(f"Part 3 compiled: {len(PART3_ENTRIES)} questions.")
