from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from django.contrib.auth.models import User

from blog.models import Post, Category, Tag




# Create your tests here.
class PostTest(TestCase):
    def test_create_tag(self):
        # Create the tag
        tag = Tag()

        # Add attributes
        tag.name = 'perl'
        tag.description = 'The Perl programming language'
        tag.slug = 'perl'

        # Save it
        tag.save()

        # Check we can find it
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 1)
        only_tag = all_tags[0]
        self.assertEquals(only_tag, tag)

        # Check attributes
        self.assertEquals(only_tag.name, 'perl')
        self.assertEquals(only_tag.description, 'The Perl programming language')
        self.assertEquals(only_tag.slug, 'perl')

    def test_create_category(self):
        category = Category()

        category.name = 'python'
        category.description = 'The python language'
        category.slug = 'python'

        category.save()

        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category, category)

        self.assertEquals(only_category.name, 'python')
        self.assertEquals(only_category.description, 'The python language')
        self.assertEquals(only_category.slug, 'python')

    # TEST 1
    def test_create_post(self):
        category = Category()
        category.name = 'python'
        category.description = 'The python language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The Python programming language'
        tag.save()

        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # site = Site()
        # site.name = 'nunfuxgvn.com'
        # site.domain = 'nunfuxgvn.com'
        # site.save()

        post = Post()
        post.title = 'First Post'
        post.content = 'My first post -yay'
        post.slug = 'first-post'
        post.pub_date = timezone.now()
        post.author = author
        # post.site = site
        post.category = category

        post.save()

        # Add the tag
        post.tags.add(tag)
        post.save()

        # Check that we can find it
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Check attributes
        self.assertEquals(only_post.title, 'First Post')
        self.assertEquals(only_post.content, 'My first post -yay')
        self.assertEquals(only_post.slug, 'first-post')
        # self.assertEquals(only_post.site.name, 'nunfuxgvn.com')
        # self.assertEquals(only_post.site.domain, 'nunfuxgvn.com')
        self.assertEquals(only_post.pub_date.day, post.pub_date.day)
        self.assertEquals(only_post.pub_date.month, post.pub_date.month)
        self.assertEquals(only_post.pub_date.year, post.pub_date.year)
        self.assertEquals(only_post.pub_date.hour, post.pub_date.hour)
        self.assertEquals(only_post.pub_date.minute, post.pub_date.minute)
        self.assertEquals(only_post.pub_date.second, post.pub_date.second)
        self.assertEquals(only_post.author.username, 'testuser')
        self.assertEquals(only_post.author.email, 'user@example.com')
        self.assertEquals(only_post.category.name, 'python')
        self.assertEquals(only_post.category.description, 'The python language')

        # Check tags
        post_tags = only_post.tags.all()
        self.assertEquals(len(post_tags), 1)
        only_post_tag = post_tags[0]
        self.assertEquals(only_post_tag, tag)
        self.assertEquals(only_post_tag.name, 'python')
        self.assertEquals(only_post_tag.description, 'The Python programming language')


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()


class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

    # TEST 2
    def test_login(self):
        # Get login page
        response = self.client.get('/admin/')

        # Check response code
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)

        # Log the user in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

    # TEST 3
    def test_logout(self):
        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

        # Log out
        self.client.logout()

        # Check response code
        response = self.client.get('/admin/')
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)

    # TEST 4
    def test_create_category(self):
        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/blog/category/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new category
        response = self.client.post('/admin/blog/category/add/', {
            'name': 'python',
            'description': 'The Python programming language'
        },
                                    follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content)

        # Check new category now in database
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)

    def test_edit_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Edit the category
        response = self.client.post('/admin/blog/category/1/', {
            'name': 'perl',
            'description': 'The Perl programming language'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)

        # Check category amended
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 1)
        only_category = all_categories[0]
        self.assertEquals(only_category.name, 'perl')
        self.assertEquals(only_category.description, 'The Perl programming language')

    def test_delete_category(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Delete the category
        response = self.client.post('/admin/blog/category/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check category deleted
        all_categories = Category.objects.all()
        self.assertEquals(len(all_categories), 0)

    def test_create_post(self):
        category = Category()
        category.name = 'python'
        category.description = 'The python language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The Python programming language'
        tag.save()

        self.client.login(username='bobsmith', password='password')

        response = self.client.get('/admin/blog/post/add/')
        self.assertEquals(response.status_code, 200)

        response = self.client.post('/admin/blog/post/add/', {
            'title': 'First Post',
            'text': 'My first post -yay',
            'pub_date_0': '2014-07-17',
            'pub_date_1': '11:41:03',
            'slug': 'first-post',
            # 'site': '1',
            'category': '1',
            'tags': '1'
        },
                                    follow=True
        )
        self.assertEquals(response.status_code, 200)

        self.assertTrue('added successfully' in response.content)

        # Check the new post is in the database
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

    # TEST 5
    def test_edit_posts(self):
        category = Category()
        category.name = 'python'
        category.description = 'The python language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The Python programming language'
        tag.save()

        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # site = Site()
        # site.name = 'nunfuxgvn.com'
        # site.domain = 'nunfuxgvn.com'
        # site.save()


        post = Post()
        post.title = 'First Post'
        post.content = 'My first post -yay'
        post.slug = 'first-post'
        post.pub_date = timezone.now()
        post.author = author
        # post.site = site
        post.save()
        post.tags.add(tag)
        post.save()

        self.client.login(username='bobsmith', password='password')

        response = self.client.post('/admin/blog/post/1/', {
            'title': 'Second Post',
            'text': 'This is my second post',
            'pub_date_0': '2014-07-17',
            'pub_date_1': '11:49:24',
            'slug': 'second-post',
            # 'site': '1',
            'category': '1',
            'tags': '1'
        },
                                    follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check post successfully changed
        self.assertTrue('changed successfully' in response.content)

        # Check post amended 
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post.title, 'Second Post')
        self.assertEquals(only_post.content, 'This is my second post')

        # TEST 6

    def test_delete_post(self):
        category = Category()
        category.name = 'python'
        category.description = 'The python language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The Python programming language'
        tag.save()

        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # site = Site()
        # site.name = 'nunfuxgvn.com'
        # site.domain = 'nunfuxgvn.com'
        # site.save()

        post = Post()
        post.title = 'First Post'
        post.test = 'My first post'
        post.slug = 'first-post'
        post.pub_date = timezone.now()
        post.author = author
        # post.site = site
        post.save()
        post.tags.add(tag)
        post.save()

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        self.client.login(username='bobsmith', password='password')

        response = self.client.post('/admin/blog/post/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        self.assertTrue('deleted successfully' in response.content)

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 0)

    def test_create_post_without_tag(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/blog/post/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new post
        response = self.client.post('/admin/blog/post/add/', {
            'title': 'My first post',
            'text': 'This is my first post',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04',
            'slug': 'my-first-post',
            # 'site': '1',
            'category': '1'
        },
                                    follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content)

        # Check new post now in database
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)


    def test_create_tag(self):
        # Log in
        self.client.login(username='bobsmith', password="password")

        # Check response code
        response = self.client.get('/admin/blog/tag/add/')
        self.assertEquals(response.status_code, 200)

        # Create the new tag
        response = self.client.post('/admin/blog/tag/add/', {
            'name': 'python',
            'description': 'The Python programming language'
        },
                                    follow=True
        )
        self.assertEquals(response.status_code, 200)

        # Check added successfully
        self.assertTrue('added successfully' in response.content)

        # Check new tag now in database
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 1)

    def test_edit_tag(self):
        # Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The Python programming language'
        tag.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Edit the tag
        response = self.client.post('/admin/blog/tag/1/', {
            'name': 'perl',
            'description': 'The Perl programming language'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check changed successfully
        self.assertTrue('changed successfully' in response.content)

        # Check tag amended
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 1)
        only_tag = all_tags[0]
        self.assertEquals(only_tag.name, 'perl')
        self.assertEquals(only_tag.description, 'The Perl programming language')

    def test_delete_tag(self):
        # Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The Python programming language'
        tag.save()

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Delete the tag
        response = self.client.post('/admin/blog/tag/1/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check tag deleted
        all_tags = Tag.objects.all()
        self.assertEquals(len(all_tags), 0)


class PostViewTest(BaseAcceptanceTest):
    def test_index(self):
        category = Category()
        category.name = 'python'
        category.description = 'The python language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'perl'
        tag.description = 'The Perl programming language'
        tag.save()

        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # site = Site()
        # site.name = 'nunfuxgvn.com'
        # site.domain = 'nunfuxgvn.com'
        # site.save()

        post = Post()
        post.title = 'First Post'
        post.content = 'My [first post](http://127.0.0.1:8000/) -yay'
        post.slug = 'first-post'
        post.pub_date = timezone.now()
        post.author = author
        # post.site = site
        post.category = category
        post.save()
        post.tags.add(tag)

        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)

        # Fetch test_index
        response = self.client.get('/')
        self.assertEquals(response.status_code, 200)

        self.assertTrue(post.title in response.content)

        self.assertTrue(markdown.markdown(post.content) in response.content)

        self.assertTrue(post.category.name in response.content)

        post_tag = all_posts[0].tags.all()[0]
        self.assertTrue(post_tag.name in response.content)

        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        self.assertTrue('<a href="http://127.0.0.1:8000/">first post</a>' in response.content)

    def test_post_page(self):
        # Create the post

        category = Category()
        category.name = 'python'
        category.description = 'The python language'
        category.save()

        # Create the tag
        tag = Tag()
        tag.name = 'perl'
        tag.description = 'The Perl programming language'
        tag.save()

        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # site = Site()
        # site.name = 'nunfuxgvn.com'
        # site.domain = 'nunfuxgvn.com'
        # site.save()

        post = Post()
        post.title = 'My first post'
        post.content = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'first-post'
        post.pub_date = timezone.now()
        post.author = author
        # post.site = site
        post.category = category
        post.save()
        post.tags.add(tag)
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the post URL
        post_url = only_post.get_absolute_url()

        # Fetch the post
        response = self.client.get(post_url)
        self.assertEquals(response.status_code, 200)

        # Check the post title is in the response
        self.assertTrue(post.title in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.content) in response.content)

        self.assertTrue(post.category.name in response.content)

        post_tag = all_posts[0].tags.all()[0]
        self.assertTrue(post_tag.name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.content) in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_category_page(self):
        # Create the category
        category = Category()
        category.name = 'python'
        category.description = 'The Python programming language'
        category.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        # site = Site()
        # site.name = 'example.com'
        # site.domain = 'example.com'
        # site.save()

        # Create the post
        post = Post()
        post.title = 'My first post'
        post.content = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.author = author
        # post.site = site
        post.category = category
        post.save()

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the category URL
        category_url = post.category.get_absolute_url()

        # Fetch the category
        response = self.client.get(category_url)
        self.assertEquals(response.status_code, 200)

        # Check the category name is in the response
        self.assertTrue(post.category.name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.content) in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_tag_page(self):
        # Create the tag
        tag = Tag()
        tag.name = 'python'
        tag.description = 'The Python programming language'
        tag.save()

        # Create the author
        author = User.objects.create_user('testuser', 'user@example.com', 'password')
        author.save()

        # Create the site
        # site = Site()
        # site.name = 'example.com'
        # site.domain = 'example.com'
        # site.save()

        # Create the post
        post = Post()
        post.title = 'My first post'
        post.content = 'This is [my first blog post](http://127.0.0.1:8000/)'
        post.slug = 'my-first-post'
        post.pub_date = timezone.now()
        post.author = author
        # post.site = site
        post.save()
        post.tags.add(tag)

        # Check new post saved
        all_posts = Post.objects.all()
        self.assertEquals(len(all_posts), 1)
        only_post = all_posts[0]
        self.assertEquals(only_post, post)

        # Get the tag URL
        tag_url = post.tags.all()[0].get_absolute_url()

        # Fetch the tag
        response = self.client.get(tag_url)
        self.assertEquals(response.status_code, 200)

        # Check the tag name is in the response
        self.assertTrue(post.tags.all()[0].name in response.content)

        # Check the post text is in the response
        self.assertTrue(markdown.markdown(post.content) in response.content)

        # Check the post date is in the response
        self.assertTrue(str(post.pub_date.year) in response.content)
        self.assertTrue(post.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(post.pub_date.day) in response.content)

        # Check the link is marked up properly
        self.assertTrue('<a href="http://127.0.0.1:8000/">my first blog post</a>' in response.content)

    def test_nonexistent_category_page(self):
        category_url = '/category/blah/'
        response = self.client.get(category_url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('No posts found' in response.content)

    def test_nonexistent_tag_page(self):
        tag_url = '/tag/blah/'
        response = self.client.get(tag_url)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('No posts found' in response.content)

        # class FlatPageViewTest(BaseAcceptanceTest):
        # def test_create_flat_page(self):
        # page = FlatPage()
        #         page.url = '/about/'
        #         page.title = 'About NFG'
        #         page.content = 'NUNFUXGVN'
        #         page.save()

        #         page.sites.add(Site.objects.all()[0])
        #         page.save()

        #         all_pages = FlatPage.objects.all()
        #         self.assertEquals(len(all_pages), 1)
        #         only_page = all_pages[0]
        #         self.assertEquals(only_page, page)

        #         self.assertEquals(only_page.url, '/about/')
        #         self.assertEquals(only_page.title, 'About NFG')
        #         self.assertEquals(only_page.content, 'NUNFUXGVN')

        #         page_url = only_page.get_absolute_url()

        #         response = self.client.get(page_url)
        #         self.assertEquals(response.status_code, 200)

        #         self.assertTrue('About NFG' in response.content)
        #         self.assertTrue('NUNFUXGVN' in response.content)