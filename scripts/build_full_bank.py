"""
Full Question Bank Builder for InterviewAI - Part 1
Roles 1-3:
1. Python Developer
2. Frontend Developer
3. Backend Developer
5+ curated questions per focus type across Easy, Medium, Hard.
"""

import os
import json

BANK_ENTRIES = []

def q(role, focus, diff, topic, question, answer):
    BANK_ENTRIES.append({
        "role": role,
        "type": focus,
        "difficulty": diff,
        "topic": topic,
        "question": question,
        "sample_answer": answer
    })

# ==============================================================================
# 1. PYTHON DEVELOPER
# ==============================================================================
# Technical (8 questions)
q("Python Developer", "Technical Interview", "Easy", "Data Structures",
  "What is the difference between list mutability and tuple immutability in Python, and when should you specifically prefer a tuple?",
  "Lists are mutable sequences allowing in-place item modification, while tuples are immutable once created. Tuples should be preferred when returning fixed records from functions, using sequence objects as dictionary keys (due to hashability), or guarding configuration constants against accidental mutation.")
q("Python Developer", "Technical Interview", "Easy", "Memory Management",
  "How does Python manage memory through reference counting and the garbage collector?",
  "CPython primarily relies on reference counting: an object deallocates immediately when its reference count drops to zero. To resolve circular references where objects reference each other, Python runs a generational garbage collector tracking cycles across three generational heuristics.")
q("Python Developer", "Technical Interview", "Easy", "Iterators & Generators",
  "What is the difference between a list comprehension and a generator expression in Python, and when is each preferred?",
  "A list comprehension eagerly creates and stores the entire list in RAM. A generator expression produces elements lazily on demand using the iterator protocol, maintaining O(1) memory footprint regardless of dataset size. Generators are ideal for large streams; list comprehensions are preferred when values must be re-used or indexed.")
q("Python Developer", "Technical Interview", "Medium", "Decorators & Metaprogramming",
  "How do Python decorators work under the hood, and why is functools.wraps important when writing parameterized decorators?",
  "A decorator is a callable that receives another function and returns a modified wrapper. Parameterized decorators require three nested functions: outer takes arguments, middle takes the function, and inner executes logic. Using functools.wraps preserves the decorated function's original name, docstring, and annotations for proper debugging and introspection.")
q("Python Developer", "Technical Interview", "Medium", "Async & Concurrency",
  "Explain the Global Interpreter Lock (GIL) in CPython and contrast how asyncio differs from multiprocessing.",
  "The GIL is a mutex preventing multiple native OS threads from executing Python bytecodes simultaneously on multicore CPUs. Asyncio provides cooperative single-threaded event-loop concurrency suited for I/O-bound tasks. Multiprocessing bypasses the GIL by spawning distinct OS processes with dedicated memory spaces, making it suitable for CPU-bound computations.")
q("Python Developer", "Technical Interview", "Medium", "Context Managers",
  "How do context managers handle exceptions raised within a 'with' block via __exit__?",
  "When exiting a 'with' block, Python invokes __exit__(exc_type, exc_val, exc_tb). If an exception occurred and __exit__ returns True, Python suppresses the exception; if it returns False or None, the exception propagates up the call stack.")
q("Python Developer", "Technical Interview", "Hard", "Metaclasses & OOP",
  "Explain how metaclasses control class creation in Python and how __new__ differs from __init__ in type instantiation.",
  "Classes are instances of metaclasses (defaulting to type). When a class body finishes executing, Python invokes the metaclass's __new__ to allocate the class object namespace and type structure, followed by __init__ to initialize class attributes. Custom metaclasses allow frameworks to register models, validate API contracts, or enforce architectural rules at import time.")
q("Python Developer", "Technical Interview", "Hard", "Asyncio Internals",
  "How does the asyncio event loop handle task cancellation and cooperative yielding, and what happens if blocking synchronous code is run inside a coroutine?",
  "Tasks yield to the event loop at 'await' points. Invoking task.cancel() injects an asyncio.CancelledError into the target coroutine at its next suspension point. If blocking synchronous I/O or CPU-heavy code executes inside a coroutine, it starves the single-threaded event loop, delaying all other concurrent coroutines. Blocking operations must be offloaded to loop.run_in_executor().")

# Behavioral (5 questions)
q("Python Developer", "Behavioral Interview", "Easy", "Learning & Tool Adoption",
  "Tell me about a time when you had to quickly pick up a new Python library or framework to deliver a project feature.",
  "When our team needed high-performance API schema validation, I researched Pydantic, reviewed its benchmark docs, created a small prototype, and shared the implementation patterns with my team to successfully integrate it before the sprint deadline.")
q("Python Developer", "Behavioral Interview", "Easy", "Code Review Collaboration",
  "Tell me about a time when you received rigorous code review feedback on your Python code. How did you handle it?",
  "A senior engineer pointed out that my list comprehension in a data ingestion loop was consuming excessive memory on large files. I appreciated the feedback, refactored to a generator pipeline, and documented the memory comparison benchmark in the pull request.")
q("Python Developer", "Behavioral Interview", "Medium", "Debugging Production Issues",
  "Describe a situation where you identified a performance bottleneck or memory leak in a Python application. How did you resolve it?",
  "I used tracemalloc and memory_profiler to trace an endpoint where memory grew continuously under load. I found unclosed database cursor references in a cyclic data structure, refactored the query handler to use explicit context managers, and verified a 40% memory reduction in staging.")
q("Python Developer", "Behavioral Interview", "Medium", "Handling Tight Deadlines",
  "Tell me about a time when an unexpected bug threatened an upcoming Python service deployment. How did you prioritize your effort?",
  "A regression in our serialization layer emerged 2 days before release. I isolated the root cause with unit tests, communicated the risk to our product lead, implemented a focused hotfix with regression guards, and safely shipped on schedule.")
q("Python Developer", "Behavioral Interview", "Hard", "Architectural Disagreements",
  "Tell me about a time when you strongly disagreed with a peer or technical lead regarding Python architecture. How did you advocate for your approach?",
  "A lead proposed migrating an I/O-bound service to a heavy multi-process model. I advocated for async FastAPI, built a load-test benchmark demonstrating it handled 5,000 req/s with 70% lower RAM and CPU overhead, and won consensus objectively with hard data.")

# Scenario Based (5 questions)
q("Python Developer", "Scenario Based Interview", "Easy", "Cron Job Failure Triage",
  "Imagine a Python scheduled worker script fails intermittently without raising an unhandled exception to your error tracking tool. How do you triage this?",
  "I would inspect exit codes, check if exceptions are swallowed in broad 'except Exception:' blocks, review system stderr redirect logs, add structured logging with correlation IDs, and implement health-check heartbeat pings upon task completion.")
q("Python Developer", "Scenario Based Interview", "Easy", "Module Import Error in Production",
  "Suppose a deployed Python application crashes on startup with 'ModuleNotFoundError' even though the package is listed in requirements.txt. What steps do you take?",
  "I check whether the virtual environment is properly activated in the container entrypoint, verify pip install layer caching in the Dockerfile, confirm python path and site-packages directories, and verify package name discrepancies between PyPI and import names.")
q("Python Developer", "Scenario Based Interview", "Medium", "OOM Crash Investigation",
  "A high-throughput Python API container in production experiences memory usage steadily climbing until Kubernetes terminates it with an OOMKilled status. What is your diagnostic plan?",
  "I analyze memory metrics and traffic spikes, reproduce the issue in staging under load using Locust, and capture tracemalloc snapshots. I check for unbounded global caching dictionaries, unclosed file descriptors, and circular references preventing garbage collection.")
q("Python Developer", "Scenario Based Interview", "Medium", "Database Connection Exhaustion",
  "Your Python backend begins throwing 'OperationalError: max connections reached' during peak traffic hours. How do you mitigate this immediately and long-term?",
  "Immediately increase pool timeouts, verify that db sessions are closed in 'finally' blocks or context managers, and enable connection pool pre-ping. Long-term, introduce connection pooling middleware (PgBouncer) and tune pool size and max overflow configurations.")
q("Python Developer", "Scenario Based Interview", "Hard", "Async Worker Starvation",
  "Suppose your Celery Python background workers are failing SLAs because task latency spiked from 40ms to 5 seconds during peak traffic. How do you isolate the root cause?",
  "I inspect worker concurrency settings, queue backlogs, and downstream dependency metrics. Using distributed tracing, I determine whether delays stem from database row-locking contention, Redis broker latency, or synchronous blocking HTTP calls choking worker threads.")

# Problem Solving (5 questions)
q("Python Developer", "Problem Solving Interview", "Easy", "Streaming Large Datasets",
  "How would you design a Python utility to parse and filter a 15GB CSV file containing transaction records on a server with only 2GB of RAM?",
  "I would use Python's generator expressions or the standard csv.reader to stream the file line by line without loading the full file into memory. Each row is parsed, validated, and written to an output stream, maintaining a constant O(1) memory footprint.")
q("Python Developer", "Problem Solving Interview", "Easy", "Duplicate Detection in Stream",
  "How would you detect duplicate customer records in an incoming high-volume data stream using Python with bounded memory?",
  "Use a Bloom Filter (e.g. pybloomfiltermmap) to check set membership in O(1) time and minimal memory. For probable duplicates, query the database or persistent cache to confirm, keeping false positive rates strictly under 1%.")
q("Python Developer", "Problem Solving Interview", "Medium", "LRU Cache Decorator",
  "How would you design and implement a thread-safe LRU (Least Recently Used) cache decorator with TTL (Time To Live) support in Python?",
  "I would use an OrderedDict or hash map with a doubly linked list for O(1) lookups and reordering. Store values with expiration timestamps. Upon eviction, remove the oldest node. Wrap internal accesses with threading.RLock to ensure thread safety.")
q("Python Developer", "Problem Solving Interview", "Medium", "Log File Frequency Counter",
  "How would you process 10 million log lines in Python to find the top 10 most frequent error messages efficiently?",
  "Use collections.Counter() streaming line-by-line using a generator, normalizing error messages by stripping dynamic timestamps and IDs. Call counter.most_common(10) which utilizes a min-heap under the hood to return top 10 in O(N log K) time.")
q("Python Developer", "Problem Solving Interview", "Hard", "Distributed Rate Limiter",
  "Design a distributed rate-limiting system in Python that enforces a limit of 100 requests per minute per IP address across 10 API instances.",
  "I would use Redis with a Sliding Window Log algorithm. Using a Redis Sorted Set (ZSET) keyed by IP, record request timestamps, prune entries older than 60s via ZREMRANGEBYSCORE, count remaining with ZCARD, and conditionally reject or accept inside an atomic Lua script.")

# HR (5 questions)
q("Python Developer", "HR Interview", "Easy", "Motivation & Role Fit",
  "What motivated you to specialize in Python development, and what types of engineering challenges bring out your best work?",
  "I was drawn to Python by its clean syntax, rapid prototyping, and powerful ecosystem. I do my best work building resilient backend services and data workflows that turn complex logic into intuitive code.")
q("Python Developer", "HR Interview", "Easy", "Workplace Collaboration",
  "What type of team communication and development workflow helps you perform at your best?",
  "I appreciate asynchronous communication with clear documentation, structured daily standups, blameless post-mortems, and a culture where pair programming is welcomed when tackling complex architectural hurdles.")
q("Python Developer", "HR Interview", "Medium", "Code Quality & Delivery Pressure",
  "How do you balance maintaining strict code quality, type hinting, and unit test coverage when a product manager is pushing for an urgent feature deadline?",
  "I prioritize shipping an MVP with clean core boundaries and essential unit tests for critical paths. I document remaining edge cases and schedule a dedicated refactoring ticket in the very next sprint to prevent hidden technical debt.")
q("Python Developer", "HR Interview", "Medium", "Mentoring & Knowledge Sharing",
  "How do you contribute to the technical growth of your peers and foster good engineering practices within your team?",
  "I write detailed pull request reviews explaining the 'why' behind suggestions, maintain engineering wiki guides for tricky workflows, and lead occasional lunch-and-learn presentations on tools like typing, pytest, and profiling.")
q("Python Developer", "HR Interview", "Hard", "Career Trajectory & Tech Evolution",
  "Where do you see Python evolving in the industry with initiatives like free-threaded CPython (nogil), and how are you preparing for that shift in your career?",
  "I follow CPython core developments, specifically free-threading and JIT compilation. I focus on deepening my understanding of native multi-threaded concurrency models and memory safety so our systems can take immediate advantage of future performance leaps.")

# ==============================================================================
# 2. FRONTEND DEVELOPER
# ==============================================================================
# Technical (8 questions)
q("Frontend Developer", "Technical Interview", "Easy", "JavaScript Scoping",
  "Explain the differences between 'var', 'let', and 'const' in JavaScript regarding lexical scoping, re-assignment, and hoisting.",
  "'var' is function-scoped and hoisted with an initial value of undefined. 'let' and 'const' are block-scoped and hoisted to the Temporal Dead Zone (TDZ). 'const' forbids re-assignment, while 'let' allows re-assignment.")
q("Frontend Developer", "Technical Interview", "Easy", "CSS Layout Models",
  "What are the primary differences between CSS Flexbox and CSS Grid, and when should you choose one over the other?",
  "Flexbox is a one-dimensional layout model (arranging items along a single axis), ideal for components like navbars and button groups. CSS Grid is a two-dimensional layout model (handling rows and columns simultaneously), optimal for overall page layouts and complex data dashboards.")
q("Frontend Developer", "Technical Interview", "Easy", "Semantic HTML & Accessibility",
  "Why is semantic HTML critical for Web Accessibility (a11y) and SEO, and how do landmark elements help assistive technologies?",
  "Semantic HTML tags convey clear meaning to search crawlers and screen readers. Landmarks like <main>, <nav>, and <article> allow keyboard users to jump directly to key regions. Non-semantic elements (e.g. <div> with onclick) fail keyboard accessibility unless manually patched.")
q("Frontend Developer", "Technical Interview", "Medium", "Event Loop Mechanics",
  "Explain the JavaScript Event Loop mechanics: how do microtasks differ from macrotasks?",
  "The Call Stack executes synchronous code. When async operations complete, their callbacks join queues. After the call stack empties, the Event Loop processes the Microtask queue completely (Promises, queueMicrotask) before processing a single task from the Macrotask queue (setTimeout, setInterval).")
q("Frontend Developer", "Technical Interview", "Medium", "Core Web Vitals",
  "How do you profile and optimize Core Web Vitals (Largest Contentful Paint, Interaction to Next Paint, Cumulative Layout Shift)?",
  "For LCP, optimize critical resources by preloading hero assets and eliminating render-blocking CSS. For INP, minimize main-thread execution using requestIdleCallback, Web Workers, and yielding via scheduler.yield(). For CLS, assign explicit dimensions to images and dynamic embeds.")
q("Frontend Developer", "Technical Interview", "Medium", "State Management Strategies",
  "Compare prop drilling mitigation strategies: when should you use React Context API versus an external store like Redux Toolkit or Zustand?",
  "React Context API is best suited for low-frequency global updates (theme, active user profile). Because Context re-renders all consumers on reference changes, high-frequency state updates degrade performance. External stores like Zustand support selector-based fine-grained subscriptions, preventing unnecessary re-renders.")
q("Frontend Developer", "Technical Interview", "Hard", "Browser Rendering Pipeline",
  "Walk me through the browser rendering engine lifecycle from HTML/CSS parse to pixel paint (DOM, CSSOM, Render Tree, Layout, Paint, Composite).",
  "The browser builds the DOM from HTML and CSSOM from CSS, merging visible nodes into the Render Tree. It computes geometry during Layout (Reflow), generates visual bitmaps across distinct layers during Paint, and uploads textures to the GPU during Composite. Properties like 'transform' and 'opacity' bypass Layout and Paint, executing directly on the GPU compositor.")
q("Frontend Developer", "Technical Interview", "Hard", "SSR Hydration & Bundlers",
  "What causes SSR hydration mismatches in frameworks like Next.js, and how do modern bundlers implement Tree Shaking?",
  "Hydration mismatches occur when server-rendered HTML differs from the client's initial render tree (due to client-only state like window dimensions or localStorage). Tree shaking statically analyzes ES Module import/export statements, building a dependency graph and eliminating unused exports in production bundles.")

# Behavioral (5 questions)
q("Frontend Developer", "Behavioral Interview", "Easy", "Cross-Browser Issues",
  "Tell me about a time when a feature you built worked in Chrome but failed on Safari or mobile browsers. How did you resolve it?",
  "Safari iOS ignored CSS flexbox height calculations inside an overflow container. I used BrowserStack to isolate the bug, applied a standards-compliant flex-basis rule with -webkit prefixes, and added cross-browser smoke tests to our PR review checklist.")
q("Frontend Developer", "Behavioral Interview", "Easy", "User Feedback on UI",
  "Tell me about a time when user feedback indicated that a UI feature you designed was confusing. What changes did you make?",
  "Users were clicking an icon button expecting a modal, but it was performing an immediate delete. I introduced an explicit text label, added a confirmation modal, and recorded an immediate 90% drop in user confusion tickets.")
q("Frontend Developer", "Behavioral Interview", "Medium", "Design Feasibility Pushback",
  "Describe a situation where a designer proposed an animation that would severely degrade mobile performance or accessibility. How did you handle it?",
  "A designer proposed a continuous 3D canvas animation running behind a login form. I measured that it throttled mobile CPU to 90% and drained battery. I demonstrated the frame drops, and collaborated to replace it with a lightweight, hardware-accelerated CSS gradient micro-animation.")
q("Frontend Developer", "Behavioral Interview", "Medium", "Refactoring Complex Components",
  "Tell me about a time when you refactored a bloated, monolithic frontend component. How did you verify you did not introduce regressions?",
  "I broke down an 800-line form component into dedicated sub-components using custom hooks for state management. I wrote comprehensive unit tests with React Testing Library covering validation states before refactoring to guarantee zero regressions.")
q("Frontend Developer", "Behavioral Interview", "Hard", "Codebase Modernization",
  "Tell me about a time when you contributed to migrating a legacy frontend codebase to a modern framework without halting feature delivery.",
  "Our team migrated a legacy jQuery application to React. I established an incremental Strangler Fig pattern: wrapped new features in micro-frontends mounted inside legacy shell pages, shared global state through custom browser DOM events, and migrated modules sprint-by-sprint with zero downtime.")

# Scenario Based (5 questions)
q("Frontend Developer", "Scenario Based Interview", "Easy", "Mobile Viewport Clipping",
  "A user reports that on small mobile screens, the primary checkout submit button is clipped below the bottom navigation bar. How do you fix this?",
  "Using '100vh' often ignores the mobile browser address bar. I fix this by using dynamic viewport units ('100dvh' or '100svh') and incorporating CSS safe-area-inset env variables (e.g., padding-bottom: env(safe-area-inset-bottom)) inside a sticky action container.")
q("Frontend Developer", "Scenario Based Interview", "Easy", "Broken Image Fallbacks",
  "Suppose dynamic avatar images hosted on a CDN intermittently return 404 errors. How do you handle this gracefully in the UI?",
  "Attach an onError handler to the img element that swaps the broken source with a fallback placeholder asset or displays a styled avatar badge containing the user's initials, ensuring the UI remains visually intact.")
q("Frontend Developer", "Scenario Based Interview", "Medium", "Third-Party Script Bloat",
  "Your site's Lighthouse performance score drops from 92 to 51 after marketing installs external tracking tag scripts. How do you remediate this without disabling tracking?",
  "I audit script execution using Chrome DevTools Performance panel, defer non-critical tracking scripts until after page load, and offload tracking execution to web workers or implement server-side tracking to eliminate client main-thread contention.")
q("Frontend Developer", "Scenario Based Interview", "Medium", "Stale Client Cache on Deploy",
  "After deploying a new frontend release, some users report seeing a blank screen until they perform a hard refresh (Ctrl+F5). What causes this and how do you fix it?",
  "This occurs when old index.html points to hashed JavaScript bundles that were deleted in the new deployment. Configure your CDN/web server with 'Cache-Control: no-cache, no-store' for index.html while maintaining immutable long-term caching for hashed static assets.")
q("Frontend Developer", "Scenario Based Interview", "Hard", "UI Table Jank",
  "Users report that filtering a table of 25,000 inventory items causes the entire browser tab to freeze for 2 seconds. How do you fix this?",
  "First, implement virtualized DOM rendering (using TanStack Virtual or react-window) so only visible rows in the viewport (~25 items) are rendered. Second, move client-side sorting and filtering calculations off the main UI thread into a Web Worker, ensuring 60fps responsiveness.")

# Problem Solving (5 questions)
q("Frontend Developer", "Problem Solving Interview", "Easy", "Accessible Modal Component",
  "How would you build an accessible modal dialog in vanilla JavaScript that traps keyboard focus, closes on ESC, and returns focus to the trigger element?",
  "Save document.activeElement upon opening, set aria-hidden on background elements, and focus the modal's first interactive control. Listen for 'Escape' key to close. Cycle focus between the first and last focusable modal elements on 'Tab'. On close, restore focus to the saved trigger element.")
q("Frontend Developer", "Problem Solving Interview", "Easy", "Sticky Navigation Bar with Scroll Direction",
  "How would you implement a smart navigation bar in CSS and JavaScript that hides on scroll down and reveals on scroll up?",
  "Track window.pageYOffset in an optimized requestAnimationFrame scroll listener. Compare current scroll position against previous scroll position: if scrolling down and past a threshold, add a CSS class with 'transform: translateY(-100%)'; if scrolling up, remove the class.")
q("Frontend Developer", "Problem Solving Interview", "Medium", "Search Autocomplete with Race Condition Prevention",
  "How would you design an autocomplete search component that prevents race conditions when rapid keystrokes trigger multiple asynchronous API calls?",
  "Wrap the input handler in a debounce function. Maintain an AbortController instance: abort the previous in-flight fetch before initiating a new request. Alternatively, track a sequence counter so stale responses arriving after newer queries are safely ignored.")
q("Frontend Developer", "Problem Solving Interview", "Medium", "Infinite Scroll with IntersectionObserver",
  "How would you design an infinite scrolling product grid that prevents memory leaks as the user scrolls through thousands of items?",
  "Use IntersectionObserver on a sentinel element to fetch next pages. Combine with DOM virtualization to unmount components far outside the viewport, replacing them with spacer div elements to preserve scroll height and prevent DOM bloat.")
q("Frontend Developer", "Problem Solving Interview", "Hard", "Offline Form Sync",
  "How would you architect an offline-capable inspection form that allows field agents to capture data offline and automatically syncs when connectivity returns?",
  "Use IndexedDB via Dexie.js to persist form submissions locally. Register a Service Worker with a Background Sync API tag. When the browser detects network reconnection, the service worker awakens, drains the IndexedDB queue in order, retries failed requests with exponential backoff, and updates the UI.")

# HR (5 questions)
q("Frontend Developer", "HR Interview", "Easy", "Design Passion & Inspiration",
  "What sparked your interest in frontend development, and what is an example of a web application you admire for its user experience?",
  "I love the intersection of software engineering and human empathy in user interfaces. I admire platforms like Linear and Stripe for their snappy keyboard shortcuts, micro-interactions, and visual craftsmanship, which inspires how I build software.")
q("Frontend Developer", "HR Interview", "Easy", "Empathy for Non-Technical Users",
  "How do you keep the perspective of non-technical or accessibility-dependent users in mind when developing web interfaces?",
  "I regularly test interfaces with keyboard-only navigation, run VoiceOver screen readers, and test on low-end mobile devices under throttled 3G network conditions to experience firsthand how real users interact with our product.")
q("Frontend Developer", "HR Interview", "Medium", "Cross-Functional Collaboration",
  "How do you establish smooth collaboration and contract agreements between frontend engineers, product designers, and backend developers?",
  "I establish early API contracts using OpenAPI specs and mock servers so frontend development can proceed concurrently. With designers, I align on shared Figma design tokens and component component states (loading, empty, error, active) before writing code.")
q("Frontend Developer", "HR Interview", "Medium", "Staying Current in Frontend",
  "How do you filter through the fast-moving JavaScript and CSS ecosystem without getting overwhelmed by framework churn?",
  "I focus on web platform standards (HTML, CSS custom properties, DOM APIs, ECMAScript proposals) rather than chasing every new library. Mastering platform fundamentals makes adopting or migrating frameworks straightforward.")
q("Frontend Developer", "HR Interview", "Hard", "Balancing Polish with Deadlines",
  "How do you handle situations where spending more time polishing animations or responsiveness conflicts with a strict commercial launch date?",
  "I categorize polish into usability blockers versus delightful enhancements. Foundational responsiveness, keyboard accessibility, and zero visual bugs are mandatory. Elaborate animations or micro-interactions are scheduled as follow-up polish tickets immediately following release.")

# ==============================================================================
# 3. BACKEND DEVELOPER
# ==============================================================================
# Technical (8 questions)
q("Backend Developer", "Technical Interview", "Easy", "REST API & HTTP Standards",
  "Explain the semantic difference between HTTP PUT and PATCH methods, and state the appropriate HTTP status codes for resource creation and validation failure.",
  "PUT is idempotent and replaces the target resource in its entirety; sending a partial payload via PUT wipes omitted fields. PATCH applies partial modifications to a resource. On successful creation, return 201 Created. On validation failure, return 422 Unprocessable Entity or 400 Bad Request.")
q("Backend Developer", "Technical Interview", "Easy", "Relational Database Joins",
  "What is the operational difference between an INNER JOIN, LEFT JOIN, and FULL OUTER JOIN in SQL queries?",
  "An INNER JOIN returns only records where there is a match in both joined tables. A LEFT JOIN returns all records from the left table and matched records from the right table, filling missing right-side values with NULLs. A FULL OUTER JOIN returns all records when there is a match in either table.")
q("Backend Developer", "Technical Interview", "Easy", "Stateless Architecture & JWT",
  "Why is statelessness beneficial for backend microservices, and how do JSON Web Tokens (JWT) support stateless authentication?",
  "Statelessness ensures that any application node can handle any user request without needing server-side session synchronization, enabling horizontal scaling behind load balancers. A JWT encodes user claims and an cryptographic HMAC or RSA signature in the token itself, allowing verification without querying a central session database.")
q("Backend Developer", "Technical Interview", "Medium", "Database Indexing & B-Trees",
  "How do B-Tree indexes speed up SQL lookups, and what are the trade-offs regarding write performance and index cardinality?",
  "B-Tree indexes maintain a balanced multi-way tree structure that enables O(log N) searches, range queries, and sorting. However, every write operation requires the database to update the index nodes and potentially rebalance branches, slowing write throughput. High-cardinality columns make efficient indexes, while low-cardinality columns are often bypassed in favor of sequential table scans.")
q("Backend Developer", "Technical Interview", "Medium", "Caching Strategies with Redis",
  "Explain the Cache-Aside pattern versus Write-Through caching with Redis, and how you mitigate cache stampede (thundering herd).",
  "In Cache-Aside, the application queries Redis first; on a miss, it reads the database, writes the result to Redis with a TTL, and returns it. In Write-Through, the application writes data to the cache and database synchronously. Cache stampede is mitigated using mutex locks (Redis SETNX lock), probabilistic early expiration, or background cache pre-warming.")
q("Backend Developer", "Technical Interview", "Medium", "Database Transactions & ACID",
  "Explain the four ACID properties in relational databases and contrast 'Read Committed' vs 'Repeatable Read' isolation levels.",
  "ACID stands for Atomicity (all-or-nothing), Consistency (schema constraints preserved), Isolation (concurrent transactions do not interfere), and Durability (committed data survives crashes). Read Committed prevents dirty reads. Repeatable Read guarantees that if a transaction reads a row twice, the data remains identical, preventing non-repeatable reads by holding shared read locks until completion.")
q("Backend Developer", "Technical Interview", "Hard", "Distributed Transactions & Saga Pattern",
  "Why is Two-Phase Commit (2PC) problematic in distributed microservice architectures, and how does the Saga Pattern handle distributed consistency?",
  "2PC requires a centralized coordinator and locks database resources across all participating services until the final commit phase, introducing high latency and blocking during network partitions. The Saga pattern breaks a distributed transaction into a sequence of local transactions: each service updates its local database and publishes an event. If a step fails, compensating transactions execute in reverse order to undo changes.")
q("Backend Developer", "Technical Interview", "Hard", "Message Queues & Event-Driven Systems",
  "How do you design an idempotent consumer in an event-driven system using Kafka or RabbitMQ when messages may be delivered at-least-once?",
  "Because at-least-once delivery guarantees duplicate delivery during network hiccups, consumers must be idempotent. This is achieved by including a unique message ID (UUID) in the event payload. The consumer records processed IDs in an ACID database transaction alongside the business data update or checks a Redis deduplication table using SET key value NX EX. If the ID was already recorded, the consumer acknowledges immediately without re-executing logic.")

# Behavioral (5 questions)
q("Backend Developer", "Behavioral Interview", "Easy", "API Documentation & Developer Experience",
  "Tell me about a time when you designed a backend API that was consumed by multiple teams. How did you ensure smooth adoption?",
  "I established clear OpenAPI contracts and generated interactive Swagger documentation before implementation. I organized an architecture walkthrough with the frontend and mobile teams, incorporated their feedback on response schemas, and provided a Postman collection with mock environments for immediate testing.")
q("Backend Developer", "Behavioral Interview", "Easy", "Handling Technical Feedback",
  "Tell me about a time when a code review revealed a serious flaw in your database transaction design. What was your response?",
  "A colleague noted that my transaction block was wrapping a third-party payment HTTP call, which held database connections open unnecessarily. I accepted the feedback, refactored to commit database state only after the external API responded, and thanked them for catching a concurrency vulnerability.")
q("Backend Developer", "Behavioral Interview", "Medium", "Production Outage Post-Mortem",
  "Describe a situation where a code deployment you authored triggered a production outage or critical regression. How did you respond?",
  "A database migration I deployed locked a high-traffic table, causing request queues to back up. I owned the incident immediately, rolled back the migration within 4 minutes, and restored traffic. During the blameless post-mortem, I documented the root cause, updated our migration guidelines to mandate non-blocking background index creation, and shared lessons with the engineering team.")
q("Backend Developer", "Behavioral Interview", "Medium", "Cross-Service Dependency Conflict",
  "Tell me about a time when a breaking change in another team's microservice disrupted your service. How did you handle the situation?",
  "A partner team altered their payload structure without incrementing their API version. I implemented an immediate defensive parsing adapter to keep our service running, scheduled a sync with their team to establish semantic versioning, and added consumer-driven contract tests (Pact) to prevent unannounced breaks.")
q("Backend Developer", "Behavioral Interview", "Hard", "Advocating for Technical Debt Refactoring",
  "Tell me about a time when you successfully persuaded engineering leadership to allocate sprint capacity for refactoring backend technical debt.",
  "Our core checkout service suffered from tightly coupled code that increased bug frequency by 35%. I gathered data showing that feature cycle time had increased from 3 days to 11 days. I proposed a phased refactoring plan dedicating 20% of capacity per sprint over two quarters, showing how it would reduce incident volume and accelerate future roadmap delivery.")

# Scenario Based (5 questions)
q("Backend Developer", "Scenario Based Interview", "Easy", "Downstream Service Outage",
  "A third-party payment processing gateway intermittently returns HTTP 500 errors and times out for 15% of your API requests. How should your backend handle this?",
  "Implement a Circuit Breaker pattern and exponential backoff retry policy for idempotent calls. When downstream error rates cross a threshold, the circuit trips open, immediately failing fast or returning a graceful fallback response to protect thread pools rather than letting requests pile up and cascade failure across our own service.")
q("Backend Developer", "Scenario Based Interview", "Easy", "Sudden Spike in Duplicate Requests",
  "Users clicking a 'Pay Now' button multiple times in rapid succession are causing duplicate charges in your backend. What immediate and permanent fixes do you implement?",
  "Immediately introduce an atomic idempotency check in Redis using an Idempotency-Key generated per checkout intent. Permanently, enforce unique database constraints on transaction tokens and ensure the frontend disables the submit button immediately upon first click.")
q("Backend Developer", "Scenario Based Interview", "Medium", "Database CPU Spike Under Load",
  "During a marketing campaign, your primary PostgreSQL database reaches 98% CPU utilization and query latency jumps from 15ms to 3 seconds. What is your immediate incident response?",
  "Immediately inspect active queries using pg_stat_activity to identify long-running, unindexed queries causing sequential scans. Cancel blocking queries if necessary, activate read replicas and redirect read traffic away from the primary, and scale connection pool limits. Post-incident, add missing indexes and introduce Redis caching on the hot query endpoints.")
q("Backend Developer", "Scenario Based Interview", "Medium", "Redis Memory Eviction Storm",
  "Your Redis cache reaches maxmemory and begins evicting active user session keys, logging thousands of users out. How do you triage and resolve this?",
  "Check Redis INFO stats to see memory usage by keyspace. Immediately change the eviction policy from volatile-lru to allkeys-lru or increase maxmemory if RAM allows. Isolate session data into a dedicated Redis instance separate from volatile cache data so cache spikes never evict authenticated sessions.")
q("Backend Developer", "Scenario Based Interview", "Hard", "Payment Webhook Reconciliation",
  "A network partition causes your service to miss Stripe payment confirmation webhooks for 45 minutes. How does your backend reconcile customer account state?",
  "First, ensure webhook endpoints are idempotent by recording Stripe event IDs. Second, implement an automated reconciliation worker that queries the Stripe API list events endpoint for the time window of the partition, identifies payments marked 'succeeded' that lack internal fulfillment records, and triggers order processing safely.")

# Problem Solving (5 questions)
q("Backend Developer", "Problem Solving Interview", "Easy", "URL Shortening Service",
  "How would you design the backend API and database architecture for a URL shortening service like Bitly handling 10 million URLs daily?",
  "Use an auto-incrementing 64-bit integer ID converted to Base62 encoding (a-z, A-Z, 0-9) to produce compact 6-7 character hashes without collisions. Store the mapping in a relational database or NoSQL key-value store with an index on the short code. Place Redis in front of the database to cache the most frequently accessed redirect URLs, achieving sub-5ms HTTP 301/302 redirects.")
q("Backend Developer", "Problem Solving Interview", "Easy", "Secure API Key Authentication",
  "How would you design an API key management system that allows developers to generate, rotate, and securely authenticate API keys?",
  "When generated, display the full API key once to the developer. Store only a cryptographic SHA-256 hash of the key in the database along with key prefix for identification (e.g. sk_live_abc...). When requests arrive with the Bearer key, hash the incoming key and perform a constant-time comparison against the stored hash.")
q("Backend Developer", "Problem Solving Interview", "Medium", "Distributed Rate Limiter",
  "How would you architect an API rate limiter capable of enforcing a limit of 5,000 requests per minute per tenant across 15 microservice instances?",
  "Implement a Sliding Window Counter algorithm using Redis. Each tenant has Redis hash keys bucketed into 10-second intervals. When a request arrives, query the current and previous window counts via a Redis Lua script. Sum the interpolated request count; if below the threshold, increment the counter and allow the request. If exceeded, return HTTP 429 with 'Retry-After' headers.")
q("Backend Developer", "Problem Solving Interview", "Medium", "Audit Trail for Financial Ledger",
  "How would you design an immutable financial ledger backend schema that guarantees that account balances can be audited and never tampered with?",
  "Use double-entry bookkeeping: every transaction creates balanced debit and credit entries in an append-only journal table. Disallow UPDATE or DELETE permissions on ledger entries at the database role level. Account balances are derived from the sum of journal entries or periodic cryptographically hashed snapshot checkpoints.")
q("Backend Developer", "Problem Solving Interview", "Hard", "High-Volume Notification Dispatcher",
  "Design an enterprise notification dispatch engine capable of routing 100,000 notifications per second across WebSockets, SMS, and Email with guaranteed delivery.",
  "Ingest notification requests into a partitioned Kafka topic. Consumers read from Kafka, apply user preference filters, and route messages to dedicated priority queues for each delivery channel (SMS, Email, Push). Use circuit breakers and rate limiters calibrated to each external provider's API limits, persist delivery statuses in Cassandra or DynamoDB, and route failed messages to a Dead Letter Queue (DLQ) for alerting.")

# HR (5 questions)
q("Backend Developer", "HR Interview", "Easy", "Engineering Motivation",
  "What aspects of backend engineering do you find most rewarding compared to other software development disciplines?",
  "I love designing the data models, system contracts, and business logic that power critical products behind the scenes. Solving problems around concurrency, data integrity, and high-availability architecture is what drives my passion.")
q("Backend Developer", "HR Interview", "Easy", "Collaboration with Product Teams",
  "How do you translate complex technical backend constraints into clear business trade-offs for non-technical product managers?",
  "I avoid jargon and focus on user impact, delivery risk, and infrastructure costs. For example, instead of explaining distributed transaction locking, I explain: 'Option A takes 2 weeks and gives instant consistency, while Option B takes 3 days but may take 2 seconds for balance updates to appear.'")
q("Backend Developer", "HR Interview", "Medium", "On-Call Rotation & Incident Ownership",
  "How do you approach on-call responsibilities, and how do you maintain a healthy work-life balance during high-stress operational rotations?",
  "I treat on-call as an opportunity to identify systemic weaknesses in our software. When alerts fire, I focus on stabilizing the user experience, followed by addressing the underlying alert fatigue. By prioritizing blameless post-mortems and fixing noisy alerts, on-call becomes calm and sustainable.")
q("Backend Developer", "HR Interview", "Medium", "Engineering Integrity & Code Reviews",
  "What is your philosophy on code reviews, and how do you give feedback that elevates code quality without creating interpersonal friction?",
  "Code reviews should protect the codebase while teaching. I frame suggestions objectively around performance, maintainability, and testing, separating critical blockers from optional nitpicks. I make sure to praise elegant implementations.")
q("Backend Developer", "HR Interview", "Hard", "Technical Leadership & Mentorship",
  "How do you mentor mid-level backend developers on adopting solid distributed systems patterns and writing clean, production-ready code?",
  "I conduct collaborative design review sessions (RFCs) before coding begins, encouraging engineers to explain their data access patterns and failure modes. In code reviews, I provide context on why an approach might struggle at 10x scale, pairing to write clean tests and structured logs.")

print(f"Part 1 compiled: {len(BANK_ENTRIES)} questions.")
