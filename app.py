from pathlib import Path

from flasgger import Swagger
from flask import Flask, jsonify, request


app = Flask(__name__)

app.config["SWAGGER"] = {
    "openapi": "3.0.3",
    "uiversion": 3,
}

# Swagger UI nacte popis API ze samostatneho OpenAPI YAML souboru.
openapi_file = Path(__file__).with_name("openapi.yaml")
Swagger(app, template_file=str(openapi_file))

# Jednoducha "databaze" v pameti. Po restartu serveru se vymaze.
policies = {}
next_id = 1


@app.get("/api/health")
def health():
    return jsonify({"status": "ok"}), 200


@app.get("/api/policies")
def list_policies():
    return jsonify(list(policies.values())), 200


@app.get("/api/policies/<int:policy_id>")
def get_policy(policy_id):
    policy = policies.get(policy_id)
    if policy is None:
        return jsonify({"error": "Policy not found"}), 404
    return jsonify(policy), 200


@app.post("/api/policies")
def create_policy():
    global next_id

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body is required"}), 400
    if not data.get("name"):
        return jsonify({"error": "Field 'name' is required"}), 400

    policy = {
        "id": next_id,
        "name": data["name"],
        "action": data.get("action", "audit"),
        "enabled": data.get("enabled", True),
    }
    policies[next_id] = policy
    next_id += 1
    return jsonify(policy), 201


@app.patch("/api/policies/<int:policy_id>")
def update_policy(policy_id):
    policy = policies.get(policy_id)
    if policy is None:
        return jsonify({"error": "Policy not found"}), 404

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "JSON body is required"}), 400

    for field in ("name", "action", "enabled"):
        if field in data:
            policy[field] = data[field]

    return jsonify(policy), 200


@app.delete("/api/policies/<int:policy_id>")
def delete_policy(policy_id):
    if policy_id not in policies:
        return jsonify({"error": "Policy not found"}), 404

    del policies[policy_id]
    return "", 204


if __name__ == "__main__":
    # Bez automatickeho reloaderu: jeden proces se snadno spousti i ukoncuje.
    app.run(host="127.0.0.1", port=5000, debug=True, use_reloader=False)
