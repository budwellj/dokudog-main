from rest_framework.viewsets import ModelViewSet
from .models import Work, UserProfile, Theme, Language
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .serializers import WorkSerializer
from django.conf import settings
import requests
from .forms import UserProfileForm, WorkForm
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator



class WorkViewSet(ModelViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer

@login_required
def get_recommendation_view(request):
    if request.method == 'POST':
        user_id = request.user.id
        recommendation_url = f'http://127.0.0.1:8000/api/recommendation/{user_id}/'  # Adjust port if necessary

        # Use the shared service key for authentication
        headers = {'Service-Key': settings.SERVICE_SECRET_KEY}

        try:
            response = requests.get(recommendation_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            recommendation = data.get('recommendation')

            if recommendation:
                # Save recommendation in session for later use
                request.session['recommendation'] = recommendation
                return render(request, 'dokudog/recommendation.html', {'recommendation': recommendation})
            else:
                error = 'No recommendation found.'
        except requests.exceptions.RequestException as e:
            error = f'An error occurred: {e}'

        return render(request, 'dokudog/recommendation.html', {'error': error})
    elif request.method == 'GET' and 'use_recommendation' in request.GET:
        # Handle "Use Recommendation" button
        recommendation = request.session.get('recommendation')
        if recommendation:
            try:
                profile = UserProfile.objects.get(user=request.user)
                work = Work.objects.get(id=recommendation['id'])
                profile.current_work = work
                profile.save()
                return redirect('homepage')
            except (UserProfile.DoesNotExist, Work.DoesNotExist):
                return render(request, 'dokudog/recommendation.html', {'error': 'Unable to set current work.'})

    return render(request, 'dokudog/recommendation.html')

@login_required
def user_info_view(request):
    user = request.user
    try:
        profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        profile = None

    return render(request, 'dokudog/user_info.html', {'user': user, 'profile': profile})

@login_required
def edit_user_settings(request):
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = None

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            user_profile = form.save(commit=False)
            user_profile.user = request.user
            user_profile.save()
            form.save_m2m()  # Save ManyToMany fields
            return redirect('user-info')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'dokudog/edit_settings.html', {'form': form})

def homepage_view(request):
    user_work = request.user.userprofile.current_work if request.user.is_authenticated else None
    greeting = f"Welcome back, {request.user.username}!" if request.user.is_authenticated else "Welcome to Dokudog!"
    
    return render(request, 'dokudog/homepage.html', {
        'user_work': user_work,
        'greeting': greeting
    })

    return render(request, 'dokudog/homepage.html', {'user_work': user_work})

#These functions are for the work search and search autocomplete functions
def autocomplete(request):
    query = request.GET.get('q', '').strip()
    if query:
        books = Work.objects.filter(title__icontains=query).values('title', 'author')[:10]
        return JsonResponse(list(books), safe=False)
    return JsonResponse([], safe=False)

def search_results(request):
    query = request.GET.get('q', '').strip()
    sort_by = request.GET.get('sort_by', '')
    selected_themes = request.GET.getlist('themes')
    selected_language = request.GET.get('language', '')

    results = Work.objects.all()
    themes = Theme.objects.all()
    languages = Language.objects.all()

    if query:
        results = results.filter(title__icontains=query)

    # Filter by themes
    if selected_themes:
        results = results.filter(themes__id__in=selected_themes).distinct()

    # Filter by language
    if selected_language:
        results = results.filter(language__id=selected_language)

    # Apply sorting
    if sort_by == 'difficulty_asc':
        results = results.order_by('difficulty')
    elif sort_by == 'difficulty_desc':
        results = results.order_by('-difficulty')

    # Existing form handling code
    form = WorkForm()
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'New work added successfully!')
            return redirect('search_results')
        else:
            messages.error(request, 'There was an error adding the work.')
    
     # Pagination
    paginator = Paginator(results, 10)  # Show 10 results per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dokudog/search_results.html', {
        'query': query,
        'results': results,
        'form': form,
        'sort_by': sort_by,
        'themes': themes,
        'selected_themes': list(map(int, selected_themes)),
        'languages': languages,
        'selected_language': int(selected_language) if selected_language else '',
        'page_obj': page_obj,
    })


@login_required
def add_work_view(request):
    if request.method == 'POST':
        form = WorkForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('search_results')  # Redirect to search page after adding
    else:
        form = WorkForm()

    return render(request, 'dokudog/add_work.html', {'form': form})