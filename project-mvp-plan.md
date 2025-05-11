## 🧭 **Trello Board: TeamTact – MVP Tracker (with Descriptions)**

---

### 📁 **1. Project Setup**

---

#### **Card**: `Frontend Setup – React + ShadCN`

**Description**:
Set up the initial frontend using React, ShadCN UI components, and a state management solution (Zustand or Context API). Configure TailwindCSS and establish a scalable project structure.

**Checklist**: `Frontend Setup Tasks`

* [ ] Create React project with Vite
* [ ] Install ShadCN and initialize it
* [ ] Configure TailwindCSS
* [ ] Set up folder structure
* [ ] Install Zustand / Context API for state

---

#### **Card**: `Backend Setup – FastAPI`

**Description**:
Initialize the FastAPI backend with all required libraries. Establish the folder layout, database connection, and prepare for scalable endpoint development.

**Checklist**: `Backend Setup Tasks`
**Title**: Dummy Title

* [ ] Initialize FastAPI project
* [ ] Set up virtual environment
* [ ] Install dependencies (FastAPI, Uvicorn, Pydantic)
* [ ] Set up ORM (SQLModel or Tortoise)
* [ ] Connect to PostgreSQL or SQLite
* [ ] Basic folder structure (routers, models, schemas)

---

### 🔐 **2. Authentication**

---

#### **Card**: `Backend JWT Auth – FastAPI`

**Description**:
Implement secure user authentication with access and refresh JWT tokens. This includes signup/login logic and token-protected endpoints.

**Checklist**: `JWT Auth - Backend Tasks`

* [ ] Sign-up route
* [ ] Login route
* [ ] Access + refresh token generation
* [ ] Token refresh route
* [ ] Password hashing
* [ ] Auth dependencies for protected routes

---

#### **Card**: `Frontend Auth – ShadCN`

**Description**:
Design and implement the frontend login/signup interface using ShadCN components. Handle JWT tokens in the browser and protect frontend routes.

**Checklist**: `Auth UI - Frontend Tasks`

* [ ] Auth pages (Login, Sign Up)
* [ ] Auth form using ShadCN components
* [ ] Store JWT token securely
* [ ] Token refresh handling
* [ ] Redirects for authenticated routes

---

### 👥 **3. Team Creation & Invitation**

---

#### **Card**: `Backend – Team Management`

**Description**:
Build backend functionality for creating a team and inviting users using a link or code. Ensure proper validation and user association with teams.

**Checklist**: `Team Management - Backend Tasks`

* [ ] Create team endpoint
* [ ] Invite link generation (with team ID)
* [ ] Join via invite code
* [ ] Validate invite code/link
* [ ] Add user to team

---

#### **Card**: `Frontend – Team Creation & Invite`

**Description**:
Create UI for team creation and joining via invite code. This includes showing generated invite links and linking users to a team.

**Checklist**: `Team Management - Frontend Tasks`

* [ ] UI to create team
* [ ] Display invite link
* [ ] Input for invite code
* [ ] Call backend endpoints
* [ ] Show confirmation on success

---

### 📋 **4. Kanban Board**

---

#### **Card**: `Backend – Task Management APIs`

**Description**:
Develop all required APIs to manage tasks including create, update, delete, move, and assignment functionality, all scoped to teams.

**Checklist**: `Task APIs - Backend`

* [ ] Create task
* [ ] Edit task
* [ ] Delete task
* [ ] Assign member to task
* [ ] Move task between statuses

---

#### **Card**: `Frontend – Kanban UI`

**Description**:
Build a dynamic Kanban board interface using drag-and-drop libraries and ShadCN UI components. Integrate with the backend for full functionality.

**Checklist**: `Kanban UI - Frontend`

* [ ] Columns: To-Do, In Progress, UAT, Done
* [ ] Task cards using ShadCN UI
* [ ] Add/edit/delete task modal
* [ ] Assign member dropdown
* [ ] Implement drag-and-drop (dnd-kit / react-beautiful-dnd)

---

### 💬 **5. Real-time Messenger**

---

#### **Card**: `Backend – WebSocket Chat`

**Description**:
Set up WebSocket routes using FastAPI to support team-specific chat rooms. Handle joining, messaging, and broadcasting in real time.

**Checklist**: `WebSocket Setup - Backend`

* [ ] Set up FastAPI WebSocket routes
* [ ] Group by team ID
* [ ] Broadcast messages to room
* [ ] Store messages in DB

---

#### **Card**: `Frontend – Chat UI`

**Description**:
Develop a chat interface using `socket.io-client` with live updates, proper styling, and support for multiple teams.

**Checklist**: `Messenger UI - Frontend`

* [ ] Connect with socket.io-client
* [ ] Sidebar or modal UI
* [ ] Show sender name and timestamp
* [ ] Auto-scroll to latest message
* [ ] Handle live updates

---

### 📊 **6. Task Tracking & Dashboard**

---

#### **Card**: `Backend – Task Stats & Filtering`

**Description**:
Create endpoints for fetching assigned/unassigned tasks and tracking user progress for dashboard views.

**Checklist**: `Dashboard APIs - Backend`

* [ ] Endpoint to list tasks by user
* [ ] Endpoint to get unassigned tasks
* [ ] Aggregate progress data (optional)

---

#### **Card**: `Frontend – Team Dashboard`

**Description**:
Build a dashboard that shows each team member’s tasks, unassigned tasks, and status counts using clear visual elements.

**Checklist**: `Team Dashboars - Frontend`

* [ ] Show each member’s tasks
* [ ] Section for unassigned tasks
* [ ] Display task counts/statuses

---

### 🚀 **7. Deployment**

---

#### **Card**: `Frontend Deployment – Vercel`

**Description**:
Deploy the frontend app to Vercel with environment variables and automatic updates from GitHub.

**Checklist**: `Deploy Frontend - Vercel`

* [ ] Connect repo
* [ ] Set environment variables
* [ ] Enable CI/CD
* [ ] Test deployment

---

#### **Card**: `Backend Deployment – Render/Railway`

**Description**:
Deploy the backend to Render or Railway with persistent database setup and secured environment variables.

**Checklist**: `Deploy Backend - Render/Railway`

* [ ] Push backend to GitHub
* [ ] Set up PostgreSQL/SQLite
* [ ] Configure environment variables
* [ ] Deploy with automatic build
* [ ] Test API endpoints in prod

---