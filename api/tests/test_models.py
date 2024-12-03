# main_app/tests/test_models.py

from django.contrib.auth import get_user_model
from django.test import TestCase
from api.models import Theme, Language, Type, Work, UserProfile

class UserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpass123'))

class ThemeModelTests(TestCase):
    def test_create_theme(self):
        theme = Theme.objects.create(name='Science Fiction')
        self.assertEqual(theme.name, 'Science Fiction')
        self.assertEqual(str(theme), 'Science Fiction')

class LanguageModelTests(TestCase):
    def test_create_language(self):
        language = Language.objects.create(name='Japanese')
        self.assertEqual(language.name, 'Japanese')
        self.assertEqual(str(language), 'Japanese')

class TypeModelTests(TestCase):
    def test_create_type(self):
        type_obj = Type.objects.create(name='Book')
        self.assertEqual(type_obj.name, 'Book')
        self.assertEqual(str(type_obj), 'Book')

class WorkModelTests(TestCase):
    def test_create_work(self):
        # Create related objects
        theme1 = Theme.objects.create(name='Science Fiction')
        theme2 = Theme.objects.create(name='Adventure')
        type_obj = Type.objects.create(name='Book')

        # Create the Work object
        work = Work.objects.create(
            title='Dune',
            author='Frank Herbert',
            difficulty=7,
            type=type_obj
        )
        # Add themes to the work
        work.themes.set([theme1, theme2])

        # Assertions
        self.assertEqual(work.title, 'Dune')
        self.assertEqual(work.author, 'Frank Herbert')
        self.assertEqual(work.difficulty, 7)
        self.assertEqual(work.type, type_obj)
        self.assertEqual(str(work), 'Dune')
        self.assertEqual(work.themes.count(), 2)
        self.assertIn(theme1, work.themes.all())
        self.assertIn(theme2, work.themes.all())

class UserProfileModelTests(TestCase):
    def test_create_user_profile(self):
        # Create a user
        User = get_user_model()
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

        # Create languages
        english = Language.objects.create(name='English')
        japanese = Language.objects.create(name='Japanese')

        # Create themes
        theme1 = Theme.objects.create(name='Science Fiction')
        theme2 = Theme.objects.create(name='Adventure')

        # Create the UserProfile
        profile = UserProfile.objects.create(
            user=user,
            difficulty_score=0.7,
            native_language=english,
            target_language=japanese
        )
        profile.themes.set([theme1, theme2])

        # Assertions
        self.assertEqual(profile.native_language, english)
        self.assertEqual(profile.target_language, japanese)
        self.assertEqual(profile.native_language.name, 'English')
        self.assertEqual(profile.target_language.name, 'Japanese')