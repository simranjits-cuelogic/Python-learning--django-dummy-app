import datetime
from django.test import TestCase

from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from .models import Question

class QuestionMethodTests(TestCase):
    def test_was_pusblished_recently_with_future_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.latest_posted(), False)

    def test_was_pusblished_recently_with_old_question(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.latest_posted(), False)

    def test_was_pusblished_recently_with_recent_question(self):
        """
        was_published_recently() should return True for questions whose
        pub_date is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=1)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.latest_posted(), True)

def create_question(question, days):
    """
    Creates a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days)
    return Question.objects.create(question = question, pub_date = time)

# NOTE: SORT OF INTEGRATION TESING IN RAILS
class QuestionViewTest(TestCase):
    def test_index_view_with_no_questions(self):
        """
        If not questions exist, an qppropriate messge should be displayed.
        """

        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(response.context['latest_questions'], [])

    def test_index_view_with_a_past_question(self):
        """
        Questions with a pub_date in the past should be display on the
        index page
        """
        create_question(question = 'Past question', days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: Past question>']
        )

    def test_index_view_with_a_future_question(self):
        """
        Questions with a pub_date in the future should not be display on the
        index page
        """
        create_question(question = 'Past question', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, 'No polls are available.')
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            []
        )

    def test_index_view_with_future_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        should be displayed.
        """
        create_question(question = 'past question', days= -30)
        create_question(question = 'future question', days= 30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: past question>']
        )

    def test_index_view_with_two_past_question(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question = 'past question1', days= -30)
        create_question(question = 'past question2', days= -30)
        response = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(
            response.context['latest_questions'],
            ['<Question: past question2>', '<Question: past question1>']
        )

# NOTE: SORT OF VIEW TESING IN RAILS
class QuestionIndexDetailsTests(TestCase):
    def test_detail_view_with_a_future_question(self):
        """
        The detail view of a question with a pub_date in the future should
        return a 404 not found.
        """
        future_question = create_question(question='future question', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_details_view_with_a_past_question(self):
        past_question = create_question(question = 'Past question', days= -5)
        url = reverse('polls:detail', args=(past_question.id, ))
        response = self.client.get(url)
        self.assertContains(response, past_question.question)
