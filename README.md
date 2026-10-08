# COURTFLOW — Court Case Management System
### Justice. Organized.

---

## 🎯 Objective
A full-stack web application demonstrating Data Structures and Algorithms through a
real-world court case management system. Built as a college DSA project using Python,
Flask, and SQLite.

---

## 🛠 Technologies Used
| Layer | Technology |
|-------|------------|
| Backend | Python 3.10+, Flask 3.x |
| Database | SQLite (court_cases.db) |
| Frontend | HTML5, CSS3, Jinja2 templates |
| JavaScript | Minimal (form confirmation only) |

---

## 📐 Data Structures & Algorithms Used

| DSA | File | Page |
|-----|------|------|
| Queue (FIFO) | `dsa/queue.py` | Hearing Queue (`/queue`) |
| Priority Queue (Heap) | `dsa/priority_queue.py` | Priority Cases (`/priority`) |
| Stack (LIFO) | `dsa/stack.py` | Completed Cases (`/completed`) |
| Linked List | `dsa/linked_list.py` | Case History (`/history`) |
| Linear Search | `dsa/searching.py` | Search Case (`/search`) |
| Binary Search | `dsa/searching.py` | Search Case (`/search`) |
| Bubble Sort | `dsa/sorting.py` | All Cases (`/cases`) |
| Dictionary / Hashing | `dsa/searching.py` | Search Case (`/search`) |

---

## ✨ Features
- **Dashboard** — Live stats, Queue front, Top priority case, Stack top
- **Add Case** — Validated form with auto-enqueue and history logging
- **All Cases** — Sortable table (Bubble Sort) with View/Edit/Delete/Complete
- **Search** — Choose Linear, Binary, or Hash search method
- **Hearing Queue** — FIFO queue with Enqueue/Dequeue/Peek operations
- **Priority Cases** — Heap-based priority ordering (High > Medium > Low)
- **Case History** — Linked list chain with Insert/Delete node operations
- **Completed Cases** — LIFO stack of completed cases
- **DSA Visualization** — ASCII-style diagrams of all structures
- Dark glassmorphism UI with gold/blue accent theme

---

## 📁 Project Structure
```
court_case_management/
├── app.py                 # Flask routes
├── database.py            # SQLite CRUD operations
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── court_cases.db         # Auto-generated on first run
├── dsa/
│   ├── __init__.py
│   ├── queue.py           # CaseQueue (FIFO)
│   ├── priority_queue.py  # PriorityQueue (heapq)
│   ├── stack.py           # CaseStack (LIFO)
│   ├── linked_list.py     # Node + LinkedList
│   ├── searching.py       # Linear, Binary, Hash search
│   └── sorting.py         # Bubble Sort + key functions
├── templates/
│   ├── base.html          # Shared layout with sidebar
│   ├── index.html         # Dashboard
│   ├── add_case.html      # Add/Edit case form
│   ├── cases.html         # All cases table
│   ├── search.html        # Search page
│   ├── queue.html         # Hearing queue
│   ├── priority.html      # Priority queue
│   ├── history.html       # Linked list history
│   ├── completed.html     # Stack of completed cases
│   └── dsa.html           # DSA visualization
└── static/
    └── style.css          # Dark glassmorphism theme
```

---

## 🚀 Installation & Running

```bash
# 1. Navigate to project directory
cd court_case_management

# 2. (Optional) Create a virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app (default port: 5050)
python app.py

# To run on a custom port:
# Windows (PowerShell): $env:PORT="8080"; python app.py
# Windows (CMD):        set PORT=8080 && python app.py
# Linux/macOS:          PORT=8080 python app.py

# 5. Open in browser
# http://127.0.0.1:5050
```

---

## 📚 DSA Explanations

### 1. Queue (FIFO — dsa/queue.py)
A Queue is like a line at a counter — the first person in line is served first.
In COURTFLOW, cases waiting for a hearing are stored in a Queue.
New cases join the back; when a hearing is held, the front case is removed (dequeued).

### 2. Stack (LIFO — dsa/stack.py)
A Stack is like a pile of papers — you always pick from the top.
Completed cases are pushed onto the stack. The most recently completed case is on top.
This allows quick access to the latest verdict.

### 3. Priority Queue (Min-Heap — dsa/priority_queue.py)
A Priority Queue processes the highest-priority case first, regardless of order.
Python's `heapq` module implements a min-heap. We encode High=0, Medium=1, Low=2
so that `heappop` always returns the most urgent case.

### 4. Linked List (dsa/linked_list.py)
A Linked List stores items as nodes, each pointing to the next.
Each case has a history chain: Case Filed → Notice Issued → Hearing Held → ...
Nodes are inserted at the tail (chronological order) and can be deleted by entry ID.

### 5. Linear Search — O(n) (dsa/searching.py)
Scans every element one by one. Works on any list. Slow for large datasets.

### 6. Binary Search — O(log n) (dsa/searching.py)
Requires a sorted list. Cuts the search range in half each step. Much faster than linear.

### 7. Dictionary/Hash Lookup — O(1) avg (dsa/searching.py)
Python dict uses a hash table. Given a Case ID, the case is found instantly without scanning.

### 8. Bubble Sort — O(n²) (dsa/sorting.py)
Repeatedly swaps adjacent out-of-order elements. Simple to understand but slow.
Used in the All Cases table to sort by Case ID, Priority, or Filing Date.

---

## ⏱ Time Complexity Table

| Operation | DSA | Time Complexity |
|-----------|-----|-----------------|
| Enqueue | Queue | O(1) |
| Dequeue | Queue | O(n) — list pop(0) |
| Stack Push | Stack | O(1) |
| Stack Pop | Stack | O(1) |
| Priority Queue Push | Heap | O(log n) |
| Priority Queue Pop | Heap | O(log n) |
| Linear Search | Array | O(n) |
| Binary Search | Sorted Array | O(log n) |
| Bubble Sort | Array | O(n²) avg |
| Dictionary Lookup | Hash Table | O(1) average |
| Linked List Insert | Linked List | O(n) |
| Linked List Delete | Linked List | O(n) |

---

## 🎓 DSA Viva Demonstration Guide

1. **Dashboard** — Show live stats. Point out Queue front, Priority top, Stack top tiles.
2. **Add Case** → Fill form → Submit. Show that case appears in Queue and History.
3. **Search** → Try Linear (any name), Binary (exact C00X), Hash (exact C00X). Explain complexity.
4. **Hearing Queue** → Peek → Dequeue. Show case moves to Completed.
5. **Priority Cases** → Show High cases always appear first regardless of order.
6. **Case History** → Select a case → Show linked list chain → Insert a node → Delete a node.
7. **Completed Cases** → Show stack (newest on top).
8. **DSA Visualization** → Explain each diagram to the examiner.
9. **All Cases** → Click sort buttons → Explain Bubble Sort is running.

---

> **Disclaimer:** COURTFLOW is a demo prototype for educational purposes only.
> All data is fictional. Not affiliated with any court or government body.
> © 2026 CourtFlow — Justice. Organized.
