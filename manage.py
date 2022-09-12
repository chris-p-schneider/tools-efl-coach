# manage.py
# Manages Flask Migration

# Imports
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from TEFLC import app, db

# --------------------------------------------

migrate = Migrate(app, db)
# Miguel Grinberg
# migrate = Migrate()
# migrate.init__app(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()