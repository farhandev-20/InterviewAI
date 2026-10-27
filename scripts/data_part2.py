"""
Full Question Bank Builder for InterviewAI - Part 2
Roles 4-6:
4. Full Stack Developer
5. Java Developer
6. UI/UX Designer
5+ curated questions per focus type across Easy, Medium, Hard.
"""

PART2_ENTRIES = []

def q(role, focus, diff, topic, question, answer):
    PART2_ENTRIES.append({
        "role": role,
        "type": focus,
        "difficulty": diff,
        "topic": topic,
        "question": question,
        "sample_answer": answer
    })

# ==============================================================================
# 4. FULL STACK DEVELOPER
# ==============================================================================
# Technical (8 questions)
q("Full Stack Developer", "Technical Interview", "Easy", "Client-Server Architecture",
  "Explain the client-server request lifecycle from the moment a user enters a URL in a browser to the backend rendering a response.",
  "The browser performs DNS resolution to obtain the server's IP address, establishes a TCP handshake and TLS encryption, sends an HTTP GET request, and the server router matches the endpoint to execute backend controller logic. The backend queries the database, formats a response (HTML/JSON), and returns HTTP status codes. The browser parses HTML/CSS to build DOM and CSSOM trees and executes JavaScript.")
q("Full Stack Developer", "Technical Interview", "Easy", "REST vs GraphQL",
  "Compare RESTful APIs with GraphQL regarding data fetching, over-fetching, and caching capabilities.",
  "REST relies on fixed endpoints with standard HTTP verbs and status codes, leveraging HTTP caching (Cache-Control, ETags) effectively, but can suffer from over-fetching or under-fetching. GraphQL provides a single endpoint where clients request exact schemas and nested relations, eliminating multiple network round trips at the expense of more complex client caching.")
q("Full Stack Developer", "Technical Interview", "Easy", "CORS Configuration",
  "What is Cross-Origin Resource Sharing (CORS), and what triggers a preflight OPTIONS request in the browser?",
  "CORS is a browser security mechanism that restricts web pages from making cross-origin HTTP requests unless the server explicitly grants permission via Access-Control-Allow-Origin headers. Preflight OPTIONS requests are triggered when requests use non-simple HTTP methods (PUT, DELETE, PATCH) or custom headers (Authorization) or non-standard Content-Types (application/json).")
q("Full Stack Developer", "Technical Interview", "Medium", "Full Stack Authentication",
  "How do you implement secure authentication in a full stack app using refresh token rotation and HTTP-only cookies?",
  "Store short-lived access tokens in memory or secure storage and store long-lived refresh tokens in an HTTP-only, Secure, SameSite=Strict cookie to prevent XSS theft. When the access token expires, the client calls a refresh endpoint; the server validates the refresh token against a revocation list in Redis, issues a new access token, and rotates the refresh token.")
q("Full Stack Developer", "Technical Interview", "Medium", "Optimistic UI Updates",
  "How do you implement optimistic UI updates on the frontend while maintaining transaction consistency on the backend?",
  "When a user triggers an action (e.g. liking a post), immediately update client state and re-render the UI optimistically before the network response arrives. Concurrently dispatch the API mutation with an idempotency key. If the backend succeeds, commit the state; if the backend returns an error, roll back client state and display an error toast.")
q("Full Stack Developer", "Technical Interview", "Medium", "Docker Full Stack Containerization",
  "How do you structure a multi-container Docker Compose setup for a full stack web app (frontend, backend API, PostgreSQL, Redis)?",
  "Define separate services in docker-compose.yml with dedicated Dockerfiles. Use multi-stage builds for frontend (Node build stage, Nginx production stage) and backend. Configure internal bridge networks, bind application volumes for development hot-reloading, configure healthchecks on Postgres and Redis, and manage secrets via environment variables.")
q("Full Stack Developer", "Technical Interview", "Hard", "Real-Time Collaboration Architecture",
  "How would you architect a full-stack real-time collaboration pipeline using WebSockets and a Redis Pub/Sub backplane?",
  "Clients connect via WebSocket to stateless API gateways. When a user mutates shared state, the gateway validates permissions, applies business rules, persists changes to the database, and publishes an event to a Redis Pub/Sub channel. Other gateway instances subscribed to the channel receive the message and broadcast it to their connected WebSocket clients.")
q("Full Stack Developer", "Technical Interview", "Hard", "Full Stack Type Safety",
  "How do you achieve end-to-end type safety between database schemas, backend API contracts, and frontend components?",
  "Use an ORM with code-generation (e.g. Prisma or SQLAlchemy + Pydantic) to derive TypeScript types or schema validation models directly from database tables. Expose APIs through OpenAPI specs with automated client generation, or use tRPC / GraphQL Code Generator so changes in backend models immediately trigger compile-time type errors in frontend code.")

# Behavioral (5 questions)
q("Full Stack Developer", "Behavioral Interview", "Easy", "End-to-End Ownership",
  "Tell me about a project where you built a complete feature end-to-end from database schema design to responsive UI. What were the biggest hurdles?",
  "I built an automated invoicing feature. I designed the SQL tables, built RESTful endpoints with Flask, and developed the React UI with real-time PDF generation. The hardest part was coordinating timezone conversions across server and client, which I resolved by standardizing on UTC internally.")
q("Full Stack Developer", "Behavioral Interview", "Easy", "Adapting to Unfamiliar Tools",
  "Tell me about a time when you had to take over an unfamiliar part of the stack outside your comfort zone. How did you succeed?",
  "Our team needed a sudden database migration and I had primarily worked on frontend. I studied our ORM documentation, reviewed past migration scripts, paired with our senior backend engineer, and wrote automated migration rollback tests before executing.")
q("Full Stack Developer", "Behavioral Interview", "Medium", "Contract Misunderstandings",
  "Describe a situation where a misunderstanding between frontend expectations and backend API specifications caused a release delay. How did you resolve it?",
  "A frontend component expected dates formatted in ISO-8601 strings, but the backend returned Unix timestamps, causing date pickers to crash in staging. I took ownership, updated the backend serialization layer, established OpenAPI schema validation, and added automated contract tests in our CI pipeline.")
q("Full Stack Developer", "Behavioral Interview", "Medium", "Balancing Full Stack Polish with Velocity",
  "Tell me about a time when you had to balance frontend polish with backend query optimizations under a tight release schedule.",
  "We had 3 days to launch a customer reporting tool. I focused initial hours on optimizing the SQL queries with indexes to ensure fast responses, and used our pre-existing UI design system components to build a clean interface quickly without writing custom CSS from scratch.")
q("Full Stack Developer", "Behavioral Interview", "Hard", "Client vs Server Computation Trade-off",
  "Tell me about a time when you had to decide whether to place a heavy computational workload on the client browser or the backend server. What data informed your trade-off?",
  "We had an analytics filter recalculating metric summaries over 50,000 datapoints. Running it on the backend incurred high network transfer overhead, while client-side processing caused jank on budget mobile devices. I benchmarked both and designed a hybrid solution: pre-aggregated rollup buckets computed on the server, with lightweight client-side filtering.")

# Scenario Based (5 questions)
q("Full Stack Developer", "Scenario Based Interview", "Easy", "Infinite Spinner Triage",
  "A customer reports that submitting a checkout form shows an infinite spinner with no error message. How do you triage whether the issue is client-side, API, or database?",
  "I inspect browser DevTools Network tab to see if the HTTP request was sent, is pending, or failed. If pending, check backend logs for database lock contention or thread hangs. If failed with CORS or 5xx, inspect gateway logs. If no request was sent, check client console for unhandled JavaScript exceptions preventing the submission.")
q("Full Stack Developer", "Scenario Based Interview", "Easy", "Cross-Domain Cookie Rejection",
  "After deploying a frontend to a separate subdomain, users can no longer stay logged in. How do you resolve this cookie authentication issue?",
  "Check cookie attributes: configure 'Domain=.yourdomain.com' so cookies are shared across subdomains, ensure 'SameSite=Lax' or 'None' (with Secure flag enabled over HTTPS), and verify backend CORS headers include 'Access-Control-Allow-Credentials: true'.")
q("Full Stack Developer", "Scenario Based Interview", "Medium", "Session Leaks Behind Reverse Proxy",
  "An intermittent bug occurs where users occasionally see another user's profile data after logging in through a shared reverse proxy. What architectural flaw causes this?",
  "The reverse proxy (e.g. Nginx, Cloudflare) is caching authenticated dynamic API responses because the backend failed to send 'Cache-Control: private, no-store, no-cache'. The proxy serves the cached response of the first user to subsequent requests. Remediate immediately by auditing Cache-Control headers on all authenticated endpoints.")
q("Full Stack Developer", "Scenario Based Interview", "Medium", "Database Deadlock on Concurrent Form Submits",
  "Your application logs report SQL deadlock exceptions when two users simultaneously edit the same shared record. How do you resolve this full-stack?",
  "Implement optimistic concurrency control: add a version integer column on the entity. When frontend sends updates, include the known version. If another write updated the version in the interim, reject with HTTP 409 Conflict and prompt the frontend user to merge or refresh changes.")
q("Full Stack Developer", "Scenario Based Interview", "Hard", "Inventory Race Conditions",
  "Your full stack application experiences race conditions when multiple users simultaneously attempt to purchase the last available stock item. How do you redesign the flow?",
  "Use database-level pessimistic locking ('SELECT ... FOR UPDATE') or optimistic concurrency control with a version column ('UPDATE inventory SET quantity = quantity - 1 WHERE id = :id AND version = :v'). Reject transactions if affected rows equal zero. For high traffic, manage stock reservations in Redis using atomic Lua decrement scripts.")

# Problem Solving (5 questions)
q("Full Stack Developer", "Problem Solving Interview", "Easy", "Direct-to-S3 File Upload",
  "How would you design a full stack file upload system supporting drag-and-drop, client-side progress bars, and direct upload to S3 using pre-signed URLs?",
  "Client initiates upload by sending file metadata (name, size, MIME type) to backend. Backend validates permissions and returns a short-lived S3 pre-signed PUT URL. Client uploads file directly to S3 via XMLHttpRequest or fetch with progress listeners, bypassing application servers. Upon S3 completion, client notifies backend to record the file URI.")
q("Full Stack Developer", "Problem Solving Interview", "Easy", "CSV Export Feature",
  "How would you implement a full stack feature allowing users to export 100,000 database records to a downloadable CSV without freezing the web server?",
  "Do not buffer 100,000 records in backend RAM. Implement streaming HTTP response (StreamingResponse in FastAPI/Flask with chunked transfer encoding) reading database records using server-side cursors in batches, piping directly into the HTTP response stream.")
q("Full Stack Developer", "Problem Solving Interview", "Medium", "Audit Logging System",
  "How would you design an end-to-end user activity audit log system that captures user actions in the frontend and persists immutable change histories in the backend?",
  "Capture significant frontend user actions with metadata (user_id, action_type, timestamp, diff) and send them through a lightweight beacon or batching queue. The backend validates and enriches events with IP, user-agent, and server timestamp, writing to an append-only audit log table with foreign key constraints, or streaming to an immutable data store like Elasticsearch.")
q("Full Stack Developer", "Problem Solving Interview", "Medium", "Real-Time User Notification Badge",
  "How would you design a live unread notification badge system where the count updates in real-time across multiple open browser tabs?",
  "Use Server-Sent Events (SSE) or WebSockets from the backend publishing notification events. On the frontend, receive the event and broadcast it across browser tabs using the BroadcastChannel API so all tabs synchronize their badge counters instantly without polling.")
q("Full Stack Developer", "Problem Solving Interview", "Hard", "Real-Time Collaborative Editor",
  "How would you architect a real-time collaborative document editor (similar to Google Docs) supporting concurrent multi-user editing and conflict resolution?",
  "Use Conflict-free Replicated Data Types (CRDTs via Yjs or Automerge) over WebSockets. Each character insertion/deletion represents an operation with a unique Lamport timestamp and peer ID. Clients apply edits locally with zero latency and broadcast operations to a WebSocket server cluster backed by Redis Pub/Sub, ensuring eventual consistency across all peers.")

# HR (5 questions)
q("Full Stack Developer", "HR Interview", "Easy", "Full Stack Motivation",
  "What do you enjoy most about being a full-stack developer rather than specializing strictly in frontend or backend?",
  "I enjoy having a panoramic view of the entire software ecosystem. Being able to conceptualize a feature, design the database schema, write the API, and craft the interactive UI gives me immense satisfaction and allows me to deliver value quickly.")
q("Full Stack Developer", "HR Interview", "Easy", "Adapting to Team Needs",
  "How do you handle situations where a sprint requires you to pivot and spend 100% of your time on backend or frontend depending on team needs?",
  "I embrace flexibility: my goal is shipping user value. If the frontend team is blocked by backend APIs, I focus on backend; if the backend is complete and UI implementation is the bottleneck, I lean into the frontend.")
q("Full Stack Developer", "HR Interview", "Medium", "Context-Switching Across Stack",
  "How do you manage your time when a sprint requires you to context-switch between UI component polish and database schema migrations?",
  "I time-box my focus sessions: I dedicate mornings to complex backend logic and database architecture when my focus is highest, and afternoons to UI styling, component wiring, and integration testing. Documenting progress before switching contexts prevents cognitive fatigue.")
q("Full Stack Developer", "HR Interview", "Medium", "Preventing Full Stack Burnout",
  "How do you keep up with learning across the entire stack without feeling overwhelmed by constant tech churn?",
  "I focus on foundational software principles—networking, data structures, caching, component state machines—rather than chasing every library. These fundamental concepts remain steady across framework transitions.")
q("Full Stack Developer", "HR Interview", "Hard", "Breadth vs Depth Growth",
  "How do you maintain deep expertise across both frontend and backend technologies without feeling spread too thin?",
  "I focus on mastering fundamental computer science principles that transcend frameworks: data structures, networking, caching, and state machines. When frameworks evolve, these core primitives make adopting new tools fast and intuitive.")

# ==============================================================================
# 5. JAVA DEVELOPER
# ==============================================================================
# Technical (8 questions)
q("Java Developer", "Technical Interview", "Easy", "JVM, JRE, and JDK",
  "Explain the differences between JVM, JRE, and JDK in the Java runtime ecosystem.",
  "JDK (Java Development Kit) is the complete software package containing the compiler (javac), debugger, and development tools. JRE (Java Runtime Environment) provides the libraries and runtime needed to execute compiled bytecode. JVM (Java Virtual Machine) is the abstract execution engine that translates Java bytecode into native machine instructions on the host OS.")
q("Java Developer", "Technical Interview", "Easy", "OOP: Overloading vs Overriding",
  "Explain method overloading versus method overriding in Java, including rules for return types and polymorphism.",
  "Method overloading (compile-time polymorphism) occurs within the same class when methods share a name but differ in argument count or types; return types alone cannot differentiate overloads. Method overriding (runtime polymorphism) occurs when a subclass redefines a parent class method with the exact same signature and compatible return type using the @Override annotation.")
q("Java Developer", "Technical Interview", "Easy", "String Constant Pool",
  "Why are String objects immutable in Java, and how does the String Constant Pool optimize memory?",
  "String immutability guarantees thread safety, security (for database connection strings, network ports, and class loading), and hash code caching for collections like HashMap. The String Constant Pool is a special memory region in the JVM heap: when a string literal is created, the JVM checks the pool to reuse existing instances rather than allocating duplicate heap memory.")
q("Java Developer", "Technical Interview", "Medium", "Java Concurrency & Locks",
  "Explain the difference between synchronized blocks, volatile variables, and ReentrantLock in Java concurrency.",
  "The 'synchronized' keyword provides mutual exclusion and visibility by acquiring intrinsic object monitor locks, blocking waiting threads. 'volatile' guarantees memory visibility across threads by bypassing CPU caches, but does not provide mutual exclusion. ReentrantLock provides explicit locking with advanced capabilities: timed lock waits (tryLock), fairness policies, and multiple Condition variables.")
q("Java Developer", "Technical Interview", "Medium", "HashMap Collision Resolution",
  "How does HashMap handle bucket collisions internally in Java 8+, and why does it convert LinkedLists to Red-Black Trees?",
  "HashMap computes key hash code to locate the bucket array index. When multiple keys hash to the same bucket, entries are stored in a linked list. In Java 8+, when bucket entries exceed TREEIFY_THRESHOLD (8 items) and array capacity is at least 64, the linked list converts to a balanced Red-Black Tree, improving worst-case search complexity from O(N) to O(log N).")
q("Java Developer", "Technical Interview", "Medium", "Spring Boot Dependency Injection",
  "How does Dependency Injection (DI) and Inversion of Control (IoC) work in Spring Boot, and what is the difference between @Component and @Bean?",
  "IoC delegates object lifecycle and dependency management to the Spring IoC Container. Spring injects dependencies using constructor, setter, or field injection. @Component is a class-level annotation indicating auto-detection via component scanning. @Bean is a method-level annotation used within @Configuration classes to manually instantiate and configure third-party or custom beans.")
q("Java Developer", "Technical Interview", "Hard", "Garbage Collection Tuning",
  "Describe the Java Garbage Collection generational heap structure (Eden, Survivor, Tenured) and explain how the G1 GC collector works.",
  "The JVM heap splits into Young Generation (Eden and two Survivor spaces: S0, S1) and Old (Tenured) Generation. New objects allocate in Eden; survivors of Minor GC cycles copy between Survivor spaces, promoting to Tenured after reaching an aging threshold. The G1 (Garbage-First) GC divides the heap into equal-sized regions and prioritizes collecting regions with the most garbage ('garbage-first') to meet predictable pause-time targets.")
q("Java Developer", "Technical Interview", "Hard", "Java 21 Virtual Threads vs Platform Threads",
  "How do Java 21 Virtual Threads (Project Loom) differ from traditional Platform Threads in execution and operating system mapping?",
  "Platform threads are 1:1 wrappers around heavy OS kernel threads, limited to a few thousand instances due to large stack memory allocations (typically 1MB). Virtual Threads are lightweight user-mode threads managed by the JVM. Millions of virtual threads can run concurrently; when a virtual thread encounters blocking I/O, the JVM unmounts it from the carrier OS thread, freeing the carrier to execute other work.")

# Behavioral (5 questions)
q("Java Developer", "Behavioral Interview", "Easy", "Refactoring Legacy Code",
  "Tell me about a time when you refactored legacy Java code to adhere to clean coding or SOLID principles. What approach did you take?",
  "I inherited a 1,500-line monolithic service class with nested if-else blocks handling payment processing. I introduced the Strategy Pattern: created a PaymentStrategy interface with distinct implementations for CreditCard, PayPal, and BankTransfer, injected via Spring factory, reducing class size by 70% and enabling isolated unit testing.")
q("Java Developer", "Behavioral Interview", "Easy", "Adopting Modern Java Features",
  "Tell me about a time when you advocated for adopting modern Java features (like Streams, Optionals, or Records) on your team.",
  "Our codebase was filled with verbose boilerplate DTOs and defensive null checks. I demonstrated how Java Records and Optional reduce boilerplate by 80% while making immutable domain contracts explicit, leading our team to adopt them in our next sprint.")
q("Java Developer", "Behavioral Interview", "Medium", "Hunting Concurrency Bugs",
  "Describe a time when you encountered an elusive multithreading race condition or concurrency bug in Java. How did you track it down?",
  "Our billing batch job intermittently produced duplicate invoice numbers under concurrent execution. I identified that developers used SimpleDateFormat across threads (which is not thread-safe). I captured thread dumps using jstack, verified the race condition, and refactored the service to use java.time.format.DateTimeFormatter and AtomicLong sequence generators.")
q("Java Developer", "Behavioral Interview", "Medium", "Resolving JPA/Hibernate N+1 Issues",
  "Tell me about a time when an unoptimized Hibernate query caused severe database slowdown. How did you fix it?",
  "An endpoint loading customer orders executed 100 individual SQL queries for each line item (N+1 problem). I used Hibernate query logging to identify the issue, added a JOIN FETCH clause in our Spring Data repository, and brought query count down to 1, reducing response time from 1.8s to 45ms.")
q("Java Developer", "Behavioral Interview", "Hard", "Major Java Version Migration",
  "Tell me about a time when you had to lead a major enterprise Java version migration (e.g. Java 8/11 to Java 17/21). What challenges arose and how did you navigate them?",
  "I led our team's migration from Java 8 to Java 17. The primary hurdle was the strong encapsulation of JDK internals (JEP 396) which broke older reflection libraries. I ran JDeps to identify incompatible dependencies, updated Spring Boot and ByteBuddy versions, resolved illegal reflective access warnings, and unlocked 20% lower GC pause times.")

# Scenario Based (5 questions)
q("Java Developer", "Scenario Based Interview", "Easy", "NoSuchBeanDefinitionException Triage",
  "A Java Spring Boot application fails to start in staging with a NoSuchBeanDefinitionException. What is your diagnostic checklist to resolve this quickly?",
  "Verify that the target class has a Spring stereotype annotation (@Service, @Component, @Repository), check that the class package is within the @ComponentScan base package hierarchy, verify that conditional annotations (@ConditionalOnProperty) are satisfied, and check if profile annotations (@Profile) match the active Spring profile.")
q("Java Developer", "Scenario Based Interview", "Easy", "NullPointerException in Production Stream",
  "A Java Stream pipeline processing customer records throws a NullPointerException in production on null map entries. How do you handle this cleanly?",
  "Add a .filter(Objects::nonNull) step prior to mapping, use Optional.ofNullable() within transformation functions, and configure Nullable/NotNull annotations with SonarQube static analysis to catch potential nulls during build.")
q("Java Developer", "Scenario Based Interview", "Medium", "Stop-The-World GC Pauses",
  "A Java microservice in production triggers frequent Stop-The-World GC pauses, causing health-check timeouts and container restarts. What steps do you take to stabilize it?",
  "Enable GC logging (-Xlog:gc*:file=gc.log) and capture heap dumps via jcmd or -XX:+HeapDumpOnOutOfMemoryError. Analyze heap dumps using Eclipse Memory Analyzer (MAT) to identify memory leaks or retention dominator trees. Tune JVM heap ratios (-Xms, -Xmx) and evaluate switching from Parallel GC to G1 or ZGC for sub-millisecond pause guarantees.")
q("Java Developer", "Scenario Based Interview", "Medium", "HikariCP Connection Pool Timeout",
  "Your Spring Boot application logs show 'HikariPool-1 - Connection is not available, request timed out after 30000ms'. What is your remediation process?",
  "Check whether long-running queries or uncommitted transactions are holding connections open. Profile active connection durations via Spring Boot Actuator metrics. Increase pool size if database capacity allows, ensure all transaction scopes (@Transactional) are tight, and add connection timeout guards.")
q("Java Developer", "Scenario Based Interview", "Hard", "Database Deadlocks in Banking Transactions",
  "A high-concurrency Java banking service experiences database deadlocks under heavy concurrent balance transfers between accounts. How do you eliminate deadlocks?",
  "Deadlocks occur when Thread A locks Account 1 then requests Account 2, while Thread B locks Account 2 then requests Account 1. Resolve this by enforcing consistent lock ordering: always acquire locks on accounts sorted by Account ID (e.g. lock min(acc1, acc2) first, then max(acc1, acc2)). This guarantees all concurrent threads acquire resources in identical sequence, mathematically preventing circular waits.")

# Problem Solving (5 questions)
q("Java Developer", "Problem Solving Interview", "Easy", "Thread-Safe Singleton",
  "How would you implement a thread-safe Singleton pattern in Java using double-checked locking, and explain why the volatile keyword is mandatory?",
  "Use a private constructor and a private static volatile instance variable. In getInstance(), check if instance is null; if so, synchronize on the class object and check null again before instantiating. The 'volatile' keyword is mandatory to prevent JVM instruction reordering where memory is allocated and assigned before constructor execution completes.")
q("Java Developer", "Problem Solving Interview", "Easy", "Custom Exception Hierarchy",
  "How would you design a clean custom exception hierarchy in Java for an enterprise order-processing service?",
  "Create an abstract BaseApplicationException extending RuntimeException. Derive specific domain exceptions (e.g. OrderNotFoundException, InsufficientInventoryException, PaymentGatewayException) with structured error codes and HTTP status mapping. Handle centrally using Spring's @ControllerAdvice.")
q("Java Developer", "Problem Solving Interview", "Medium", "Custom ThreadPoolExecutor Configuration",
  "How would you design a custom thread pool in Java using ThreadPoolExecutor for a CPU-bound vs I/O-bound workload?",
  "For CPU-bound tasks, set core and max pool size to Runtime.getRuntime().availableProcessors() + 1 to prevent excessive thread context switching. For I/O-bound tasks, set pool size higher (e.g. 2x - 4x CPU cores) to keep cores saturated while threads await I/O. Use a bounded ArrayBlockingQueue with an explicit RejectedExecutionHandler (CallerRunsPolicy) to apply natural backpressure under overload.")
q("Java Developer", "Problem Solving Interview", "Medium", "Thread-Safe In-Memory Cache with ConcurrentHashMap",
  "How would you implement a thread-safe, high-concurrency in-memory cache in Java with entry TTL expiration without blocking reads?",
  "Use a ConcurrentHashMap storing CacheEntry(value, expiryTimestamp). Reads check expiryTimestamp in O(1) lock-free time; if expired, remove and return null. A ScheduledExecutorService runs a background cleanup worker every 60 seconds to sweep and evict expired entries without blocking concurrent readers.")
q("Java Developer", "Problem Solving Interview", "Hard", "High-Throughput Order Matching Engine",
  "How would you design a high-throughput Java financial matching engine that processes 50,000 order transactions per second with sub-millisecond latency?",
  "Avoid standard garbage collection churn by using the LMAX Disruptor ring buffer pattern instead of standard queues. Use lock-free, zero-allocation data structures with off-heap memory (Unsafe or Foreign Function & Memory API). Pin critical threads to dedicated CPU cores using thread affinity, keeping hot order books in CPU L1/L2 caches.")

# HR (5 questions)
q("Java Developer", "HR Interview", "Easy", "Ecosystem Dedication",
  "What has kept you dedicated to the Java ecosystem, and what modern Java features do you find most impactful in your daily workflow?",
  "Java's backward compatibility, rock-solid enterprise stability, and the vibrant open-source ecosystem make it an engineering powerhouse. Recent innovations like Records, Pattern Matching, and Virtual Threads have made the language concise and modern.")
q("Java Developer", "HR Interview", "Easy", "Enterprise Software Engineering Values",
  "What qualities do you look for in an enterprise Java engineering team?",
  "I value teams that take pride in clean domain-driven architecture, robust testing standards, blameless post-mortems, and continuous professional growth.")
q("Java Developer", "HR Interview", "Medium", "Testing Culture with JUnit & Mockito",
  "How do you ensure strong unit test and integration test coverage using JUnit 5 and Mockito in enterprise delivery pipelines?",
  "I follow test-driven patterns where unit tests verify isolated business rules with mocked dependencies using Mockito, and SpringBootTest/Testcontainers verify real database queries against containerized PostgreSQL. I enforce code coverage thresholds in CI to maintain software quality.")
q("Java Developer", "HR Interview", "Medium", "Handling Legacy Enterprise Codebases",
  "How do you stay motivated and deliver value when working with complex legacy Java systems that cannot be immediately rewritten?",
  "I approach legacy code with respect for the business value it generates. I improve it incrementally: writing regression tests before modifying code, decoupling modules sprint by sprint, and celebrating small refactoring wins that improve stability.")
q("Java Developer", "HR Interview", "Hard", "Standardization vs Developer Autonomy",
  "In large enterprise environments, how do you balance following strict corporate Java frameworks with adopting newer, lighter tools?",
  "I respect enterprise guardrails that guarantee security, observability, and compliance, while advocating for innovation through controlled proof-of-concept projects. Demonstrating tangible developer productivity or cost savings builds trust with architecture committees.")

# ==============================================================================
# 6. UI/UX DESIGNER
# ==============================================================================
# Technical (8 questions)
q("UI/UX Designer", "Technical Interview", "Easy", "UI vs UX Fundamentals",
  "What is the fundamental difference between User Experience (UX) and User Interface (UI) design, and how do they collaborate?",
  "UX design focuses on the user's overall journey, information architecture, pain points, and usability testing to ensure a product solves real needs intuitively. UI design focuses on the visual and interactive surface: typography, color systems, spacing, component aesthetics, and micro-interactions. UX defines how it works; UI defines how it looks and feels.")
q("UI/UX Designer", "Technical Interview", "Easy", "Visual Hierarchy Principles",
  "Explain the core principles of Visual Hierarchy (scale, contrast, proximity, spacing) and how they guide user attention on a landing page.",
  "Visual hierarchy organizes elements so users naturally digest information in order of importance. Scale uses size to indicate prominence; Contrast directs the eye to primary CTAs against background canvas; Proximity groups related items (e.g. labels next to inputs); Spacing (white space) prevents cognitive overload and creates elegance.")
q("UI/UX Designer", "Technical Interview", "Easy", "WCAG Accessibility Standards",
  "What are the WCAG 2.1 AA accessibility requirements regarding text color contrast ratios and interactive touch target sizing?",
  "WCAG 2.1 AA requires a minimum contrast ratio of 4.5:1 for normal body text and 3:1 for large text (18pt or 14pt bold) against its background. For mobile and touch interactions, interactive targets (buttons, icons) should have a minimum hit area of 44x44 CSS pixels to ensure accessible operation for users with motor impairments.")
q("UI/UX Designer", "Technical Interview", "Medium", "Design Systems & Tokens",
  "How do design tokens help maintain visual consistency across Web, iOS, and Android platforms, and how do you structure them?",
  "Design tokens are platform-agnostic key-value pairs representing design decisions (colors, spacing, typography, elevation). They are structured in tiers: Global tokens (e.g. 'blue-500: #3b82f6'), Semantic tokens (e.g. 'color-brand-primary: {blue-500}'), and Component tokens (e.g. 'btn-bg-primary: {color-brand-primary}'). Automated build tools transform them into CSS variables, Swift constants, and Android XML.")
q("UI/UX Designer", "Technical Interview", "Medium", "Usability Testing Synthesis",
  "How do you conduct and synthesize findings from qualitative usability testing sessions (moderated vs unmoderated)?",
  "Define research objectives, recruit representative user cohorts, and formulate unbiased task prompts. During sessions, observe behaviors and think-aloud feedback without leading the participant. Synthesize data using affinity mapping: cluster observations into patterns, calculate Task Completion Rate and System Usability Scale (SUS), and prioritize usability issues by severity.")
q("UI/UX Designer", "Technical Interview", "Medium", "Micro-Interactions & Feedback",
  "What role do micro-interactions play in user experience, and what are the four stages of a micro-interaction (Trigger, Rules, Feedback, Loops/Modes)?",
  "Micro-interactions provide delightful, clear feedback that reinforces system state. Trigger initiates the interaction (user clicks toggle). Rules determine what happens (toggle changes active boolean). Feedback communicates the state change (smooth color transition and haptic vibration). Loops/Modes govern duration and repeat behaviors (e.g. auto-save indicator fading out after 2s).")
q("UI/UX Designer", "Technical Interview", "Hard", "Data-Dense Enterprise UX",
  "How do you design data-dense interfaces (complex financial tables, analytics dashboards) that remain ergonomic, legible, and responsive?",
  "Prioritize progressive disclosure: show summary metrics upfront and allow drill-downs via expanding rows or side sheets. In tables, pin freeze-columns (IDs and primary names), provide customizable column visibility, use monospaced numerals for right-aligned data, provide dense/compact view toggles, and use subtle zebra striping with hover row highlighting.")
q("UI/UX Designer", "Technical Interview", "Hard", "Measuring UX ROI",
  "How do you define and track quantitative UX metrics (SUS, Time on Task, Drop-off, CSAT) to demonstrate business ROI to executive leadership?",
  "Align UX improvements directly with revenue and efficiency KPIs: track Time on Task to prove operational labor cost reduction in internal tools; measure Funnel Drop-off rates and Task Completion Rates to demonstrate conversion gains; administer regular System Usability Scale (SUS) benchmarking surveys to track satisfaction trends over product releases.")

# Behavioral (5 questions)
q("UI/UX Designer", "Behavioral Interview", "Easy", "Handling Stakeholder Critique",
  "Tell me about a time when a stakeholder disliked your visual design. How did you handle the critique and iterate?",
  "A product lead felt my checkout redesign was too stark. Rather than taking it defensively, I asked open-ended questions to uncover their underlying concern: they feared users would miss security assurances. I incorporated trust badges, SSL icons, and subtle elevation without cluttering the clean layout, winning enthusiastic approval.")
q("UI/UX Designer", "Behavioral Interview", "Easy", "Conducting User Interviews",
  "Tell me about a time when user interviews provided an unexpected insight that changed your design approach.",
  "While designing a scheduling tool, I observed that doctors rarely used desktop computers during patient consults. They relied entirely on one-handed mobile tablet interactions, which prompted us to pivot the design to large thumb-accessible action sheets.")
q("UI/UX Designer", "Behavioral Interview", "Medium", "Research Challenging Assumptions",
  "Describe a project where user research directly challenged your initial design hypothesis. How did you pivot the design direction?",
  "I designed a dashboard assuming power users wanted comprehensive filtering options exposed on the homepage. Usability testing revealed that 80% of participants felt overwhelmed and abandoned tasks. I pivoted to a simplified search-first interface with progressive disclosure for advanced filters, which increased task completion from 55% to 92%.")
q("UI/UX Designer", "Behavioral Interview", "Medium", "Collaborating with Frontend Engineers",
  "Tell me about a time when technical constraints prevented an engineering team from implementing your exact design. How did you compromise?",
  "A complex layout animation caused frame drops on older Android devices. I paired with the frontend developer in Figma, explored native CSS transitions, and simplified the spring animation into a clean fade-and-slide effect that preserved delight while running smoothly at 60fps.")
q("UI/UX Designer", "Behavioral Interview", "Hard", "Defending UX in MVP Scope",
  "Tell me about a time when engineering or product wanted to cut critical accessibility or usability features from an MVP. How did you advocate for users?",
  "Engineering proposed cutting keyboard navigation and focus rings from a form release to save sprint time. I demonstrated how this would exclude keyboard-only and screen-reader users, exposing the company to legal compliance risk under ADA/WCAG. I worked with engineers to identify quick-win semantic HTML fixes that restored full accessibility with minimal dev effort.")

# Scenario Based (5 questions)
q("UI/UX Designer", "Scenario Based Interview", "Easy", "Mobile CTA Abandonment",
  "A client reports that users are consistently missing the primary 'Checkout' button on a mobile site. What design audits and changes do you conduct?",
  "Audit the screen using visual contrast analyzers and eye-tracking heuristics: check if the button is pushed below the fold by large hero images, has insufficient contrast against background cards, or competes visually with nearby promotional banners. Fix by implementing a high-contrast sticky bottom CTA bar with safe-area spacing.")
q("UI/UX Designer", "Scenario Based Interview", "Easy", "Form Error State Confusion",
  "Users report getting frustrated because a long registration form clears input fields when an error occurs. How do you redesign this interaction?",
  "Preserve all entered user data, highlight the specific invalid inputs with clear red borders and descriptive helper text below the field (e.g. 'Password must include at least 1 number'), and auto-scroll the viewport to the first invalid field upon submit.")
q("UI/UX Designer", "Scenario Based Interview", "Medium", "Funnel Drop-Off Redesign",
  "Your analytics show a 45% drop-off rate on step 3 of a 5-step registration onboarding funnel. Walk me through how you investigate and redesign the experience.",
  "Inspect session replays (FullStory/Hotjar) on step 3 to observe user confusion or form validation rage clicks. Identify whether step 3 asks for sensitive data (SSN, credit card) prematurely without explanation. Redesign by reducing required inputs, adding inline helper explanations on why data is needed, and introducing a clear progress step indicator.")
q("UI/UX Designer", "Scenario Based Interview", "Medium", "Dark Mode Inversion Pitfalls",
  "A company hastily launches Dark Mode by inverting all colors, resulting in unreadable text and harsh saturated contrast. How do you design an authentic dark mode?",
  "Do not use pure black (#000000) or pure white (#FFFFFF); use dark grays (#121212, #1E1E1E) with subtle elevation layers (lighter grays indicating elevation). Desaturate vibrant primary brand colors to prevent eye strain, and verify WCAG contrast compliance for all text tiers.")
q("UI/UX Designer", "Scenario Based Interview", "Hard", "Fragmented Design Debt Cleanup",
  "You join a SaaS company with 5 years of accumulated UI inconsistencies and no design system. Engineering refuses a full rewrite. How do you bring order iteratively?",
  "Conduct a comprehensive UI audit: inventory all button variants, font styles, and color hexes into a shared audit deck to illustrate the fragmentation. Create an MVP core design system in Figma focusing on the top 5 high-impact components (Button, Input, Modal, Typography, Card). Partner with engineers to replace components incrementally sprint-by-sprint during regular feature work.")

# Problem Solving (5 questions)
q("UI/UX Designer", "Problem Solving Interview", "Easy", "Complex Settings Redesign",
  "How would you redesign a confusing, cluttered settings page with over 50 configuration options to make it easy for users to find what they need?",
  "Group settings into intuitive, user-centered categories (Account, Security, Notifications, Billing) validated via card-sorting research. Implement a prominent global search bar with instant query highlighting, use clean toggle switches with inline status descriptions, and separate advanced developer settings into a collapsed progressive disclosure section.")
q("UI/UX Designer", "Problem Solving Interview", "Easy", "E-Commerce Filter Navigation",
  "How would you design a responsive filter drawer for an apparel e-commerce store with over 20 filter facets (size, color, brand, price, fit)?",
  "On desktop, use an expandable left sidebar with active filter chips at the top and clear counts. On mobile, provide a floating 'Filter & Sort' pill that opens a full-height bottom sheet with sticky 'View Results (240)' button updating counts dynamically.")
q("UI/UX Designer", "Problem Solving Interview", "Medium", "Sensitive Healthcare Onboarding",
  "How would you design a mobile onboarding flow for a healthcare app that must collect sensitive medical history while keeping the user engaged and feeling secure?",
  "Break the intake into bite-sized, single-topic cards rather than a monolithic form. Provide prominent privacy trust badges ('HIPAA Compliant & Encrypted'), explain plainly why each health question is needed, allow users to save progress and complete later, and use empathetic, conversational copy.")
q("UI/UX Designer", "Problem Solving Interview", "Medium", "Search Autocomplete with Categorized Results",
  "How would you design an omnichannel search autocomplete dropdown that displays matching products, articles, and brand categories simultaneously?",
  "Group results into clear visual sections with subtle headers (Suggested Products, Help Articles, Categories). Use bold text to highlight matching query substrings, display product thumbnails with prices, and support full keyboard navigation (Up/Down arrow keys and Enter to select).")
q("UI/UX Designer", "Problem Solving Interview", "Hard", "Enterprise RBAC Permissions Interface",
  "How would you design an intuitive permissions management interface for enterprise teams with granular role-based access control (RBAC) across hundreds of users and projects?",
  "Design a matrix view with role templates (Admin, Editor, Viewer, Custom) that allow one-click bulk assignment. For granular permissions, use an accordion hierarchy grouped by resource domain. Provide an interactive 'Permission Preview' simulator allowing administrators to test and see the exact UI perspective of any user before applying changes.")

# HR (5 questions)
q("UI/UX Designer", "HR Interview", "Easy", "Design Passion & Inspiration",
  "What sparked your passion for UI/UX design, and what design portfolio piece are you most proud of?",
  "I was inspired by how thoughtful design can remove frustration from everyday life and empower people. I am most proud of redesigning a patient portal where intuitive workflows and accessible typography helped elderly patients schedule appointments independently.")
q("UI/UX Designer", "HR Interview", "Easy", "Handling Creative Roadblocks",
  "How do you overcome creative burnout or design roadblocks when working on complex enterprise workflows?",
  "I step away from Figma to study how completely different industries solve complex data problems, sketch low-fidelity ideas on paper without pixel constraints, and conduct quick informal user interviews to reconnect with genuine user needs.")
q("UI/UX Designer", "HR Interview", "Medium", "Cross-Disciplinary Design Critiques",
  "How do you facilitate productive design critiques with engineers and product managers who may not have formal design backgrounds?",
  "I frame critiques around objective user problems rather than subjective aesthetic preferences. I present designs alongside user research data, outline specific constraints, and ask targeted questions like 'Does this component clearly communicate system state?' to foster constructive technical collaboration.")
q("UI/UX Designer", "HR Interview", "Medium", "Design Mentorship & Growth",
  "How do you share design methodologies and mentor junior designers or non-designers in your organization?",
  "I conduct open design critique sessions, document design system guidelines with detailed usage dos-and-don'ts in Zeroheight or Storybook, and lead workshops on user interviewing techniques for product managers.")
q("UI/UX Designer", "HR Interview", "Hard", "Advocating for User-Centered Culture",
  "How do you advocate for user-centered design in an organization that has historically been engineering-driven or sales-driven?",
  "I bridge the gap by connecting UX directly to commercial metrics: showing how confusing flows cause churn or increase customer support ticket costs. Inviting engineers and sales leaders to observe live usability testing sessions builds instant empathy for user struggles.")

print(f"Part 2 compiled: {len(PART2_ENTRIES)} questions.")
