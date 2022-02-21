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
    context = {"form": form}
    qs = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(qs)
    data = form.cleaned_data
    from_city, to_city, cities = data["from_city"], data["to_city"], data["cities"]
    traveling_time = data["traveling_time"]
    all_routes = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(all_routes):
        raise ValueError("Подходящего маршрута не существует")
    if cities:
        _cities = [city.id for city in cities]
        right_routes = [r for r in all_routes if all(city in r for city in _cities)]
        if not right_routes:
            raise ValueError("Маршрут через эти города невозможен")
    else:
        right_routes = all_routes

    routes = []
    all_trains = {}
    for q in qs:
        all_trains.setdefault((q.from_city_id, q.to_city_id), [])
        all_trains[(q.from_city_id, q.to_city_id)].append(q)
    for route in right_routes:
        tmp = {"trains": []}
        total_time = 0
        for i in range(len(route) - 1):
            qs = all_trains[(route[i], route[i + 1])]
            q = qs[0]
            total_time += q.travel_time
            tmp["trains"].append(q)
        tmp["total_time"] = total_time
        if total_time <= traveling_time:
            routes.append(tmp)
    if not routes:
        raise ValueError("Время в пути больше заданного")

    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = sorted(list(set(r["total_time"] for r in routes)))
        for time in times:
            for route in routes:
                if time == route["total_time"]:
                    sorted_routes.append(route)

    context["routes"], context["cities"] = sorted_routes, {"from_city": from_city, "to_city": to_city}

    return context
