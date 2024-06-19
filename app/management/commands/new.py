from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app.models import Question, Answer, Tag, Like, Profile
import random
import string
class Command(BaseCommand):
    help = 'Loads test data into the database'
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, default=10000, help='Number of users to create')

    def handle(self, *args, **options):
        users_count = options['ratio']
        questions_count = users_count * 10
        answers_count = users_count * 100
        tags_count = users_count
        likes_count =  users_count * 200

        users = []

        for _ in range(users_count):
            user = User(
                username=''.join(random.choices(string.ascii_letters + string.digits, k=10)),
                email="test@test.com",
                password='testpassword')
            users.append(user)

        User.objects.bulk_create(users)

        profiles = []
        for item in User.objects.all():
            profile = Profile(
                user=item
            )
            profiles.append(profile)

        Profile.objects.bulk_create(profiles)

        tags = []
        for _ in range(tags_count):
            tag = Tag(
                name=''.join(random.choices(string.ascii_letters + string.digits, k=10)))
            tags.append(tag)

        Tag.objects.bulk_create(tags)

        # Create questions
        questions = []
        for _ in range(questions_count):
            question = Question(
                author = random.choice(User.objects.all()),
                title=''.join(random.choices(string.ascii_letters + string.digits, k=50)),
                text=''.join(random.choices(string.ascii_letters + string.digits, k=100)))
            questions.append(question)

        Question.objects.bulk_create(questions)
        for item in Question.objects.all():
            tags = random.choices(Tag.objects.all(), k=3)
            item.tag.add(tags[0])
            item.tag.add(tags[1])
            item.tag.add(tags[2])

        # Create answers
        answers = []
        for _ in range(answers_count):
            answer = Answer(
                author=random.choice(User.objects.all()),
                question=random.choice(Question.objects.all()),
                text=''.join(random.choices(string.ascii_letters + string.digits, k=200)))
            answers.append(answer)

        Answer.objects.bulk_create(answers)

        # Create votes


        likes = []
        for _ in range(likes_count):
            like = Like(
                user=random.choice(User.objects.all()),
                status=random.choice(["l", "d"]))
            likes.append(like)
        Like.objects.bulk_create(likes)

        for item in Like.objects.all()[:(len(Like.objects.all())//2)]:
            answer = random.choice(Answer.objects.all())
            answer.like.add(item)
        for item in Like.objects.all()[(len(Like.objects.all()) // 2):]:
            question = random.choice(Question.objects.all())
            question.like.add(item)

