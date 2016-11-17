from django.shortcuts import render, redirect
from lcc.models import Lcc
from lcc.lcc_parser import LccData


def index(request):
    lcc_query = request.GET.get('lcc')
    lcc_list = []
    if lcc_query:
        try:
            lcc = LccData.parse(lcc_query)
        except ValueError:
            pass
        else:
            query =  Lcc.objects.filter(
                main_class_start__gte=lcc.main_class_start,
                main_class_end__lte=lcc.main_class_end,
            )
            if lcc.sub_class_start is not None:
                query = query.filter(
                    sub_class_start__gte=lcc.sub_class_start,
                )
            if lcc.sub_class_end is not None:
                query = query.filter(
                    sub_class_end__lte=lcc.sub_class_end,
                )
            lcc_list = query.all()

    return render(request, 'lcc/index.html', {
        'lcc_list': lcc_list,
        'lcc_query': lcc_query or '',
    })


def add_lcc(request):
    assert request.method == 'POST'  # lol errors
    raw = request.POST['lcc']
    lcc = LccData.parse(raw)
    Lcc.objects.create(
        main_class_start=lcc.main_class_start,
        sub_class_start=lcc.sub_class_start,
        main_class_end=lcc.main_class_end,
        sub_class_end=lcc.sub_class_end,
        value=raw,
        regal=request.POST['regal'],
    )
    return redirect('index')

