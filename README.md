# NKA Generator

**NKA Generator** is a modern web application for designing, simulating, and visualizing **nondeterministic finite automats**. The project features a Next.js frontend for interactive automat building and a Python backend for automat logic and simulation.

---

## Features

- **Visual NFA Designer:** Create and edit nondeterministic finite automat via an intuitive web UI.
- **Simulation:** Test input strings on your NFA and visualize the computation paths in real time.
- **Visualization:** See states, transitions, and all possible nondeterministic branches.
- **Educational Tool:** Ideal for learning and teaching formal languages and automat theory.

---

## Tech Stack

### Frontend

- **Next.js** (React, TypeScript)
- **Tailwind CSS** (modern styling)
- **ReactFlow** (graph visualization)

### Backend

- **Python 3.9+**
- **FastAPI** (REST API)
- **NetworkX / Graphviz** (for graph operations and automat visualization)
- **Custom automat logic**

### Deployment

- **Docker & Docker Compose**

---

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/LukasCec/NKA-Generator.git

cd NKA-Generator-main/src
```

---

### 2. Start with Docker Compose

```bash
docker-compose up --build
```

- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend API:** [http://localhost:8000](http://localhost:8000)

---

### 3. Usage

1. Open [http://localhost:3000](http://localhost:3000) in your web browser.
2. Enter the regular expression to visualise it's automat
3. Use the visual editor to discover states, transitions etc.
4. Enter input strings to test if given automat accepts it.


---

## Project Structure

```bash
NKA-Generator-main/
├── src/
│   ├── backend/               # FastAPI app, NKA logic, API endpoints
│   ├── frontend/              # Next.js app, automat UI, visualization
│   ├── docker-compose.yml     # Multi-service orchestration
│   └── ...
├── README.md
└── ...
```

---

## Example API Usage

**Simulate an input string on your NFA:**

`POST /simulate`

```json
{
  "states": ["q0", "q1"],
  "alphabet": ["a", "b"],
  "transitions": {
    "q0": {"a": ["q0", "q1"], "b": ["q0"]},
    "q1": {"b": ["q1"]}
  },
  "start_state": "q0",
  "accept_states": ["q1"],
  "input_string": "aab"
}
```

**Response:**

```json
{
  "accepted": true,
  "paths": [
    ["q0", "q0", "q1", "q1"],
    ["q0", "q1", "q1", "q1"]
  ]
}
```

---

## Screenshots

_Add screenshots of the UI and automat diagrams here!_

---

## License

This project is for educational and personal use.  
For commercial use, review all included library licenses.

---

## Credits

- Next.js, React, TypeScript
- FastAPI, Python
- ReactFlow

---

Learn, visualize, and experiment with automat using **NKA Generator**!
