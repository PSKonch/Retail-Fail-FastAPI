# Retail-Fail-FastAPI

The "RetailFail" project is an attempt to build a grocery store using Clean Architecture and a stack of FastAPI, PostgreSQL, Redis, Celery, SQLAlchemy, and MongoDB. The goal is to create a simple and maintainable solution capable of handling product and order management.

About the project: RetailFail is a store project that leverages Clean Architecture to ensure modularity and a well-structured codebase. The technology stack enables efficient request handling and background task processing, with SQLAlchemy for ORM and MongoDB for handling flexible, unstructured data.

Features:

Product Management: add, edit, delete products, with filtering and sorting.
Order Management: create and track orders.
Redis caching for quick access to popular data.
Celery for background tasks and handling long-running operations.
MongoDB for flexible storage of unstructured data and logs.
Technologies:

FastAPI for building a REST API.
PostgreSQL for core data storage.
SQLAlchemy as the ORM for PostgreSQL.
Redis for caching.
Celery for background tasks.
MongoDB for managing flexible or unstructured data.
Setup:

Clone the repository and configure the .env file for PostgreSQL, Redis, and MongoDB connections.
Run Docker Compose to start all services.
You’re all set!
