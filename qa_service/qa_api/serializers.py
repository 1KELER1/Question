from rest_framework import serializers
from typing import Dict, Any, OrderedDict
from .models import Question, Answer
from .validators import validate_question_text, validate_answer_text, validate_uuid_format


class AnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для ответов"""

    text = serializers.CharField(validators=[validate_answer_text])
    user_id = serializers.CharField(validators=[validate_uuid_format])

    class Meta:
        model = Answer
        fields: tuple[str, ...] = ('id', 'question', 'user_id', 'text', 'created_at')
        read_only_fields: tuple[str, ...] = ('id', 'created_at')


class QuestionListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка вопросов"""

    answers_count = serializers.ReadOnlyField()
    text = serializers.CharField(validators=[validate_question_text])

    class Meta:
        model = Question
        fields: tuple[str, ...] = ('id', 'text', 'created_at', 'answers_count')
        read_only_fields: tuple[str, ...] = ('id', 'created_at', 'answers_count')


class QuestionDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра вопроса с ответами"""

    answers = AnswerSerializer(many=True, read_only=True)
    text = serializers.CharField(validators=[validate_question_text])

    class Meta:
        model = Question
        fields: tuple[str, ...] = ('id', 'text', 'created_at', 'answers')
        read_only_fields: tuple[str, ...] = ('id', 'created_at', 'answers')


class CreateAnswerSerializer(serializers.ModelSerializer):
    """Сериализатор для создания ответа"""

    text = serializers.CharField(validators=[validate_answer_text])
    user_id = serializers.CharField(validators=[validate_uuid_format])

    class Meta:
        model = Answer
        fields: tuple[str, ...] = ('user_id', 'text')

    def create(self, validated_data: Dict[str, Any]) -> Answer:
        """Создание ответа с привязкой к вопросу"""
        question_id: int = self.context['question_id']
        return Answer.objects.create(question_id=question_id, **validated_data)
