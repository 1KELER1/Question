from rest_framework import serializers
from typing import Any
import uuid
import re


def validate_text_not_empty(value: str) -> str:
    """Валидатор для проверки, что текст не пустой и не состоит только из пробелов"""
    if not value or not value.strip():
        raise serializers.ValidationError("Текст не может быть пустым")
    return value.strip()


def validate_uuid_format(value: str) -> str:
    """Валидатор для проверки корректности UUID"""
    try:
        uuid.UUID(str(value))
        return value
    except ValueError:
        raise serializers.ValidationError("Некорректный формат UUID")


def validate_question_text(value: str) -> str:
    """Специальный валидатор для текста вопроса"""
    value = validate_text_not_empty(value)

    if len(value) < 10:
        raise serializers.ValidationError("Текст вопроса должен содержать минимум 10 символов")

    if len(value) > 1000:
        raise serializers.ValidationError("Текст вопроса не должен превышать 1000 символов")

    # Проверка на наличие вопросительного знака
    if not value.endswith('?'):
        raise serializers.ValidationError("Вопрос должен заканчиваться знаком '?'")

    return value


def validate_answer_text(value: str) -> str:
    """Специальный валидатор для текста ответа"""
    value = validate_text_not_empty(value)

    if len(value) < 5:
        raise serializers.ValidationError("Текст ответа должен содержать минимум 5 символов")

    if len(value) > 2000:
        raise serializers.ValidationError("Текст ответа не должен превышать 2000 символов")

    return value
