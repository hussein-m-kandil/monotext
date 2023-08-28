from django.test import TestCase
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from ..models import Post, Comment, Like

# Create your tests here.


class ModelsRelationsTest (TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username="Jack", password="pass123")
        user2 = User.objects.create_user(
            username="Sparrow", password="pass321")
        post1 = Post.objects.create(
            title="Strong Post",
            text="These are strong words of the strong post.",
            owner=user1,
        )
        post2 = Post.objects.create(
            title="New Post",
            text="This is the new post.",
            owner=user2,
        )
        Comment.objects.create(
            text="Keep it up!",
            post=post1,
            owner=user2,
        )
        Comment.objects.create(
            text="Good job!",
            post=post2,
            owner=user1,
        )
        Like.objects.create(
            post=post1,
            owner=user2,
        )
        Like.objects.create(
            post=post2,
            owner=user1,
        )

    def setUp(self):
        self.user1 = User.objects.get(id=1)
        self.user2 = User.objects.get(id=2)
        self.post1 = Post.objects.get(id=1)
        self.post2 = Post.objects.get(id=2)
        self.comment1 = Comment.objects.get(id=1)
        self.comment2 = Comment.objects.get(id=2)
        self.like1 = Like.objects.get(id=1)
        self.like2 = Like.objects.get(id=2)

    def test_relations_between_models(self):
        self.assertEqual(self.post1.owner, self.user1)
        self.assertEqual(self.post2.owner, self.user2)
        self.assertEqual(self.post1.comments.count(), 1)
        self.assertEqual(self.post2.comments.count(), 1)
        self.assertEqual(Comment.objects.filter(
            owner=self.user2)[0], self.comment1)
        self.assertEqual(Comment.objects.filter(
            owner=self.user1)[0], self.comment2)
        self.assertEqual(Comment.objects.filter(
            post=self.post1)[0].owner, self.user2)
        self.assertEqual(Comment.objects.filter(
            post=self.post2)[0].owner, self.user1)
        self.assertEqual(self.post1.likes.count(), 1)
        self.assertEqual(self.post2.likes.count(), 1)
        self.assertEqual(Like.objects.filter(owner=self.user2)[0], self.like1)
        self.assertEqual(Like.objects.filter(owner=self.user1)[0], self.like2)
        self.assertEqual(Like.objects.filter(
            post=self.post1)[0].owner, self.user2)
        self.assertEqual(Like.objects.filter(
            post=self.post2)[0].owner, self.user1)
        comment3 = Comment.objects.create(
            text="Very good!",
            post=self.post1,
            owner=self.user2,
        )
        comment4 = Comment.objects.create(
            text="Very nice!",
            post=self.post2,
            owner=self.user1,
        )
        self.assertEqual(self.post1.comments.count(), 2)
        self.assertEqual(self.post2.comments.count(), 2)
        self.assertEqual(Comment.objects.filter(
            owner=self.user2)[1], comment3)
        self.assertEqual(Comment.objects.filter(
            owner=self.user1)[1], comment4)
        self.assertEqual(Comment.objects.filter(
            post=self.post1)[1].owner, self.user2)
        self.assertEqual(Comment.objects.filter(
            post=self.post2)[1].owner, self.user1)

    def test_unique_constraint_on_likes(self):
        self.assertRaises(
            IntegrityError,
            (lambda post, user: Like.objects.create(post=post, owner=user)),
            post=self.post1,
            user=self.user2,
        )
