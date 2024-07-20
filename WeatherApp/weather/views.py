from django.shortcuts import render

def index(request) -> render:
    return render(
        request=request,
        template_name='weather/index.html'
    )
