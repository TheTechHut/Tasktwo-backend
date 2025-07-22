# 🎫 Ticketing System API

This project uses FastAPI for backend logic and includes auto-generated Swagger/OpenAPI docs.

---

## 🔐 Role-Based Access

| Role      | Access Privileges                                           |
|-----------|-------------------------------------------------------------|
| Customer  | Create tickets, view only their own tickets                 |
| Agent     | View all tickets, update ticket status/resolution           |
| Admin     | Full control: assign tickets, view/update any ticket        |

Access control is enforced using FastAPI dependencies and JWT authentication.

---

## 👨‍💼 Admin Assignment Flow

Admins can assign tickets to agents via this endpoint:

### 📝 Steps:
1. Admin logs in and receives a JWT token.
2. Sends a PATCH request with:
   - `ticket_id` (in path)
   - `agent_id` (as query param)
3. The system:
   - Assigns the ticket to the specified agent
   - Updates the status to **Assigned**

---

## 🤖 Chatbot Embed Endpoint

Allow **external clients or chatbots** to fetch ticket data securely via a token, without needing full authentication.

### 🔐 Generate Embed Token

```http
GET /tickets/tickets/generate_embed_token/{ticket_id}