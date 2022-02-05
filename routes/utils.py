from trains.models import Train


def dfs_paths(graph, start, goal):
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(qs):
    graph = {}
    for q in qs:
        graph.setdefault(q.from_city_id, set())
        graph[q.from_city_id].add(q.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    qs = Train.objects.all()
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    cities = data['cities']
    traveling_time = data['traveling_time']
    all_routes = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(all_routes):
        raise ValueError('Подходящего маршрута не существует')
    if cities:
        _cities = [city.id for city in cities]
        # right_routes = []
        # for r in all_routes:
        #     if all(city in r for city in _cities):
        #         right_routes.append(r)
        right_routes = [r for r in all_routes if all(city in r for city in _cities)]
        if not right_routes:
            raise ValueError('Маршрут через эти города невозможен')
    return context
