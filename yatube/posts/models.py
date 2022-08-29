from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Group(models.Model):
    title = models.CharField('название', max_length=200)
    slug = models.SlugField('адрес', unique=True)
    description = models.TextField('описание')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'сообщество'
        verbose_name_plural = 'сообщества'


class Post(models.Model):
    text = models.TextField('текст')
    pub_date = models.DateTimeField('дата', auto_now_add=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='автор'
    )
    group = models.ForeignKey(
        Group,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='posts',
        verbose_name='сообщество'
    )

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        ordering = ['-pub_date']
