import os
import sqlalchemy
import sqlalchemy.orm

import pyramid_jinja2

from pyramid.interfaces import IAuthenticationPolicy
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.exceptions import ConfigurationError

from stucco_auth import security
from stucco_auth import tables
from stucco_auth import views
from stucco_auth.tm import TM, SESSION_KEY
from stucco_auth.interfaces import IAuthRoot

SESSION_FACTORY_KEY = __name__ + '.db_session_factory'

import logging
log = logging.getLogger(__name__)


def new_request_listener(event):
    """Assign request.db as required by stucco_auth views.

    stucco_auth requires a transaction-managed SQLAlchemy session to be
    available as request.db. How this will be obtained depends on the
    kind of session factory and transaction manager that are in use.
    """
    event.request.db = event.request.environ[SESSION_KEY]

def includeme(c):
    """Starter stucco_auth configuration."""
    config_views(c)

def config_views(c):
    """Add stucco_auth views to Pyramid configurator instance."""
    c.add_view(views.login, name='login', context=IAuthRoot,
        renderer='login.jinja2')
    c.add_view(views.login_post, name='login', context=IAuthRoot,
        request_method='POST')
    c.add_view(views.logout, name='logout', context=IAuthRoot)
    # caller places this where they want it
    # c.add_static_view('static', 'stucco_auth:static')

def persistent_random_secret(session, key):
    """Retrieve or create random, persistent named secret."""
    tkt_secret = session.query(tables.Settings).get(key)
    if tkt_secret is None:
        tkt_secret = tables.Settings(key=key,
                value=os.urandom(16).encode('hex'))
        log.info("Generated new secret '%s'", key)
        session.add(tkt_secret)
    return tkt_secret

def auth_tkt_secret(session):
    """Retrieve stored auth_tkt secret, or make and store a secure new one."""
    return persistent_random_secret(session, 'auth_tkt_secret')

def demo_app(global_config, **settings):
    """Return the example application for stucco_auth."""
    from stucco_auth.models import get_root

    engine = sqlalchemy.engine_from_config(settings)
    Session = sqlalchemy.orm.sessionmaker(bind=engine)
    settings[SESSION_FACTORY_KEY] = Session

    session = Session()
    try:
        import stucco_evolution
        stucco_evolution.initialize(session.connection())
        stucco_evolution.create_or_upgrade_packages(session.connection(), 
                                                    'stucco_auth')

        tkt_secret = auth_tkt_secret(session)

        authentication_policy = AuthTktAuthenticationPolicy(
            tkt_secret.value, callback=security.lookup_groups)

        authorization_policy = ACLAuthorizationPolicy()

        config = Configurator(root_factory=get_root,
                              settings=settings,
                              authentication_policy=authentication_policy,
                              authorization_policy=authorization_policy)

        config.add_renderer('.jinja2', pyramid_jinja2.renderer_factory)

        # Configure beaker session:
        import pyramid_beaker
        session_factory = \
            pyramid_beaker.session_factory_from_settings(settings)
        config.set_session_factory(session_factory)
        config.include('stucco_auth.includeme')
        config.add_static_view('static', 'stucco_auth:static')
        config.add_view(context=IAuthRoot, renderer='welcome.jinja2')
        # event handler will only work if stucco_auth.tm is being used
        config.add_subscriber(new_request_listener, NewRequest)

        app = config.make_wsgi_app()
        tm = TM(app, Session)

        # For pshell compatibility:
        tm.registry, tm.threadlocal_manager, tm.root_factory = \
                app.registry, app.threadlocal_manager, app.root_factory

        # In case database work was done during init:
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

    return tm
