from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from .models import Question, Option
from .forms import QuestionForm, OptionForm, OptionFormSet
from django.contrib import messages
from django.forms import formset_factory
from django.views.generic import CreateView

# Create your views here.

def homeview(request):
    # Clear all quiz-related session data when returning to home
    for key in list(request.session.keys()):
        if key.startswith('answer_'):
            del request.session[key]
    request.session.modified = True
    return render(request, 'driving/home.html', {})

class QuizView(View):
    def get(self, request, question_id=None):
        if question_id:
            question = get_object_or_404(Question, id=question_id)
        else:
            question = Question.objects.order_by('id').first()
            if not question:
                return render(request, 'driving/no_questions.html')
        
        # Get all questions for navigation
        all_questions = list(Question.objects.all().order_by('id'))
        
        # Get the previous answer if any
        previous_answer = request.session.get(f'answer_{question.id}')
        
        # Prepare question status for navigation
        question_status = {}
        for q in all_questions:
            answer_id = request.session.get(f'answer_{q.id}')
            if answer_id:
                try:
                    option = Option.objects.get(id=answer_id, question=q)
                    question_status[q.id] = 'correct' if option.is_correct else 'incorrect'
                except Option.DoesNotExist:
                    question_status[q.id] = 'unanswered'
            else:
                question_status[q.id] = 'unanswered'
        
        return render(request, 'driving/quiz.html', {
            'question': question,
            'options': question.options.all(),
            'previous_answer': previous_answer,
            'show_feedback': previous_answer is not None,
            'is_correct': previous_answer and Option.objects.get(id=previous_answer).is_correct if previous_answer else False,
            'correct_option': question.options.filter(is_correct=True).first(),
            'all_questions': all_questions,
            'question_status': question_status
        })

    def post(self, request, question_id):
        question = get_object_or_404(Question, id=question_id)
        selected_option_id = request.POST.get('option')
        
        if selected_option_id:
            try:
                selected_option = Option.objects.get(id=selected_option_id, question=question)
                # Store the answer in the session
                request.session[f'answer_{question_id}'] = selected_option_id
                request.session.modified = True
            except Option.DoesNotExist:
                pass
        
        # Redirect to the same question to show the answer
        return redirect('driving:quiz_question', question_id=question_id)

class QuizCompleteView(View):
    def get(self, request):
        # Get all questions
        questions = Question.objects.all()
        total_questions = questions.count()
        correct_answers = 0
        
        # Check each question's answer
        for question in questions:
            answer_id = request.session.get(f'answer_{question.id}')
            if answer_id:
                try:
                    option = Option.objects.get(id=answer_id, question=question)
                    if option.is_correct:
                        correct_answers += 1
                except Option.DoesNotExist:
                    pass
        
        # Calculate score percentage
        score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
        
        # Clear the session after showing results
        for key in list(request.session.keys()):
            if key.startswith('answer_'):
                del request.session[key]
        request.session.modified = True
        
        return render(request, 'driving/quiz_complete.html', {
            'total_questions': total_questions,
            'correct_answers': correct_answers,
            'score_percentage': round(score_percentage, 2),
        })
        
def add_question(request):
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, request.FILES)
        option_formset = OptionFormSet(request.POST, instance=Question())
        
        if question_form.is_valid() and option_formset.is_valid():
            question = question_form.save()
            options = option_formset.save(commit=False)
            
            # Check if at least one option is marked as correct
            if not any(option.is_correct for option in options):
                messages.error(request, 'At least one option must be marked as correct.')
                question.delete()  # Clean up the question if validation fails
                return render(request, 'driving/add_question.html', {
                    'question_form': question_form,
                    'option_formset': option_formset,
                })
            
            # Save all options
            for option in options:
                option.question = question
                option.save()
            
            messages.success(request, 'Question and options added successfully!')
            return redirect('driving:add_question')
    else:
        question_form = QuestionForm()
        option_formset = OptionFormSet(queryset=Option.objects.none())
    
    return render(request, 'driving/add_question.html', {
        'question_form': question_form,
        'option_formset': option_formset,
    })