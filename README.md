# QA REST API Demo

A small Python project created to practice REST API testing and basic test automation.

The project contains two main parts:

- `app.py` - a simple REST API backend built with Flask
- `client.py` - an automated API client that sends HTTP requests and validates responses

The API works with simple security policy data. All data is stored only in memory and is deleted when the server is restarted.

## Technologies

- Python
- Flask
- Requests
- Swagger / OpenAPI
- Flasgger
- JSON
- HTTP / REST API

## Project structure

```text
qa-rest-api-demo/
├── app.py
├── client.py
├── openapi.yaml
├── requirements.txt
└── README.md
```

## 1. Setup

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

When the virtual environment is active, `(.venv)` is displayed at the beginning of the terminal line.

## 2. Start the REST API

Run the backend:

```bash
python3 app.py
```

The API will run at:

```text
http://127.0.0.1:5000
```

Keep this terminal running while testing the API.

## 3. Swagger UI

When the backend is running, Swagger UI is available at:

```text
http://127.0.0.1:5000/apidocs/
```

The Swagger documentation is based on `openapi.yaml`.

It can be used to manually explore the endpoints, send requests and inspect:

- request URL
- request body
- HTTP status code
- response headers
- response body

Example flow:

1. `GET /api/health`
2. `POST /api/policies`
3. Copy the returned policy `id`
4. Use the ID in `GET /api/policies/{policy_id}`
5. Try a non-existing ID and verify the `404` response

## 4. Automated API scenario

Open another terminal, activate the virtual environment and run:

```bash
source .venv/bin/activate
python3 client.py
```

The client executes the following scenario:

1. `GET /api/health` - verifies that the API is available
2. `POST /api/policies` - creates a new policy
3. `GET /api/policies/{id}` - retrieves the created policy
4. Negative `POST` request without the required `name` field - expects HTTP `400`
5. `PATCH /api/policies/{id}` - updates the policy
6. `DELETE /api/policies/{id}` - deletes the policy
7. Another `GET` request - verifies that the deleted resource returns HTTP `404`

## API test example

Sending a request:

```python
response = requests.post(
    "http://127.0.0.1:5000/api/policies",
    json={"name": "Block USB copy", "action": "block"},
    timeout=5,
)
```

Validating the HTTP status code:

```python
assert response.status_code == 201
```

Validating data in the JSON response:

```python
assert response.json()["action"] == "block"
```

This demonstrates the basic principle of automated API testing:

**send a request, receive a response and compare the actual result with the expected result.**

## What this project demonstrates

The project covers:

- REST API basics
- CRUD operations
- GET, POST, PATCH and DELETE requests
- HTTP status code validation
- JSON response validation
- Positive and negative testing
- Required field validation
- Swagger / OpenAPI documentation
- Basic API test automation using Python assertions

CRUD stands for Create, Read, Update and Delete.

## AI-assisted development

I used AI as a learning and debugging assistant while building this project.

It helped me understand some Flask and Python concepts, analyse errors and improve the API test flow. I reviewed and tested the generated suggestions and used the project to better understand how the individual parts work together.

## Why I built this project

I created this project as a practical exercise to improve my Python and API testing skills.

My goal was not only to send API requests, but to understand the full flow between the client and backend, validate expected responses, test negative scenarios and investigate unexpected behaviour.

I am currently continuing to develop my Python skills and gradually moving towards test automation.

## Troubleshooting

### ModuleNotFoundError

The virtual environment may not be active or the dependencies may not be installed:

```bash
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

### Connection refused

The Flask backend is probably not running.

Start it with:

```bash
python3 app.py
```

### Port 5000 is already in use

On macOS, port 5000 may be used by AirPlay Receiver.

Change the port in `app.py`, for example to:

```text
5050
```

and update the `BASE_URL` in `client.py` accordingly.