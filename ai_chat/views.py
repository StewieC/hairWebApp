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
            return JsonResponse({'error': 'Please enter a hair-related question.'}, status=400)

        # HAIR-ONLY SYSTEM PROMPT (customizes ChatGPT to restrict topics)
        system_prompt = """
        You are HairGPT, a specialized hair care expert. You ONLY respond to questions about hair, scalp, routines, products, styling, curl patterns, breakage, and hair health.
        - Be friendly, professional, concise (150-250 words).
        - Structure: 1. Summary, 2. Step-by-step routine, 3. Product suggestions, 4. Tips to avoid mistakes.
        - If the question is NOT about hair (e.g., code, weather, math), respond ONLY: "I'm HairGPT—your hair care specialist! Ask me about routines, products, or styling tips."
        - Never answer off-topic questions, generate code, or discuss anything else.
        """

        try:
            response = requests.post(
                'https://api.openai.com/v1/chat/completions',
                headers={
                    'Authorization': f'Bearer {settings.OPENAI_API_KEY}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': 'gpt-4o-mini',
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
                error_msg = response.json().get('error', {}).get('message', 'Unknown error')
                return JsonResponse({'error': f'API Error: {error_msg}. Check your key or credits.'}, status=500)

        except requests.exceptions.Timeout:
            return JsonResponse({'error': 'Request timed out—try again.'}, status=500)
        except Exception as e:
            return JsonResponse({'error': f'Connection error: {str(e)}. Check internet/key.'}, status=500)

    return render(request, 'ai_chat/ai_chat.html')