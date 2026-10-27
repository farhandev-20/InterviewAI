"""
Comprehensive generator for services/question_bank.py.
Builds curated questions for 9 roles x 5 focus types x 3 difficulties,
plus normalization and progressive selection helpers.
"""
import os
import sys

DATA = []

def add_q(role, focus, difficulty, topic, question, sample_answer):
    DATA.append({
        "role": role,
        "type": focus,
        "difficulty": difficulty,
        "topic": topic,
        "question": question,
        "sample_answer": sample_answer
    })

# =========================================================================
# 1. PYTHON DEVELOPER
# =========================================================================
# Technical
add_q("Python Developer", "Technical Interview", "Easy", "Python Data Structures",
      "What is the difference between list mutability and tuple immutability in Python, and in what situations would you specifically choose a tuple?",
      "Lists in Python are mutable sequences allowing in-place modifications (append, pop, slice assignments), while tuples are immutable once created. Tuples should be preferred when passing fixed collections between functions, using composite dictionary keys (due to hashability), or guarding configuration constants against accidental mutation.")
add_q("Python Developer", "Technical Interview", "Easy", "Memory Management",
      "How does Python manage memory through reference counting and the garbage collector?",
      "CPython uses reference counting as its immediate deallocation mechanism: each object tracks the count of references pointing to it, deallocating immediately when it hits zero. To handle circular references that reference counting cannot resolve, Python runs a generational garbage collector that inspects cyclical references across three generational heuristics.")
add_q("Python Developer", "Technical Interview", "Easy", "Iterators & Comprehensions",
      "What is the difference between a list comprehension and a generator expression in Python, and when is each preferred?",
      "A list comprehension constructs and stores the entire list in memory eagerly, returning a list object. A generator expression produces items lazily one at a time using the iterator protocol, maintaining O(1) memory footprint regardless of dataset size. Generators are preferred for large datasets or streaming files; list comprehensions are preferred when elements must be accessed repeatedly or indexed.")
add_q("Python Developer", "Technical Interview", "Medium", "Decorators & Metaprogramming",
      "How do Python decorators work under the hood, and why is functools.wraps important when writing parameterized decorators?",
      "A decorator is a callable that receives another function and returns a modified wrapper function. Parameterized decorators use three nested functions: the outer handles decorator arguments, the middle receives the decorated function, and the inner wraps the call. Using functools.wraps preserves original function metadata (such as __name__, __doc__, and type signatures), preventing introspection and debugging issues.")
add_q("Python Developer", "Technical Interview", "Medium", "Async & Concurrency",
      "Explain the Global Interpreter Lock (GIL) in CPython and contrast how asyncio differs from multiprocessing.",
      "The GIL is a mutex in CPython that prevents multiple native OS threads from executing Python bytecodes simultaneously on multicore CPUs. Asyncio uses a cooperative single-threaded event loop to handle thousands of I/O-bound network connections concurrently without thread overhead. Multiprocessing bypasses the GIL by spawning distinct OS processes with dedicated memory spaces, making it suitable for CPU-bound computations.")
add_q("Python Developer", "Technical Interview", "Medium", "Context Managers",
      "How do context managers in Python handle exceptions raised within a 'with' block, and how does __exit__ dictate suppression?",
      "When a 'with' statement executes, Python calls __enter__ and assigns the result to any 'as' target. Upon exiting the block, __exit__(exc_type, exc_val, exc_tb) is invoked. If an unhandled exception occurred, these arguments contain the exception details. If __exit__ returns True, Python suppresses the exception; if it returns False or None, the exception propagates upwards.")
add_q("Python Developer", "Technical Interview", "Hard", "CPython Internals & Metaclasses",
      "Explain how metaclasses control class creation in Python and how __new__ differs from __init__ in type instantiation.",
      "In Python, classes are themselves instances of metaclasses (defaulting to type). When a class statement executes, Python calls the metaclass's __new__ method to allocate the class object namespace and type structure, followed by __init__ to initialize class attributes. Custom metaclasses or __init_subclass__ allow frameworks to register subclasses, validate method contracts, or enforce architectural rules at import time.")
add_q("Python Developer", "Technical Interview", "Hard", "Asyncio Architecture & Performance",
      "How does the asyncio event loop handle task cancellation and cooperative yielding, and what happens if blocking synchronous code is run inside a coroutine?",
      "Asyncio tasks yield control to the event loop at 'await' points. Calling task.cancel() injects an asyncio.CancelledError into the target coroutine at its next suspension point. If blocking synchronous I/O or CPU-heavy code executes inside a coroutine, it blocks the entire single-threaded event loop, starving all other concurrent tasks. To avoid this, blocking calls must be offloaded to loop.run_in_executor().")

# Behavioral
add_q("Python Developer", "Behavioral Interview", "Easy", "Learning & Tool Adoption",
      "Tell me about a time when you had to quickly pick up a new Python library or framework to deliver a project feature.",
      "I explain the context: our team needed to implement fast schema validation. I researched Pydantic, reviewed documentation, built a small proof-of-concept benchmark, shared my findings with the team in our engineering sync, and successfully integrated it into our API pipeline on schedule.")
add_q("Python Developer", "Behavioral Interview", "Medium", "Debugging Production Issues",
      "Describe a situation where you identified a performance bottleneck or memory leak in a Python application. How did you resolve it?",
      "I detail using memory_profiler and tracemalloc to trace an issue where an endpoint was accumulating unclosed database connections. I isolated the cyclic reference holding references to active cursors, refactored the query handler to use explicit context managers, and verified a 40% memory reduction in staging before deploying.")
add_q("Python Developer", "Behavioral Interview", "Hard", "Architectural Disagreements",
      "Tell me about a time when you strongly disagreed with a peer or technical lead regarding Python architecture. How did you advocate for your approach?",
      "A lead proposed migrating an existing I/O-bound sync Flask service to a complex multi-process architecture. I proposed using FastAPI with async endpoints instead. I built a reproducible benchmark demonstrating that async handled our expected 5,000 req/s load with 70% lower RAM and CPU overhead, winning consensus objectively.")

# Scenario Based
add_q("Python Developer", "Scenario Based Interview", "Easy", "Cron Job Failure Triage",
      "Imagine a Python scheduled worker script fails intermittently without raising an unhandled exception to your error tracking tool. How do you triage this?",
      "I would inspect the script's exit codes, verify if exceptions are being swallowed in overly broad 'except Exception:' blocks, check system-level stdout/stderr redirect logs, add structured logging with contextual execution IDs, and implement health-check heartbeat pings upon task completion.")
add_q("Python Developer", "Scenario Based Interview", "Medium", "OOM Crash Investigation",
      "A high-throughput Python API container in production experiences memory usage steadily climbing until Kubernetes terminates it with an OOMKilled status. What is your diagnostic plan?",
      "First, check container heap metrics and request traffic correlations. Next, reproduce the leak in a staging environment under simulated load using Locust and tracemalloc snapshots to identify which object types are growing unboundedly. Common culprits include global caching dicts without eviction policies, unclosed file descriptors, or cyclic references preventing garbage collection.")
add_q("Python Developer", "Scenario Based Interview", "Hard", "Async Worker Starvation",
      "Suppose your Celery Python background workers are failing SLAs because task latency spiked from 40ms to 5 seconds during peak traffic. How do you isolate the root cause?",
      "I check worker concurrency configurations (prefork vs gevent), queue backlogs, and downstream dependency metrics. I profile task execution times using OpenTelemetry tracing to distinguish whether the slowdown is caused by database row-locking contention, Redis broker network latency, or synchronous third-party HTTP calls blocking the worker threads.")

# Problem Solving
add_q("Python Developer", "Problem Solving Interview", "Easy", "Streaming Large Datasets",
      "How would you design a Python utility to parse and filter a 15GB CSV file containing transaction records on a server with only 2GB of RAM?",
      "I would utilize Python's generator expressions or the standard csv.reader to stream the file line by line without loading the full file into memory. Each row is parsed, validated, and yield-returned or written immediately to an output stream, maintaining a constant O(1) memory footprint.")
add_q("Python Developer", "Problem Solving Interview", "Medium", "LRU Cache Decorator",
      "How would you design and implement a thread-safe LRU (Least Recently Used) cache decorator with TTL (Time To Live) support in Python?",
      "I would use an OrderedDict or a combination of a hash map and a doubly linked list to achieve O(1) lookups and reordering. For each entry, store the cached result along with a timestamp. When capacity is exceeded, evict the oldest node. To ensure thread safety under concurrent calls, protect access to the internal data structures with a threading.Lock or threading.RLock.")
add_q("Python Developer", "Problem Solving Interview", "Hard", "Distributed Rate Limiter",
      "Design a distributed rate-limiting system in Python that enforces a limit of 100 requests per minute per IP address across 10 API instances.",
      "I would use Redis with a Sliding Window Log or Token Bucket algorithm. Using a Redis Sorted Set (ZSET) keyed by IP, we record timestamps of incoming requests, remove entries older than (current_time - 60s) via ZREMRANGEBYSCORE, count the remaining cardinality with ZCARD, and conditionally reject or accept the request inside an atomic Redis Lua script to prevent race conditions.")

# HR
add_q("Python Developer", "HR Interview", "Easy", "Motivation & Role Fit",
      "What motivated you to specialize in Python development, and what types of engineering challenges bring out your best work?",
      "I was drawn to Python because of its expressive syntax, vibrant ecosystem, and rapid prototyping capabilities. I thrive when building scalable backend APIs and data integration pipelines that solve real user problems with clean, maintainable architecture.")
add_q("Python Developer", "HR Interview", "Medium", "Code Quality & Delivery Pressure",
      "How do you balance maintaining strict code quality, type hinting, and unit test coverage when a product manager is pushing for an urgent feature deadline?",
      "I prioritize shipping an MVP with clean core boundaries and essential unit tests covering critical failure paths. I explicitly communicate remaining edge cases and schedule a dedicated refactoring ticket in the very next sprint, avoiding hidden technical debt.")
add_q("Python Developer", "HR Interview", "Hard", "Career Trajectory & Tech Evolution",
      "Where do you see Python evolving in the industry with initiatives like free-threaded CPython (nogil), and how are you preparing for that shift in your career?",
      "I actively follow CPython core developments, particularly the removal of the GIL and JIT compilation improvements. I focus on deepening my understanding of native multi-threaded concurrency models and memory safety so our systems can take immediate advantage of future performance leaps.")

# =========================================================================
# 2. FRONTEND DEVELOPER
# =========================================================================
# Technical
add_q("Frontend Developer", "Technical Interview", "Easy", "JavaScript Scoping & Variables",
      "Explain the differences between 'var', 'let', and 'const' in JavaScript regarding lexical scoping, re-assignment, and hoisting.",
      "'var' is function-scoped (or globally scoped if declared outside a function) and hoisted with an initial value of undefined. 'let' and 'const' are block-scoped and hoisted to the Temporal Dead Zone (TDZ), meaning accessing them prior to declaration triggers a ReferenceError. 'const' prevents variable re-assignment, while 'let' allows re-assignment.")
add_q("Frontend Developer", "Technical Interview", "Easy", "CSS Layout Mechanics",
      "What are the primary differences between CSS Flexbox and CSS Grid, and when should you choose one over the other?",
      "Flexbox is primarily a one-dimensional layout model (arranging items along a single main axis as a row or column), ideal for UI components like navbars, badge groups, and card headers. CSS Grid is a two-dimensional layout model (handling rows and columns simultaneously), optimal for overall page layouts, complex dashboard matrices, and media galleries.")
add_q("Frontend Developer", "Technical Interview", "Easy", "Semantic HTML & Accessibility",
      "Why is semantic HTML critical for Web Accessibility (a11y) and SEO, and how do landmarks like <main>, <nav>, and <article> assist assistive technologies?",
      "Semantic HTML tags convey meaning to both search engine crawlers and screen readers. Assistive technologies use landmarks like <main>, <nav>, and <section> to allow keyboard users to jump directly to key page regions without tabbing through every link. Non-semantic markup (e.g. <div> with onclick) fails keyboard navigation and ARIA role mappings unless manually patched.")
add_q("Frontend Developer", "Technical Interview", "Medium", "Event Loop & Asynchronous JS",
      "Explain the JavaScript Event Loop mechanics: how do microtasks (Promises, MutationObserver) differ from macrotasks (setTimeout, setInterval)?",
      "The Call Stack executes synchronous code. When async operations complete, their callbacks join queues. After the call stack empties, the Event Loop processes the Microtask queue completely (including microtasks queued by other microtasks) before processing a single task from the Macrotask queue. Consequently, Promise resolutions execute before setTimeout callbacks.")
add_q("Frontend Developer", "Technical Interview", "Medium", "Core Web Vitals Optimization",
      "How do you profile and optimize Core Web Vitals (Largest Contentful Paint, Interaction to Next Paint, Cumulative Layout Shift) in a modern web app?",
      "For LCP, optimize critical resource paths by preloading hero images, using modern formats (WebP/AVIF), and eliminating render-blocking CSS. For INP, minimize long tasks on the main thread using requestIdleCallback, Web Workers, and yielding via scheduler.yield(). For CLS, assign explicit width/height dimensions to images and dynamic embeds, and reserve skeleton space for async content.")
add_q("Frontend Developer", "Technical Interview", "Medium", "State Management Patterns",
      "Compare prop drilling mitigation strategies: when should you use React Context API versus an external store like Redux Toolkit or Zustand?",
      "React Context API is best suited for low-frequency global updates (theme, active user profile, localization). Because Context triggers re-renders on all consuming components whenever the value reference changes, high-frequency state updates cause performance drops. External stores like Zustand or Redux Toolkit support selector-based fine-grained subscriptions, preventing unnecessary re-renders.")
add_q("Frontend Developer", "Technical Interview", "Hard", "Browser Rendering Pipeline",
      "Walk me through the browser rendering engine lifecycle from HTML/CSS parse to pixel paint (DOM, CSSOM, Render Tree, Layout, Paint, Composite), and explain how CSS properties affect reflow.",
      "The browser builds the DOM from HTML and CSSOM from CSS, combining visible nodes into the Render Tree. It computes geometry during Layout (Reflow), generates visual bitmaps across distinct layers during Paint, and uploads textures to the GPU during Composite. Properties like 'width' and 'top' trigger expensive Layout + Paint, while 'transform' and 'opacity' bypass Layout and Paint entirely, executing directly on the GPU compositor.")
add_q("Frontend Developer", "Technical Interview", "Hard", "SSR Hydration & Code Splitting",
      "What causes SSR hydration mismatches in frameworks like Next.js, and how do modern bundlers implement Tree Shaking?",
      "Hydration mismatches occur when the server-rendered HTML tree differs from the client's initial render tree (often due to client-only state like window.innerWidth, localStorage, or date formatting). Tree shaking works by statically analyzing ES Module import/export statements, building a dependency graph, and eliminating export nodes that are never referenced in production bundles.")

# Behavioral
add_q("Frontend Developer", "Behavioral Interview", "Easy", "Cross-Browser Compatibility",
      "Tell me about a time when a feature you built worked in Chrome but failed on Safari or mobile browsers. How did you resolve it?",
      "I detail an incident where Safari iOS ignored CSS flexbox height calculations inside an overflow container. I used BrowserStack and Web Inspector remote debugging to isolate the issue, applied a standards-compliant flex-basis rule with -webkit prefixes, and added cross-browser smoke tests to our PR review checklist.")
add_q("Frontend Developer", "Behavioral Interview", "Medium", "Pushing Back on Unrealistic Designs",
      "Describe a situation where a designer proposed a visual animation that would severely degrade mobile performance or accessibility. How did you handle it?",
      "A designer proposed a continuous 3D canvas animation running in the background of a login form. I measured that it throttled mobile CPU usage to 90% and drained battery. I scheduled a quick review, demonstrated the frame drops, and collaborated to replace it with a lightweight, hardware-accelerated CSS gradient micro-animation that met visual goals without degrading performance.")
add_q("Frontend Developer", "Behavioral Interview", "Hard", "Legacy Codebase Migration",
      "Tell me about a time when you led or contributed to migrating a legacy frontend codebase to a modern framework without halting feature delivery.",
      "Our team migrated a legacy jQuery application to React. I established an incremental Strangler Fig pattern: we wrapped new features in micro-frontends mounted inside legacy shell pages, shared global state through custom browser DOM events, and migrated modules sprint-by-sprint with zero downtime and no release freezes.")

# Scenario Based
add_q("Frontend Developer", "Scenario Based Interview", "Easy", "Mobile Viewport Clipping",
      "A user reports that on small iPhone screens, the primary checkout submit button is clipped below the bottom navigation bar. How do you diagnose and fix this?",
      "I verify CSS viewport units: using '100vh' often ignores the mobile browser address bar and dynamic bottom chrome. I fix this by using dynamic viewport units ('100dvh' or '100svh') and incorporating CSS safe-area-inset env variables (e.g., padding-bottom: env(safe-area-inset-bottom)) inside a sticky action container.")
add_q("Frontend Developer", "Scenario Based Interview", "Medium", "Third-Party Script Bloat",
      "Your site's Lighthouse performance score drops from 92 to 51 after marketing installs four external analytics and tracking tag scripts. How do you remediate this without disabling tracking?",
      "I audit script execution using Chrome DevTools Performance panel. I move non-critical tracking scripts to load asynchronously using 'defer' or dynamically inject them after the 'load' event. I evaluate offloading tracking work to web workers using Partytown or implementing server-side tracking (Google Tag Manager Server-side) to eliminate client thread contention.")
add_q("Frontend Developer", "Scenario Based Interview", "Hard", "UI Stutter on Large Tables",
      "Users report that filtering a table of 25,000 inventory items causes the entire browser tab to freeze for 2 seconds. How do you fix this?",
      "First, implement virtualized DOM rendering (using TanStack Virtual or react-window) so only visible rows in the viewport (~25 items) are rendered in the DOM. Second, move client-side sorting, fuzzy searching, and filtering calculations off the main UI thread into a Web Worker, ensuring 60fps responsiveness during active typing.")

# Problem Solving
add_q("Frontend Developer", "Problem Solving Interview", "Easy", "Accessible Modal Dialog",
      "How would you build an accessible modal dialog in vanilla JavaScript that traps keyboard focus, closes on ESC, and returns focus to the trigger element?",
      "When the modal opens, save document.activeElement, set aria-hidden on background containers, and focus the first interactive element inside the modal. Add a keydown listener for 'Escape' to dismiss. For 'Tab' navigation, query all focusable elements within the modal; if tabbing forward from the last element, cycle focus to the first, and vice versa. On close, restore focus to the saved trigger element.")
add_q("Frontend Developer", "Problem Solving Interview", "Medium", "Debounced Search with Autocomplete",
      "How would you design an autocomplete search component that prevents race conditions when rapid keystrokes trigger multiple asynchronous API calls?",
      "Wrap the input handler in a custom debounce function (e.g. 300ms delay). To handle out-of-order API responses, maintain an AbortController instance: abort the previous in-flight fetch before initiating a new request. Alternatively, track a sequence counter or use an async cancellation token so stale responses arriving after newer queries are safely discarded.")
add_q("Frontend Developer", "Problem Solving Interview", "Hard", "Offline-First Form Sync",
      "How would you architect an offline-capable inspection form that allows field agents to capture data and photos offline and automatically syncs when connectivity returns?",
      "Use IndexedDB via a library like Dexie.js to persist form submissions and binary photo Blobs locally. Register a Service Worker with a Background Sync API tag ('sync-inspections'). When the browser detects network reconnection, the service worker awakens, drains the IndexedDB queue in chronological order, retries failed requests with exponential backoff, and dispatches BroadcastChannel events to update the UI.")

# HR
add_q("Frontend Developer", "HR Interview", "Easy", "Design Passion & Inspiration",
      "What sparked your interest in frontend development, and what is an example of a web application you admire for its user experience?",
      "I love the intersection of technical software engineering and human empathy in user interfaces. I admire platforms like Linear and Stripe for their snappy keyboard shortcuts, micro-interactions, and visual craftsmanship, which inspires how I build software.")
add_q("Frontend Developer", "HR Interview", "Medium", "Collaborating with Designers & Backend",
      "How do you establish smooth collaboration and contract agreements between frontend engineers, product designers, and backend developers?",
      "I establish early API contracts using OpenAPI/Swagger specs and mock servers so frontend development can proceed concurrently. With designers, I align on shared Figma design tokens and component component states (loading, empty, error, active) before writing production code.")
add_q("Frontend Developer", "HR Interview", "Hard", "Handling Design Perfection vs Deadlines",
      "How do you handle situations where spending more time polishing animations or responsiveness conflicts with a strict commercial launch date?",
      "I categorize Polish into usability blockers versus delightful enhancements. Foundational responsiveness, keyboard accessibility, and zero visual bugs are mandatory. Elaborate animations or micro-interactions are scheduled as follow-up polish tickets immediately following release.")

# =========================================================================
# 3. BACKEND DEVELOPER
# =========================================================================
# Technical
add_q("Backend Developer", "Technical Interview", "Easy", "REST API Standards & HTTP Codes",
      "Explain the semantic difference between HTTP PUT and PATCH methods, and state the appropriate HTTP status codes for resource creation and validation failure.",
      "PUT is idempotent and replaces the target resource in its entirety; sending a partial payload via PUT wipes omitted fields. PATCH applies partial modifications to a resource without overwriting unmentioned fields. On successful creation, return 201 Created with a Location header. On validation failure, return 422 Unprocessable Entity or 400 Bad Request.")
add_q("Backend Developer", "Technical Interview", "Easy", "Relational Database Joins",
      "What is the operational difference between an INNER JOIN, LEFT JOIN, and FULL OUTER JOIN in SQL queries?",
      "An INNER JOIN returns only records where there is a match in both joined tables. A LEFT JOIN returns all records from the left table and matched records from the right table, filling missing right-side values with NULLs. A FULL OUTER JOIN returns all records when there is a match in either table, filling non-matching sides with NULLs.")
add_q("Backend Developer", "Technical Interview", "Easy", "Stateless Architecture & JWT",
      "Why is statelessness beneficial for backend microservices, and how do JSON Web Tokens (JWT) support stateless authentication?",
      "Statelessness ensures that any application node can handle any user request without needing server-side session synchronization, enabling seamless horizontal scaling behind load balancers. A JWT encodes user claims and an cryptographic HMAC or RSA signature in the token itself; any node holding the verification key can validate authenticity without querying a central session database.")
add_q("Backend Developer", "Technical Interview", "Medium", "Database Indexing & Query Plans",
      "How do B-Tree indexes speed up SQL lookups, and what are the trade-offs regarding write performance and index cardinality?",
      "B-Tree indexes maintain a balanced multi-way tree structure that enables O(log N) searches, range queries, and sorting. However, every INSERT, UPDATE, or DELETE requires the database to update the index nodes and potentially rebalance branches, slowing write throughput. High-cardinality columns (e.g. UUIDs, emails) make efficient indexes, while low-cardinality columns (e.g. booleans) are often ignored by query optimizers in favor of sequential table scans.")
add_q("Backend Developer", "Technical Interview", "Medium", "Caching Strategies with Redis",
      "Explain the Cache-Aside pattern versus Write-Through caching with Redis, and how you mitigate cache stampede (thundering herd).",
      "In Cache-Aside, the application queries Redis first; on a cache miss, it reads the database, writes the result to Redis with a TTL, and returns it. In Write-Through, the application writes data to the cache and database synchronously. Cache stampede occurs when an expired hot key causes thousands of concurrent requests to hit the database simultaneously. It is mitigated using mutex locks (Redis SETNX lock), probabilistic early expiration (XFetch), or background pre-warming.")
add_q("Backend Developer", "Technical Interview", "Medium", "Database Transactions & ACID",
      "Explain the four ACID properties in relational databases and contrast 'Read Committed' vs 'Repeatable Read' isolation levels.",
      "ACID stands for Atomicity (all-or-nothing), Consistency (schema constraints preserved), Isolation (concurrent transactions do not interfere), and Durability (committed data survives crashes). Read Committed prevents dirty reads (reading uncommitted data). Repeatable Read guarantees that if a transaction reads a row twice, the data remains identical, preventing non-repeatable reads by holding shared read locks until transaction completion.")
add_q("Backend Developer", "Technical Interview", "Hard", "Distributed Transactions & Saga Pattern",
      "Why is Two-Phase Commit (2PC) problematic in distributed microservice architectures, and how does the Saga Pattern handle distributed consistency?",
      "2PC requires a centralized coordinator and locks database resources across all participating services until the final commit phase, introducing high latency, single points of failure, and blocking during network partitions. The Saga pattern breaks a distributed transaction into a sequence of local transactions: each service updates its local database and publishes an event. If a step fails, the Saga executes compensating transactions in reverse order to undo changes.")
add_q("Backend Developer", "Technical Interview", "Hard", "Message Queues & Event-Driven Systems",
      "How do you design an idempotent consumer in an event-driven system using Kafka or RabbitMQ when messages may be delivered at-least-once?",
      "Because at-least-once delivery guarantees duplicate delivery during network hiccups, consumers must be idempotent. This is achieved by including a unique message ID (UUID) in the event payload. The consumer records processed IDs in an ACID database transaction alongside the business data update or checks a Redis deduplication table using SET key value NX EX. If the ID was already recorded, the consumer acknowledges the message immediately without re-executing logic.")

# Behavioral
add_q("Backend Developer", "Behavioral Interview", "Easy", "API Documentation & Developer Experience",
      "Tell me about a time when you designed a backend API that was consumed by multiple teams. How did you ensure smooth adoption?",
      "I established clear OpenAPI contracts and generated interactive Swagger documentation before implementation. I organized an architecture walkthrough with the frontend and mobile teams, incorporated their feedback on response schemas, and provided a Postman collection with mock environments for immediate testing.")
add_q("Backend Developer", "Behavioral Interview", "Medium", "Production Outage Post-Mortem",
      "Describe a situation where a code deployment you authored triggered a production outage or critical regression. How did you respond?",
      "A database migration I deployed locked a high-traffic table, causing request queues to back up. I owned the incident immediately, rolled back the migration within 4 minutes, and restored traffic. During the blameless post-mortem, I documented the root cause, updated our migration guidelines to mandate non-blocking background index creation, and shared lessons with the engineering team.")
add_q("Backend Developer", "Behavioral Interview", "Hard", "Advocating for Technical Debt Refactoring",
      "Tell me about a time when you successfully persuaded engineering leadership to allocate sprint capacity for refactoring backend technical debt.",
      "Our core checkout service suffered from tightly coupled spaghetti code that increased bug frequency by 35%. I gathered data showing that feature cycle time had increased from 3 days to 11 days. I proposed a phased refactoring plan dedicating 20% of capacity per sprint over two quarters, showing how it would reduce incident volume and accelerate future roadmap delivery.")

# Scenario Based
add_q("Backend Developer", "Scenario Based Interview", "Easy", "Downstream Service Outage",
      "A third-party payment processing gateway intermittently returns HTTP 500 errors and times out for 15% of your API requests. How should your backend handle this?",
      "Implement a Circuit Breaker pattern (e.g. Resilience4j or PyBreaker) and exponential backoff retry policy for idempotent calls. When downstream error rates cross a threshold, the circuit trips open, immediately failing fast or returning a graceful fallback response to protect thread pools rather than letting requests pile up and cascade failure across our own service.")
add_q("Backend Developer", "Scenario Based Interview", "Medium", "Database CPU Spike Under Load",
      "During a marketing campaign, your primary PostgreSQL database reaches 98% CPU utilization and query latency jumps from 15ms to 3 seconds. What is your immediate incident response?",
      "Immediately inspect active queries using pg_stat_activity to identify long-running, unindexed queries causing sequential scans. Cancel blocking queries if necessary, activate read replicas and redirect read traffic away from the primary, and scale connection pool limits. Post-incident, add missing indexes and introduce Redis caching on the hot query endpoints.")
add_q("Backend Developer", "Scenario Based Interview", "Hard", "Payment Webhook Reconciliation",
      "A network partition causes your service to miss Stripe payment confirmation webhooks for 45 minutes. How does your backend reconcile customer account state?",
      "First, ensure webhook endpoints are idempotent by recording Stripe event IDs. Second, implement an automated reconciliation reconciliation worker that queries the Stripe API list events endpoint for the time window of the partition, identifies payments marked 'succeeded' that lack internal fulfillment records, and triggers order processing safely.")

# Problem Solving
add_q("Backend Developer", "Problem Solving Interview", "Easy", "URL Shortening Service",
      "How would you design the backend API and database architecture for a URL shortening service like Bitly handling 10 million URLs daily?",
      "Use an auto-incrementing 64-bit integer ID converted to Base62 encoding (a-z, A-Z, 0-9) to produce compact 6-7 character hashes without collisions. Store the mapping in a relational database or NoSQL key-value store with an index on the short code. Place Redis in front of the database to cache the most frequently accessed redirect URLs, achieving sub-5ms HTTP 301/302 redirects.")
add_q("Backend Developer", "Problem Solving Interview", "Medium", "Distributed Rate Limiter",
      "How would you architect an API rate limiter capable of enforcing a limit of 5,000 requests per minute per tenant across 15 microservice instances?",
      "Implement a Sliding Window Counter algorithm using Redis. Each tenant has Redis hash keys bucketed into 10-second intervals. When a request arrives, query the current and previous window counts via a Redis Lua script. Sum the interpolated request count; if below the threshold, increment the counter and allow the request. If exceeded, return HTTP 429 with 'Retry-After' headers.")
add_q("Backend Developer", "Problem Solving Interview", "Hard", "High-Volume Notification Dispatcher",
      "Design an enterprise notification dispatch engine capable of routing 100,000 notifications per second across WebSockets, SMS, and Email with guaranteed delivery.",
      "Ingest notification requests into a partitioned Kafka topic. Consumers read from Kafka, apply user preference filters, and route messages to dedicated priority queues for each delivery channel (SMS, Email, Push). Use circuit breakers and rate limiters calibrated to each external provider's API limits, persist delivery statuses in Cassandra or DynamoDB, and route failed messages to a Dead Letter Queue (DLQ) for alerting.")

# HR
add_q("Backend Developer", "HR Interview", "Easy", "Engineering Motivation",
      "What aspects of backend engineering do you find most rewarding compared to other software development disciplines?",
      "I love designing the data models, system contracts, and business logic that power critical products behind the scenes. Solving problems around concurrency, data integrity, and high-availability architecture is what drives my passion.")
add_q("Backend Developer", "HR Interview", "Medium", "On-Call Rotation & Incident Ownership",
      "How do you approach on-call responsibilities, and how do you maintain a healthy work-life balance during high-stress operational rotations?",
      "I treat on-call as an opportunity to identify systemic weaknesses in our software. When alerts fire, I focus on stabilizing the user experience, followed by addressing the underlying alert fatigue. By prioritizing blameless post-mortems and fixing noisy alerts, on-call becomes calm and sustainable.")
add_q("Backend Developer", "HR Interview", "Hard", "Technical Leadership & Mentorship",
      "How do you mentor mid-level backend developers on adopting solid distributed systems patterns and writing clean, production-ready code?",
      "I conduct collaborative design review sessions (RFCs) before coding begins, encouraging engineers to explain their data access patterns and failure modes. In code reviews, I provide context on why an approach might struggle at 10x scale, pairing to write clean tests and structured logs.")

print("Added Backend Developer questions...")
