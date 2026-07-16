# src/webapp.py
from flask import Flask, request, jsonify, render_template
from .allocation import can_enrol_with_plan, check_eligibility
from .seed_scenarios import build_seed, Course

app = Flask(__name__, template_folder="../templates", static_folder="../static")

def compute(seed: str):
    status, cur, plan = build_seed(seed)
    ready, reason = can_enrol_with_plan(status, cur, plan)
    return {
        "seed": seed,
        "status": status,
        "current": cur,
        "ready": ready,
        "reason": reason,
        "enrolEnabled": bool(ready),
        "plan": [c.__dict__ for c in plan],
    }

@app.get("/")
def index():
    # serve the minimal UI; JS will call /state
    return render_template("index.html")

@app.get("/state")
def state():
    seed = request.args.get("seed", "domestic_ok")
    return jsonify(compute(seed))

@app.post("/fix")
def fix():
    seed = request.args.get("seed", "domestic_ok")
    status, cur, plan = build_seed(seed)
    ready, reason = can_enrol_with_plan(status, cur, plan)
    if ready:
        return jsonify({"ok": True, "changed": False, **compute(seed)})

    # minimal auto-fixes that mirror your H1 brief
    if reason and "< 12" in reason:
        plan.append(Course("FIX12", 6, "OnCampus"))
    elif reason and "on-campus unit required" in reason:
        # flip one Online to OnCampus
        for c in plan:
            if c.mode == "Online":
                c.mode = "OnCampus"
                break
    elif reason and "online unit limit exceeded" in reason:
        for c in plan:
            if c.mode == "Online":
                c.mode = "OnCampus"
                break
    # re-evaluate
    ready2, reason2 = can_enrol_with_plan(status, cur, plan)
    return jsonify({
        "ok": ready2, "changed": True,
        "seed": seed, "status": status, "current": cur,
        "ready": ready2, "reason": reason2, "enrolEnabled": bool(ready2),
    })

if __name__ == "__main__":
    app.run(debug=True)
