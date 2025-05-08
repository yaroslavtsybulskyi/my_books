# FastAPI Books Library

A simple FastAPI application demonstrating:
- CRUD operations for books, authors, and publishers
- SQLAlchemy relationships (One-to-Many, Many-to-Many)
- Background tasks
- WebSocket support

---

## Getting Started

###  Prerequisites

- Python 3.8+
- [virtualenv](https://virtualenv.pypa.io/)
- SQLite (default) or modify for another DB
- Uvicorn with WebSocket support

```bash
pip install -r requirements.txt
```

Running the App
```bash
uvicorn main:app --reload
```

The app will be available at http://127.0.0.1:8000  

API Endpoints  

Base path: /mylib  
	•	GET /books/ – List all books  
	•	POST /books/ – Add a book  
	•	PATCH /books/{id} – Update book  
	•	DELETE /books/{id} – Delete book  
	•	GET /authors/ – List authors  
	•	POST /authors/ – Add author  
	•	GET /publishers/ – List publishers  
	•	POST /publishers/ – Add publisher  
	•	DELETE /publishers/{id} – Delete publisher  

WebSocket Testing (Postman or Browser)  
```
ws://localhost:8000/ws/chat/{client_id}
```
Replace {client_id} with any string like user123.   

In Postman:  
	1.	Open a new WebSocket Request tab.  
	2.	Connect to: ws://localhost:8000/ws/chat/user123  
	3.	Send a text message (e.g. "Hello WebSocket")  
	4.	You’ll receive back a confirmation message from the server.  

Notes  
	•	Data is stored in books.db (SQLite).  
	•	Base.metadata.create_all() auto-generates tables.  
	•	WebSocket sends back messages and logs disconnects.  
