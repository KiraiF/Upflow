# Upflow

Upflow is a simple Reddit-style clone built as a personal project for learning and experimentation. It's not production-ready — just a fun project to practice Django, Python, and web development.

## Features

- User authentication (signup, login, logout)
- Create, edit, and delete posts
- Comment on posts
- Upvote and downvote posts and comments
- Browse posts by newest or most popular
- Basic responsive front-end

## Technologies Used

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Database: PostgreSQL

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/KiraiF/Upflow.git
cd Upflow
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Create a superuser:

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Open your browser and go to [http://127.0.0.1:8000](http://127.0.0.1:8000)


## Contributing

Feel free to fork, make improvements, and submit pull requests. This is a learning project, so all contributions are welcome!

## License

MIT License.

