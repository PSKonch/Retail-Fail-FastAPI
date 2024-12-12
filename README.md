# RetailFail-FastAPI

RetailFail is a grocery store management project built with a focus on Clean Architecture. It leverages a modern tech stack to ensure a maintainable, modular, and efficient solution for handling products, orders, and user interactions. With support for background tasks, caching, and flexible data storage, RetailFail is designed to handle complex operations seamlessly.

## About the Project

RetailFail aims to demonstrate best practices in software development, with a strong emphasis on:

- **Modularity**: Ensuring a well-structured and scalable codebase.
- **Efficiency**: Handling requests and background tasks with minimal latency.
- **Flexibility**: Supporting structured data (SQL) and unstructured data (NoSQL) in a single solution.
- **Clean Architecture**: Separation of concerns, allowing for easy modifications and testing.

## Key Features

### Product Management
- Add, edit, and delete products.
- Search, filter, and sort products by category, name, or price.
- Automatic removal of products from carts when deleted.
- Cascading deletions for categories and their associated products.

### Cart Management
- Add products to the cart or increase their quantity.
- Decrease product quantity or remove products from the cart.
- Clear the cart entirely.
- Automatic updates to remove unavailable products.

### Order Management
- Create orders directly from the cart.
- Send notifications upon order placement.
- Flexible storage of order history in MongoDB.

### Caching
- Dynamic caching with Redis for frequently accessed data.
- Optimized response times for popular queries.

### Background Task Processing
- Celery for handling long-running operations and asynchronous tasks.
- Example: Sending order confirmation messages.

### Flexible Data Storage
- PostgreSQL for structured data (products, orders, categories).
- MongoDB for unstructured data (order history, logs).

## Technologies Used

- **FastAPI**: For building a high-performance REST API.
- **PostgreSQL**: As the primary database for structured data.
- **SQLAlchemy**: ORM for PostgreSQL, ensuring efficient and maintainable database interactions.
- **Redis**: For caching frequently accessed data.
- **Celery**: For asynchronous task processing.
- **RabbitMQ**: As the Celery broker.
- **MongoDB**: For storing unstructured data such as order history and logs.
- **Docker Compose**: For containerized deployment of all services.

## Architecture

RetailFail follows the principles of Clean Architecture:
- **Domain Layer**: Contains core business logic.
- **Application Layer**: Includes use cases and service orchestration.
- **Infrastructure Layer**: Handles database interactions, messaging, and caching.
- **Presentation Layer**: API endpoints built with FastAPI.

## Setup Instructions

### Prerequisites

- Docker and Docker Compose installed on your system.
- A `.env` file with configuration for PostgreSQL, Redis, RabbitMQ, and MongoDB.

### Steps to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/PSKonch/Retail-Fail-FastAPI.git
   cd Retail-Fail-FastAPI
   ```

2. Configure the `.env` file with the necessary environment variables:
   ```env
   # PostgreSQL Configuration
   POSTGRES_NAME=your_database_name
   POSTGRES_HOST=your_database_host
   POSTGRES_PORT=5432
   POSTGRES_USER=your_database_user
   POSTGRES_PASSWORD=your_database_password

   # SMTP Server Configuration
   SMTP_SERVER=smtp.example.com
   SMTP_PORT=587
   SMTP_USERNAME=your_smtp_user
   SMTP_PASSWORD=your_smtp_password

   # Redis Configuration (default values provided in code)
   REDIS_HOST=localhost
   REDIS_PORT=6379

   # RabbitMQ Configuration (default values provided in code)
   RABBITMQ_HOST=localhost
   RABBITMQ_PORT=5672
   RABBITMQ_USER=guest
   RABBITMQ_PASSWORD=guest
   ```

3. Start the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```

4. Access the API documentation at `http://localhost:8000/docs`.

## Future Improvements

- **Notifications**: Enhance user notifications with personalized updates.
- **Analytics**: Add analytics for user behavior and sales trends.
- **Advanced Search**: Implement full-text search for products and orders.
- **Load Testing**: Optimize performance under high traffic using tools like `Locust` or `k6`.
- **Frontend Integration**: Although currently backend-focused, a frontend could be integrated using FastUI or another framework.

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

---

For any questions or feedback, please contact Dimitriy Shaban at [shaban.benito.dimitri@gmail.com].

