from django.core import mail
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from django.conf import settings

from model_mommy import mommy

from simplemooc.courses.models import Course

class CourseManagerTestCase(TestCase):

    def setUp(self):
        self.courses_django = mommy.make('courses.Course', name='Python na Web com Django', _quantity=10)
        self.courses_dev = mommy.make('courses.Course', name='Python para Devs', _quantity=10)
        #self.course1 = mommy.make('courses.Course')
        self.client = Client()

    def tearDown(self):
        Course.objects.all().delete()

    def test_search_course(self):
        search = Course.objects.search('django')
        self.assertEqual(len(search), 10)
        search = Course.objects.search('dev')
        self.assertEqual(len(search), 10)