from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# "מסד נתונים" זמני בזיכרון – מספיק להדגמת הספרינט
tasks = []
expenses = []
next_task_id = 1
next_expense_id = 1


@app.route("/")
def home():
    # דף הבית יעביר אוטומטית למסך המשימות
    return redirect(url_for("tasks_page"))


@app.route("/tasks", methods=["GET"])
def tasks_page():
    """
    מסך ניהול משימות:
    - מציג רשימת משימות
    - מאפשר סינון לפי סטטוס (חדש/בתהליך/בוצע)
    """
    status_filter = request.args.get("status")  # למשל ?status=חדש

    if status_filter:
        filtered_tasks = [t for t in tasks if t["status"] == status_filter]
    else:
        filtered_tasks = tasks

    return render_template("tasks.html", tasks=filtered_tasks, current_status=status_filter)


@app.route("/tasks/create", methods=["POST"])
def create_task():
    """
    יצירת משימה חדשה (User Story: יצירת משימה)
    """
    global next_task_id
    title = request.form.get("title")

    if title:
        tasks.append({
            "id": next_task_id,
            "title": title,
            "status": "חדש"
        })
        next_task_id += 1

    return redirect(url_for("tasks_page"))


@app.route("/tasks/<int:task_id>/edit", methods=["POST"])
def edit_task(task_id):
    """
    עריכת משימה קיימת (User Story: עריכת משימה)
    """
    new_title = request.form.get("title")
    new_status = request.form.get("status")

    for t in tasks:
        if t["id"] == task_id:
            if new_title:
                t["title"] = new_title
            if new_status:
                t["status"] = new_status
            break

    return redirect(url_for("tasks_page"))


@app.route("/tasks/<int:task_id>/delete", methods=["POST"])
def delete_task(task_id):
    """
    מחיקת משימה (User Story: מחיקת משימה)
    """
    global tasks
    tasks = [t for t in tasks if t["id"] != task_id]
    return redirect(url_for("tasks_page"))


@app.route("/budget", methods=["GET"])
def budget_page():
    """
    מסך הוצאות + סיכום (User Stories: הוספת הוצאה, סיכום הוצאות)
    """
    total = sum(e["amount"] for e in expenses)
    return render_template("budget.html", expenses=expenses, total=total)


@app.route("/budget/add", methods=["POST"])
def add_expense():
    """
    הוספת הוצאה (User Story: הוספת הוצאה)
    """
    global next_expense_id
    description = request.form.get("description")
    amount_str = request.form.get("amount")

    try:
        amount = float(amount_str)
    except (TypeError, ValueError):
        amount = 0

    if description and amount > 0:
        expenses.append({
            "id": next_expense_id,
            "description": description,
            "amount": amount
        })
        next_expense_id += 1

    return redirect(url_for("budget_page"))


if __name__ == "__main__":
    app.run(debug=True)
