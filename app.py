"""
app.py  –  COURTFLOW Flask Application
=======================================
Main entry point. All routes are defined here.
DSA structures are rebuilt from SQLite on every request (stateless approach
suitable for a college project demo).
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import re
from datetime import date

import database as db
from dsa.queue         import CaseQueue
from dsa.priority_queue import PriorityQueue
from dsa.stack         import CaseStack
from dsa.linked_list   import LinkedList
from dsa.searching     import linear_search, binary_search, hash_lookup
from dsa.sorting       import bubble_sort, key_case_id, key_priority, key_filing_date

app = Flask(__name__)
app.secret_key = "courtflow-dsa-secret-2026"

# Ensure DB is initialized on app startup (for serverless environments like Vercel)
try:
    db.init_db()
except Exception:
    pass



# ==========================================================================
# HELPER: build_structures()
# Reads all data from SQLite and populates every DSA structure.
# Called at the start of each route that needs DSA data.
# ==========================================================================
def build_structures():
    """
    Load all PENDING cases from SQLite and insert them into:
      - CaseQueue        (FIFO queue for hearings)
      - PriorityQueue    (heap-based priority queue)
      - dict             (hash table for O(1) lookup)
    Load all COMPLETED cases into:
      - CaseStack        (LIFO stack, most-recent on top)
    Load all history entries into per-case LinkedLists.
    """
    all_cases = db.get_all_cases()
    pending   = [c for c in all_cases if c["status"] == "Pending"]
    completed = [c for c in all_cases if c["status"] == "Completed"]

    # ---- Queue (FIFO – ordered by filing date) ----
    queue = CaseQueue()
    for case in sorted(pending, key=lambda x: x["filing_date"]):
        queue.enqueue(case)

    # ---- Priority Queue (heap) ----
    pq = PriorityQueue()
    for case in pending:
        pq.push(case)

    # ---- Stack (LIFO – completed cases) ----
    stack = CaseStack()
    for case in sorted(completed, key=lambda x: x.get("filing_date", "")):
        stack.push(case)   # most-recently completed will be last pushed => top

    # ---- Dictionary / Hash Table for O(1) lookup ----
    case_dict = {c["case_id"]: c for c in all_cases}

    # ---- Linked Lists per case (history chains) ----
    linked_lists = {}       # { case_id: LinkedList }
    all_history = db.get_all_history()
    for entry in all_history:
        cid = entry["case_id"]
        if cid not in linked_lists:
            linked_lists[cid] = LinkedList()
        linked_lists[cid].insert(entry)

    return queue, pq, stack, case_dict, linked_lists


# ==========================================================================
# VALIDATION HELPERS
# ==========================================================================
def validate_case_id(case_id):
    """Case ID must match pattern C followed by 3 digits, e.g. C001."""
    return bool(re.match(r'^C\d{3}$', case_id))


REQUIRED_FIELDS = ["case_id","plaintiff","defendant","case_type",
                   "priority","filing_date"]

def validate_case_form(form):
    """Return a list of error messages for the add/edit case form."""
    errors = []
    for field in REQUIRED_FIELDS:
        if not form.get(field, "").strip():
            errors.append(f"'{field.replace('_',' ').title()}' is required.")
    if form.get("case_id") and not validate_case_id(form["case_id"].strip()):
        errors.append("Case ID must be in format C followed by 3 digits (e.g., C001).")
    if form.get("priority") not in ("High", "Medium", "Low", "", None):
        errors.append("Priority must be High, Medium, or Low.")
    return errors


# ==========================================================================
# ROUTES
# ==========================================================================

# --- Dashboard ---
@app.route("/")
def index():
    stats = db.get_stats()
    queue, pq, stack, case_dict, _ = build_structures()
    queue_front   = queue.peek()
    top_priority  = pq.peek()
    stack_top     = stack.peek()
    queue_size    = queue.size()
    return render_template(
        "index.html",
        stats=stats,
        queue_front=queue_front,
        top_priority=top_priority,
        stack_top=stack_top,
        queue_size=queue_size,
    )


# --- Add Case ---
@app.route("/add", methods=["GET", "POST"])
def add_case():
    if request.method == "POST":
        form = request.form.to_dict()

        errors = validate_case_form(form)
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("add_case.html", form=form)

        case_id = form["case_id"].strip().upper()
        if db.get_case_by_id(case_id):
            flash(f"Case ID '{case_id}' already exists. Choose a different ID.", "error")
            return render_template("add_case.html", form=form)

        form["case_id"] = case_id
        db.insert_case(form)

        # Add initial history entry via Linked List (stored to DB)
        today_str = date.today().isoformat()
        db.insert_history(case_id, "Case Filed", today_str,
                          f"Case {case_id} filed by {form['plaintiff']} against {form['defendant']}.")

        flash(f"Case {case_id} added successfully and enqueued for hearing.", "success")
        return redirect(url_for("cases"))

    return render_template("add_case.html", form={})


# --- All Cases ---
@app.route("/cases")
def cases():
    sort_by  = request.args.get("sort", "case_id")
    order    = request.args.get("order", "asc")
    all_cases = db.get_all_cases()

    # Use Bubble Sort (DSA) for sorting
    key_map = {
        "case_id":     key_case_id,
        "priority":    key_priority,
        "filing_date": key_filing_date,
    }
    key_fn = key_map.get(sort_by, key_case_id)
    reverse = (order == "desc")
    all_cases = bubble_sort(all_cases, key_fn, reverse=reverse)

    return render_template("cases.html", cases=all_cases,
                           sort_by=sort_by, order=order)


# --- Edit Case ---
@app.route("/edit/<case_id>", methods=["GET", "POST"])
def edit_case(case_id):
    case = db.get_case_by_id(case_id)
    if not case:
        flash(f"Case '{case_id}' not found.", "error")
        return redirect(url_for("cases"))

    if request.method == "POST":
        form = request.form.to_dict()
        form["case_id"] = case_id  # preserve original ID
        errors = []
        for field in ["plaintiff","defendant","case_type","priority","filing_date"]:
            if not form.get(field, "").strip():
                errors.append(f"'{field.replace('_',' ').title()}' is required.")
        if errors:
            for e in errors:
                flash(e, "error")
            return render_template("add_case.html", form=form, edit=True)

        db.update_case(form)
        flash(f"Case {case_id} updated successfully.", "success")
        return redirect(url_for("cases"))

    return render_template("add_case.html", form=case, edit=True)


# --- Delete Case ---
@app.route("/delete/<case_id>", methods=["POST"])
def delete_case(case_id):
    case = db.get_case_by_id(case_id)
    if not case:
        flash(f"Case '{case_id}' not found.", "error")
    else:
        db.delete_case(case_id)
        flash(f"Case {case_id} deleted.", "success")
    return redirect(url_for("cases"))


# --- Mark Completed ---
@app.route("/complete/<case_id>", methods=["POST"])
def complete_case(case_id):
    case = db.get_case_by_id(case_id)
    if not case:
        flash(f"Case '{case_id}' not found.", "error")
    elif case["status"] == "Completed":
        flash(f"Case {case_id} is already marked completed.", "error")
    else:
        db.mark_completed(case_id)
        today_str = date.today().isoformat()
        db.insert_history(case_id, "Hearing Completed", today_str,
                          "Case hearing concluded. Verdict delivered.")
        flash(f"Case {case_id} marked as completed and pushed to the stack.", "success")
    return redirect(url_for("cases"))


# --- Search ---
@app.route("/search", methods=["GET", "POST"])
def search():
    results = []
    query   = ""
    method  = "linear"
    algo_used = ""
    not_found = False

    if request.method == "POST":
        query  = request.form.get("query", "").strip()
        method = request.form.get("method", "linear")

        if not query:
            flash("Please enter a search query.", "error")
            return render_template("search.html", results=[], query=query, method=method)

        all_cases = db.get_all_cases()
        _, _, _, case_dict, _ = build_structures()

        if method == "linear":
            results = linear_search(all_cases, query, field="case_id")
            if not results:   # try plaintiff too
                results = linear_search(all_cases, query, field="plaintiff")
            algo_used = "Linear Search — O(n): Scanned every case one by one."

        elif method == "binary":
            # Binary search requires sorted list by case_id
            sorted_cases = bubble_sort(list(all_cases), key_case_id)
            result = binary_search(sorted_cases, query.upper())
            results = [result] if result else []
            algo_used = "Binary Search — O(log n): List sorted by Case ID, then halved each step."

        elif method == "hash":
            result = hash_lookup(case_dict, query.upper())
            results = [result] if result else []
            algo_used = "Dictionary/Hash Lookup — O(1) avg: Direct key access via hash table."

        if not results:
            not_found = True

    return render_template(
        "search.html",
        results=results, query=query, method=method,
        algo_used=algo_used, not_found=not_found
    )


# --- Hearing Queue ---
@app.route("/queue", methods=["GET", "POST"])
def hearing_queue():
    queue, _, _, _, _ = build_structures()
    message = None
    peeked  = None
    action  = request.form.get("action") if request.method == "POST" else None

    if action == "dequeue":
        front = queue.peek()
        if front is None:
            flash("Queue is empty. No cases waiting for hearing.", "error")
        else:
            case_id = front["case_id"]
            db.mark_completed(case_id)
            today_str = date.today().isoformat()
            db.insert_history(case_id, "Hearing Held (Dequeue)", today_str,
                              "Case dequeued from hearing queue. Hearing conducted.")
            flash(f"Case {case_id} dequeued — hearing held. Case marked completed and pushed to stack.", "success")
            return redirect(url_for("hearing_queue"))

    elif action == "peek":
        peeked = queue.peek()
        if peeked is None:
            flash("Queue is empty — nothing to peek.", "error")
        else:
            message = f"Front of queue: Case {peeked['case_id']} — {peeked['plaintiff']} vs {peeked['defendant']}"

    queue_list = queue.display()
    return render_template(
        "queue.html",
        queue_list=queue_list, peeked=peeked, message=message,
        queue_size=queue.size()
    )


# --- Priority Queue ---
@app.route("/priority")
def priority_queue_view():
    _, pq, _, _, _ = build_structures()
    priority_list  = pq.display()
    top = pq.peek()
    return render_template("priority.html", priority_list=priority_list, top=top)


# --- Case History (Linked List) ---
@app.route("/history", methods=["GET", "POST"])
def history():
    _, _, _, case_dict, linked_lists = build_structures()
    all_cases = db.get_all_cases()
    selected_id = request.args.get("case_id") or (all_cases[0]["case_id"] if all_cases else None)
    chain = []
    selected_case = None
    message = None

    if request.method == "POST":
        action = request.form.get("action")
        case_id_form = request.form.get("case_id", "").strip().upper()

        if action == "insert":
            action_text = request.form.get("action_text", "").strip()
            note        = request.form.get("note", "").strip()
            action_date = request.form.get("action_date", date.today().isoformat())
            if not case_id_form or not action_text:
                flash("Case ID and Action are required to insert a history entry.", "error")
            elif not db.get_case_by_id(case_id_form):
                flash(f"Case '{case_id_form}' not found.", "error")
            else:
                db.insert_history(case_id_form, action_text, action_date, note)
                flash(f"History entry inserted for Case {case_id_form}.", "success")
                selected_id = case_id_form
                return redirect(url_for("history", case_id=selected_id))

        elif action == "delete":
            entry_id = request.form.get("entry_id")
            if not entry_id:
                flash("No entry selected for deletion.", "error")
            else:
                # Use LinkedList delete (mirrors DB delete)
                cid_of_entry = request.form.get("entry_case_id", "").strip()
                if cid_of_entry in linked_lists:
                    linked_lists[cid_of_entry].delete(int(entry_id))
                db.delete_history_entry(int(entry_id))
                flash(f"History entry #{entry_id} deleted.", "success")
                selected_id = cid_of_entry or selected_id
                return redirect(url_for("history", case_id=selected_id))

    if selected_id:
        selected_case = db.get_case_by_id(selected_id)
        ll = linked_lists.get(selected_id, LinkedList())
        chain = ll.display()

    return render_template(
        "history.html",
        all_cases=all_cases,
        selected_id=selected_id,
        selected_case=selected_case,
        chain=chain,
        case_dict=case_dict,
    )


# --- Completed Cases (Stack) ---
@app.route("/completed")
def completed():
    _, _, stack, _, _ = build_structures()
    completed_list = stack.display()  # top of stack first
    stack_top = stack.peek()
    return render_template("completed.html", completed_list=completed_list, stack_top=stack_top)


# --- DSA Visualization ---
@app.route("/dsa")
def dsa_viz():
    queue, pq, stack, case_dict, linked_lists = build_structures()
    all_cases = db.get_all_cases()
    return render_template(
        "dsa.html",
        queue_list     = queue.display(),
        pq_list        = pq.display(),
        stack_list     = stack.display(),
        case_dict      = case_dict,
        linked_lists   = {k: v.display() for k, v in linked_lists.items()},
        all_cases      = all_cases,
    )


# ==========================================================================
# Run
# ==========================================================================
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5050))
    db.init_db()
    print(f"\n * COURTFLOW running on http://127.0.0.1:{port} (Press CTRL+C to quit)\n")
    app.run(debug=True, port=port)

