from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from typing import Dict, Any
import uuid

from .models import Question, Answer


class QuestionModelTest(TestCase):
    """Тесты модели Question"""

    def test_create_question(self) -> None:
        """Тест создания вопроса"""
        question: Question = Question.objects.create(
            text="Это тестовый вопрос?"
        )
        self.assertEqual(question.text, "Это тестовый вопрос?")
        self.assertEqual(question.answers_count, 0)


class QuestionAPITest(APITestCase):
    """Тесты API для вопросов"""

    def setUp(self) -> None:
        """Подготовка тестовых данных"""
        self.question: Question = Question.objects.create(
            text="Тестовый вопрос для API?"
        )

    def test_get_questions_list(self) -> None:
        """Тест получения списка вопросов"""
        url: str = reverse('qa_api:question-list-create')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_question(self) -> None:
        """Тест создания нового вопроса"""
        url: str = reverse('qa_api:question-list-create')
        data: Dict[str, str] = {
            'text': 'Новый тестовый вопрос?'
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.count(), 2)

    def test_create_answer(self) -> None:
        """Тест создания ответа"""
        url: str = reverse('qa_api:create-answer', kwargs={'question_id': self.question.id})
        data: Dict[str, str] = {
            'text': 'Тестовый ответ на вопрос',
            'user_id': str(uuid.uuid4())
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Answer.objects.count(), 1)

    def test_delete_question_cascades(self) -> None:
        """Тест каскадного удаления ответов при удалении вопроса"""
        # Создаем ответ
        Answer.objects.create(
            question=self.question,
            user_id=uuid.uuid4(),
            text='Тестовый ответ'
        )

        # Удаляем вопрос
        url: str = reverse('qa_api:question-detail', kwargs={'pk': self.question.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)
        self.assertEqual(Answer.objects.count(), 0)
