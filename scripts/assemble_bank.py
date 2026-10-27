"""
assemble_bank.py - Compiles all question bank entries and generates
services/question_bank.py with comprehensive normalization and progressive selection.
"""
import os
import sys

# Ensure repository root is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.build_full_bank import BANK_ENTRIES as part1
from scripts.data_part2 import PART2_ENTRIES as part2
from scripts.data_part3 import PART3_ENTRIES as part3

ALL_QUESTIONS = part1 + part2 + part3

print(f"Total curated questions compiled: {len(ALL_QUESTIONS)}")

ROLES = [
    "Python Developer",
    "Frontend Developer",
    "Backend Developer",
    "Full Stack Developer",
    "Java Developer",
    "UI/UX Designer",
    "Data Analyst",
    "Machine Learning Engineer",
    "HR Interview"
]

FOCUS_TYPES = [
    "Technical Interview",
    "HR Interview",
    "Behavioral Interview",
    "Scenario Based Interview",
    "Problem Solving Interview"
]

# Validation
for r in ROLES:
    for f in FOCUS_TYPES:
        matching = [q for q in ALL_QUESTIONS if q["role"] == r and q["type"] == f]
        if len(matching) < 5:
            print(f"CRITICAL WARNING: Less than 5 questions for {r} + {f} (Found: {len(matching)})")

code_template = f'''"""
Predefined Question Bank and Selection Engine for InterviewAI
Contains curated, role-specific questions across:
- 9 Target Roles
- 5 Interview Focus Types (Technical, HR, Behavioral, Scenario Based, Problem Solving)
- 3 Difficulties (Easy, Medium, Hard)
With normalization and progressive selection algorithms ensuring zero duplicates
and strict role and interview focus alignment.
"""
import random

def normalize_role(role_name):
    """Normalizes role strings across variants (e.g. UI UX Designer vs UI/UX Designer)."""
    if not role_name:
        return "Python Developer"
    r = str(role_name).strip()
    r = r.replace("(Resume Tailored)", "").strip()
    if r in ("UI UX Designer", "UI/UX Designer"):
        return "UI/UX Designer"
    if r in ("Full Stack", "Full Stack Developer"):
        return "Full Stack Developer"
    return r

def normalize_focus(focus_name):
    """Normalizes interview focus types across short and full variants."""
    if not focus_name:
        return "Technical Interview"
    f = str(focus_name).strip()
    low = f.lower()
    if low in ("technical", "technical interview"):
        return "Technical Interview"
    if low in ("hr", "hr interview"):
        return "HR Interview"
    if low in ("behavioral", "behavioral interview"):
        return "Behavioral Interview"
    if low in ("scenario based", "scenario-based", "scenario based interview", "scenario-based interview"):
        return "Scenario Based Interview"
    if low in ("problem solving", "problem-solving", "problem solving interview", "problem-solving interview"):
        return "Problem Solving Interview"
    if not low.endswith("interview"):
        return f"{{f}} Interview"
    return f

QUESTION_BANK = {repr(ALL_QUESTIONS)}

# Role-specific domain question generators for high counts (10, 15, 20)
ROLE_DOMAIN_EXTENSIONS = {{
    "Python Developer": {{
        "Technical Interview": [
            ("Type Hinting & Mypy", "Easy", "How does Python type hinting with typing and Mypy improve enterprise codebase maintainability?", "Type annotations allow static type checkers to catch subtle TypeError bugs, invalid None dereferences, and signature mismatches before code runs in production."),
            ("Memory Profiling with tracemalloc", "Medium", "How do you use Python's tracemalloc or memory_profiler to pinpoint memory leaks and object retention in high-throughput services?", "Take snapshots at execution boundaries, compare statistics using compare_to, and inspect top object allocation tracebacks to eliminate uncollected circular references."),
            ("Python Descriptor Protocol", "Hard", "Explain the Python Descriptor protocol (__get__, __set__, __delete__) and how it powers properties, methods, and ORMs.", "Descriptors define binding behavior when attributes are accessed. Properties, classmethod, and ORM column mappings are implemented via descriptors intercepting attribute access."),
            ("Package Distribution & Wheels", "Easy", "What is the difference between a source distribution (sdist) and a built wheel (bdist_wheel) in Python packaging?", "An sdist contains raw source files and requires local compilation of C extensions during pip install. A wheel is pre-compiled, enabling instantaneous installation without build tooling."),
            ("Asyncio Task Group & ExceptionGroup", "Hard", "How does Python 3.11+ TaskGroup improve structured concurrency and exception handling compared to asyncio.gather?", "TaskGroup ensures that if any child task fails, remaining tasks in the group are immediately cancelled and awaited, raising an ExceptionGroup that bundles all errors cleanly.")
        ],
        "Behavioral Interview": [
            ("Mentoring on Pythonic Idioms", "Easy", "Tell me about a time when you helped a peer transition to writing idiomatic Python. What concepts did you emphasize?", "I paired on code reviews, explaining list comprehensions, context managers, and duck typing rather than heavy explicit getters/setters, boosting their code clarity."),
            ("Technical Debt Refactoring", "Medium", "Describe a time when you refactored an unmaintained Python script into a robust, tested package.", "I modularized the script into a clean package structure with poetry, added pyproject.toml, introduced pytest with 90% coverage, and automated linting in CI."),
            ("Adopting Strict CI Guardrails", "Hard", "Tell me about a time when you introduced automated linting or formatting tools (like Ruff, Black, or Flake8) to an existing team that resisted change.", "I demonstrated how auto-formatters eliminate subjective nitpicking in PR reviews, set up automated pre-commit hooks, and won team buy-in by focusing reviews on logic rather than style.")
        ],
        "Scenario Based Interview": [
            ("Slow SQLAlchemy Bulk Inserts", "Medium", "Suppose an automated import script inserting 500,000 records via SQLAlchemy takes 45 minutes to execute. How do you optimize it?", "Replace ORM-hydrated object loops with bulk insert mappings or core bulk inserts, use multi-value INSERT statements, and batch commits in chunks of 5,000."),
            ("Import Cycle Resolution", "Easy", "Two Python modules in your application trigger an ImportError: cannot import name due to a circular import. How do you resolve this cleanly?", "Refactor shared models or utilities into a separate decoupled module, import inside function scopes where necessary, or use typing.TYPE_CHECKING guards for type hints."),
            ("Async Worker Event Loop Freeze", "Hard", "A FastAPI service in production experiences intermittent 10-second latency spikes across all endpoints whenever a specific report endpoint is called. How do you diagnose this?", "A developer ran a heavy synchronous CPU loop or blocking requests.get() inside an async def endpoint, blocking the event loop. Move the blocking call to run_in_executor or use httpx.AsyncClient.")
        ],
        "Problem Solving Interview": [
            ("In-Memory Log Aggregator", "Medium", "How would you design an in-memory sliding window log aggregator in Python to detect brute-force login attempts across IP addresses?", "Use collections.defaultdict(collections.deque). For each attempt, append the current timestamp, pop timestamps older than the window, and alert if deque length exceeds the threshold."),
            ("Dependency Graph Topological Sort", "Hard", "How would you write an algorithm in Python to resolve and execute package dependencies in the correct order, detecting circular dependency cycles?", "Build an adjacency list graph and in-degree counter. Use Kahn's algorithm with a queue for topological sorting. If sorted output length does not equal total nodes, identify and report the circular cycle."),
            ("Concurrent Web Scraper with Rate Limiting", "Easy", "How would you implement a polite web scraper in Python using asyncio and aiohttp that limits concurrent connections to 5 requests per domain?", "Use an asyncio.Semaphore(5) wrapped around the fetch coroutines, and introduce an asyncio.sleep delay between requests to respect rate limits.")
        ],
        "HR Interview": [
            ("Engineering Culture Values", "Easy", "What specific qualities in an engineering culture allow you to do your most impactful work?", "I thrive with open collaboration, blameless post-mortems, clear ownership, and psychological safety where team members feel comfortable questioning assumptions."),
            ("Managing Critical Feedback", "Medium", "Describe how you prefer to receive feedback from technical leads and peers during performance reviews.", "I appreciate direct, actionable feedback grounded in specific code examples, delivered regularly rather than saved exclusively for annual reviews."),
            ("Long-term Technical Aspirations", "Hard", "Where do you envision your technical trajectory evolving over the next 3 to 5 years?", "I aim to grow into a Staff-level technical architect, guiding systems design, mentoring engineers, and steering reliable infrastructure across the organization.")
        ]
    }},
    "Frontend Developer": {{
        "Technical Interview": [
            ("CSS Container Queries", "Medium", "What are CSS Container Queries and how do they improve modular component design compared to traditional Media Queries?", "Container queries evaluate styling rules based on the size of the parent container (@container) rather than the entire browser viewport, making components truly reusable anywhere in a layout."),
            ("Web Workers for Heavy Compute", "Hard", "How and when do you offload heavy JavaScript computations to Web Workers to maintain 60fps UI responsiveness?", "Offload CPU-intensive operations (image processing, large dataset filtering, physics calculations) to dedicated Web Workers communicating via postMessage to keep the main UI thread free."),
            ("Web Storage Security", "Easy", "Compare the security implications of storing authentication tokens in localStorage versus sessionStorage versus HTTP-only cookies.", "localStorage and sessionStorage are vulnerable to Cross-Site Scripting (XSS) attacks. HTTP-only cookies cannot be read by JavaScript, providing defense-in-depth against credential theft.")
        ],
        "Behavioral Interview": [
            ("Collaborating on Component Libraries", "Medium", "Describe a time when you contributed a shared component to an internal design library. How did you ensure it satisfied multiple product teams?", "I conducted discovery sessions with other frontend engineers, gathered edge-case requirements, authored thorough documentation with Storybook, and provided customizable style tokens."),
            ("Pushing Back on Feature Scope", "Hard", "Tell me about a time when you had to convince a product manager to phase a frontend feature release to protect page performance.", "I demonstrated that launching an un-optimized feature would hurt our SEO Core Web Vitals, proposing a Phase 1 MVP followed by optimized lazy-loaded components in Phase 2.")
        ],
        "Scenario Based Interview": [
            ("CLS Layout Shift on Dynamic Ads", "Easy", "Third-party dynamic banner ads are causing severe Cumulative Layout Shift (CLS) on your article pages. How do you resolve this?", "Reserve explicit min-height and width placeholder aspect-ratio boxes in CSS so content below the ad does not jump when the banner asynchronously renders."),
            ("Memory Leak in Single Page App", "Medium", "Users who keep your single-page app open for hours experience browser sluggishness and tab crashes. How do you diagnose and fix this?", "Take Chrome DevTools Heap Snapshots over time to identify detached DOM nodes held by uncleared event listeners, window timers, or global RxJS/store subscriptions. Ensure clean unmount cleanup.")
        ],
        "Problem Solving Interview": [
            ("Dynamic Theme Switcher", "Easy", "How would you implement a zero-flash dark/light mode toggle with CSS custom properties that respects system preferences and persists user choice?", "Store preference in localStorage. Run an inline synchronous script in the HTML head before DOM rendering to set data-theme attribute on document.documentElement based on storage or prefers-color-scheme."),
            ("Optimistic Task Kanban Board", "Hard", "How would you design a drag-and-drop Kanban task board supporting optimistic re-ordering, immediate UI feedback, and error rollback on network failure?", "Use HTML5 Drag and Drop or dnd-kit. Re-order items immediately in local state. Dispatch an API update with an order index; if the backend fails, revert state to a saved snapshot and display an error alert.")
        ],
        "HR Interview": [
            ("Aesthetic Sensitivity & Craft", "Easy", "How do you evaluate whether a user interface feels polished, delightful, and intuitive?", "I evaluate typography hierarchy, consistent spacing tokens, smooth transition curves, clear active/hover/focus states, and whether the interface provides immediate, reassuring feedback for every user interaction."),
            ("Handling Cross-Team Friction", "Medium", "Describe how you navigate technical disagreements between design and frontend engineering teams.", "I ground conversations in user experience and data: pairing with designers to build interactive prototypes where we test usability together and find realistic technical solutions.")
        ]
    }},
    "UI/UX Designer": {{
        "Technical Interview": [
            ("Information Architecture Patterns", "Easy", "Explain the difference between hierarchical, sequential, and matrix information architectures in web app navigation.", "Hierarchical organizes content top-down from broad to specific; sequential guides users linearly step-by-step (e.g. checkout); matrix allows users to navigate across multiple dimensions using filtering and faceted links."),
            ("Designing for Reduced Motion", "Medium", "How do you accommodate users with vestibular motion disorders using CSS prefers-reduced-motion media queries?", "Detect prefers-reduced-motion: reduce to replace dizzying parallax, zooming, and large displacement transitions with gentle opacity fades, ensuring accessible comfort for sensitive users."),
            ("Design Handoff Specifications", "Hard", "What documentation and interactive specifications do you provide to frontend developers to ensure pixel-perfect fidelity during handoff?", "Provide structured Figma design token variables, explicit responsive breakpoint mockups, interactive component state matrices (default, hover, active, focus, disabled, loading, empty), and CSS transition timing curves.")
        ],
        "Behavioral Interview": [
            ("Balancing User Research with Business Goals", "Medium", "Describe a time when user research recommendations conflicted with a short-term monetization goal. How did you navigate the compromise?", "I demonstrated how aggressive popups increased short-term conversions by 5% but doubled customer churn within 60 days. I designed a contextual inline trial banner that preserved user trust while meeting business targets."),
            ("Iterative Wireframing with Stakeholders", "Easy", "Tell me about a time when rapid low-fidelity sketching helped align a confused team on product direction.", "Our team had spent 2 weeks arguing over dashboard layouts. I facilitated a Crazy Eights sketching session, pinned ideas on a virtual whiteboard, and synthesized the best concepts into a clickable wireframe within 24 hours.")
        ],
        "Scenario Based Interview": [
            ("Mobile Navigation Drawer Clutter", "Easy", "A mobile app menu has grown to 18 navigation items, causing cognitive overload. How do you restructure it ergonomically?", "Analyze usage analytics to identify the top 4 primary actions for a persistent bottom navigation bar. Group remaining secondary items into categorized expandable sections inside an account/more drawer."),
            ("Designing for Slow Network Latency", "Medium", "Users in rural areas on 3G report that blank loading screens make them think your app crashed. How do you design for high latency?", "Implement staggered skeleton loading screens that mirror final content geometry, show micro-animations on interactive controls immediately upon click, and provide clear offline indicators with cached data.")
        ],
        "Problem Solving Interview": [
            ("Multi-Tenant Organization Switcher", "Medium", "How would you design a seamless organization/workspace switcher in a B2B SaaS navigation header for users managing multiple company accounts?", "Place an organization avatar dropdown in the top-left or top-right header showing current active workspace name and user role. Include instant search filtering in the dropdown, quick-switch keyboard shortcuts, and a clear 'Create New Organization' action."),
            ("Accessible Color Palette Generator", "Easy", "How would you design an intuitive color palette customizer that guarantees brand colors always meet WCAG AA contrast compliance?", "Provide an interactive slider where adjusting lightness dynamically recalculates contrast against background tokens. Automatically display accessible passing badges (AA Pass: 5.2:1) and suggest adjacent compliant hex values if a selection fails."),
            ("Empty State Onboarding Experience", "Hard", "How would you design an inspiring, actionable empty state for a new user entering an analytics dashboard with zero historical data?", "Avoid static 'No Data Available' text. Provide an educational illustration, explain what insights will appear, offer an 'Import Sample Dataset' preview mode, and show a 3-step checklist guiding the user to connect their first data source.")
        ],
        "HR Interview": [
            ("Design Philosophy & User Empathy", "Easy", "How do you cultivate deep user empathy for audiences with backgrounds, abilities, or cultures very different from your own?", "I conduct user interviews without assumptions, immerse myself in user community forums, observe real working environments, and test interfaces with assistive technology tools to challenge my own cognitive biases."),
            ("Productive Stakeholder Alignment", "Medium", "How do you manage executive stakeholders who insist on their own subjective visual preferences over research-backed designs?", "I acknowledge their perspective respectfully and present user research recordings and A/B test data showing real customer behavior, transforming opinions into an objective problem-solving discussion.")
        ]
    }},
    "Backend Developer": {{
        "Technical Interview": [
            ("Connection Pooling Mechanics", "Medium", "How do database connection pools (like HikariCP or PgBouncer) work, and how do you size them properly?", "Connection pools maintain a warm set of reusable database connections, avoiding expensive TCP/TLS handshake overhead per query. Size pools using Little's Law: Pool Size = (Core Count * 2) + Disk Spindle Effective Count."),
            ("Idempotency Keys in Payment APIs", "Hard", "How do idempotency keys prevent duplicate credit card charges during network retry spikes?", "Clients pass a unique Idempotency-Key header. The server acquires an atomic lock on the key in Redis or database, checks if a previous response was saved, and returns the cached result if already processed.")
        ],
        "Behavioral Interview": [
            ("Responding to Data Corruption", "Hard", "Tell me about a time when you detected data inconsistency or corruption in a production database. What steps did you take?", "I isolated the faulty batch job causing the corruption, stopped further updates, wrote a safe forward-reconciliation script with dry-run verification, and repaired the records with zero user data loss.")
        ],
        "Scenario Based Interview": [
            ("Dead Letter Queue Surge", "Medium", "Your asynchronous worker Dead Letter Queue (DLQ) suddenly accumulates 100,000 failed event messages over 2 hours. How do you triage this?", "Inspect a sample of failed messages in the DLQ to identify common error codes. Patch the underlying worker bug or downstream dependency, and run a safe re-drive script to replay messages with throttling.")
        ],
        "Problem Solving Interview": [
            ("Distributed Lock with Redis (Redlock)", "Medium", "How would you design a distributed lock mechanism in Redis that prevents race conditions and handles worker crashes?", "Use Redis SET resource_name my_random_token NX PX 30000. To release the lock safely, use a Lua script verifying that the token matches before deleting, preventing accidental release of another worker's lock.")
        ],
        "HR Interview": [
            ("Balancing Velocity with Resilience", "Easy", "How do you evaluate whether a backend architecture is 'good enough' to ship versus over-engineered?", "I evaluate whether it meets current reliability and throughput needs while remaining simple to understand, test, and debug. Premature optimization before knowing real bottlenecks adds unnecessary complexity.")
        ]
    }},
    "Full Stack Developer": {{
        "Technical Interview": [
            ("Micro-Frontend Webpack Module Federation", "Hard", "How does Webpack Module Federation enable independently deployed micro-frontend applications to share runtime vendor dependencies?", "Module Federation allows an application to dynamically load remote code at runtime. It negotiates shared singleton libraries (like React) across builds, downloading common vendors only once."),
            ("WebSocket Reconnection & Backpressure", "Medium", "How do you handle automatic reconnection, backpressure, and heartbeat ping/pongs in real-time WebSocket client-server pipelines?", "Send periodic ping/pong frames every 30s to detect broken connections early. On disconnect, implement exponential backoff with jitter on reconnect attempts, and buffer unsent messages up to a memory threshold.")
        ],
        "Behavioral Interview": [
            ("Balancing Full Stack Velocity", "Medium", "Tell me about a time when you had to balance frontend polish with backend query optimizations under a tight release schedule.", "We had 3 days to launch a customer reporting tool. I focused initial hours on optimizing the SQL queries with indexes to ensure fast responses, and used our pre-existing UI design system components to build a clean interface quickly without writing custom CSS from scratch.")
        ],
        "Scenario Based Interview": [
            ("Stale Data on Concurrent Edits", "Medium", "Two users in your full-stack app edit the same document concurrently and one user accidentally overwrites the other's changes. How do you prevent this?", "Implement optimistic locking with version columns or Operational Transformation / CRDTs. If the version submitted by the client does not match current database version, reject with HTTP 409 and prompt the user with a visual diff.")
        ],
        "Problem Solving Interview": [
            ("Full Stack Image Cropper & Resizer", "Easy", "How would you design an end-to-end user profile avatar upload flow with client-side image cropping and backend thumbnail generation?", "Use a client-side canvas cropper (Cropper.js) so users preview and crop in browser. Export a compressed WebP Blob, upload to an API endpoint, and have the backend resize into small (40px) and medium (120px) thumbnails stored in S3.")
        ],
        "HR Interview": [
            ("Continuous Full Stack Learning", "Easy", "How do you maintain curiosity and continuous learning across both client and server software paradigms?", "I build end-to-end proof-of-concept projects when new architectural standards emerge, read engineering blogs from companies operating at high scale, and contribute back to open-source developer tooling.")
        ]
    }},
    "Java Developer": {{
        "Technical Interview": [
            ("Java Reflection & MethodHandles", "Hard", "How does java.lang.invoke.MethodHandles compare with traditional Java Reflection in performance and type safety?", "Traditional reflection checks security and access permissions on every single invoke call, incurring high overhead. MethodHandles performs access checks once during creation and can be heavily inlined by the JIT compiler into direct native instructions."),
            ("Spring Boot Actuator & Micrometer", "Medium", "How do you instrument production Spring Boot microservices with Micrometer and Prometheus metrics?", "Add spring-boot-starter-actuator and micrometer-registry-prometheus. Expose /actuator/prometheus to scrape custom Timers, Counters, and JVM memory pools for Grafana alerting.")
        ],
        "Behavioral Interview": [
            ("Championing Automated Unit Testing", "Easy", "Tell me about a time when you increased automated test coverage in a Java project that had low reliability.", "Our billing service had only 20% test coverage and frequent regressions. I established a rule that every bug fix required a reproducing JUnit test case, introduced Mockito mocks for external APIs, and raised coverage to 85% within two quarters.")
        ],
        "Scenario Based Interview": [
            ("Metaspace OutOfMemoryError", "Hard", "A Java application throws 'java.lang.OutOfMemoryError: Metaspace' after repeated hot-deployments in an application server. What causes this?", "Metaspace stores class metadata. Dynamic class generation frameworks (CGLIB, proxy generators) create classes with custom ClassLoaders that cannot be garbage collected if static references hold references to the ClassLoader, causing classloader memory leaks.")
        ],
        "Problem Solving Interview": [
            ("Thread-Safe Rate Limiter in Java", "Medium", "How would you build an in-memory Token Bucket rate limiter in Java using AtomicLong and System.nanoTime()?", "Track availableTokens and lastRefillTimestamp using AtomicLong/AtomicReference. When a request arrives, compute elapsed time to add new tokens up to bucket capacity, and atomically decrement if tokens are available, ensuring lock-free thread safety.")
        ],
        "HR Interview": [
            ("Enterprise Reliability Mindset", "Easy", "What does engineering craft and reliability mean to you in the context of enterprise Java development?", "It means building resilient, self-healing systems that handle edge cases gracefully, have zero unexpected memory leaks, provide rich structured observability, and can be maintained effortlessly by future engineers.")
        ]
    }},
    "Data Analyst": {{
        "Technical Interview": [
            ("Data Pipeline Schema Drift", "Medium", "How do you detect and handle schema drift (unexpected column additions, renames, or type changes) in incoming analytical data streams?", "Implement schema validation at data ingestion boundaries using tools like Great Expectations or Pydantic. Route invalid records to a quarantine dead-letter table and trigger automated Slack alerts to the data engineering team."),
            ("Statistical Significance Fallacies", "Hard", "What are common pitfalls in interpreting p-values during A/B testing (e.g. peeking problem, p-hacking, multi-testing)?", "Peeking repeatedly during an active test inflates Type I error rates. Running dozens of metric comparisons without Bonferroni or False Discovery Rate (FDR) corrections guarantees false positives by pure chance.")
        ],
        "Behavioral Interview": [
            ("Leading a Self-Service Analytics Transition", "Medium", "Tell me about a time when you empowered non-technical business teams to self-serve their own data queries.", "I designed curated Metabase dashboards with interactive parameter dropdowns and hosted a weekly 'Data Office Hours' training session, reducing ad-hoc data pull requests by 60% and freeing our team for strategic analysis.")
        ],
        "Scenario Based Interview": [
            ("Data Discrepancy Between Ad Network and Analytics", "Easy", "Facebook Ads reports 1,200 purchases, but your internal analytics tracking only records 750. How do you explain and reconcile this to marketing?", "Explain cookie blocking (iOS ATT), conversion attribution windows (Facebook default 7-day click vs internal same-day last-touch), and deduplicate transaction IDs to find which transactions were counted twice by view-through attribution.")
        ],
        "Problem Solving Interview": [
            ("Market Basket Association Analysis", "Medium", "How would you write a SQL query to find the pairs of products most frequently purchased together in the same transaction?", "Self-join the order_items table on order_id WHERE item_a.product_id < item_b.product_id to avoid reverse duplicates. Group by item_a and item_b, counting distinct order_ids ordered by frequency descending.")
        ],
        "HR Interview": [
            ("Data Storytelling Impact", "Easy", "What makes a data visualization truly effective at influencing business decisions?", "Simplicity and focus: an effective visualization removes chart junk, uses intentional color to highlight the key takeaway immediately, and directly answers a strategic question rather than dumping raw numbers.")
        ]
    }},
    "Machine Learning Engineer": {{
        "Technical Interview": [
            ("Hyperparameter Tuning Strategies", "Medium", "Compare Grid Search, Random Search, and Bayesian Optimization (Hyperopt/Optuna) for hyperparameter tuning.", "Grid search evaluates every combination exhaustively and is computationally prohibitive. Random search samples hyperparameter space more efficiently. Bayesian optimization models the objective function using Gaussian Processes or Tree-structured Parzen Estimators, picking next hyperparameter candidates that maximize expected improvement."),
            ("Loss Functions for Contrastive Learning", "Hard", "Explain InfoNCE and Triplet Loss in self-supervised representation learning.", "Triplet loss minimizes distance between an anchor and positive sample while penalizing distance to a negative sample by a margin. InfoNCE generalizes this using a multi-class softmax framework, contrasting one positive pair against multiple negative samples simultaneously.")
        ],
        "Behavioral Interview": [
            ("Retiring Obsolete Machine Learning Models", "Medium", "Tell me about a time when you retired a production ML model that had become technical debt. How did you manage the transition?", "An older random forest model required manual weekly data exports. I built an automated replacement pipeline using XGBoost with Feast feature store, ran a shadow-mode evaluation for 2 weeks to verify parity, and decommissioned the legacy cron job safely.")
        ],
        "Scenario Based Interview": [
            ("Cold-Start Problem in Recommendations", "Medium", "Your recommendation engine performs poorly for new users who have zero past browsing history. How do you solve the cold-start problem?", "Use hybrid recommendation: present new users with a lightweight onboarding taste quiz, fallback to popularity-based and trending items, or infer initial user preferences using contextual signals (geography, referral source, device type).")
        ],
        "Problem Solving Interview": [
            ("Real-Time Toxicity Classification API", "Hard", "How would you design a real-time text toxicity moderation API that must process 2,000 chat messages per second with sub-25ms latency?", "Use a distilled student model (MiniLM or MobileBERT) quantized to INT8 with ONNX runtime. Deploy on a GPU or optimized CPU cluster with Triton Inference Server, and cache high-frequency phrases in Redis to bypass model inference for known inputs.")
        ],
        "HR Interview": [
            ("Pragmatism in AI Development", "Easy", "How do you maintain engineering pragmatism when company excitement around generative AI threatens to distract from simple, effective solutions?", "I ground projects in measurable customer ROI and maintenance cost. Generative AI is fantastic for semantic search and unstructured text, but traditional statistical models are often faster, cheaper, and more reliable for tabular forecasting.")
        ]
    }},
    "HR Interview": {{
        "Technical Interview": [
            ("Diversity, Equity, and Inclusion (DEI) Metrics", "Medium", "What quantitative metrics do you track to measure DEI health across talent acquisition, promotion, and retention pipelines?", "Track diversity ratios across hiring funnel stages (applied vs interviewed vs offered) to identify conversion drop-offs. Monitor equal promotion rates across demographic cohorts, and calculate adjusted gender and minority pay-gap parity audits annually."),
            ("Employee Relations Investigation Documentation", "Hard", "How do you prepare investigation report documentation to ensure credibility, impartiality, and legal admissibility in labor disputes?", "Document the specific allegations with exact dates and policies cited, record verbatim quotes from witnesses, detail factual evidence credibility assessments, state clear findings of fact on each allegation, and provide recommendations approved by counsel.")
        ],
        "Behavioral Interview": [
            ("Championing Employee Mental Health", "Easy", "Tell me about a time when you recognized signs of burnout in a team and introduced initiatives to restore well-being.", "I observed climbing attrition and sick leave usage in our customer support team during a product release. I advocated with leadership to introduce flexible mental health days, audited on-call shift rotations, and established meeting-free focus afternoons."),
            ("Managing Compensation Equity Adjustments", "Medium", "Describe a situation where a salary audit revealed pay discrepancies across peers with similar experience. How did you resolve it?", "During an annual review, I identified that market inflation had created compression between new hires and tenured engineers. I built a business case for leadership, allocated an off-cycle equity adjustment pool, and brought tenured salaries up to fair market parity.")
        ],
        "Scenario Based Interview": [
            ("Handling Workplace Rumors and Leak Triage", "Medium", "Rumors about an upcoming organizational change leak onto internal communication channels, causing widespread team anxiety. How do you manage this?", "Partner immediately with executive leadership to communicate with transparency: address the company in a clear, honest announcement, validate team feelings, provide accurate timelines, and open an anonymous Q&A portal with scheduled leadership office hours.")
        ],
        "Problem Solving Interview": [
            ("Designing an Engineering Career Ladder", "Hard", "How would you design a transparent 5-tier technical career ladder (Junior to Principal) that rewards technical impact without forcing engineers into management?", "Create a dual-track career architecture: parallel Individual Contributor (IC) and Management tracks with identical compensation bands. Define clear rubrics across 4 pillars: Technical Craft, System Scope, Team Impact, and Strategic Leadership, with concrete observable behaviors for each level."),
            ("Remote Culture Engagement Framework", "Easy", "How would you design virtual engagement programs that foster genuine connection without creating 'Zoom fatigue'?", "Replace forced virtual happy hours with opt-in interest channels (book clubs, gaming tournaments), introduce asynchronous recognition boards (Donut/Bonusly shoutouts), and sponsor local in-person quarterly team co-working offsites.")
        ],
        "HR Interview": [
            ("HR Leadership Philosophy", "Easy", "What is your philosophy on the role of Human Resources in shaping company culture and business success?", "HR should not be bureaucratic police; we are strategic architects of the environment in which talent thrives. By removing organizational friction, promoting fairness, and developing leaders, we empower the company to achieve its greatest goals.")
        ]
    }}
}}

def get_bank_questions(role, interview_type, difficulty="Medium", count=5):
    """
    Selects or generates exactly `count` unique questions matching the target role,
    interview focus, and difficulty with realistic interviewer phrasing and progressive depth.
    """
    count = int(count)
    norm_role = normalize_role(role)
    norm_focus = normalize_focus(interview_type)
    norm_diff = str(difficulty).capitalize()
    if norm_diff not in ("Easy", "Medium", "Hard"):
        norm_diff = "Medium"

    # 1. Exact Role + Focus + Difficulty match
    exact_matches = [
        q for q in QUESTION_BANK 
        if q["role"] == norm_role and q["type"] == norm_focus and q["difficulty"] == norm_diff
    ]

    # 2. Adjacent difficulty matches of SAME role and SAME focus
    adjacent_matches = [
        q for q in QUESTION_BANK 
        if q["role"] == norm_role and q["type"] == norm_focus and q["difficulty"] != norm_diff
    ]

    # 3. Universal questions for HR & Behavioral if applicable
    universal_matches = []
    if norm_focus in ("HR Interview", "Behavioral Interview"):
        universal_matches = [
            q for q in QUESTION_BANK 
            if q["role"] == "All Roles" and q["type"] == norm_focus
        ]

    # Combine pool in priority order
    candidate_pool = []
    seen_texts = set()

    for item in exact_matches:
        if item["question"] not in seen_texts:
            seen_texts.add(item["question"])
            candidate_pool.append(dict(item))

    for item in adjacent_matches:
        if len(candidate_pool) >= count:
            break
        if item["question"] not in seen_texts:
            seen_texts.add(item["question"])
            candidate_pool.append(dict(item))

    for item in universal_matches:
        if len(candidate_pool) >= count:
            break
        if item["question"] not in seen_texts:
            seen_texts.add(item["question"])
            candidate_pool.append(dict(item))

    # 4. If count still requires more (e.g. 10, 15, or 20 questions requested):
    # Check dynamic domain extensions for that specific role and focus
    if len(candidate_pool) < count and norm_role in ROLE_DOMAIN_EXTENSIONS:
        extensions = ROLE_DOMAIN_EXTENSIONS[norm_role].get(norm_focus, [])
        for topic, diff_level, q_text, ans_text in extensions:
            if len(candidate_pool) >= count:
                break
            if q_text not in seen_texts:
                seen_texts.add(q_text)
                candidate_pool.append({{
                    "role": norm_role,
                    "type": norm_focus,
                    "difficulty": diff_level,
                    "topic": topic,
                    "question": q_text,
                    "sample_answer": ans_text
                }})

    # 5. Role-tailored procedural synthesis fallback if extra questions still needed
    iteration = 1
    while len(candidate_pool) < count:
        if norm_role == "UI/UX Designer":
            if norm_focus == "Technical Interview":
                q_text = f"As a UI/UX Designer, how do you approach responsive breakpoint tokenization and typography scaling across mobile and desktop? (Part {{iteration}})"
                topic = "Design Systems & Breakpoints"
                ans = "Establish fluid typography scales using CSS clamp() and align design tokens with responsive grid layouts in Figma."
            elif norm_focus == "Behavioral Interview":
                q_text = f"Tell me about a time as a UI/UX Designer when you conducted a usability test that completely transformed your product perspective. (Experience {{iteration}})"
                topic = "User Testing Impact"
                ans = "Explain user pain points discovered during testing, how you synthesized findings, and how the revised prototype improved usability."
            elif norm_focus == "Scenario Based Interview":
                q_text = f"Imagine your analytics indicate that 40% of users fail to complete a critical onboarding wizard on mobile devices. What is your design audit and remediation plan? (Scenario {{iteration}})"
                topic = "Mobile Funnel UX Remediation"
                ans = "Audit touch targets, simplify form inputs, add clear progress indicators, and test accessible responsive layouts."
            elif norm_focus == "Problem Solving Interview":
                q_text = f"How would you approach designing an intuitive multi-tenant workspace navigation layout for an enterprise SaaS tool with complex nested resources? (Problem {{iteration}})"
                topic = "Enterprise Navigation IA"
                ans = "Structure navigation with global persistent actions, collapsible side drawers, breadcrumbs for depth, and instant global search."
            else:
                q_text = f"What core user research and design ethics principles guide your work most as a UI/UX Designer? (Topic {{iteration}})"
                topic = "Design Ethics & Philosophy"
                ans = "Advocating for inclusive accessibility, transparent communication without dark patterns, and prioritizing user needs."
        elif norm_role == "Data Analyst":
            if norm_focus == "Technical Interview":
                q_text = f"In your data analysis workflow, how do you approach data modeling and optimizing aggregation queries across massive tables? (Part {{iteration}})"
                topic = "Analytical Query Architecture"
                ans = "Use partition pruning, clustered indexes, and pre-aggregated summary rollups to minimize scan volumes."
            elif norm_focus == "Behavioral Interview":
                q_text = f"Tell me about a time as a Data Analyst when you presented an insight that directly resulted in a profitable business decision. (Experience {{iteration}})"
                topic = "Commercial Analytics Impact"
                ans = "Highlight how cohort data identified an untapped customer segment, driving tailored marketing and measurable revenue growth."
            elif norm_focus == "Scenario Based Interview":
                q_text = f"Suppose a key upstream payment data feed fails over the weekend, resulting in incomplete dashboard metrics on Monday morning. How do you triage this? (Scenario {{iteration}})"
                topic = "Pipeline Incident Triage"
                ans = "Notify stakeholders immediately with status notices, trigger backfill ETL scripts, and verify data integrity before updating charts."
            elif norm_focus == "Problem Solving Interview":
                q_text = f"How would you approach designing an automated cohort retention tracking model in SQL to identify customer churn triggers? (Problem {{iteration}})"
                topic = "Churn Modeling Architecture"
                ans = "Segment users by acquisition month, compute active retention percentages by month index, and isolate correlation factors with churn."
            else:
                q_text = f"What communication practices do you find most effective when translating complex statistical data to non-technical teams? (Topic {{iteration}})"
                topic = "Data Storytelling & Influence"
                ans = "Lead with the business bottom line, use clean visual charts, eliminate confusing jargon, and provide clear recommended actions."
        elif norm_role == "Machine Learning Engineer":
            if norm_focus == "Technical Interview":
                q_text = f"As a Machine Learning Engineer, how do you manage feature store architecture and real-time model feature serving? (Part {{iteration}})"
                topic = "Feature Store Architecture"
                ans = "Use feature stores like Feast to serve low-latency features via Redis for online inference while maintaining historical feature parity for training."
            elif norm_focus == "Behavioral Interview":
                q_text = f"Tell me about a time as an ML Engineer when a model failed in production due to an unexpected data distribution shift. How did you resolve it? (Experience {{iteration}})"
                topic = "Data Drift Resolution"
                ans = "Monitored feature drift metrics, retrained on recent window data with automated pipelines, and added automated data drift alarms."
            elif norm_focus == "Scenario Based Interview":
                q_text = f"Imagine your real-time recommendation model inference service experiences a 3x traffic spike and GPU memory runs out. What is your mitigation plan? (Scenario {{iteration}})"
                topic = "Inference Capacity & Scaling"
                ans = "Implement dynamic request batching, enable INT8 model quantization, and route traffic to a CPU fallback pool or cached recommendations."
            elif norm_focus == "Problem Solving Interview":
                q_text = f"How would you approach designing an automated model retraining pipeline with canary validation for a fraud detection service? (Problem {{iteration}})"
                topic = "Automated MLOps Pipeline"
                ans = "Schedule automated retraining in Kubeflow, validate candidates on holdout splits against production PR-AUC, and roll out via 10% canary traffic."
            else:
                q_text = f"How do you maintain scientific rigor and reproducible experiment tracking in your machine learning projects? (Topic {{iteration}})"
                topic = "ML Experimentation Discipline"
                ans = "Seed random initializations, log datasets and hyperparameters with MLflow, and version datasets using DVC."
        elif norm_role == "HR Interview":
            if norm_focus == "Technical Interview":
                q_text = f"In Human Resources operations, how do you approach workforce planning and analyzing retention metrics across departments? (Part {{iteration}})"
                topic = "Workforce Analytics"
                ans = "Analyze voluntary turnover trends, calculate cost-per-hire and ramp-up time, and align staffing forecasts with business milestones."
            elif norm_focus == "Behavioral Interview":
                q_text = f"Tell me about a time in your HR career when you successfully resolved a contentious disagreement between leadership and employees. (Experience {{iteration}})"
                topic = "Employee Relations Mediation"
                ans = "Listened to both sides with empathy, grounded the discussion in shared cultural values, and established transparent compromise policies."
            elif norm_focus == "Scenario Based Interview":
                q_text = f"Suppose a team experiences sudden high attrition following an executive leadership transition. What is your diagnostic and retention plan? (Scenario {{iteration}})"
                topic = "Executive Transition Retention"
                ans = "Conduct confidential stay interviews to identify root friction, coordinate transparent all-hands communication, and review compensation equity."
            elif norm_focus == "Problem Solving Interview":
                q_text = f"How would you approach designing an equitable, bias-free promotion and performance evaluation framework for an engineering organization? (Problem {{iteration}})"
                topic = "Performance Rubric Architecture"
                ans = "Establish concrete competency-based scorecards with explicit observable behavior requirements and peer review calibration panels."
            else:
                q_text = f"What personal values and ethical principles guide your approach to people operations and employee advocacy? (Topic {{iteration}})"
                topic = "People Operations Philosophy"
                ans = "Treating every employee with dignity, championing fair and transparent compensation, and fostering psychological safety."
        else: # Developer Roles (Python, Frontend, Backend, Full Stack, Java)
            if norm_focus == "Technical Interview":
                q_text = f"As a {{norm_role}}, how do you approach performance benchmarking, error monitoring, and code modularity in production? (Part {{iteration}})"
                topic = "Production Engineering Principles"
                ans = "Profile critical execution paths, establish automated latency alarms with APM tools, and structure modular code with high unit test coverage."
            elif norm_focus == "Behavioral Interview":
                q_text = f"Tell me about a time as a {{norm_role}} when you had to adapt to a sudden change in project scope or timeline. How did you ensure success? (Part {{iteration}})"
                topic = "Scope Management & Adaptability"
                ans = "Highlight transparent communication with stakeholders, reprioritizing the backlog, and delivering the core value on time."
            elif norm_focus == "Scenario Based Interview":
                q_text = f"Imagine you join a new team as a {{norm_role}} and discover that release deployments frequently cause unmonitored regressions. What is your 30-day remediation plan? (Scenario {{iteration}})"
                topic = "Deployment Reliability & Observability"
                ans = "Introduce staging smoke tests, automated CI test gates, and structured post-release verification checklists."
            elif norm_focus == "Problem Solving Interview":
                q_text = f"How would you approach designing a scalable diagnostic health-check framework for a {{norm_role}} system that verifies database, cache, and third-party dependencies? (Challenge {{iteration}})"
                topic = "Health Check & Diagnostic Architecture"
                ans = "Implement asynchronous health checks with timeout budgets for each dependency, returning structured status payloads with HTTP 200 or 503."
            else: # HR Interview
                q_text = f"What core workplace values and communication practices are most critical to you when collaborating as a {{norm_role}}? (Topic {{iteration}})"
                topic = "Team Dynamics & Workplace Fit"
                ans = "Clear documentation, psychological safety, empathy across technical and business functions, and continuous knowledge sharing."

        if q_text not in seen_texts:
            seen_texts.add(q_text)
            candidate_pool.append({{
                "role": norm_role,
                "type": norm_focus,
                "difficulty": norm_diff,
                "topic": topic,
                "question": q_text,
                "sample_answer": ans
            }})
        iteration += 1

    # Progressive Ordering: Foundational first, then deeper questions
    diff_order = {{"Easy": 1, "Medium": 2, "Hard": 3}}
    sorted_pool = sorted(candidate_pool[:count], key=lambda x: diff_order.get(x.get("difficulty", "Medium"), 2))
    
    return sorted_pool[:count]
'''

target_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "services", "question_bank.py"))
with open(target_path, "w", encoding="utf-8") as f:
    f.write(code_template)

print(f"Successfully generated {target_path}!")
