__author__ = 'nick'

from remodel.models import Model
from remodel.helpers import create_tables, create_indexes
from remodel.object_handler import ObjectHandler
import remodel.connection


class Country(Model):
    has_many = ('City',)


class City(Model):
    belongs_to = ('Country',)

create_tables()
create_indexes()

romania = Country.create(name='Romania', continent='Europe')

timisoara = City.create(name='Timisoara', country=romania)
bucharest = City.create(name='Bucharest', country=romania)
romania["cities"].add(timisoara, bucharest)
romania = Country.get(name='Romania')
# romania["cities"].create(name="Iasi")
for i in romania["cities"].filter():
    if i["name"] == 'Iasi' or i["name"] == 'Sibiu':
        i.delete()
    print(i.fields.as_dict())
print(len(City.all()))
for i in City.all():
    i.delete()

print(len(City.all()))