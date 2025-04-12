### To run the server
Run the application using `uvicorn src.main:app --reload`

### To perform database migration use
`alembic revision --autogenerate -m "Initial migration"`
`alembic upgrade head`

### To update migrations
`alembic revision --autogenerate -m "Added quantity column"`
`alembic upgrade head`