from django.db.models import Sum
from django.http import HttpResponse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas

from .models import IngredientAmount


def generate_shopping_list(user):
    shopping_list = IngredientAmount.objects.filter(
        recipe__carts__user=user).values(
        'ingredient__name',
        'ingredient__measurement_unit'
    ).annotate(quantity=Sum('amount')).order_by()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="shopping_list.pdf"'
    )
    pdfmetrics.registerFont(TTFont('Sarai', 'Sarai.ttf', 'UTF-8'))
    page = Canvas(filename=response)
    page.setFont('Gargi', 24)
    page.drawString(210, 800, 'Список покупок')
    page.setFont('Gargi', 16)
    height = 760
    is_page_done = False
    for idx, ingr in enumerate(shopping_list, start=1):
        is_page_done = False
        page.drawString(60, height, text=(
            f'{idx}. {ingr["ingredient__name"]} - {ingr["quantity"]} '
            f'{ingr["ingredient__measurement_unit"]}'
        ))
        height -= 30
        if height <= 40:
            page.showPage()
            is_page_done = True
    if not is_page_done:
        page.showPage()
    page.save()
    return response
