bash:
	docker compose run --rm api bash

migrate:
	docker compose run --rm api bash -c "./manage.py migrate"

migrations:
	docker compose run --rm api bash -c "./manage.py makemigrations"

superuser:
	docker compose run --rm api python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser(username='root', password='root')"

check:
	docker compose run --rm api black --check .

format:
	docker compose run --rm api black .