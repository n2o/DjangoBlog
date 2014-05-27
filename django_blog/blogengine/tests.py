from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from blogengine.models import Post, Category
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import markdown

# Create your tests here.
class PostTest(TestCase):
    def test_create_category(self):
        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/blogengine/category/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new category
        response = self.client.post('/admin/blogengine/category/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        # self.assertTrue('added successfully' in response.content)

        # Check new category now in database
        all_categories = Category.objects.all()
        # self.assertEqual(len(all_categories), 1)

    def test_edit_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Edit the category
        response = self.client.post('/admin/blogengine/category/1/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        # self.assertTrue('changed successfully' in response.content)

        # Check category amended
        # all_categories = Category.objects.all()
        # self.assertEqual(len(all_categories), 1)
        # only_category = all_categories[0]
        # self.assertEqual(only_category.name, 'perl')
        # self.assertEqual(only_category.description, 'The Perl programming language')

    def test_delete_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Delete the category
        response = self.client.post('/admin/blogengine/category/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        # self.assertTrue('deleted successfully' in response.content)

        # Check category deleted
        # all_categories = Category.objects.all()
        # self.assertEqual(len(all_categories), 0)

    def test_create_post(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()

        # Set the attributes
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.author = author
        post.site = site
        post.category = category

        # Save it
        post.save()

        # Check we can find it
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Check attributes
        self.assertEqual(only_post.title, 'My first post')
        self.assertEqual(only_post.text, 'This is my first blog post')
        self.assertEqual(only_post.slug, 'my-first-post')
        self.assertEqual(only_post.pub_date.day, post.pub_date.day)
        self.assertEqual(only_post.pub_date.month, post.pub_date.month)
        self.assertEqual(only_post.pub_date.year, post.pub_date.year)
        self.assertEqual(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEqual(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEqual(only_post.pub_date.second, post.pub_date.second)
        self.assertEqual(only_post.author.username, 'testuser')
        self.assertEqual(only_post.author.email, 'user@example.com')
        self.assertEqual(only_post.category.name, 'python')
        self.assertEqual(only_post.category.description, 'The Python programming language')


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()


class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

    def test_create_category(self):
        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/blogengine/category/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new category
        response = self.client.post('/admin/blogengine/category/add/', {
            'name': 'python',
            'description': 'The Python programming language'
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        # self.assertTrue('added successfully' in response.content)

        # Check new category now in database
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)

    def test_edit_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Edit the category
        response = self.client.post('/admin/blogengine/category/1/', {
            'name': 'perl',
            'description': 'The Perl programming language'
            }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        # self.assertTrue('changed successfully' in response.content)

        # Check category amended
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEqual(only_category.name, 'perl')
        self.assertEqual(only_category.description, 'The Perl programming language')

    def test_delete_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Delete the category
        response = self.client.post('/admin/blogengine/category/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        # self.assertTrue('deleted successfully' in response.content)

        # Check category deleted
        all_categories = Category.objects.all()
        self.assertEqual(len(all_categories), 0)

    def test_login(self):
        # Get login page
        response = self.client.get('/admin/')

        # Check response code
        self.assertEqual(response.status_code, 200)

        # Check 'Log in' in response
        #self.assertTrue('Log in' in response.content.split())

        # Log the user in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        # self.assertTrue('Log out' in response.content)

    def test_logout(self):
        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log out' in response
        # self.assertTrue('Log out' in response.content)

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code, 200)

        # Check 'Log in' in response
        # self.assertTrue('Log in' in response.content)

    def test_create_post(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/blogengine/post/add/')
        self.assertEqual(response.status_code, 200)

        # Create the new post
        response = self.client.post('/admin/blogengine/post/add/', {
                'title': 'My first post',
                'text': 'This is my first post',
                'pub_date_0': '2013-12-28',
                'pub_date_1': '22:00:04',
                'slug': 'my-first-post',
                'category': '1',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check added successfully
        # self.assertTrue('added successfully' in response.content)

        # Check new post now in database
        # all_posts = Post.objects.all()
        # self.assertEqual(len(all_posts), 1)

    def test_edit_post(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.author = author
        post.site = site
        post.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Edit the post
        response = self.client.post('/admin/blogengine/post/1/', {
                'title': 'My second post',
                'text': 'This is my second blog post',
                'pub_date_0': '2013-12-28',
                'pub_date_1': '22:00:04',
                'slug': 'my-second-post',
                'category': '1',
            },
            follow=True
        )
        self.assertEqual(response.status_code, 200)

        # Check changed successfully
        # self.assertTrue('changed successfully' in response.content)

        # Check post amended
        # all_posts = Post.objects.all()
        # self.assertEqual(len(all_posts), 1)
        # only_post = all_posts[0]
        # self.assertEqual(only_post.title, 'My second post')
        # self.assertEqual(only_post.text, 'This is my second blog post')

    def test_delete_post(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is my first blog post'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.author = author
        post.site = site
        post.category = category
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Delete the post
        response = self.client.post('/admin/blogengine/post/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEqual(response.status_code, 200)

        # Check deleted successfully
        # self.assertTrue('deleted successfully' in response.content)

        # Check post amended
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 0)

class PostViewTest(BaseAcceptanceTest):
    def test_index(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.author = author
        post.site = site
        post.category = category
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)

        # Fetch the index
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

        # Check the post title is in the response
        # self.assertTrue(post.title in response.content)

        # Check the post text is in the response
        # self.assertTrue(markdown.markdown(post.text) in response.content)

        # Check the post date is in the response
        # self.assertTrue(str(post.pub_date.year) in response.content)
        # self.assertTrue(post.pub_date.strftime('%b') in response.content)
        # self.assertTrue(str(post.pub_date.day) in response.content)

        # Check the link is marked up properly
        # self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_post_page(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        site = Site()
        site.name = 'example.com'
        site.domain = 'example.com'
        site.save()

        # Create the post
        post = Post()
        post.title = 'My first post'
        post.text = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.author = author
        post.site = site
        post.category = category
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEqual(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEqual(only_post, post)

        # Get the post URL
        post_url = only_post.get_absolute_url()

        # Fetch the post
        response = self.client.get(post_url)
        self.assertEqual(response.status_code, 200)

        # Check the post title is in the response
        # self.assertTrue(post.title in response.content)

        # Check the post text is in the response
        # self.assertTrue(markdown.markdown(post.text) in response.content)

        # Check the post date is in the response
        # self.assertTrue(str(post.pub_date.year) in response.content)
        # self.assertTrue(post.pub_date.strftime('%b') in response.content)
        # self.assertTrue(str(post.pub_date.day) in response.content)


class FlatPageViewTest(BaseAcceptanceTest):
    def test_create_flat_page(self):
        # Create flat page
        page = FlatPage()
        page.url = '/about/'
        page.title = 'About me'
        page.content = 'All about me'
        page.save()

        # Add the site
        page.sites.add(Site.objects.all()[0])
        page.save()

        # Check new page saved
        all_pages = FlatPage.objects.all()
        self.assertEqual(len(all_pages), 1)
        only_page = all_pages[0]
        self.assertEqual(only_page, page)

        # Check data correct
        self.assertEqual(only_page.url, '/about/')
        self.assertEqual(only_page.title, 'About me')
        self.assertEqual(only_page.content, 'All about me')

        # Get URL
        page_url = str(only_page.get_absolute_url())

        # Get the page
        response = self.client.get(page_url)
        self.assertEqual(response.status_code, 200)

        # Check title and content in response
        # self.assertTrue('About me' in response.content)
        # self.assertTrue('All about me' in response.content)
