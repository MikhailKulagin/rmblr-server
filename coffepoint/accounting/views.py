from collections import defaultdict
from django.views.generic import TemplateView, DetailView
from django.db.models.functions import Replace
from django.db.models import Value
from django.shortcuts import get_object_or_404

from .models import User, CupMaterials


class CupData:
    def __init__(self):
        self.owner_name = None

    def get_shelves(self) -> dict:
        """
        Группируем чашки по полкам, определяем состав чашек.
        Чашки заведенные в БД без связи с материалами не будут отображаться, т.к. от идем от CupMaterials (надо ли?)
        :return: dict
        """
        query = CupMaterials.objects.select_related('cup', 'material')
        if self.owner_name:
            query = query.filter(cup__owner__username=self.owner_name)
        query = query.all()
        selves = defaultdict(dict)
        cup_materials = defaultdict(list)
        for raw in query:
            cup_id = raw.cup.id
            shelf_name = raw.cup.shelf.number
            cup_materials[cup_id].append(raw.material.title)
            cup_data = {'cup_id': raw.cup.id,
                        'owner_name': raw.cup.owner.username if raw.cup.owner else None,
                        'shelf_name': raw.cup.shelf.number,
                        'cup_volume': raw.cup,
                        }
            selves[shelf_name][cup_id] = cup_data
        for shelf_data in selves.values():
            for cup_id, cup_data in shelf_data.items():
                cup_data['owner_name'] = cup_data['owner_name'].replace(' ', '') \
                    if cup_data['owner_name'] else None
                cup_data['materials'] = sorted(cup_materials.get(cup_id, []))
        return dict(selves)


class AccountungView(TemplateView, CupData):
    template_name = "index.html"

    def __init__(self):
        CupData.__init__(self)
        self.context = None

    def get_context_data(self):
        shelves = self.get_shelves()
        self.context = {"shelves": shelves, 'owner_name': None}
        return self.context


class UserView(DetailView, CupData):
    template_name = "user.html"
    model = User

    def __init__(self):
        CupData.__init__(self)
        self.context = None

    def get_object(self, **kwargs):
        # Все replace из-за юзера "mr. Zolp"
        user = get_object_or_404(User.objects.annotate(owner_name=Replace('username',
                                                                          Value(' '),
                                                                          Value(''))
                                                       ),
                                 owner_name=self.kwargs['owner_name'])
        self.owner_name = user.username
        shelves = self.get_shelves()
        self.context = {"shelves": shelves, 'owner_name': user.username}

    def get_context_data(self, **kwargs):
        return self.context
