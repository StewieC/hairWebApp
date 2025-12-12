# core/views.py
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
# from .models import QuizResponse

class HomeView(TemplateView):
    template_name = 'core/home.html'

def quiz_submit(request):
    if request.method == 'POST':
        hair_type = request.POST.get('hair_type')
        scalp_type = request.POST.get('scalp_type')
        concerns = request.POST.getlist('concerns')  # checkbox
        porosity = request.POST.get('porosity', '')

        # Save to database
        quiz = QuizResponse.objects.create(
            hair_type=hair_type,
            scalp_type=scalp_type,
            concerns=concerns,
            porosity=porosity
        )

        # Save in session too (for immediate display)
        request.session['quiz_result'] = {
            'hair_type': hair_type,
            'scalp_type': scalp_type,
            'concerns': concerns,
            'porosity': porosity,
        }

        return redirect('quiz_result')

    return redirect('home')

def quiz_result(request):
    result = request.session.get('quiz_result')
    if not result:
        return redirect('home')
    return render(request, 'core/quiz_result.html', {'result': result})

import requests
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def ai_hair_chat(request):
    if request.method == 'POST':
        user_query = request.POST.get('query', '').strip()
        
        if not user_query:
            return JsonResponse({'error': 'Please ask a question about hair.'})

        # Safety prompt — forces Grok to ONLY answer hair questions
        system_prompt = """
        You are HairGrok, a professional hair care expert.
        You ONLY answer questions about hair, scalp, routines, products, styling, and hair health.
        If the user asks anything unrelated (code, math, politics, etc.), reply:
        "I'm HairGrok — I only help with hair care! Ask me about curls, dryness, products, or routines."
        Be friendly, concise, and helpful. Use simple language.
        """

        try:
            response = requests.post(
                'https://api.groq.com/openai/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {settings.GROQ_API_KEY}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': 'llama3-8b-8192',  # Super fast & free
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_query}
                    ],
                    'max_tokens': 500,
                    'temperature': 0.7,
                },
                timeout=15
            )

            if response.status_code == 200:
                ai_reply = response.json()['choices'][0]['message']['content']
                return JsonResponse({'response': ai_reply})
            else:
                return JsonResponse({'error': f'API Error {response.status_code}. Check your key.'})

        except Exception as e:
            return JsonResponse({'error': 'Connection failed. Try again.'})

    return render(request, 'core/ai_chat.html')