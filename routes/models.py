from django.db import models


class Route(models.Model):
    name = models.CharField(max_length=50,
                            unique=True,
                            verbose_name='Название маршрута')
    travel_times = models.PositiveSmallIntegerField(verbose_name='Общее время в пути')
    from_city = models.ForeignKey('cities.City',
                                  on_delete=models.CASCADE,
                                  # null=True, blank=True,
                                  related_name='route_from_city_set',
                                  verbose_name='Из какого города')
    to_city = models.ForeignKey('cities.City',
                                on_delete=models.CASCADE,
                                # null=True, blank=True,
                                related_name='route_to_city_set',
                                verbose_name='В какой город')

    def __str__(self):
        return f'Поезд №{self.name} из города {self.from_city} в {self.to_city}'

    class Meta:
        verbose_name = 'Поезд'
        verbose_name_plural = 'поезда'
        ordering = ['travel_time']