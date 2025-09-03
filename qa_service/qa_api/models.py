from django.db import models
from django.core.validators import MinLengthValidator
from typing import TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from django.db.models.query import QuerySet


class Question(models.Model):
    """Модель вопроса"""

    text: str = models.TextField(
        validators=[MinLengthValidator(10)],
        help_text="Текст вопроса (минимум 10 символов)"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name: str = "Вопрос"
        verbose_name_plural: str = "Вопросы"
        ordering: list[str] = ['-created_at']

    def __str__(self) -> str:
        return f"Вопрос #{self.pk}: {self.text[:50]}..."

    @property
    def answers_count(self) -> int:
        """Количество ответов на вопрос"""
        return self.answers.count()


class Answer(models.Model):
    """Модель ответа на вопрос"""

    question: Question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Вопрос"
    )
    user_id: str = models.UUIDField(
        help_text="UUID пользователя, оставившего ответ"
    )
    text: str = models.TextField(
        validators=[MinLengthValidator(5)],
        help_text="Текст ответа (минимум 5 символов)"
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name: str = "Ответ"
        verbose_name_plural: str = "Ответы"
        ordering: list[str] = ['created_at']

    def __str__(self) -> str:
        return f"Ответ #{self.pk} на вопрос #{self.question.pk}"
