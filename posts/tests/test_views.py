from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Post, Comment, Like
from ..forms import PostModelForm, CommentModelForm

# Create your tests here.


class IndexViewTest(TestCase):
    username = "Jack"
    password = "pass123"

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username=cls.username,
            password=cls.password,
        )
        post = Post.objects.create(
            title="Post #1",
            text="Blah...",
            owner=user,
        )
        post = Post.objects.create(
            title="Post #2",
            text="Blah blah...",
            owner=user,
        )
        post = Post.objects.create(
            title="Post #3",
            text="Blah blah blah...",
            owner=user,
        )
        post = Post.objects.create(
            title="Post #4",
            text="Blah blah blah blah...",
            owner=user,
        )

    def test_redirect_without_log_in(self):
        profile_url = reverse("posts:index")
        response = self.client.get(profile_url)
        self.assertRedirects(
            response,
            "/accounts/login/?next=" + profile_url,
        )

    def test_post_comment_forms_in_context(self):
        is_logged_in = self.client.login(
            username=self.username,
            password=self.password,
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
            username=self.username,
            password=self.password,
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(reverse("posts:index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["post_list"]), 3)
        self.assertEqual(
            response.context["post_list"][0],
            Post.objects.last()
        )
        self.client.logout()


class ProfileViewTest(TestCase):
    username = "Jack"
    password = "pass123"
    username2 = "Sparrow"
    password2 = "pass321"

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username=cls.username,
            password=cls.password,
        )
        user2 = User.objects.create_user(
            username=cls.username2,
            password=cls.password2,
        )
        Post.objects.create(
            title="user1 post #1",
            text="blah...",
            owner=user1,
        )
        Post.objects.create(
            title="user1 post #2",
            text="blah 2...",
            owner=user1,
        )
        Post.objects.create(
            title="user1 post #3",
            text="blah 3...",
            owner=user1,
        )
        Post.objects.create(
            title="user1 post #4",
            text="blah 4...",
            owner=user1,
        )
        Post.objects.create(
            title="user2 post #1",
            text="blah...",
            owner=user2,
        )
        Post.objects.create(
            title="user2 post #2",
            text="blah 2...",
            owner=user2,
        )
        Post.objects.create(
            title="user2 post #3",
            text="blah 3...",
            owner=user2,
        )
        Post.objects.create(
            title="user2 post #4",
            text="blah 4...",
            owner=user2,
        )

    def setUp(self):
        self.user1 = User.objects.first()
        self.user2 = User.objects.last()
        self.user1_post_list = (Post.objects.filter(owner=self.user1)
                                .select_related().order_by("-created_at"))
        self.user2_post_list = (Post.objects.filter(owner=self.user2)
                                .select_related().order_by("-created_at"))

    def test_redirect_without_log_in(self):
        profile_url = reverse("posts:profile",
                              kwargs={"username": self.username, })
        response = self.client.get(profile_url)
        self.assertRedirects(
            response,
            "/accounts/login/?next=" + profile_url,
        )

    def test_get_only_user1_profile_posts(self):
        is_logged_in = self.client.login(
            username=self.username,
            password=self.password,
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(reverse(
            "posts:profile",
            kwargs={
                "username": self.username,
            },
        ))
        self.assertEqual(response.status_code, 200)
        len_post_list = len(response.context["post_list"])
        i = 0
        while i < len_post_list:
            self.assertEqual(
                response.context["post_list"][i],
                self.user1_post_list[i],
            )
            i += 1

    def test_get_only_user2_profile_posts(self):
        is_logged_in = self.client.login(
            username=self.username,
            password=self.password,
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(reverse(
            "posts:profile",
            kwargs={
                "username": self.username2,
            },
        ))
        self.assertEqual(response.status_code, 200)
        len_post_list = len(response.context["post_list"])
        i = 0
        while i < len_post_list:
            self.assertEqual(
                response.context["post_list"][i],
                self.user2_post_list[i],
            )
            i += 1

    def test_pagination_3_posts_per_page(self):
        is_logged_in = self.client.login(
            username=self.username,
            password=self.password,
        )
        self.assertTrue(is_logged_in)
        url = reverse("posts:profile",
                      kwargs={"username": self.username}) + "?page=1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        len_post_list = len(response.context["post_list"])
        print(response.context["post_list"])
        self.assertEqual(len_post_list, 3)
        i = 0
        while i < len_post_list:
            self.assertEqual(
                response.context["post_list"][i],
                self.user1_post_list[i],
            )
            i += 1
        self.assertTrue(response.context["page_obj"].has_next())


class PostViewTest(TestCase):
    username = "Jack"
    password = "pass123"

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username=cls.username,
            password=cls.password,
        )
        Post.objects.create(
            title="Strong Post",
            text="These are strong words of the strong post.",
            owner=user,
        )

    def setUp(self):
        self.form = PostModelForm()
        self.post = Post.objects.last()

    def test_redirect_without_log_in(self):
        profile_url = reverse(
            "posts:post_detail",
            kwargs={
                "username": self.username,
                "post_pk": self.post.id,
            },
        )
        response = self.client.get(profile_url)
        self.assertRedirects(
            response,
            "/accounts/login/?next=" + profile_url,
        )

    def test_get_post_detail_page(self):
        is_logged_in = self.client.login(
            username=self.username,
            password=self.password,
        )
        self.assertTrue(is_logged_in)
        response = self.client.get(
            reverse("posts:post_detail", kwargs={
                "username": self.username,
                "post_pk": self.post.id,
            }))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("post" in response.context)
        self.assertEqual(response.context["post"], self.post)
        self.client.logout()

    def test_json_errors_with_invalid_text_field(self):
        is_logged_in = self.client.login(
            username=self.username,
            password=self.password,
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
            username=self.username,
            password=self.password,
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
            "posts:post_detail", kwargs={
                "username": self.username,
                "post_pk": self.post.id,
            }
        ))
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertTrue(Post.objects.last().title == "New Post")
        self.client.logout()


class CommentViewTest(TestCase):
    username = "Jack"
    password = "pass123"

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username=cls.username,
            password=cls.password
        )
        Post.objects.create(
            title="Strong Post",
            text="These are strong words of the strong post.",
            owner=user,
        )

    def setUp(self):
        self.form = CommentModelForm()
        self.post = Post.objects.get(id=1)

    def test_redirect_without_log_in(self):
        self.form.data["text"] = ""
        profile_url = reverse(
            "posts:comment_create",
            kwargs={
                "post_pk": self.post.id
            },
        )
        response = self.client.post(profile_url, self.form.data, follow=True)
        self.assertRedirects(
            response,
            "/accounts/login/?next=" + profile_url,
        )

    def test_json_errors_with_invalid_text_field(self):
        is_logged_in = self.client.login(
            username=self.username,
            password=self.password,
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
            username=self.username,
            password=self.password,
        )
        self.assertTrue(is_logged_in)
        self.form.data["text"] = "Nice post!"
        response = self.client.post(
            reverse("posts:comment_create", kwargs={"post_pk": self.post.id}),
            self.form.data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            "posts:post_detail", kwargs={
                "username": self.username,
                "post_pk": self.post.id,
            }
        ))
        self.client.logout()


class PostCommentsViewTest(TestCase):
    """ NOTE: This tests assumes that the comments chunks are paginated by '2' """
    username = "Jack"
    password = "pass123"

    @classmethod
    def setUpTestData(cls):
        """ Create a post to put some comments on it. """
        user = User.objects.create_user(
            username=cls.username,
            password=cls.password,
        )
        post = Post.objects.create(
            title="Strong Post",
            text="These are strong words of the strong post.",
            owner=user,
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
                owner=user,
            )
            i += 1

    def setUp(self):
        """ Attributes for the post and its comments. """
        self.post = Post.objects.first()
        self.comments_qs = (Comment.objects.filter(post=self.post)
                            .select_related().order_by("-created_at"))

    def test_redirect_without_log_in(self):
        profile_url = reverse(
            "posts:post_comments",
            kwargs={"post_pk": self.post.id}
        ) + "?page=1"
        response = self.client.get(profile_url)
        self.assertRedirects(
            response,
            "/accounts/login/?next=" + profile_url,
        )

    def test_first_comments_chunk_without_get_arg(self):
        is_logged_in = self.client.login(
            username=self.username,
            password=self.password,
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
            username=self.username,
            password=self.password,
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
            username=self.username,
            password=self.password,
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
            username=self.username,
            password=self.password,
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
            username=self.username,
            password=self.password,
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


class PostLikesAndPostDislikeViewsTest(TestCase):
    username1 = "Jack"
    username2 = "Sparrow"
    password1 = "pass123"
    password2 = "pass321"

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(
            username=cls.username1, password=cls.password1)
        user2 = User.objects.create_user(
            username=cls.username2, password=cls.password2)
        Post.objects.create(text="Blah 1...", owner=user1)
        Post.objects.create(text="Blah 2...", owner=user2)

    def setUp(self):
        self.user1 = User.objects.first()
        self.user2 = User.objects.last()
        self.post1 = Post.objects.first()
        self.post2 = Post.objects.last()
        Like.objects.create(post=self.post2, owner=self.user1)
        Like.objects.create(post=self.post2, owner=self.user2)

    def login_logic(self, username, password):
        return self.client.login(
            username=username,
            password=password,
        )

    def test_likes_count_before_any_likes(self):
        self.assertTrue(self.login_logic(self.username1, self.password1))
        response = self.client.get(
            reverse("posts:post_likes", kwargs={"post_pk": self.post1.id}))
        self.assertEqual(response.status_code, 200)
        json_resp = response.json()
        self.assertTrue("likes" in json_resp)
        self.assertEqual(json_resp["likes"], 0)
        self.client.logout()

    def test_likes_count_after_some_likes(self):
        # 'user1' like 'post1'
        self.assertTrue(self.login_logic(self.username1, self.password1))
        response = self.client.post(
            reverse("posts:post_likes", kwargs={"post_pk": self.post1.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("posts:post_likes", kwargs={"post_pk": self.post1.id})
        )
        json_resp = response.json()
        self.assertTrue("likes" in json_resp)
        self.assertEqual(json_resp["likes"], 1)
        self.client.logout()
        # 'user2' like 'post1'
        self.assertTrue(self.login_logic(self.username2, self.password2))
        response = self.client.post(
            reverse("posts:post_likes", kwargs={"post_pk": self.post1.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("posts:post_likes", kwargs={"post_pk": self.post1.id})
        )
        json_resp = response.json()
        self.assertTrue("likes" in json_resp)
        self.assertEqual(json_resp["likes"], 2)
        self.client.logout()

    def test_likes_count_after_some_dislikes(self):
        # User1 dislike post2
        self.assertTrue(self.login_logic(self.username1, self.password1))
        response = self.client.post(
            reverse("posts:post_dislike", kwargs={"post_pk": self.post2.id}),
            follow=True,
        )
        self.assertRedirects(
            response,
            reverse("posts:post_likes", kwargs={"post_pk": self.post2.id})
        )
        json_resp = response.json()
        self.assertTrue("likes" in json_resp)
        self.assertEqual(json_resp["likes"], 1)
        self.client.logout()
        # 'user2' dislike 'post2'
        self.assertTrue(self.login_logic(self.username2, self.password2))
        response = self.client.post(
            reverse("posts:post_dislike", kwargs={"post_pk": self.post2.id}),
            follow=True
        )
        self.assertRedirects(
            response,
            reverse("posts:post_likes", kwargs={"post_pk": self.post2.id})
        )
        json_resp = response.json()
        self.assertTrue("likes" in json_resp)
        self.assertEqual(json_resp["likes"], 0)
        self.client.logout()
