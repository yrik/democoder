from django.core.urlresolvers import reverse
from django.utils import formats

from django_webtest import WebTest
from webtest import Upload
from model_mommy import mommy

from core.models import (
    Article,
    User,
)


class AuthTestMixin(object):

    def init_users(self):
        # Create User object
        self.user = User.objects.create(email='user@mail.com')
        self.user.set_password('test')
        self.user.save()

    def login(self, login, password):
        resp = self.app.get(reverse('auth'))
        form = resp.forms[0]
        form['login'] = login
        form['password'] = password
        form.submit('login_form')

    def logout(self):
        resp = self.app.get('/accounts/logout/')
        resp.form.submit()


class ArticleTest(WebTest, AuthTestMixin):

    def test_create(self):
        """Create Article object using view
        Check database for created object
        """
        self.init_users()

        article = mommy.make('core.Article')

        url = reverse('article-create')

        # Access forbidden for AnonymousUser
        resp = self.app.get(url, status=302)

        self.login(self.user.email, 'test')

        resp = self.app.get(url)

        form = resp.form
        form['description'] = article.description
        form['title'] = article.title
        form.submit()

        article_created = Article.objects.latest('id')

        self.assertEqual(
            article_created.description,
            article.description
        )
        self.assertEqual(
            article_created.title,
            article.title
        )

        self.logout()

    def test_list(self):
        """Create list of Article in database,
        open list view and
        check that selected fields are visible
        for each object
        """
        self.init_users()

        article_list = []
        for i in range(10):
            article = mommy.make('core.Article')
            article_list.append(article)

        url = reverse('article-list')

        article_list = []
        for i in range(10):
            article = mommy.make('core.Article')
            article_list.append(article)

        url = reverse('article-list')

        url = reverse('article-list')
        resp = self.app.get(url)

        for article in article_list:
            self.assertContains(resp, article.description)
            self.assertContains(resp, article.title)

        article_list = []
        for i in range(10):
            article = mommy.make('core.Article')
            article_list.append(article)

        url = reverse('article-list')

        self.login(self.user.email, 'test')

        url = reverse('article-list')
        resp = self.app.get(url)

        for article in article_list:
            self.assertContains(resp, article.description)
            self.assertContains(resp, article.title)

        self.logout()
