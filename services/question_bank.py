"""
Predefined Question Bank for InterviewAI Phase 2
Contains 50+ Technical Questions & 30+ HR Questions categorized by Role, Topic, and Difficulty.
"""

QUESTION_BANK = [
    # ==========================================
    # PYTHON DEVELOPER - TECHNICAL (10 Questions)
    # ==========================================
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "Python Fundamentals",
        "question": "What is the difference between list mutability and tuple immutability in Python, and when should you prefer a tuple?",
        "sample_answer": "Lists are mutable data structures in Python, meaning elements can be modified, added, or removed after creation using methods like append() or extend(). Tuples are immutable sequence objects whose elements cannot be altered once instantiated. Tuples should be preferred when returning multiple values from a function, defining fixed configuration keys, or using sequence items as dictionary keys (since tuple hashable property is preserved)."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "Memory Management",
        "question": "Explain how garbage collection and reference counting work in Python.",
        "sample_answer": "Python uses reference counting as its primary memory management mechanism. Every object maintains a counter of active references. When an object's reference count drops to zero, Python immediately deallocates its memory. To handle circular references (e.g. object A referencing object B and vice versa), Python includes a generational garbage collector that periodically detects and cleans unreachable reference cycles."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Advanced Decorators",
        "question": "How do Python decorators work under the hood? Write a brief conceptual explanation of a decorator that accepts parameters.",
        "sample_answer": "A decorator in Python is a callable object (function or class) that takes another function as an argument and extends its behavior without explicitly modifying its source code. When a decorator accepts parameters, it requires three nested functions: the outer function receives the decorator arguments, the middle wrapper receives the target function, and the inner wrapper executes target logic with *args and **kwargs."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Async & Concurrency",
        "question": "What is the GIL (Global Interpreter Lock) in CPython, and how does asyncio differ from multiprocessing?",
        "sample_answer": "The Global Interpreter Lock (GIL) is a mutex in CPython that prevents multiple native threads from executing Python bytecodes concurrently on separate CPU cores. Asyncio provides cooperative single-threaded event-loop concurrency ideal for I/O-bound tasks. Multiprocessing bypasses the GIL by spawning separate OS processes with dedicated memory spaces, making it optimal for CPU-bound computation."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Generators & Iterators",
        "question": "Explain the mechanics of Python generators using 'yield' versus returning a populated list from a function.",
        "sample_answer": "Functions returning lists load all items into memory simultaneously before returning. Generators use the 'yield' keyword to produce a lazy iterator stream. Memory consumption remains O(1) regardless of sequence size because values are computed on demand during iteration (__next__ calls)."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Metaclasses & OOP",
        "question": "What is a metaclass in Python, and how does class creation differ between __new__ and __init__?",
        "sample_answer": "A metaclass is a 'class of a class' that defines how a class object itself is constructed. When Python executes a class block, it calls the metaclass's __new__ method to allocate the class object, followed by __init__ to initialize its attributes before returning it."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Context Managers",
        "question": "How do context managers handle exceptions raised within a 'with' block via __exit__?",
        "sample_answer": "The __exit__(self, exc_type, exc_val, exc_tb) method receives exception details if an error occurs within the block. If __exit__ returns True, the exception is suppressed and program execution continues smoothly after the with statement. If it returns False or None, the exception propagates normally."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Data Structures",
        "question": "How are Python dictionaries implemented under the hood since Python 3.6 to guarantee insertion order?",
        "sample_answer": "Dictionaries use a dual-array architecture: a dense array storing (hash, key, value) tuples in insertion order and a sparse hash table index array pointing to indices in the dense array. This drastically reduces memory overhead while preserving exact insertion order."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "Modules & Imports",
        "question": "What is the purpose of '__init__.py' and '__main__.py' in a Python package?",
        "sample_answer": "__init__.py marks a directory as a Python package namespace and executes package initialization code upon import. __main__.py defines the entry point when executing a package directly via 'python -m package_name'."
    },
    {
        "role": "Python Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Web Frameworks",
        "question": "Compare Flask and Django architecture. When would you select Flask over Django for a microservice?",
        "sample_answer": "Django is a batteries-included monolithic framework featuring an ORM, admin panel, and authentication system out of the box. Flask is a lightweight WSGI microframework providing maximum flexibility. Flask is ideal for lightweight microservices or custom tailored database architectures where minimal overhead is required."
    },

    # ==========================================
    # FRONTEND DEVELOPER - TECHNICAL (10 Questions)
    # ==========================================
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "JavaScript Fundamentals",
        "question": "Explain the difference between 'var', 'let', and 'const' in JavaScript regarding scoping and hoisting.",
        "sample_answer": "'var' is function-scoped and hoisted to the top of its scope with an initial value of undefined. 'let' and 'const' are block-scoped and hoisted into a Temporal Dead Zone (TDZ), accessing them before initialization throws a ReferenceError. 'const' additionally prevents reassignment of variable reference binding."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "CSS Layouts",
        "question": "What are the primary differences between CSS Flexbox and CSS Grid?",
        "sample_answer": "Flexbox is designed for one-dimensional layouts (either a row or a column), making it ideal for navbar alignment or button stacks. CSS Grid is designed for two-dimensional layouts (rows and columns simultaneously), making it optimal for complex page structures and photo galleries."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "DOM Performance",
        "question": "What is the Virtual DOM in modern frameworks, and how does reconciliation work?",
        "sample_answer": "The Virtual DOM is an in-memory lightweight JavaScript object representation of the real DOM. During state changes, the framework creates a new Virtual DOM tree, performs a diffing algorithm against the previous snapshot to identify minimal exact DOM mutations, and batches updates into the real browser DOM to maximize render performance."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Asynchronous JS",
        "question": "Explain Event Loop mechanics: microtasks vs macrotasks in the browser runtime.",
        "sample_answer": "The Event Loop monitors the Call Stack and Task Queues. When the call stack clears, the loop empties the Microtask Queue (Promises, process.nextTick, queueMicrotask) completely before picking a single task from the Macrotask Queue (setTimeout, setInterval, I/O events). Microtasks always take priority over macrotasks."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Web Security",
        "question": "What is CORS (Cross-Origin Resource Sharing), and how do preflight OPTIONS requests work?",
        "sample_answer": "CORS is an HTTP-header based security mechanism enforced by browsers that restricts cross-origin resource requests. For non-simple HTTP requests (such as custom headers or non-standard Content-Types), the browser automatically sends a preflight OPTIONS request to verify whether the server allows the origin and method before dispatching the actual request."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Performance Optimization",
        "question": "How do you optimize Core Web Vitals (LCP, INP, CLS) for a modern web application?",
        "sample_answer": "LCP (Largest Contentful Paint) is improved by compressing hero assets, using lazy loading, and CDN caching. INP (Interaction to Next Paint) is optimized by breaking long JavaScript tasks using requestIdleCallback or Web Workers. CLS (Cumulative Layout Shift) is minimized by reserving explicit width and height dimensions on images and dynamic containers."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "State Management",
        "question": "Compare prop drilling mitigation strategies: Context API vs Redux/Zustand global stores.",
        "sample_answer": "Prop drilling is passing data down multiple component layers unnecessarily. React Context API distributes values across subtree components without prop drilling, but re-renders all consumer components whenever the context value object changes. Global state libraries like Redux or Zustand use selective subscriptions, allowing components to re-render only when specific slice selectors change."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "JavaScript Closures",
        "question": "Define a closure in JavaScript and give a practical use case.",
        "sample_answer": "A closure is a function bundled together with references to its surrounding lexical environment, allowing an inner function to retain access to variables declared in an outer function even after the outer execution context has finished. Practical use cases include data privacy (private counter functions), event handler currying, and memoization caches."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "HTML5 & Accessibility",
        "question": "Why is semantic HTML important for SEO and ARIA accessibility compliance?",
        "sample_answer": "Semantic HTML elements (such as <header>, <nav>, <article>, <main>) communicate explicit structural meaning to search engine crawlers and screen readers. They provide built-in keyboard accessibility focus management, improving SEO domain indexability and assistive software navigation."
    },
    {
        "role": "Frontend Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Build Tools & Bundlers",
        "question": "How does Tree Shaking work in modern bundlers like ESBuild or Webpack?",
        "sample_answer": "Tree shaking relies on static ES Module syntax (import and export statements) to construct a module dependency graph. During production compilation, the bundler dead-code eliminates unreferenced code exports, drastically reducing final bundle payloads."
    },

    # ==========================================
    # JAVA DEVELOPER - TECHNICAL (10 Questions)
    # ==========================================
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "Java Core",
        "question": "What is the difference between JVM, JRE, and JDK in Java runtime ecosystem?",
        "sample_answer": "JDK (Java Development Kit) is the full developer toolset including compilers (javac) and debuggers. JRE (Java Runtime Environment) provides libraries and the JVM required to run compiled Java applications. JVM (Java Virtual Machine) is the abstract execution engine that interprets compiled bytecode (.class files) into native machine instructions."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "Object-Oriented Programming",
        "question": "Explain method overloading vs method overriding in Java.",
        "sample_answer": "Method overloading occurs within the same class when methods share the same name but differ in parameter signature (compile-time polymorphism). Method overriding occurs when a subclass provides a specific implementation for a method declared in its superclass using the @Override annotation (runtime polymorphism)."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Spring Framework",
        "question": "How does Dependency Injection (DI) and Inversion of Control (IoC) work in Spring?",
        "sample_answer": "Inversion of Control (IoC) transfers object creation and lifecycle management from developer code to the Spring Container. Dependency Injection (DI) is the pattern used by Spring to automatically inject component dependencies (via @Autowired constructor or field injection) at runtime."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Multithreading",
        "question": "Explain the difference between synchronized blocks and ReentrantLock in Java concurrency.",
        "sample_answer": "Synchronized blocks are language-level implicit lock constructs managed automatically by the JVM upon entering/exiting a code block. ReentrantLock is an explicit java.util.concurrent API lock offering advanced capabilities like interruptible locking, fairness policies, and tryLock() timeouts."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Collections Framework",
        "question": "How does HashMap handle collisions internally in Java 8+?",
        "sample_answer": "Java HashMaps use an array of buckets. When key hash codes collisionally map to the same bucket, entries form a linked list. In Java 8+, if bucket collisions exceed 8 nodes and array capacity is at least 64, the linked list transforms into a Red-Black Tree, improving lookup complexity from O(n) to O(log n)."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Memory & GC",
        "question": "Describe Java Garbage Collection generations (Eden, Survivor, Tenured) and G1 GC collector mechanics.",
        "sample_answer": "Java heap memory is divided into Young Generation (Eden and two Survivor spaces S0/S1) and Old (Tenured) Generation. New objects allocate in Eden. Survived objects move to Survivor spaces and eventually get promoted to Tenured generation after aging thresholds. Garbage-First (G1) collector partitions the heap into equal region blocks, targeting region sweeps with the highest garbage volume."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "JVM Tuning",
        "question": "How do you diagnose OutOfMemoryError: Java heap space vs Metaspace?",
        "sample_answer": "Heap space OutOfMemoryError indicates the application exceeded allocated max heap (-Xmx) due to memory leaks or large object retention. Metaspace OutOfMemoryError occurs when class metadata memory exceeds limits (-XX:MaxMetaspaceSize) caused by excessive dynamic class loading (e.g. CGLIB proxies)."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "Java 8 Features",
        "question": "What are Java Streams and how do intermediate operations differ from terminal operations?",
        "sample_answer": "Java Streams are wrapper pipelines that allow functional-style data processing over sequences of elements. Intermediate operations (filter, map) are lazy and return a new stream without executing computation until a terminal operation (collect, count, forEach) is invoked."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Database Persistence",
        "question": "Explain Hibernate/JPA N+1 select problem and how to resolve it.",
        "sample_answer": "The N+1 problem occurs when fetching an entity list executes 1 initial query to fetch N parent records, followed by N separate SQL queries to retrieve associated child entities. It is resolved using JOIN FETCH in JPQL queries, EntityGraphs, or setting BatchSize annotations."
    },
    {
        "role": "Java Developer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Microservices",
        "question": "How do you implement Resilience4j Circuit Breakers in Spring Boot microservices?",
        "sample_answer": "Resilience4j Circuit Breaker intercepts remote calls. If downstream failures exceed configured error rate thresholds (e.g. 50%), the breaker transitions from CLOSED to OPEN state, immediately failing calls with a fallback response to prevent cascading system collapse."
    },

    # ==========================================
    # FULL STACK DEVELOPER - TECHNICAL (10 Questions)
    # ==========================================
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "HTTP Protocol",
        "question": "What is the difference between GET, POST, PUT, and PATCH HTTP methods?",
        "sample_answer": "GET retrieves server data without side effects (safe/idempotent). POST creates new resource records. PUT replaces an entire resource representation with the payload (idempotent). PATCH applies partial modifications to an existing resource."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "Database Design",
        "question": "Explain SQL Relational Databases vs NoSQL Document Databases and when to choose each.",
        "sample_answer": "SQL databases (PostgreSQL, MySQL) use structured schemas, tables, and strict ACID transaction compliance, making them ideal for financial or complex relational systems. NoSQL databases (MongoDB) store flexible JSON-like documents, scaling horizontally for unstructured or rapidly evolving data schemas."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Authentication",
        "question": "How does JWT (JSON Web Token) authentication work, and how do you store tokens securely on the client?",
        "sample_answer": "JWT contains a base64-encoded Header, Payload, and cryptographic Signature. Upon user login, the server issues a signed token. On the client, storing tokens in HTTP-Only, Secure, SameSite cookies protects against XSS attacks compared to LocalStorage."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "System Design",
        "question": "How do you design a high-availability URL Shortening Service (like Bitly)?",
        "sample_answer": "A URL shortener uses an API gateway, a distributed hash generator (e.g. Base62 encoding of an auto-incrementing ID or KGS Key Generation Service), a high-speed Redis cache layer for popular links, and a persistent SQL/NoSQL DB storing short code to long URL mappings."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "WebSockets",
        "question": "How do WebSockets differ from HTTP Long Polling for real-time applications?",
        "sample_answer": "HTTP Long Polling keeps an HTTP connection open until the server responds, closing and reopening connections continuously (high header overhead). WebSockets establish a single persistent full-duplex TCP connection, allowing lightweight bi-directional frame communication with minimal latency."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Caching Strategies",
        "question": "Explain Cache-Aside vs Write-Through vs Write-Behind caching patterns.",
        "sample_answer": "In Cache-Aside, the application checks the cache; on cache miss, it reads from the DB and updates the cache. In Write-Through, data is written synchronously to cache and DB simultaneously. In Write-Behind, data is written to cache immediately, and asynchronously flushed to DB in background batches."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Database Indexing",
        "question": "How do B-Tree indexes accelerate SQL database queries, and what are the trade-offs?",
        "sample_answer": "B-Tree indexes maintain a balanced tree structure allowing O(log n) search, insertion, and range queries on column values. The trade-off is additional storage overhead and slower write performance (INSERT/UPDATE/DELETE) because index trees must rebalance upon writes."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "API Design",
        "question": "What are RESTful API best practices regarding URI naming conventions and HTTP status codes?",
        "sample_answer": "REST URIs should use plural nouns representing resources (/api/v1/users) rather than verbs. Correct HTTP status codes must be returned: 200 OK, 201 Created, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 500 Internal Server Error."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Docker & Containerization",
        "question": "Why containerize applications with Docker, and what is the difference between a Docker Image and Container?",
        "sample_answer": "Docker package applications with dependencies into portable immutable environments to eliminate 'works on my machine' bugs. A Docker Image is an executable blueprint package layer; a Docker Container is a running instantiated instance of that image."
    },
    {
        "role": "Full Stack",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "CI/CD & Deployment",
        "question": "Explain Blue/Green Deployment strategy vs Canary Deployments.",
        "sample_answer": "Blue/Green deployment runs two identical environments: Blue (current live) and Green (new release). Traffic switches instantly at router level. Canary deployment gradually rolls out the new version to a small percentage of user traffic (e.g. 5%), monitoring error rates before complete deployment."
    },

    # ==========================================
    # UI UX DESIGNER - TECHNICAL (5 Questions)
    # ==========================================
    {
        "role": "UI UX Designer",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "Design Principles",
        "question": "What is the difference between User Experience (UX) and User Interface (UI) design?",
        "sample_answer": "UX design focuses on the overall journey, wireframing, architecture, and problem-solving aspect of how a user interacts with a product efficiently. UI design focuses on visual aesthetics, typography, color schemes, component states, and interactive micro-animations."
    },
    {
        "role": "UI UX Designer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Design Systems",
        "question": "How do design tokens help maintain visual consistency across Web and Mobile platforms?",
        "sample_answer": "Design tokens store visual properties (colors, spacing, font sizes, elevation shadows) as platform-agnostic key-value pairs (JSON). They sync automatically across Web (CSS Variables), iOS (Swift), and Android (XML/Compose) codebases."
    },
    {
        "role": "UI UX Designer",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Accessibility",
        "question": "What are WCAG 2.1 contrast ratio guidelines for normal text vs large text?",
        "sample_answer": "WCAG 2.1 AA level requires a contrast ratio of at least 4.5:1 for normal text and 3:1 for large text (18pt or 14pt bold). AAA level requires 7:1 for normal text and 4.5:1 for large text."
    },
    {
        "role": "UI UX Designer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "User Research",
        "question": "How do you conduct usability testing sessions to iterate on high-fidelity prototypes?",
        "sample_answer": "Usability sessions involve assigning scenario tasks to representative target users, observing interactions without leading hints, recording completion rates and friction points, and prioritizing iterative design updates based on severity."
    },
    {
        "role": "UI UX Designer",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Information Architecture",
        "question": "What is Card Sorting in UX research, and when do you choose open vs closed card sorting?",
        "sample_answer": "Card Sorting evaluates website information architecture navigation categories. Open card sorting allows users to organize topics into custom named groups (ideal for new products). Closed card sorting requires sorting topics into predefined category headings (ideal for validating existing navigation)."
    },

    # ==========================================
    # DATA ANALYST - TECHNICAL (5 Questions)
    # ==========================================
    {
        "role": "Data Analyst",
        "type": "Technical",
        "difficulty": "Easy",
        "topic": "SQL Queries",
        "question": "What is the difference between WHERE and HAVING clauses in SQL?",
        "sample_answer": "WHERE filters rows before any grouping or aggregation takes place. HAVING filters aggregated group results after GROUP BY execution."
    },
    {
        "role": "Data Analyst",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "SQL Window Functions",
        "question": "Explain ROW_NUMBER(), RANK(), and DENSE_RANK() window functions in SQL.",
        "sample_answer": "ROW_NUMBER() assigns a unique sequential integer to every row. RANK() assigns identical rank to tie values but skips subsequent numbers (1, 2, 2, 4). DENSE_RANK() assigns identical ranks to ties without skipping subsequent numbers (1, 2, 2, 3)."
    },
    {
        "role": "Data Analyst",
        "type": "Technical",
        "difficulty": "Medium",
        "topic": "Pandas & Python",
        "question": "How do you handle missing or null data in a Pandas DataFrame (fillna vs dropna vs interpolation)?",
        "sample_answer": "dropna() removes rows or columns containing NaN values (used when missing data is negligible). fillna() replaces NaNs with static values, mean, or median. interpolate() estimates missing numeric values based on neighboring values."
    },
    {
        "role": "Data Analyst",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Statistics & A/B Testing",
        "question": "What is a p-value in statistical hypothesis testing, and what does p < 0.05 signify?",
        "sample_answer": "A p-value is the probability of obtaining test results at least as extreme as observed, assuming the null hypothesis is true. A p-value less than 0.05 rejects the null hypothesis, indicating statistically significant differences between test variants."
    },
    {
        "role": "Data Analyst",
        "type": "Technical",
        "difficulty": "Hard",
        "topic": "Data Visualization",
        "question": "When should you choose a Histogram over a Bar Chart for business analytics reporting?",
        "sample_answer": "Bar charts display comparisons across discrete categorical data (e.g. Sales by Region). Histograms display frequency distributions of continuous numerical variables divided into continuous range bins (e.g. User Age Distribution)."
    },

    # ==========================================
    # HR / BEHAVIORAL QUESTIONS (30 Questions)
    # ==========================================
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Self Introduction",
        "question": "Tell me about yourself and walk me through your background.",
        "sample_answer": "I am a passionate software engineer with strong experience in building scalable web applications and solving complex algorithmic challenges. In my recent roles, I led feature development, collaborated with cross-functional teams, and consistently delivered high-quality software."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Strengths & Weaknesses",
        "question": "What are your greatest professional strengths and your biggest area for growth?",
        "sample_answer": "My primary strength is systematic problem solving and adaptability to new technologies under tight deadlines. My area for growth is sometimes spending too much time perfectionizing early prototypes; I have learned to focus on delivering MVP iterations first."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "STAR Behavioral - Conflict",
        "question": "Describe a situation where you had a technical disagreement with a teammate or lead. How did you resolve it?",
        "sample_answer": "Situation: We disagreed on database migration strategies. Action: I scheduled a short meeting, presented benchmark performance data comparing both approaches objectively, listened to their concerns regarding rollback safety, and reached a consensus on a hybrid strategy. Result: Zero downtime deployment."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "STAR Behavioral - Pressure",
        "question": "Give an example of a project where you faced a tight deadline or unexpected failure. How did you handle it?",
        "sample_answer": "Situation: A critical third-party API outage 2 days before product launch. Action: I implemented a fallback mock caching strategy and communicated status updates to stakeholders transparently. Result: We launched on schedule with minimal impact."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Leadership & Ownership",
        "question": "Describe a time when you took initiative on a project without being explicitly asked.",
        "sample_answer": "Situation: Noticed build times were taking 25 minutes. Action: Researched CI pipeline caching and refactored Docker multi-stage builds on my own initiative. Result: Cut build times down to 4 minutes, saving team developer hours daily."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Career Motivations",
        "question": "Why do you want to join our company and what excites you about this role?",
        "sample_answer": "I admire your company's focus on engineering excellence and high-scale user impact. This role aligns perfectly with my background in building resilient applications and my passion for continuous learning."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Teamwork",
        "question": "How do you handle working with team members who have different communication styles?",
        "sample_answer": "I adapt by active listening, clarifying expectations in written documentation, using visual diagrams for technical ideas, and maintaining an open, respectful feedback loop."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Handling Feedback",
        "question": "Tell me about a time you received constructive criticism on your code or work performance. How did you respond?",
        "sample_answer": "During a peer review, a senior colleague pointed out missing edge-case error handling in my module. I welcomed the feedback, updated the unit test coverage immediately, and incorporated defensive programming into my standard workflow."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Work-Life Balance",
        "question": "How do you prioritize your daily workload when managing multiple competing deadlines?",
        "sample_answer": "I categorize tasks using an Eisenhower urgency/importance matrix, align priorities with product leads during daily standups, and focus on high-impact deliverables first."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Adaptability",
        "question": "Describe a time when project requirements changed drastically midway through development.",
        "sample_answer": "Situation: Client shifted core specifications 1 week before release. Action: Kept calm, refactored decoupled modules, updated sprint backlog priorities with the team. Result: Delivered modified feature scope successfully."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Failure & Resilience",
        "question": "Tell me about a mistake you made in production code and what lessons you took away from it.",
        "sample_answer": "Early in my career, I deployed an unindexed query causing high database CPU usage. I owned the issue, issued an immediate rollback, added missing column indexes, and introduced mandatory query explain-plan checks in our pull request guidelines."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Remote Work",
        "question": "How do you stay self-motivated and maintain high productivity in a remote environment?",
        "sample_answer": "I maintain a dedicated workspace, set structured daily goals, communicate progress asynchronously via Slack/Jira, and take planned short breaks to sustain focus."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Mentorship",
        "question": "How do you onboard or mentor junior developers joining your team?",
        "sample_answer": "I create comprehensive onboarding docs, pair-program on initial bug fixes, encourage open questions without judgment, and provide constructive code review feedback."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Ethics & Accountability",
        "question": "What would you do if you noticed a security flaw or ethical compliance issue right before a deployment deadline?",
        "sample_answer": "I would immediately notify the tech lead and engineering manager, explain the severity risk objectively, and recommend pausing deployment to patch the vulnerability safely."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Future Goals",
        "question": "Where do you see yourself professionally in 3 to 5 years?",
        "sample_answer": "I see myself taking on technical leadership responsibilities, architecting large-scale systems, and helping mentor junior engineers while continuing to master cutting-edge software practices."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Problem Solving",
        "question": "How do you approach learning a completely unfamiliar technology stack required for a new project?",
        "sample_answer": "I start by reading official documentation, building a small proof-of-concept project to understand fundamentals, and reviewing open-source production implementations."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Cross-Functional Collaboration",
        "question": "How do you work effectively with non-technical stakeholders (e.g., Product Managers, Designers)?",
        "sample_answer": "I translate complex technical constraints into plain business impact language, use wireframes and prototypes for alignment, and set realistic scope expectations."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Negotiation & Influence",
        "question": "Describe a time when you persuaded management to allocate time for technical debt refactoring.",
        "sample_answer": "I presented data demonstrating how legacy debt slowed down feature velocity by 30% and increased bug reports. By showing long-term ROI, management approved a 20% refactoring budget per sprint."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Decision Making",
        "question": "How do you handle ambiguity when given vague specifications for a feature?",
        "sample_answer": "I break down requirements, document assumptions, schedule a short sync with the product manager to clarify open questions, and draft an RFC before writing code."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Company Alignment",
        "question": "What values matter most to you in an engineering team environment?",
        "sample_answer": "Psychological safety, open communication, continuous learning, blameless post-mortems, and a shared passion for high-quality software."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Crisis Management",
        "question": "How do you handle a scenario where multiple production servers go down simultaneously?",
        "sample_answer": "Follow incident response protocol: establish a war room, assign clear incident commander roles, communicate status page updates, analyze logs to identify root cause, apply hotfix, and publish a post-mortem."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Feedback Delivery",
        "question": "How do you give constructive feedback to a peer without damaging your working relationship?",
        "sample_answer": "I deliver feedback privately, focus on specific code behaviors rather than personal traits, frame comments objectively, and highlight positive contributions."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Continuous Improvement",
        "question": "What technical book, blog, or course has impacted your development practices recently?",
        "sample_answer": "Reading 'Designing Data-Intensive Applications' by Martin Kleppmann significantly expanded my understanding of distributed systems, consensus algorithms, and database storage engines."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Scope Management",
        "question": "What do you do when scope creep threatens to push back an agreed release date?",
        "sample_answer": "Highlight the impact on milestone dates immediately to the product manager, offer options (e.g. deferring non-essential features to Phase 2), and preserve core release quality."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Motivation",
        "question": "What keeps you passionate about software engineering after years in the industry?",
        "sample_answer": "The thrill of solving complex real-world problems and creating software that directly improves users' lives."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Customer Centricity",
        "question": "How do customer feedback and bug reports influence your technical decisions?",
        "sample_answer": "Customer feedback validates whether technical investments deliver genuine user value. I prioritize bugs affecting user workflow before adding non-essential technical optimizations."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Resource Allocation",
        "question": "How do you choose between building a custom in-house solution vs buying a third-party API tool?",
        "sample_answer": "Evaluate core competency: if the feature provides a distinct competitive advantage, build in-house. If it is commodity infrastructure (e.g. auth, email delivery), buying third-party saves engineering time."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Easy",
        "topic": "Work Habits",
        "question": "How do you document your code and technical architecture for future maintainers?",
        "sample_answer": "I write self-documenting code with clear variable names, maintain updated README files, document complex algorithms with inline docstrings, and record architectural decision records (ADRs)."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Medium",
        "topic": "Accountability",
        "question": "Describe a situation where a project failed to meet expectations. What was your takeaway?",
        "sample_answer": "We over-engineered a feature that users ultimately didn't adoption. The key lesson was validating customer demand early with lean prototypes before spending months in development."
    },
    {
        "role": "All Roles",
        "type": "HR",
        "difficulty": "Hard",
        "topic": "Long Term Vision",
        "question": "How do you balance short-term feature delivery speed with long-term code maintainability?",
        "sample_answer": "Write clean, modular code with solid test coverage from day one. Avoid shortcuts that create unmanageable tech debt, and schedule dedicated maintenance refactoring in regular sprints."
    }
]
