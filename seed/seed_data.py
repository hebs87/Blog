from faker import Faker

from main.models import Blog, Comment, Category


def generate_blog_data(faker):
    """ Generate seed data for Blog model """
    blogs = [Blog(title=faker.sentence(), body=faker.paragraph()) for _ in range(0, 500)]
    Blog.objects.bulk_create(blogs)


def generate_comment_data(faker):
    """ Generate seed data for Comment model """
    for blog in Blog.objects.iterator():
        comments = [Comment(comment=faker.paragraph(), blog=blog) for _ in range(0, 3)]
        Comment.objects.bulk_create(comments)


def generate_category_data():
    """ Generate seed data for Category model """
    data = ['Web Development', 'Databases', 'Data Science', 'Security', 'Django', 'Python']
    categories = [Category(name=i) for i in data]
    Category.objects.bulk_create(categories)


def generate_seed_data():
    """ Generates seed data for all models """
    faker = Faker()

    # Generate Blog data
    generate_blog_data(faker)

    # Generate Comment data
    generate_comment_data(faker)

    # Generate Category data
    generate_category_data()
