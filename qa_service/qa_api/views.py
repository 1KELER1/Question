from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from django.db import transaction
from typing import Optional
import logging

from .models import Question, Answer
from .serializers import (
    QuestionListSerializer,
    QuestionDetailSerializer,
    AnswerSerializer,
    CreateAnswerSerializer
)

logger = logging.getLogger(__name__)


class QuestionListCreateView(generics.ListCreateAPIView):
    """
    API endpoint для работы с вопросами.

    GET: Получить список всех вопросов
    POST: Создать новый вопрос
    """

    queryset = Question.objects.all()
    serializer_class = QuestionListSerializer

    def perform_create(self, serializer) -> None:
        """Логирование создания нового вопроса"""
        question: Question = serializer.save()
        logger.info(f"Создан новый вопрос с ID {question.id}")


class QuestionDetailView(generics.RetrieveDestroyAPIView):
    """
    API endpoint для детального просмотра и удаления вопроса.

    GET: Получить вопрос со всеми ответами
    DELETE: Удалить вопрос (каскадно с ответами)
    """

    queryset = Question.objects.prefetch_related('answers')
    serializer_class = QuestionDetailSerializer

    def destroy(self, request, *args, **kwargs) -> Response:
        """Удаление вопроса с каскадным удалением ответов"""
        question: Question = self.get_object()
        answers_count: int = question.answers_count

        with transaction.atomic():
            question.delete()
            logger.info(f"Удален вопрос с ID {kwargs['pk']} и {answers_count} ответов")

        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def create_answer(request, question_id: int) -> Response:
    """
    API endpoint для создания ответов на вопрос.

    GET: Показать форму для создания ответа
    POST: Создать новый ответ к вопросу
    """

    question: Question = get_object_or_404(Question, id=question_id)

    if request.method == 'GET':
        # Показать информацию о вопросе и форму для ответа
        serializer = CreateAnswerSerializer()
        return Response({
            'question': QuestionDetailSerializer(question).data,
            'answer_form': serializer.data
        })

    elif request.method == 'POST':
        serializer = CreateAnswerSerializer(
            data=request.data,
            context={'question_id': question_id}
        )

        if serializer.is_valid():
            answer: Answer = serializer.save()
            response_serializer = AnswerSerializer(answer)

            logger.info(f"Создан ответ с ID {answer.id} для вопроса {question_id}")

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnswerDetailView(generics.RetrieveDestroyAPIView):
    """
    API endpoint для просмотра и удаления ответа.

    GET: Получить конкретный ответ
    DELETE: Удалить ответ
    """

    queryset = Answer.objects.select_related('question')
    serializer_class = AnswerSerializer

    def destroy(self, request, *args, **kwargs) -> Response:
        """Удаление ответа"""
        answer: Answer = self.get_object()
        answer_id: int = answer.id
        question_id: int = answer.question.id

        answer.delete()
        logger.info(f"Удален ответ с ID {answer_id} к вопросу {question_id}")

        return Response(status=status.HTTP_204_NO_CONTENT)
