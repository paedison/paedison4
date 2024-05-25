from a_common.utils import HtmxHttpRequest
from a_psat import filters


def get_filterset(request: HtmxHttpRequest):
    psat_filter = filters.PsatFilter if request.user.is_authenticated else filters.AnonymousPsatFilter
    return psat_filter(data=request.GET, request=request)


def get_page_added_path(request: HtmxHttpRequest, page: int):
    curr_path = request.get_full_path()
    if 'page=' not in curr_path:
        curr_path += '&page=1' if '?' in curr_path else '?page=1'
    next_path = curr_path.replace(f'page={page}', f'page={page + 1}')
    return {
        'curr_path': curr_path,
        'next_path': next_path,
    }


def get_elided_page_range(request, filterset=None, number=None, *, on_each_side=5, on_ends=1):
    if filterset is None:
        filterset = get_filterset(request)
    if number is None:
        number = int(request.GET.get('page', 1))
    num_pages = filterset.qs.count() // 10 + 1
    page_range = range(1, num_pages + 1)
    print(number, num_pages)
    print(filterset.qs.count())

    _ellipsis = "…"
    if num_pages <= (on_each_side + on_ends) * 2:
        yield from page_range
        return

    if number > (1 + on_each_side + on_ends) + 1:
        yield from range(1, on_ends + 1)
        yield _ellipsis
        yield from range(number - on_each_side, number + 1)
    else:
        yield from range(1, number + 1)

    if number < (num_pages - on_each_side - on_ends) - 1:
        yield from range(number + 1, number + on_each_side + 1)
        yield _ellipsis
        yield from range(num_pages - on_ends + 1, num_pages + 1)
    else:
        yield from range(number + 1, num_pages + 1)