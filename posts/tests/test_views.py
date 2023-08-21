from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, Comment, Like
from ..forms import PostModelForm, CommentModelForm

# Create your tests here.


class IndexViewTest(TestCase):
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

    def test_post_comment_forms_in_context(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123"
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(reverse("posts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue((
            "post_form" in response.context
            and
            "comment_form" in response.context
        ))
        self.assertTrue((
            isinstance(response.context["post_form"], PostModelForm)
            and
            isinstance(response.context["comment_form"], CommentModelForm)
        ))
        self.client.logout()

    def test_posts_order_in_context(self):
        is_logged_in = self.client.login(
            username="Sparrow",
            password="pass321"
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(reverse("posts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context), 2)
        self.assertEqual(
            response.context["post_list"][0],
            Post.objects.get(id=2)
        )
        self.client.logout()


class PostViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username="Jack", password="pass123")
        post = Post.objects.create(
            title="Strong Post",
            text="These are strong words of the strong post.",
            owner=user1,
        )

    def setUp(self):
        self.form = PostModelForm()
        self.post = Post.objects.last()

    def test_get_post_detail_page(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(
            reverse("posts:post_detail", kwargs={"post_pk": self.post.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("post" in response.context)
        self.assertEqual(response.context["post"], self.post)
        self.client.logout()

    def test_json_errors_with_invalid_text_field(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        self.form.data["title"] = ""
        self.form.data["text"] = "A"
        response = self.client.post(
            reverse("posts:post_create"),
            self.form.data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(json_resp["text"][0],
                         "Post must have at least 2 characters!")
        self.assertRaises(KeyError, lambda: json_resp["title"])
        self.client.logout()

    def test_redirect_with_valid_text_field(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        self.form.data["title"] = "New Post"
        self.form.data["text"] = "Nice post!"
        response = self.client.post(
            reverse("posts:post_create"),
            self.form.data,
            follow=True,
        )
        self.post = Post.objects.last()
        self.assertRedirects(response, reverse(
            "posts:post_detail", kwargs={"post_pk": self.post.id}))
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertTrue(Post.objects.last().title == "New Post")
        self.client.logout()


class CommentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username="Jack", password="pass123")
        Post.objects.create(
            title="Strong Post",
            text="These are strong words of the strong post.",
            owner=user1,
        )

    def setUp(self):
        self.form = CommentModelForm()
        self.post = Post.objects.get(id=1)

    def test_json_errors_with_invalid_text_field(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        self.form.data["text"] = ""
        response = self.client.post(
            reverse("posts:comment_create", kwargs={"post_pk": self.post.id}),
            self.form.data,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertEqual(json_resp["text"][0], "This field is required.")
        self.client.logout()

    def test_redirect_with_valid_text_field(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        self.form.data["text"] = "Nice post!"
        response = self.client.post(
            reverse("posts:comment_create", kwargs={"post_pk": self.post.id}),
            self.form.data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            "posts:post_detail", kwargs={"post_pk": self.post.id}))
        self.client.logout()


class PostCommentsViewTest(TestCase):
    """ NOTE: This tests assumes that the comments chunks are paginated by '2' """

    @classmethod
    def setUpTestData(cls):
        """ Create a post to put some comments on it. """
        user1 = User.objects.create_user(
            username="Jack", password="pass123")
        post = Post.objects.create(
            title="Strong Post",
            text="These are strong words of the strong post.",
            owner=user1,
        )
        comments_text = [
            "This is a real strong post!",
            "String words!",
            "Nice post!",
            "Keep it up!",
            "Good job!",
        ]
        i = 0
        while (i < 5):
            Comment.objects.create(
                text=comments_text[i],
                post=post,
                owner=user1,
            )
            i += 1

    def setUp(self):
        """ Attributes for the post and its comments. """
        self.post = Post.objects.get(id=1)
        self.comments_qs = (Comment.objects.filter(post=self.post)
                            .select_related().order_by("-created_at"))

    def test_first_comments_chunk_without_get_arg(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(
            reverse("posts:post_comments", kwargs={"post_pk": self.post.id}))
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        id = 5
        for comment_obj in json_resp["commentsChunk"]:
            self.assertEqual(
                comment_obj["text"],
                self.comments_qs.get(id=comment_obj["id"]).text,
            )
            self.assertEqual(
                comment_obj["id"],
                self.comments_qs.get(id=id).id,
            )
            id -= 1
        self.assertTrue(json_resp["hasNext"])
        self.assertEqual(json_resp["commentsCount"], 5)
        self.client.logout()

    def test_first_comments_chunk(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(
            reverse("posts:post_comments", kwargs={"post_pk": self.post.id}) + "?page=1")
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        id = 3
        for comment_obj in json_resp["commentsChunk"]:
            self.assertEqual(
                comment_obj["text"],
                self.comments_qs.get(id=comment_obj["id"]).text,
            )
            self.assertEqual(
                comment_obj["id"],
                self.comments_qs.get(id=id).id,
            )
            id -= 1
        self.assertTrue(json_resp["hasNext"])
        self.client.logout()

    def test_second_comments_chunk(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(
            reverse("posts:post_comments", kwargs={"post_pk": self.post.id}) + "?page=2")
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        id = 3
        for comment_obj in json_resp["commentsChunk"]:
            self.assertEqual(
                comment_obj["text"],
                self.comments_qs.get(id=comment_obj["id"]).text,
            )
            self.assertEqual(
                comment_obj["id"],
                self.comments_qs.get(id=id).id,
            )
            id -= 1
        self.assertTrue(json_resp["hasNext"])
        self.client.logout()

    def test_first_comments_chunk(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(
            reverse("posts:post_comments", kwargs={"post_pk": self.post.id}) + "?page=3")
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        id = 1
        for comment_obj in json_resp["commentsChunk"]:
            self.assertEqual(
                comment_obj["text"],
                self.comments_qs.get(id=comment_obj["id"]).text,
            )
            self.assertEqual(
                comment_obj["id"],
                self.comments_qs.get(id=id).id,
            )
            id -= 1
        self.assertFalse(json_resp["hasNext"])
        self.client.logout()

    def test_last_comments_chunk_with_page_number_beyond_range(self):
        is_logged_in = self.client.login(
            username="Jack",
            password="pass123",
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(
            reverse("posts:post_comments", kwargs={"post_pk": self.post.id}) + "?page=4")
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        id = 1
        for comment_obj in json_resp["commentsChunk"]:
            self.assertEqual(
                comment_obj["text"],
                self.comments_qs.get(id=comment_obj["id"]).text,
            )
            self.assertEqual(
                comment_obj["id"],
                self.comments_qs.get(id=id).id,
            )
            id -= 1
        self.assertFalse(json_resp["hasNext"])
        self.client.logout()
