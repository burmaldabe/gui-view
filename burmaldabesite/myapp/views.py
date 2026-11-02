from django.shortcuts import render

def index(request):
    return render(request, 'myapp/index.html')

def table_view(request):
    table_data = {
        'headers': ['ID (int)', 'Code (smallint)', 'Score (float)', 'Name (char 50)'],
        'rows': [
            ['1', '7', '1050.25', 'Burmalda_Red_Block'],
            ['2', '14', '3200.00', 'Burmalda_Black_Block'],
            ['3', '0', '0.00', 'Zero_Sector'],
            ['4', '32', '740.50', 'High_Stakes_Node'],
        ]
    }
    return render(request, 'myapp/table_view.html', {'table': table_data})

def diagram_view(request):
    """Представление Диаграммы БД в стиле SSMS 2022"""
    return render(request, 'myapp/diagram_view.html')

def roulette_view(request):
    return render(request, 'myapp/roulette.html')