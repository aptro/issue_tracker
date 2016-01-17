from flask.ext.script import Manager, Server, Shell
from app import application



manager = Manager(application)

manager.add_command("shell", Shell(use_ipython=True))
manager.add_command("runserver", Server(
        use_debugger=True,
        use_reloader=True,
        host='0.0.0.0',
        port=5000))


if __name__ == "__main__":
    manager.run()
