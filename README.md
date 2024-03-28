# Social Network Docker Project

This repository contains a Social Network project configured to run inside a Docker container. It provides a convenient way to set up and run the Django project in a consistent environment across different systems.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Docker: [Installation guide](https://docs.docker.com/get-docker/)
- Docker Compose: [Installation guide](https://docs.docker.com/compose/install/)

## Getting Started

To get started with this project, follow these steps:

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/django-docker-project.git
   ```

2. Change into the project directory:

   ```
   cd django-docker-project
   ```

3. Build the Docker image:

   ```
   docker-compose build
   ```

4. Start the Docker container:

   ```
   docker-compose up
   ```

5. Access the Django project in your web browser:

   ```
   http://localhost:8000
   ```

## Project Structure

The project directory structure is organized as follows:

- `socialnetwork/`: Django project directory.
- `requirements.txt`: Python dependencies for the Django project.
- `Dockerfile`: Dockerfile for building the Docker image.
- `docker-compose.yml`: Docker Compose configuration file for defining services.

## Configuration

You can customize the project configuration by modifying the following files:

- `socialnetwork/settings.py`: Django settings file.
- `docker-compose.yml`: Docker Compose configuration file.
- `Dockerfile`: Dockerfile for building the Docker image.

## Usage

- Use Django management commands inside the Docker container:

  ```
  docker-compose run web python manage.py <command>
  ```

- Access the Django shell:

  ```
  docker-compose run web python manage.py shell
  ```

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvement, please open an issue or a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

