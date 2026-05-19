import faker_commerce
from faker import Faker

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from newhire.blog.models import Category, Post, Tag

fake = Faker()
fake.add_provider(faker_commerce.Provider)
User = get_user_model()


class Command(BaseCommand):
    help = "Generate sample data for testing purposes"

    def add_arguments(self, parser):
        parser.add_argument("n", type=int, default=1, nargs="?")

    @transaction.atomic
    def _clear_data(self):
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        deleted_users_count, _ = User.objects.filter(
            is_staff=True,
            is_superuser=False,
        ).delete()

        self.stdout.write(
            self.style.WARNING(
                "Cleared existing posts, tags, categories, "
                f"and {deleted_users_count} non-admin users"
            )
        )

    def _generate_categories(self, n=3):
        for _ in range(n):
            name = fake.ecommerce_category()
            Category.objects.create(name=name)

        self.stdout.write(
            self.style.SUCCESS(f"Generated successfully {n} categories")
        )

    def _generate_tags(self):
        tag_names = [
            "best-seller",
            "new-arrival",
            "discount",
            "free-shipping",
            "eco-friendly",
            "premium",
            "handmade",
            "limited-edition",
            "gift-idea",
            "clearance",
        ]

        for name in tag_names:
            Tag.objects.create(name=name)

        self.stdout.write(
            self.style.SUCCESS(f"Generated successfully {len(tag_names)} tags")
        )

    def _generate_posts(self, n=10):
        all_categories = Category.objects.all()
        all_tags = list(Tag.objects.all())
        author, created = User.objects.get_or_create(
            email=fake.email(),
            defaults={
                "name": fake.name(),
                "is_staff": True,
            },
        )
        if created:
            author.set_password("password123")
            author.save(update_fields=["password"])

        for _ in range(n):
            title = fake.sentence(nb_words=6)
            body = fake.paragraph(nb_sentences=5)
            category = fake.random_element(elements=all_categories)
            post = Post.objects.create(
                title=title,
                body=body,
                category=category,
                author=author,
            )
            post.tags.set(fake.random_elements(elements=all_tags, length=3, unique=True))

        self.stdout.write(
            self.style.SUCCESS(f"Generated successfully {n} posts")
        )

        posts = Post.objects.all()
        for post in posts:
            self.stdout.write(
                self.style.SUCCESS(
                    f"Generated post: {post.title} in category {post.category.name}"
                )
            )

    def handle(self, *args, **options):
        self._clear_data()
        self._generate_categories(n=5)
        self._generate_tags()
        self._generate_posts(n=options.get("n"))