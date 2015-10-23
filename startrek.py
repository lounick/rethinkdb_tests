__author__ = 'nick'
import remodel.utils
import remodel.connection
from remodel.models import Model
import rethinkdb as r

conn = r.connect(db='fleet').repl()

print(r.db_list().run())
if not "fleet" in r.db_list().run():
    r.db_create("fleet").run()
    conn = r.connect(db='fleet').repl()

print(r.db_list().run())
remodel.connection.pool.configure(db="fleet")
conn = remodel.connection.get_conn()

class Starship(Model):
    has_many = ("Crewmember",)

class Crewmember(Model):
    belongs_to = ("Starship",)

remodel.utils.create_tables()
remodel.utils.create_indexes()

voyager = Starship.create(name="Voyager", category="Intrepid", registry="NCC-74656")

voyager["crewmembers"].add(
    Crewmember(name="Janeway", rank="Captain", species="Human"),
    Crewmember(name="Neelix", rank="Morale Officer", species="Talaxian"),
    Crewmember(name="Tuvok", rank="Lt Commander", species="Vulcan"))

enterprise = Starship.create(name="Enterprise", category="Galaxy", registry="NCC-1701-D")
enterprise["crewmembers"].add(
    Crewmember(name="Picard", rank="Captain", species="Human"),
    Crewmember(name="Data", rank="Lt Commander", species="Android"),
    Crewmember(name="Troi", rank="Counselor", species="Betazed"))

defiant = Starship.create(name="Defiant", category="Defiant", registry="NX-74205")
defiant["crewmembers"].add(
    Crewmember(name="Sisko", rank="Captain", species="Human"),
    Crewmember(name="Dax", rank="Lt Commander", species="Trill"),
    Crewmember(name="Kira", rank="Major", species="Bajoran"))

voyager = Starship.get(name="Voyager")

for human in voyager["crewmembers"].filter(species="Human"):
  print human["name"]

for starship in Starship.all():
    print(starship.fields.as_dict())