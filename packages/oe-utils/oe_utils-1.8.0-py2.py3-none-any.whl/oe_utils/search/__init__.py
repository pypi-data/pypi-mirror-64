# -*- coding: utf-8 -*-
from math import ceil

from deprecated import deprecated
from pyramid.httpexceptions import HTTPBadRequest
from webob.multidict import MultiDict


ES_FIELDS = ('_score', '_id', '_type', '_index', '_source')


def validate_params(params, valid_keys, fail_on_invalid_key=True):
    p = MultiDict()
    for k, v in params.items():
        if k in valid_keys:
            p.add(k, v)
        elif fail_on_invalid_key:
            raise HTTPBadRequest("invalid search parameter")
    return p


@deprecated(version="1.5.0", reason="You should use validate_params")
def get_valid_params(params, valid_keys):
    return validate_params(params, valid_keys, fail_on_invalid_key=False)


def parse_sort_string(
    sort, default=None, fulltext=None, tiebreaker=None, **translations
):
    """
    Parse a sort string for use with elasticsearch.

    If no custom default and no sort string: "_score" becomes the default.

    :param sort: the sort string
    :type sort: str, optional
    :param default: optional custom default sort parameter
    :type default: list, optional
    :param fulltext:  maps fulltext field to "_score"
    :type: fulltext: str, optional
    :param tiebreaker: optional tiebreaker to break equal sort scores
    :type tiebreaker: list, optional
    :param translations: **kwarg that translates sort field string to correct ES field
                          e.g "name" = "name.raw"
    :return: ES ready sort list
    """
    added_field_names = set()
    sortlist = []
    if sort:
        sort_values = sort.rsplit(",")
        for sort_value in sort_values:
            sort_value = sort_value.strip()
            order = "desc" if sort_value[0:1] == "-" else "asc"
            field = sort_value[1:] if sort_value[0:1] in ["-", "+"] else sort_value
            if field == fulltext:
                added_field_names.add("_score")
                sortlist.append("_score")
                continue

            if translations:
                field = translations.get(field, field)

            added_field_names.add(field)

            field_sort = {
                field: {
                    "order": order
                }
            }
            if field not in ES_FIELDS:
                field_sort[field]['unmapped_type'] = 'string'
                field_sort[field]['missing'] = '_last'
            sortlist.append(field_sort)
    elif default:
        sortlist.extend(default)
    if "_score" not in added_field_names:
        sortlist.append("_score")
    if tiebreaker:
        sortlist.extend(tiebreaker)

    return sortlist


def parse_filter_params(query_params, filterable):
    """
    Parse query_params to a filter params dict.

    Merge multiple values for one key to a list.
    Filter out keys that aren't filterable.

    :param query_params: query params
    :param filterable: list of filterable keys
    :return: dict of filter values
    """
    if query_params is not None:
        filter_params = {}
        for fq in query_params.mixed():
            if fq in filterable:
                filter_params[fq] = query_params.mixed().get(fq)
        return filter_params
    else:
        return {}


class SearchResultPager(object):
    """
    Helper class for paging search results.

    based on http://atlas-core.readthedocs.org/
    en/latest/_modules/flask_sqlalchemy.html Pagination
    """

    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def prev(self):
        return self.page - 1 if self.has_prev else None

    @property
    def has_next(self):
        return self.page < self.pages

    @property
    def next(self):
        return self.page + 1 if self.has_next else None

    def iter_pages(self, left_edge=2, left_current=2, right_current=5, right_edge=2):
        """Iterate over the page numbers in the pagination.

        The four parameters control the thresholds how many numbers should
        be produced from the sides.  Skipped page numbers are represented
        as `None`.
        """
        last = 0
        try:
            xrange  # noqa
        except NameError:
            xrange = range
        for num in xrange(1, self.pages + 1):
            if (
                num <= left_edge
                or (self.page - left_current - 1 < num < self.page + right_current)
                or num > self.pages - right_edge
            ):
                if last + 1 != num:
                    yield None
                yield num
                last = num
