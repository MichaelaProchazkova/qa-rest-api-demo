# REST API Test Scenarios

## POST /api/policies | Security Policies API demo application

This document summarizes manual and automatable test scenarios for the endpoint that creates a security policy.

The goal is to verify not only successful record creation, but also validation of required fields, data types, allowed values, boundary inputs, and subsequent persistence of the created data.

## Tested contract

| Item | Value |
|---|---|
| Method and path | `POST /api/policies` |
| Content type | `application/json` |
| Required field | `name` as a non-empty text value |
| Optional fields | `action`: `audit` or `block`; `enabled`: boolean |
| Successful result | `201 Created` and JSON of the created policy with a new `id` |
| Validation error | `400 Bad Request` or `422 Unprocessable Entity`, depending on the agreed API contract |

## Preconditions and execution

- The Flask server is running at `http://127.0.0.1:5000`.
- Swagger UI is available at `http://127.0.0.1:5000/apidocs/`.
- For each scenario, use **Try it out** in the `POST /policies` section, update the JSON payload, and select **Execute**.
- Compare the actual result shown in **Server response** with the expected result in this document and with the OpenAPI specification.
- For successful creation, use the returned `id` in `GET /policies/{policy_id}` to verify the stored state.

## Test matrix

| ID | Scenario | Input | Expected result |
|---|---|---|---|
| TC01 | Valid complete request | All fields | `201` and correct values |
| TC02 | Required field only | Only `name` | `201` and default values |
| TC03 | Missing `name` | No `name` field | `400` |
| TC04 | Empty `name` | `name` is `""` | `400` |
| TC05 | `null` value | `name` is `null` | `400` |
| TC06 | Invalid `action` | `action` is `destroy` | `400` or `422` |
| TC07 | Wrong data type | `enabled` is `"yes"` | `400` or `422` |
| TC08 | Empty JSON | `{}` | `400` |
| TC09 | Request without body | No JSON body | `400` |
| TC10 | Duplicate name | Same request sent twice | According to business rule |
| TC11 | Very long name | Extremely long text | Controlled validation |
| TC12 | Follow-up verification | POST followed by GET | Data is stored |

# Detailed test scenarios

## TC01 - Valid complete request

**Category:** Positive

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": "Block USB copy",
  "action": "block",
  "enabled": true
}
```

**Expected status:** `201 Created`

**Checks:**

- The response contains a new numeric `id`.
- `name`, `action`, and `enabled` match the values sent in the request.
- The response Content-Type is `application/json`.

## TC02 - Required field only

**Category:** Positive and default values

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": "Minimal policy"
}
```

**Expected status:** `201 Created`

**Checks:**

- The policy is created.
- `action` is set to the default value `audit`.
- `enabled` is set to the default value `true`.

## TC03 - Missing required field `name`

**Category:** Negative

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "action": "block",
  "enabled": true
}
```

**Expected status:** `400 Bad Request`

**Checks:**

- The response contains a clear description of the missing field.
- No new record is created.
- The API does not return an unhandled `500` error.

## TC04 - Empty name

**Category:** Negative and equivalence class

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": "",
  "action": "block",
  "enabled": true
}
```

**Expected status:** `400 Bad Request`

**Checks:**

- An empty string is rejected in the same way as a missing required field.
- The error response follows the agreed error format.

## TC05 - `null` value in required field

**Category:** Negative

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": null,
  "action": "block",
  "enabled": true
}
```

**Expected status:** `400 Bad Request`

**Checks:**

- `null` is not accepted as a valid name.
- No record with invalid data is created.

## TC06 - Invalid `action` value

**Category:** Negative and API contract validation

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": "Invalid action test",
  "action": "destroy",
  "enabled": true
}
```

**Expected status:** `400 Bad Request` or `422 Unprocessable Entity`

**Checks:**

- The API accepts only `audit` and `block`, as defined in the OpenAPI specification.
- The response explains which value is invalid.

**Note:** The current demo backend may return `201`. In that case, there is a mismatch between the documentation and implementation, which is a valid QA finding.

## TC07 - Wrong data type for `enabled`

**Category:** Negative and type validation

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": "Wrong type",
  "action": "block",
  "enabled": "yes"
}
```

**Expected status:** `400 Bad Request` or `422 Unprocessable Entity`

**Checks:**

- Text is not accepted instead of the boolean value `true` or `false`.
- The response describes the data type error.

**Note:** If the backend returns `201`, the implementation does not enforce the data type declared in the OpenAPI specification.

## TC08 - Empty JSON object

**Category:** Negative

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{}
```

**Expected status:** `400 Bad Request`

**Checks:**

- The API rejects the request because the required `name` field is missing.
- No new record is created.

## TC09 - Request without JSON body

**Category:** Negative and protocol-level

**Endpoint:** `POST /api/policies`

**Request body:** No request body

**Expected status:** `400 Bad Request`

**Checks:**

- The API reports that a JSON body is required.
- The API does not return `500` or an HTML error page.

## TC10 - Duplicate name

**Category:** Business rule

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": "Duplicate policy",
  "action": "block",
  "enabled": true
}
```

**Expected status:** Must be defined by the business requirement.

**Checks:**

- Send the same request twice.
- If names must be unique, a response such as `409 Conflict` may be expected.
- If duplicates are allowed, the second request should return `201` with a different `id`.

**Note:** A tester should not invent the expected behaviour. If the rule is not defined in the requirements or documentation, it should be clarified with an analyst or developer.

## TC11 - Extremely long name

**Category:** Boundary

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": "<A repeated approximately 5000 times>",
  "action": "block",
  "enabled": true
}
```

**Expected status:** Controlled validation according to the defined maximum length.

**Checks:**

- The API does not fail with `500`.
- The accepted maximum length should be defined in the requirements or OpenAPI schema.
- When the limit is exceeded, the API returns a consistent validation error.

## TC12 - Follow-up verification of stored data

**Category:** Integration

**Endpoint:** `POST /api/policies`

**Request body:**

```json
{
  "name": "Stored policy",
  "action": "audit",
  "enabled": true
}
```

**Expected status:** The POST request returns `201` and the following GET request returns `200`.

**Checks:**

- Save the `id` returned by the POST response.
- Execute `GET /api/policies/{id}`.
- Values returned by GET match the values sent in the POST request.
- This verifies the actually available state, not only the creation response.

# Extension for a real secured API

For a production API with authentication and authorization, additional scenarios would include:

- A request without a token returns `401 Unauthorized`.
- A request with an invalid or expired token returns `401 Unauthorized`.
- An authenticated user without the required role receives `403 Forbidden`.
- An authorized user can create a policy and the operation is recorded in the audit log.
- Sensitive information and tokens do not appear in error responses or normal application logs.

# What to verify in every scenario

| Area | Check |
|---|---|
| HTTP | Method, URL, status code, Content-Type, and required headers |
| Response | JSON structure, required fields, data types, and concrete values |
| Business | Correct defaults, allowed values, and duplicate handling rules |
| System state | The record actually exists and can be retrieved with a follow-up GET |
| Errors | Consistent error description without unhandled `500` responses |
| Documentation | Actual API behaviour matches the OpenAPI specification |

# Interview summary

For one endpoint, I would not test only the happy path.

For a POST request, I would cover a valid complete payload, required fields only, missing and empty values, incorrect data types, invalid values, boundary lengths and, depending on business rules, duplicate handling and authorization.

I would not verify only the status code. I would also validate the response structure and values. For a created object, I would use a follow-up GET request to verify that it is actually available with the correct data.

At the same time, I would compare the real API behaviour with the OpenAPI documentation.
