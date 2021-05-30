from start import *
from db import Users, Developers


# DB creation
@app.cli.command('db.create')
def db_create():
    db.create_all()
    print('Database created successfully !')


@app.cli.command('db.drop')
def db_drop():
    db.drop_all()
    print('Database dropped successfully !')


@app.cli.command('db.seed')
def db_seed():

    dev1 = Developers(first_name='John',
                      last_name='Daniel',
                      module='KNOWN',
                      prog_lang='Java')
    dev2 = Developers(first_name='Gilly',
                      last_name='Crisp',
                      module='UKNOWN',
                      prog_lang='Java')
    dev3 = Developers(first_name='Honey',
                      last_name='Creeper',
                      module='DEADLY',
                      prog_lang='Java')
    db.session.add(dev1)
    db.session.add(dev2)
    db.session.add(dev3)

    # Users
    test_user = Users(first_name='test',
                      last_name='user',
                      email='user@test.com',
                      password='pass')
    db.session.add(test_user)

    # commit the data to the tables in the DB
    db.session.commit()
    print("Database seeding completed successfully !")
