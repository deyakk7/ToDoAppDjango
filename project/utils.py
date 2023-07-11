from django.core.paginator import Paginator

from datetime import datetime, timezone

def search_query(request):
    empty = False
    if request.user.is_authenticated:
        search_query = ""
        if request.GET.get('search_query'):
            search_query = request.GET.get('search_query')
        tasks = request.user.task_set.filter(
            title__icontains=search_query).order_by('complete', 'due')
        if not tasks:
            empty = True
        else:
            for task in tasks:
                timeleft = task.due - datetime.now(timezone.utc)
                timeleft = max(0, int(timeleft.total_seconds()))
                task.timeleft = timeleft
        return tasks, request.GET.get('search_query'), empty
    

def paginateTask(request, tasks, pages):
    paginator = Paginator(tasks, pages)
    tasks = paginator.get_page(request.GET.get('page'))
    page = tasks.number
    left_index = page - 2
    if left_index < 1:
        left_index = 1
    right_index = page + 3
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1
    custom_range = range(left_index, right_index)

    return custom_range, tasks