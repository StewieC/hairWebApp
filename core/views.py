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
import json

@csrf_exempt  
def ai_hair_chat(request):
    if request.method == 'POST':
        user_query = request.POST.get('query', '').strip()
        if not user_query:
            return JsonResponse({'error': 'Please enter a question.'}, status=400)

        # Custom system prompt to restrict to hair care only
        system_prompt = """
        You are a hair care expert named 'HairGrok'. You ONLY answer questions about hair care, routines, products, styling, scalp health, and related topics.
        - Be friendly, professional, and concise (200 words max).
        - Structure responses: 1. Summary, 2. Key advice, 3. Product suggestions, 4. Warnings.
        - If the question is NOT about hair (e.g., coding, weather), politely say: "I'm HairGrok, your hair care specialist! Ask me about routines, products, or styling."
        - Never answer off-topic questions or generate code/math.
        """

        try:
            response = requests.post(
                'https://api.x.ai/v1/chat/completions',  # Grok endpoint
                headers={
                    'Authorization': f'Bearer {settings.GROK_API_KEY}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': 'grok-beta',  # Fast, free-tier model; use 'grok-4' for advanced
                    'messages': [
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': user_query}
                    ],
                    'max_tokens': 400,
                    'temperature': 0.7,  # Balanced creativity
                },
                timeout=10
            )

            if response.status_code == 200:
                ai_response = response.json()['choices'][0]['message']['content']
                return JsonResponse({'response': ai_response})
            else:
                return JsonResponse({'error': 'API error—try again.'}, status=500)

        except Exception as e:
            return JsonResponse({'error': f'Connection issue: {str(e)}'}, status=500)

    return render(request, 'core/ai_chat.html')  # Frontend form page