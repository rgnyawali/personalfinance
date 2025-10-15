from django.db import models
from django.urls import reverse

class Question(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='quiz_images/', blank=True, null=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"Question {self.id}"

    def get_absolute_url(self):
        return reverse('quiz_question', kwargs={'question_id': self.id})

    def get_next_question(self):
        return Question.objects.filter(id__gt=self.id).order_by('id').first()

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=200)
    is_correct = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.question} - Option {self.id}"