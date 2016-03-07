from fabric.api import *
from fabric.contrib import files
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--user', 
                    help='the target user', 
                    action='store', 
                    default='ubuntu', 
                    dest='user')
parser.add_argument('--hosts', 
                    help='the target address', 
                    action='store', 
                    dest='hosts')
subparsers = parser.add_subparsers(dest="subparser_name")
create_keystone_db = subparsers.add_parser('create-keystone-db',
                                           help='create the keystone database', )
create_keystone_db.add_argument('--root-db-pass', 
                    help='the openstack database root passowrd',
                   action='store', 
                   default=None, 
                   dest='root_db_pass')
create_keystone_db.add_argument('--keystone-db-pass', 
                    help='keystone db passowrd',
                    action='store', 
                    default=None, 
                    dest='keystone_db_pass')

install = subparsers.add_parser('install',
                                help='install keystone')
install.add_argument('--admin_token',
                    help='define the value of the initial administration token',
                    action='store',
                    default=None,
                    dest='admin_token')
install.add_argument('--connection',
                    help='database connection string e.g. mysql+pymysql://keystone:PASS@CONTROLLER_VIP/keystone',
                    action='store',
                    default=None,
                    dest='connection')
install.add_argument('--memcache_servers',
                    help='memcached servers',
                    action='store',
                    default=None,
                    dest='memcache_servers')
install.add_argument('--populate',
                    help='populate the keystone database',
                    action='store_true',
                    default=False,
                    dest='populate')

create_entity_and_endpoint = subparsers.add_parser('create-entity-and-endpoint',
                                                   help='create the service entity and API endpoints',)
create_entity_and_endpoint.add_argument('--os-token',
                                        help='the admin token',
                                        action='store',
                                        default=None,
                                        dest='os_token')
create_entity_and_endpoint.add_argument('--os-url',
                                        help='keystone endpoint url e.g. http://controller:35357/v3',
                                        action='store',
                                        default=None,
                                        dest='os_url')
create_entity_and_endpoint.add_argument('--public-endpoint',
                                        help='the public endpoint e.g. http://controller:5000/v2.0',
                                        action='store',
                                        default=None,
                                        dest='public_endpoint')
create_entity_and_endpoint.add_argument('--internal-endpoint',
                                        help='the internal endpoint e.g. http://controller:5000/v2.0',
                                        action='store',
                                        default=None,
                                        dest='internal_endpoint')
create_entity_and_endpoint.add_argument('--admin-endpoint',
                                        help='the admin endpoint e.g. http://controller:35357/v2.0',
                                        action='store',
                                        default=None,
                                        dest='admin_endpoint')

create_projects_users_roles = subparsers.add_parser('create-projects-users-roles',
                                                    help='create an administrative and demo project, user, and role for administrative and testing operations in your environment')
create_projects_users_roles.add_argument('--os-token',
                                        help='the admin token',
                                        action='store',
                                        default=None,
                                        dest='os_token')
create_projects_users_roles.add_argument('--os-url',
                                        help='keystone endpoint url e.g. http://controller:35357/v3',
                                        action='store',
                                        default=None,
                                        dest='os_url')
create_projects_users_roles.add_argument('--admin-pass',
                                        help='passowrd for admin user',
                                        action='store',
                                        default=None,
                                        dest='admin_pass')
create_projects_users_roles.add_argument('--demo-pass',
                                        help='passowrd for demo user',
                                        action='store',
                                        default=None,
                                        dest='demo_pass')



args = parser.parse_args()

conf_keystone_conf = """[DEFAULT]

#
# From keystone
#

# A "shared secret" that can be used to bootstrap Keystone. This "token" does
# not represent a user, and carries no explicit authorization. To disable in
# production (highly recommended), remove AdminTokenAuthMiddleware from your
# paste application pipelines (for example, in keystone-paste.ini). (string
# value)
admin_token = {{ admin_token }}

# The base public endpoint URL for Keystone that is advertised to clients
# (NOTE: this does NOT affect how Keystone listens for connections). Defaults
# to the base host URL of the request. E.g. a request to
# http://server:5000/v3/users will default to http://server:5000. You should
# only need to set this value if the base URL contains a path (e.g. /prefix/v3)
# or the endpoint should be found on a different server. (string value)
#public_endpoint = <None>

# The base admin endpoint URL for Keystone that is advertised to clients (NOTE:
# this does NOT affect how Keystone listens for connections). Defaults to the
# base host URL of the request. E.g. a request to http://server:35357/v3/users
# will default to http://server:35357. You should only need to set this value
# if the base URL contains a path (e.g. /prefix/v3) or the endpoint should be
# found on a different server. (string value)
#admin_endpoint = <None>

# Maximum depth of the project hierarchy. WARNING: setting it to a large value
# may adversely impact performance. (integer value)
#max_project_tree_depth = 5

# Limit the sizes of user & project ID/names. (integer value)
#max_param_size = 64

# Similar to max_param_size, but provides an exception for token values.
# (integer value)
#max_token_size = 8192

# Similar to the member_role_name option, this represents the default role ID
# used to associate users with their default projects in the v2 API. This will
# be used as the explicit role where one is not specified by the v2 API.
# (string value)
#member_role_id = 9fe2ff9ee4384b1894a90878d3e92bab

# This is the role name used in combination with the member_role_id option; see
# that option for more detail. (string value)
#member_role_name = _member_

# The value passed as the keyword "rounds" to passlib's encrypt method.
# (integer value)
# Minimum value: 1000
# Maximum value: 100000
#crypt_strength = 10000

# The maximum number of entities that will be returned in a collection, with no
# limit set by default. This global limit may be then overridden for a specific
# driver, by specifying a list_limit in the appropriate section (e.g.
# [assignment]). (integer value)
#list_limit = <None>

# Set this to false if you want to enable the ability for user, group and
# project entities to be moved between domains by updating their domain_id.
# Allowing such movement is not recommended if the scope of a domain admin is
# being restricted by use of an appropriate policy file (see
# policy.v3cloudsample as an example). (boolean value)
#domain_id_immutable = true

# If set to true, strict password length checking is performed for password
# manipulation. If a password exceeds the maximum length, the operation will
# fail with an HTTP 403 Forbidden error. If set to false, passwords are
# automatically truncated to the maximum length. (boolean value)
#strict_password_check = false

# The HTTP header used to determine the scheme for the original request, even
# if it was removed by an SSL terminating proxy. Typical value is
# "HTTP_X_FORWARDED_PROTO". (string value)
#secure_proxy_ssl_header = <None>

#
# From keystone.notifications
#

# Default publisher_id for outgoing notifications (string value)
#default_publisher_id = <None>

# Define the notification format for Identity Service events. A "basic"
# notification has information about the resource being operated on. A "cadf"
# notification has the same information, as well as information about the
# initiator of the event. (string value)
# Allowed values: basic, cadf
#notification_format = basic

#
# From oslo.log
#

# Print debugging output (set logging level to DEBUG instead of default INFO
# level). (boolean value)
#debug = true

# If set to false, will disable INFO logging level, making WARNING the default.
# (boolean value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
verbose = true

# The name of a logging configuration file. This file is appended to any
# existing logging configuration files. For details about logging configuration
# files, see the Python logging module documentation. (string value)
# Deprecated group/name - [DEFAULT]/log_config
#log_config_append = <None>

# DEPRECATED. A logging.Formatter log message format string which may use any
# of the available logging.LogRecord attributes. This option is deprecated.
# Please use logging_context_format_string and logging_default_format_string
# instead. (string value)
#log_format = <None>

# Format string for %%(asctime)s in log records. Default: %(default)s . (string
# value)
#log_date_format = %Y-%m-%d %H:%M:%S

# (Optional) Name of log file to output to. If no default is set, logging will
# go to stdout. (string value)
# Deprecated group/name - [DEFAULT]/logfile
#log_file = <None>

# (Optional) The base directory used for relative --log-file paths. (string
# value)
# Deprecated group/name - [DEFAULT]/logdir
#log_dir = <None>
log_dir = /var/log/keystone

# Use syslog for logging. Existing syslog format is DEPRECATED and will be
# changed later to honor RFC5424. (boolean value)
#use_syslog = false

# (Optional) Enables or disables syslog rfc5424 format for logging. If enabled,
# prefixes the MSG part of the syslog message with APP-NAME (RFC5424). The
# format without the APP-NAME is deprecated in Kilo, and will be removed in
# Mitaka, along with this option. (boolean value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#use_syslog_rfc_format = true

# Syslog facility to receive log lines. (string value)
#syslog_log_facility = LOG_USER

# Log output to standard error. (boolean value)
#use_stderr = true

# Format string to use for log messages with context. (string value)
#logging_context_format_string = %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [%(request_id)s %(user_identity)s] %(instance)s%(message)s

# Format string to use for log messages without context. (string value)
#logging_default_format_string = %(asctime)s.%(msecs)03d %(process)d %(levelname)s %(name)s [-] %(instance)s%(message)s

# Data to append to log format when level is DEBUG. (string value)
#logging_debug_format_suffix = %(funcName)s %(pathname)s:%(lineno)d

# Prefix each line of exception output with this format. (string value)
#logging_exception_prefix = %(asctime)s.%(msecs)03d %(process)d ERROR %(name)s %(instance)s

# List of logger=LEVEL pairs. (list value)
#default_log_levels = amqp=WARN,amqplib=WARN,boto=WARN,qpid=WARN,sqlalchemy=WARN,suds=INFO,oslo.messaging=INFO,iso8601=WARN,requests.packages.urllib3.connectionpool=WARN,urllib3.connectionpool=WARN,websocket=WARN,requests.packages.urllib3.util.retry=WARN,urllib3.util.retry=WARN,keystonemiddleware=WARN,routes.middleware=WARN,stevedore=WARN,taskflow=WARN

# Enables or disables publication of error events. (boolean value)
#publish_errors = false

# The format for an instance that is passed with the log message. (string
# value)
#instance_format = "[instance: %(uuid)s] "

# The format for an instance UUID that is passed with the log message. (string
# value)
#instance_uuid_format = "[instance: %(uuid)s] "

# Enables or disables fatal status of deprecations. (boolean value)
#fatal_deprecations = false

#
# From oslo.messaging
#

# Size of RPC connection pool. (integer value)
# Deprecated group/name - [DEFAULT]/rpc_conn_pool_size
#rpc_conn_pool_size = 30

# ZeroMQ bind address. Should be a wildcard (*), an ethernet interface, or IP.
# The "host" option should point or resolve to this address. (string value)
#rpc_zmq_bind_address = *

# MatchMaker driver. (string value)
#rpc_zmq_matchmaker = local

# ZeroMQ receiver listening port. (integer value)
#rpc_zmq_port = 9501

# Number of ZeroMQ contexts, defaults to 1. (integer value)
#rpc_zmq_contexts = 1

# Maximum number of ingress messages to locally buffer per topic. Default is
# unlimited. (integer value)
#rpc_zmq_topic_backlog = <None>

# Directory for holding IPC sockets. (string value)
#rpc_zmq_ipc_dir = /var/run/openstack

# Name of this node. Must be a valid hostname, FQDN, or IP address. Must match
# "host" option, if running Nova. (string value)
#rpc_zmq_host = localhost

# Seconds to wait before a cast expires (TTL). Only supported by impl_zmq.
# (integer value)
#rpc_cast_timeout = 30

# Heartbeat frequency. (integer value)
#matchmaker_heartbeat_freq = 300

# Heartbeat time-to-live. (integer value)
#matchmaker_heartbeat_ttl = 600

# Size of executor thread pool. (integer value)
# Deprecated group/name - [DEFAULT]/rpc_thread_pool_size
#executor_thread_pool_size = 64

# The Drivers(s) to handle sending notifications. Possible values are
# messaging, messagingv2, routing, log, test, noop (multi valued)
#notification_driver =

# AMQP topic used for OpenStack notifications. (list value)
# Deprecated group/name - [rpc_notifier2]/topics
#notification_topics = notifications

# Seconds to wait for a response from a call. (integer value)
#rpc_response_timeout = 60

# A URL representing the messaging driver to use and its full configuration. If
# not set, we fall back to the rpc_backend option and driver specific
# configuration. (string value)
#transport_url = <None>

# The messaging driver to use, defaults to rabbit. Other drivers include qpid
# and zmq. (string value)
#rpc_backend = rabbit

# The default exchange under which topics are scoped. May be overridden by an
# exchange name specified in the transport_url option. (string value)
#control_exchange = keystone

#
# From oslo.service.service
#

# Enable eventlet backdoor.  Acceptable values are 0, <port>, and
# <start>:<end>, where 0 results in listening on a random tcp port number;
# <port> results in listening on the specified port number (and not enabling
# backdoor if that port is in use); and <start>:<end> results in listening on
# the smallest unused port number within the specified range of port numbers.
# The chosen port is displayed in the service's log file. (string value)
#backdoor_port = <None>

# Enables or disables logging values of all registered options when starting a
# service (at DEBUG level). (boolean value)
#log_options = true


[assignment]

#
# From keystone
#

# Entrypoint for the assignment backend driver in the keystone.assignment
# namespace. Supplied drivers are ldap and sql. If an assignment driver is not
# specified, the identity driver will choose the assignment driver. (string
# value)
#driver = <None>


[auth]

#
# From keystone
#

# Allowed authentication methods. (list value)
#methods = external,password,token,oauth1

# Entrypoint for the password auth plugin module in the keystone.auth.password
# namespace. (string value)
#password = <None>

# Entrypoint for the token auth plugin module in the keystone.auth.token
# namespace. (string value)
#token = <None>

# Entrypoint for the external (REMOTE_USER) auth plugin module in the
# keystone.auth.external namespace. Supplied drivers are DefaultDomain and
# Domain. The default driver is DefaultDomain. (string value)
#external = <None>

# Entrypoint for the oAuth1.0 auth plugin module in the keystone.auth.oauth1
# namespace. (string value)
#oauth1 = <None>


[cache]

#
# From keystone
#

# Prefix for building the configuration dictionary for the cache region. This
# should not need to be changed unless there is another dogpile.cache region
# with the same configuration name. (string value)
#config_prefix = cache.keystone

# Default TTL, in seconds, for any cached item in the dogpile.cache region.
# This applies to any cached method that doesn't have an explicit cache
# expiration time defined for it. (integer value)
#expiration_time = 600

# Dogpile.cache backend module. It is recommended that Memcache with pooling
# (keystone.cache.memcache_pool) or Redis (dogpile.cache.redis) be used in
# production deployments.  Small workloads (single process) like devstack can
# use the dogpile.cache.memory backend. (string value)
#backend = keystone.common.cache.noop

# Arguments supplied to the backend module. Specify this option once per
# argument to be passed to the dogpile.cache backend. Example format:
# "<argname>:<value>". (multi valued)
#backend_argument =

# Proxy classes to import that will affect the way the dogpile.cache backend
# functions. See the dogpile.cache documentation on changing-backend-behavior.
# (list value)
#proxies =

# Global toggle for all caching using the should_cache_fn mechanism. (boolean
# value)
#enabled = false

# Extra debugging from the cache backend (cache keys, get/set/delete/etc
# calls). This is only really useful if you need to see the specific cache-
# backend get/set/delete calls with the keys/values.  Typically this should be
# left set to false. (boolean value)
#debug_cache_backend = false

# Memcache servers in the format of "host:port". (dogpile.cache.memcache and
# keystone.cache.memcache_pool backends only). (list value)
memcache_servers = {{ memcache_servers }}

# Number of seconds memcached server is considered dead before it is tried
# again. (dogpile.cache.memcache and keystone.cache.memcache_pool backends
# only). (integer value)
#memcache_dead_retry = 300

# Timeout in seconds for every call to a server. (dogpile.cache.memcache and
# keystone.cache.memcache_pool backends only). (integer value)
#memcache_socket_timeout = 3

# Max total number of open connections to every memcached server.
# (keystone.cache.memcache_pool backend only). (integer value)
#memcache_pool_maxsize = 10

# Number of seconds a connection to memcached is held unused in the pool before
# it is closed. (keystone.cache.memcache_pool backend only). (integer value)
#memcache_pool_unused_timeout = 60

# Number of seconds that an operation will wait to get a memcache client
# connection. (integer value)
#memcache_pool_connection_get_timeout = 10


[catalog]

#
# From keystone
#

# Catalog template file name for use with the template catalog backend. (string
# value)
#template_file = default_catalog.templates

# Entrypoint for the catalog backend driver in the keystone.catalog namespace.
# Supplied drivers are kvs, sql, templated, and endpoint_filter.sql (string
# value)
#driver = sql

# Toggle for catalog caching. This has no effect unless global caching is
# enabled. (boolean value)
#caching = true

# Time to cache catalog data (in seconds). This has no effect unless global and
# catalog caching are enabled. (integer value)
#cache_time = <None>

# Maximum number of entities that will be returned in a catalog collection.
# (integer value)
#list_limit = <None>


[cors]

#
# From oslo.middleware
#

# Indicate whether this resource may be shared with the domain received in the
# requests "origin" header. (string value)
#allowed_origin = <None>

# Indicate that the actual request can include user credentials (boolean value)
#allow_credentials = true

# Indicate which headers are safe to expose to the API. Defaults to HTTP Simple
# Headers. (list value)
#expose_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma

# Maximum cache age of CORS preflight requests. (integer value)
#max_age = 3600

# Indicate which methods can be used during the actual request. (list value)
#allow_methods = GET,POST,PUT,DELETE,OPTIONS

# Indicate which header field names may be used during the actual request.
# (list value)
#allow_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma


[cors.subdomain]

#
# From oslo.middleware
#

# Indicate whether this resource may be shared with the domain received in the
# requests "origin" header. (string value)
#allowed_origin = <None>

# Indicate that the actual request can include user credentials (boolean value)
#allow_credentials = true

# Indicate which headers are safe to expose to the API. Defaults to HTTP Simple
# Headers. (list value)
#expose_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma

# Maximum cache age of CORS preflight requests. (integer value)
#max_age = 3600

# Indicate which methods can be used during the actual request. (list value)
#allow_methods = GET,POST,PUT,DELETE,OPTIONS

# Indicate which header field names may be used during the actual request.
# (list value)
#allow_headers = Content-Type,Cache-Control,Content-Language,Expires,Last-Modified,Pragma


[credential]

#
# From keystone
#

# Entrypoint for the credential backend driver in the keystone.credential
# namespace. (string value)
#driver = sql


[database]

#
# From oslo.db
#

# The file name to use with SQLite. (string value)
# Deprecated group/name - [DEFAULT]/sqlite_db
#sqlite_db = oslo.sqlite

# If True, SQLite uses synchronous mode. (boolean value)
# Deprecated group/name - [DEFAULT]/sqlite_synchronous
#sqlite_synchronous = true

# The back end to use for the database. (string value)
# Deprecated group/name - [DEFAULT]/db_backend
#backend = sqlalchemy

# The SQLAlchemy connection string to use to connect to the database. (string
# value)
# Deprecated group/name - [DEFAULT]/sql_connection
# Deprecated group/name - [DATABASE]/sql_connection
# Deprecated group/name - [sql]/connection
#connection = <None>
connection = {{ connection }}

# The SQLAlchemy connection string to use to connect to the slave database.
# (string value)
#slave_connection = <None>

# The SQL mode to be used for MySQL sessions. This option, including the
# default, overrides any server-set SQL mode. To use whatever SQL mode is set
# by the server configuration, set this to no value. Example: mysql_sql_mode=
# (string value)
#mysql_sql_mode = TRADITIONAL

# Timeout before idle SQL connections are reaped. (integer value)
# Deprecated group/name - [DEFAULT]/sql_idle_timeout
# Deprecated group/name - [DATABASE]/sql_idle_timeout
# Deprecated group/name - [sql]/idle_timeout
#idle_timeout = 3600

# Minimum number of SQL connections to keep open in a pool. (integer value)
# Deprecated group/name - [DEFAULT]/sql_min_pool_size
# Deprecated group/name - [DATABASE]/sql_min_pool_size
#min_pool_size = 1

# Maximum number of SQL connections to keep open in a pool. (integer value)
# Deprecated group/name - [DEFAULT]/sql_max_pool_size
# Deprecated group/name - [DATABASE]/sql_max_pool_size
#max_pool_size = <None>

# Maximum number of database connection retries during startup. Set to -1 to
# specify an infinite retry count. (integer value)
# Deprecated group/name - [DEFAULT]/sql_max_retries
# Deprecated group/name - [DATABASE]/sql_max_retries
#max_retries = 10

# Interval between retries of opening a SQL connection. (integer value)
# Deprecated group/name - [DEFAULT]/sql_retry_interval
# Deprecated group/name - [DATABASE]/reconnect_interval
#retry_interval = 10

# If set, use this value for max_overflow with SQLAlchemy. (integer value)
# Deprecated group/name - [DEFAULT]/sql_max_overflow
# Deprecated group/name - [DATABASE]/sqlalchemy_max_overflow
#max_overflow = <None>

# Verbosity of SQL debugging information: 0=None, 100=Everything. (integer
# value)
# Deprecated group/name - [DEFAULT]/sql_connection_debug
#connection_debug = 0

# Add Python stack traces to SQL as comment strings. (boolean value)
# Deprecated group/name - [DEFAULT]/sql_connection_trace
#connection_trace = false

# If set, use this value for pool_timeout with SQLAlchemy. (integer value)
# Deprecated group/name - [DATABASE]/sqlalchemy_pool_timeout
#pool_timeout = <None>

# Enable the experimental use of database reconnect on connection lost.
# (boolean value)
#use_db_reconnect = false

# Seconds between retries of a database transaction. (integer value)
#db_retry_interval = 1

# If True, increases the interval between retries of a database operation up to
# db_max_retry_interval. (boolean value)
#db_inc_retry_interval = true

# If db_inc_retry_interval is set, the maximum seconds between retries of a
# database operation. (integer value)
#db_max_retry_interval = 10

# Maximum retries in case of connection error or deadlock error before error is
# raised. Set to -1 to specify an infinite retry count. (integer value)
#db_max_retries = 20


[domain_config]

#
# From keystone
#

# Entrypoint for the domain config backend driver in the
# keystone.resource.domain_config namespace. (string value)
#driver = sql

# Toggle for domain config caching. This has no effect unless global caching is
# enabled. (boolean value)
#caching = true

# TTL (in seconds) to cache domain config data. This has no effect unless
# domain config caching is enabled. (integer value)
#cache_time = 300


[endpoint_filter]

#
# From keystone
#

# Entrypoint for the endpoint filter backend driver in the
# keystone.endpoint_filter namespace. (string value)
#driver = sql

# Toggle to return all active endpoints if no filter exists. (boolean value)
#return_all_endpoints_if_no_filter = true


[endpoint_policy]

#
# From keystone
#

# Enable endpoint_policy functionality. (boolean value)
#enabled = true

# Entrypoint for the endpoint policy backend driver in the
# keystone.endpoint_policy namespace. (string value)
#driver = sql


[eventlet_server]

#
# From keystone
#

# The number of worker processes to serve the public eventlet application.
# Defaults to number of CPUs (minimum of 2). (integer value)
# Deprecated group/name - [DEFAULT]/public_workers
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#public_workers = <None>

# The number of worker processes to serve the admin eventlet application.
# Defaults to number of CPUs (minimum of 2). (integer value)
# Deprecated group/name - [DEFAULT]/admin_workers
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#admin_workers = <None>

# The IP address of the network interface for the public service to listen on.
# (string value)
# Deprecated group/name - [DEFAULT]/bind_host
# Deprecated group/name - [DEFAULT]/public_bind_host
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#public_bind_host = 0.0.0.0

# The port number which the public service listens on. (integer value)
# Minimum value: 1
# Maximum value: 65535
# Deprecated group/name - [DEFAULT]/public_port
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#public_port = 5000

# The IP address of the network interface for the admin service to listen on.
# (string value)
# Deprecated group/name - [DEFAULT]/bind_host
# Deprecated group/name - [DEFAULT]/admin_bind_host
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#admin_bind_host = 0.0.0.0

# The port number which the admin service listens on. (integer value)
# Minimum value: 1
# Maximum value: 65535
# Deprecated group/name - [DEFAULT]/admin_port
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#admin_port = 35357

# If set to false, disables keepalives on the server; all connections will be
# closed after serving one request. (boolean value)
#wsgi_keep_alive = true

# Timeout for socket operations on a client connection. If an incoming
# connection is idle for this number of seconds it will be closed. A value of
# '0' means wait forever. (integer value)
#client_socket_timeout = 900

# Set this to true if you want to enable TCP_KEEPALIVE on server sockets, i.e.
# sockets used by the Keystone wsgi server for client connections. (boolean
# value)
# Deprecated group/name - [DEFAULT]/tcp_keepalive
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#tcp_keepalive = false

# Sets the value of TCP_KEEPIDLE in seconds for each server socket. Only
# applies if tcp_keepalive is true. (integer value)
# Deprecated group/name - [DEFAULT]/tcp_keepidle
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#tcp_keepidle = 600


[eventlet_server_ssl]

#
# From keystone
#

# Toggle for SSL support on the Keystone eventlet servers. (boolean value)
# Deprecated group/name - [ssl]/enable
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#enable = false

# Path of the certfile for SSL. For non-production environments, you may be
# interested in using `keystone-manage ssl_setup` to generate self-signed
# certificates. (string value)
# Deprecated group/name - [ssl]/certfile
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#certfile = /etc/keystone/ssl/certs/keystone.pem

# Path of the keyfile for SSL. (string value)
# Deprecated group/name - [ssl]/keyfile
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#keyfile = /etc/keystone/ssl/private/keystonekey.pem

# Path of the CA cert file for SSL. (string value)
# Deprecated group/name - [ssl]/ca_certs
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#ca_certs = /etc/keystone/ssl/certs/ca.pem

# Require client certificate. (boolean value)
# Deprecated group/name - [ssl]/cert_required
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#cert_required = false


[federation]

#
# From keystone
#

# Entrypoint for the federation backend driver in the keystone.federation
# namespace. (string value)
#driver = sql

# Value to be used when filtering assertion parameters from the environment.
# (string value)
#assertion_prefix =

# Value to be used to obtain the entity ID of the Identity Provider from the
# environment (e.g. if using the mod_shib plugin this value is `Shib-Identity-
# Provider`). (string value)
#remote_id_attribute = <None>

# A domain name that is reserved to allow federated ephemeral users to have a
# domain concept. Note that an admin will not be able to create a domain with
# this name or update an existing domain to this name. You are not advised to
# change this value unless you really have to. (string value)
#federated_domain_name = Federated

# A list of trusted dashboard hosts. Before accepting a Single Sign-On request
# to return a token, the origin host must be a member of the trusted_dashboard
# list. This configuration option may be repeated for multiple values. For
# example: trusted_dashboard=http://acme.com trusted_dashboard=http://beta.com
# (multi valued)
#trusted_dashboard =

# Location of Single Sign-On callback handler, will return a token to a trusted
# dashboard host. (string value)
#sso_callback_template = /etc/keystone/sso_callback_template.html


[fernet_tokens]

#
# From keystone
#

# Directory containing Fernet token keys. (string value)
#key_repository = /etc/keystone/fernet-keys/

# This controls how many keys are held in rotation by keystone-manage
# fernet_rotate before they are discarded. The default value of 3 means that
# keystone will maintain one staged key, one primary key, and one secondary
# key. Increasing this value means that additional secondary keys will be kept
# in the rotation. (integer value)
#max_active_keys = 3


[identity]

#
# From keystone
#

# This references the domain to use for all Identity API v2 requests (which are
# not aware of domains). A domain with this ID will be created for you by
# keystone-manage db_sync in migration 008. The domain referenced by this ID
# cannot be deleted on the v3 API, to prevent accidentally breaking the v2 API.
# There is nothing special about this domain, other than the fact that it must
# exist to order to maintain support for your v2 clients. (string value)
#default_domain_id = default

# A subset (or all) of domains can have their own identity driver, each with
# their own partial configuration options, stored in either the resource
# backend or in a file in a domain configuration directory (depending on the
# setting of domain_configurations_from_database). Only values specific to the
# domain need to be specified in this manner. This feature is disabled by
# default; set to true to enable. (boolean value)
#domain_specific_drivers_enabled = false

# Extract the domain specific configuration options from the resource backend
# where they have been stored with the domain data. This feature is disabled by
# default (in which case the domain specific options will be loaded from files
# in the domain configuration directory); set to true to enable. (boolean
# value)
#domain_configurations_from_database = false

# Path for Keystone to locate the domain specific identity configuration files
# if domain_specific_drivers_enabled is set to true. (string value)
#domain_config_dir = /etc/keystone/domains

# Entrypoint for the identity backend driver in the keystone.identity
# namespace. Supplied drivers are ldap and sql. (string value)
#driver = sql

# Toggle for identity caching. This has no effect unless global caching is
# enabled. (boolean value)
#caching = true

# Time to cache identity data (in seconds). This has no effect unless global
# and identity caching are enabled. (integer value)
#cache_time = 600

# Maximum supported length for user passwords; decrease to improve performance.
# (integer value)
# Maximum value: 4096
#max_password_length = 4096

# Maximum number of entities that will be returned in an identity collection.
# (integer value)
#list_limit = <None>


[identity_mapping]

#
# From keystone
#

# Entrypoint for the identity mapping backend driver in the
# keystone.identity.id_mapping namespace. (string value)
#driver = sql

# Entrypoint for the public ID generator for user and group entities in the
# keystone.identity.id_generator namespace. The Keystone identity mapper only
# supports generators that produce no more than 64 characters. (string value)
#generator = sha256

# The format of user and group IDs changed in Juno for backends that do not
# generate UUIDs (e.g. LDAP), with keystone providing a hash mapping to the
# underlying attribute in LDAP. By default this mapping is disabled, which
# ensures that existing IDs will not change. Even when the mapping is enabled
# by using domain specific drivers, any users and groups from the default
# domain being handled by LDAP will still not be mapped to ensure their IDs
# remain backward compatible. Setting this value to False will enable the
# mapping for even the default LDAP driver. It is only safe to do this if you
# do not already have assignments for users and groups from the default LDAP
# domain, and it is acceptable for Keystone to provide the different IDs to
# clients than it did previously.  Typically this means that the only time you
# can set this value to False is when configuring a fresh installation.
# (boolean value)
#backward_compatible_ids = true


[kvs]

#
# From keystone
#

# Extra dogpile.cache backend modules to register with the dogpile.cache
# library. (list value)
#backends =

# Prefix for building the configuration dictionary for the KVS region. This
# should not need to be changed unless there is another dogpile.cache region
# with the same configuration name. (string value)
#config_prefix = keystone.kvs

# Toggle to disable using a key-mangling function to ensure fixed length keys.
# This is toggle-able for debugging purposes, it is highly recommended to
# always leave this set to true. (boolean value)
#enable_key_mangler = true

# Default lock timeout (in seconds) for distributed locking. (integer value)
#default_lock_timeout = 5


[ldap]

#
# From keystone
#

# URL for connecting to the LDAP server. (string value)
#url = ldap://localhost

# User BindDN to query the LDAP server. (string value)
#user = <None>

# Password for the BindDN to query the LDAP server. (string value)
#password = <None>

# LDAP server suffix (string value)
#suffix = cn=example,cn=com

# If true, will add a dummy member to groups. This is required if the
# objectclass for groups requires the "member" attribute. (boolean value)
#use_dumb_member = false

# DN of the "dummy member" to use when "use_dumb_member" is enabled. (string
# value)
#dumb_member = cn=dumb,dc=nonexistent

# Delete subtrees using the subtree delete control. Only enable this option if
# your LDAP server supports subtree deletion. (boolean value)
#allow_subtree_delete = false

# The LDAP scope for queries, "one" represents oneLevel/singleLevel and "sub"
# represents subtree/wholeSubtree options. (string value)
# Allowed values: one, sub
#query_scope = one

# Maximum results per page; a value of zero ("0") disables paging. (integer
# value)
#page_size = 0

# The LDAP dereferencing option for queries. The "default" option falls back to
# using default dereferencing configured by your ldap.conf. (string value)
# Allowed values: never, searching, always, finding, default
#alias_dereferencing = default

# Sets the LDAP debugging level for LDAP calls. A value of 0 means that
# debugging is not enabled. This value is a bitmask, consult your LDAP
# documentation for possible values. (integer value)
#debug_level = <None>

# Override the system's default referral chasing behavior for queries. (boolean
# value)
#chase_referrals = <None>

# Search base for users. Defaults to the suffix value. (string value)
#user_tree_dn = <None>

# LDAP search filter for users. (string value)
#user_filter = <None>

# LDAP objectclass for users. (string value)
#user_objectclass = inetOrgPerson

# LDAP attribute mapped to user id. WARNING: must not be a multivalued
# attribute. (string value)
#user_id_attribute = cn

# LDAP attribute mapped to user name. (string value)
#user_name_attribute = sn

# LDAP attribute mapped to user email. (string value)
#user_mail_attribute = mail

# LDAP attribute mapped to password. (string value)
#user_pass_attribute = userPassword

# LDAP attribute mapped to user enabled flag. (string value)
#user_enabled_attribute = enabled

# Invert the meaning of the boolean enabled values. Some LDAP servers use a
# boolean lock attribute where "true" means an account is disabled. Setting
# "user_enabled_invert = true" will allow these lock attributes to be used.
# This setting will have no effect if "user_enabled_mask" or
# "user_enabled_emulation" settings are in use. (boolean value)
#user_enabled_invert = false

# Bitmask integer to indicate the bit that the enabled value is stored in if
# the LDAP server represents "enabled" as a bit on an integer rather than a
# boolean. A value of "0" indicates the mask is not used. If this is not set to
# "0" the typical value is "2". This is typically used when
# "user_enabled_attribute = userAccountControl". (integer value)
#user_enabled_mask = 0

# Default value to enable users. This should match an appropriate int value if
# the LDAP server uses non-boolean (bitmask) values to indicate if a user is
# enabled or disabled. If this is not set to "True" the typical value is "512".
# This is typically used when "user_enabled_attribute = userAccountControl".
# (string value)
#user_enabled_default = True

# List of attributes stripped off the user on update. (list value)
#user_attribute_ignore = default_project_id

# LDAP attribute mapped to default_project_id for users. (string value)
#user_default_project_id_attribute = <None>

# Allow user creation in LDAP backend. (boolean value)
#user_allow_create = true

# Allow user updates in LDAP backend. (boolean value)
#user_allow_update = true

# Allow user deletion in LDAP backend. (boolean value)
#user_allow_delete = true

# If true, Keystone uses an alternative method to determine if a user is
# enabled or not by checking if they are a member of the
# "user_enabled_emulation_dn" group. (boolean value)
#user_enabled_emulation = false

# DN of the group entry to hold enabled users when using enabled emulation.
# (string value)
#user_enabled_emulation_dn = <None>

# Use the "group_member_attribute" and "group_objectclass" settings to
# determine membership in the emulated enabled group. (boolean value)
#user_enabled_emulation_use_group_config = false

# List of additional LDAP attributes used for mapping additional attribute
# mappings for users. Attribute mapping format is <ldap_attr>:<user_attr>,
# where ldap_attr is the attribute in the LDAP entry and user_attr is the
# Identity API attribute. (list value)
#user_additional_attribute_mapping =

# Search base for projects. Defaults to the suffix value. (string value)
# Deprecated group/name - [ldap]/tenant_tree_dn
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_tree_dn = <None>

# LDAP search filter for projects. (string value)
# Deprecated group/name - [ldap]/tenant_filter
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_filter = <None>

# LDAP objectclass for projects. (string value)
# Deprecated group/name - [ldap]/tenant_objectclass
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_objectclass = groupOfNames

# LDAP attribute mapped to project id. (string value)
# Deprecated group/name - [ldap]/tenant_id_attribute
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_id_attribute = cn

# LDAP attribute mapped to project membership for user. (string value)
# Deprecated group/name - [ldap]/tenant_member_attribute
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_member_attribute = member

# LDAP attribute mapped to project name. (string value)
# Deprecated group/name - [ldap]/tenant_name_attribute
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_name_attribute = ou

# LDAP attribute mapped to project description. (string value)
# Deprecated group/name - [ldap]/tenant_desc_attribute
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_desc_attribute = description

# LDAP attribute mapped to project enabled. (string value)
# Deprecated group/name - [ldap]/tenant_enabled_attribute
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_enabled_attribute = enabled

# LDAP attribute mapped to project domain_id. (string value)
# Deprecated group/name - [ldap]/tenant_domain_id_attribute
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_domain_id_attribute = businessCategory

# List of attributes stripped off the project on update. (list value)
# Deprecated group/name - [ldap]/tenant_attribute_ignore
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_attribute_ignore =

# Allow project creation in LDAP backend. (boolean value)
# Deprecated group/name - [ldap]/tenant_allow_create
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_allow_create = true

# Allow project update in LDAP backend. (boolean value)
# Deprecated group/name - [ldap]/tenant_allow_update
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_allow_update = true

# Allow project deletion in LDAP backend. (boolean value)
# Deprecated group/name - [ldap]/tenant_allow_delete
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_allow_delete = true

# If true, Keystone uses an alternative method to determine if a project is
# enabled or not by checking if they are a member of the
# "project_enabled_emulation_dn" group. (boolean value)
# Deprecated group/name - [ldap]/tenant_enabled_emulation
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_enabled_emulation = false

# DN of the group entry to hold enabled projects when using enabled emulation.
# (string value)
# Deprecated group/name - [ldap]/tenant_enabled_emulation_dn
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_enabled_emulation_dn = <None>

# Use the "group_member_attribute" and "group_objectclass" settings to
# determine membership in the emulated enabled group. (boolean value)
#project_enabled_emulation_use_group_config = false

# Additional attribute mappings for projects. Attribute mapping format is
# <ldap_attr>:<user_attr>, where ldap_attr is the attribute in the LDAP entry
# and user_attr is the Identity API attribute. (list value)
# Deprecated group/name - [ldap]/tenant_additional_attribute_mapping
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#project_additional_attribute_mapping =

# Search base for roles. Defaults to the suffix value. (string value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_tree_dn = <None>

# LDAP search filter for roles. (string value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_filter = <None>

# LDAP objectclass for roles. (string value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_objectclass = organizationalRole

# LDAP attribute mapped to role id. (string value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_id_attribute = cn

# LDAP attribute mapped to role name. (string value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_name_attribute = ou

# LDAP attribute mapped to role membership. (string value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_member_attribute = roleOccupant

# List of attributes stripped off the role on update. (list value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_attribute_ignore =

# Allow role creation in LDAP backend. (boolean value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_allow_create = true

# Allow role update in LDAP backend. (boolean value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_allow_update = true

# Allow role deletion in LDAP backend. (boolean value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_allow_delete = true

# Additional attribute mappings for roles. Attribute mapping format is
# <ldap_attr>:<user_attr>, where ldap_attr is the attribute in the LDAP entry
# and user_attr is the Identity API attribute. (list value)
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#role_additional_attribute_mapping =

# Search base for groups. Defaults to the suffix value. (string value)
#group_tree_dn = <None>

# LDAP search filter for groups. (string value)
#group_filter = <None>

# LDAP objectclass for groups. (string value)
#group_objectclass = groupOfNames

# LDAP attribute mapped to group id. (string value)
#group_id_attribute = cn

# LDAP attribute mapped to group name. (string value)
#group_name_attribute = ou

# LDAP attribute mapped to show group membership. (string value)
#group_member_attribute = member

# LDAP attribute mapped to group description. (string value)
#group_desc_attribute = description

# List of attributes stripped off the group on update. (list value)
#group_attribute_ignore =

# Allow group creation in LDAP backend. (boolean value)
#group_allow_create = true

# Allow group update in LDAP backend. (boolean value)
#group_allow_update = true

# Allow group deletion in LDAP backend. (boolean value)
#group_allow_delete = true

# Additional attribute mappings for groups. Attribute mapping format is
# <ldap_attr>:<user_attr>, where ldap_attr is the attribute in the LDAP entry
# and user_attr is the Identity API attribute. (list value)
#group_additional_attribute_mapping =

# CA certificate file path for communicating with LDAP servers. (string value)
#tls_cacertfile = <None>

# CA certificate directory path for communicating with LDAP servers. (string
# value)
#tls_cacertdir = <None>

# Enable TLS for communicating with LDAP servers. (boolean value)
#use_tls = false

# Specifies what checks to perform on client certificates in an incoming TLS
# session. (string value)
# Allowed values: demand, never, allow
#tls_req_cert = demand

# Enable LDAP connection pooling. (boolean value)
#use_pool = false

# Connection pool size. (integer value)
#pool_size = 10

# Maximum count of reconnect trials. (integer value)
#pool_retry_max = 3

# Time span in seconds to wait between two reconnect trials. (floating point
# value)
#pool_retry_delay = 0.1

# Connector timeout in seconds. Value -1 indicates indefinite wait for
# response. (integer value)
#pool_connection_timeout = -1

# Connection lifetime in seconds. (integer value)
#pool_connection_lifetime = 600

# Enable LDAP connection pooling for end user authentication. If use_pool is
# disabled, then this setting is meaningless and is not used at all. (boolean
# value)
#use_auth_pool = false

# End user auth connection pool size. (integer value)
#auth_pool_size = 100

# End user auth connection lifetime in seconds. (integer value)
#auth_pool_connection_lifetime = 60


[matchmaker_redis]

#
# From oslo.messaging
#

# Host to locate redis. (string value)
#host = 127.0.0.1

# Use this port to connect to redis host. (integer value)
#port = 6379

# Password for Redis server (optional). (string value)
#password = <None>


[matchmaker_ring]

#
# From oslo.messaging
#

# Matchmaker ring file (JSON). (string value)
# Deprecated group/name - [DEFAULT]/matchmaker_ringfile
#ringfile = /etc/oslo/matchmaker_ring.json


[memcache]

#
# From keystone
#

# Memcache servers in the format of "host:port". (list value)
#servers = localhost:11211

# Number of seconds memcached server is considered dead before it is tried
# again. This is used by the key value store system (e.g. token pooled
# memcached persistence backend). (integer value)
#dead_retry = 300

# Timeout in seconds for every call to a server. This is used by the key value
# store system (e.g. token pooled memcached persistence backend). (integer
# value)
#socket_timeout = 3

# Max total number of open connections to every memcached server. This is used
# by the key value store system (e.g. token pooled memcached persistence
# backend). (integer value)
#pool_maxsize = 10

# Number of seconds a connection to memcached is held unused in the pool before
# it is closed. This is used by the key value store system (e.g. token pooled
# memcached persistence backend). (integer value)
#pool_unused_timeout = 60

# Number of seconds that an operation will wait to get a memcache client
# connection. This is used by the key value store system (e.g. token pooled
# memcached persistence backend). (integer value)
#pool_connection_get_timeout = 10


[oauth1]

#
# From keystone
#

# Entrypoint for hte OAuth backend driver in the keystone.oauth1 namespace.
# (string value)
#driver = sql

# Duration (in seconds) for the OAuth Request Token. (integer value)
#request_token_duration = 28800

# Duration (in seconds) for the OAuth Access Token. (integer value)
#access_token_duration = 86400


[os_inherit]

#
# From keystone
#

# role-assignment inheritance to projects from owning domain or from projects
# higher in the hierarchy can be optionally enabled. (boolean value)
#enabled = false


[oslo_messaging_amqp]

#
# From oslo.messaging
#

# address prefix used when sending to a specific server (string value)
# Deprecated group/name - [amqp1]/server_request_prefix
#server_request_prefix = exclusive

# address prefix used when broadcasting to all servers (string value)
# Deprecated group/name - [amqp1]/broadcast_prefix
#broadcast_prefix = broadcast

# address prefix when sending to any server in group (string value)
# Deprecated group/name - [amqp1]/group_request_prefix
#group_request_prefix = unicast

# Name for the AMQP container (string value)
# Deprecated group/name - [amqp1]/container_name
#container_name = <None>

# Timeout for inactive connections (in seconds) (integer value)
# Deprecated group/name - [amqp1]/idle_timeout
#idle_timeout = 0

# Debug: dump AMQP frames to stdout (boolean value)
# Deprecated group/name - [amqp1]/trace
#trace = false

# CA certificate PEM file to verify server certificate (string value)
# Deprecated group/name - [amqp1]/ssl_ca_file
#ssl_ca_file =

# Identifying certificate PEM file to present to clients (string value)
# Deprecated group/name - [amqp1]/ssl_cert_file
#ssl_cert_file =

# Private key PEM file used to sign cert_file certificate (string value)
# Deprecated group/name - [amqp1]/ssl_key_file
#ssl_key_file =

# Password for decrypting ssl_key_file (if encrypted) (string value)
# Deprecated group/name - [amqp1]/ssl_key_password
#ssl_key_password = <None>

# Accept clients using either SSL or plain TCP (boolean value)
# Deprecated group/name - [amqp1]/allow_insecure_clients
#allow_insecure_clients = false


[oslo_messaging_qpid]

#
# From oslo.messaging
#

# Use durable queues in AMQP. (boolean value)
# Deprecated group/name - [DEFAULT]/amqp_durable_queues
# Deprecated group/name - [DEFAULT]/rabbit_durable_queues
#amqp_durable_queues = false

# Auto-delete queues in AMQP. (boolean value)
# Deprecated group/name - [DEFAULT]/amqp_auto_delete
#amqp_auto_delete = false

# Send a single AMQP reply to call message. The current behaviour since oslo-
# incubator is to send two AMQP replies - first one with the payload, a second
# one to ensure the other have finish to send the payload. We are going to
# remove it in the N release, but we must keep backward compatible at the same
# time. This option provides such compatibility - it defaults to False in
# Liberty and can be turned on for early adopters with a new installations or
# for testing. Please note, that this option will be removed in the Mitaka
# release. (boolean value)
#send_single_reply = false

# Qpid broker hostname. (string value)
# Deprecated group/name - [DEFAULT]/qpid_hostname
#qpid_hostname = localhost

# Qpid broker port. (integer value)
# Deprecated group/name - [DEFAULT]/qpid_port
#qpid_port = 5672

# Qpid HA cluster host:port pairs. (list value)
# Deprecated group/name - [DEFAULT]/qpid_hosts
#qpid_hosts = $qpid_hostname:$qpid_port

# Username for Qpid connection. (string value)
# Deprecated group/name - [DEFAULT]/qpid_username
#qpid_username =

# Password for Qpid connection. (string value)
# Deprecated group/name - [DEFAULT]/qpid_password
#qpid_password =

# Space separated list of SASL mechanisms to use for auth. (string value)
# Deprecated group/name - [DEFAULT]/qpid_sasl_mechanisms
#qpid_sasl_mechanisms =

# Seconds between connection keepalive heartbeats. (integer value)
# Deprecated group/name - [DEFAULT]/qpid_heartbeat
#qpid_heartbeat = 60

# Transport to use, either 'tcp' or 'ssl'. (string value)
# Deprecated group/name - [DEFAULT]/qpid_protocol
#qpid_protocol = tcp

# Whether to disable the Nagle algorithm. (boolean value)
# Deprecated group/name - [DEFAULT]/qpid_tcp_nodelay
#qpid_tcp_nodelay = true

# The number of prefetched messages held by receiver. (integer value)
# Deprecated group/name - [DEFAULT]/qpid_receiver_capacity
#qpid_receiver_capacity = 1

# The qpid topology version to use.  Version 1 is what was originally used by
# impl_qpid.  Version 2 includes some backwards-incompatible changes that allow
# broker federation to work.  Users should update to version 2 when they are
# able to take everything down, as it requires a clean break. (integer value)
# Deprecated group/name - [DEFAULT]/qpid_topology_version
#qpid_topology_version = 1


[oslo_messaging_rabbit]

#
# From oslo.messaging
#

# Use durable queues in AMQP. (boolean value)
# Deprecated group/name - [DEFAULT]/amqp_durable_queues
# Deprecated group/name - [DEFAULT]/rabbit_durable_queues
#amqp_durable_queues = false

# Auto-delete queues in AMQP. (boolean value)
# Deprecated group/name - [DEFAULT]/amqp_auto_delete
#amqp_auto_delete = false

# Send a single AMQP reply to call message. The current behaviour since oslo-
# incubator is to send two AMQP replies - first one with the payload, a second
# one to ensure the other have finish to send the payload. We are going to
# remove it in the N release, but we must keep backward compatible at the same
# time. This option provides such compatibility - it defaults to False in
# Liberty and can be turned on for early adopters with a new installations or
# for testing. Please note, that this option will be removed in the Mitaka
# release. (boolean value)
#send_single_reply = false

# SSL version to use (valid only if SSL enabled). Valid values are TLSv1 and
# SSLv23. SSLv2, SSLv3, TLSv1_1, and TLSv1_2 may be available on some
# distributions. (string value)
# Deprecated group/name - [DEFAULT]/kombu_ssl_version
#kombu_ssl_version =

# SSL key file (valid only if SSL enabled). (string value)
# Deprecated group/name - [DEFAULT]/kombu_ssl_keyfile
#kombu_ssl_keyfile =

# SSL cert file (valid only if SSL enabled). (string value)
# Deprecated group/name - [DEFAULT]/kombu_ssl_certfile
#kombu_ssl_certfile =

# SSL certification authority file (valid only if SSL enabled). (string value)
# Deprecated group/name - [DEFAULT]/kombu_ssl_ca_certs
#kombu_ssl_ca_certs =

# How long to wait before reconnecting in response to an AMQP consumer cancel
# notification. (floating point value)
# Deprecated group/name - [DEFAULT]/kombu_reconnect_delay
#kombu_reconnect_delay = 1.0

# How long to wait before considering a reconnect attempt to have failed. This
# value should not be longer than rpc_response_timeout. (integer value)
#kombu_reconnect_timeout = 60

# The RabbitMQ broker address where a single node is used. (string value)
# Deprecated group/name - [DEFAULT]/rabbit_host
#rabbit_host = localhost

# The RabbitMQ broker port where a single node is used. (integer value)
# Deprecated group/name - [DEFAULT]/rabbit_port
#rabbit_port = 5672

# RabbitMQ HA cluster host:port pairs. (list value)
# Deprecated group/name - [DEFAULT]/rabbit_hosts
#rabbit_hosts = $rabbit_host:$rabbit_port

# Connect over SSL for RabbitMQ. (boolean value)
# Deprecated group/name - [DEFAULT]/rabbit_use_ssl
#rabbit_use_ssl = false

# The RabbitMQ userid. (string value)
# Deprecated group/name - [DEFAULT]/rabbit_userid
#rabbit_userid = guest

# The RabbitMQ password. (string value)
# Deprecated group/name - [DEFAULT]/rabbit_password
#rabbit_password = guest

# The RabbitMQ login method. (string value)
# Deprecated group/name - [DEFAULT]/rabbit_login_method
#rabbit_login_method = AMQPLAIN

# The RabbitMQ virtual host. (string value)
# Deprecated group/name - [DEFAULT]/rabbit_virtual_host
#rabbit_virtual_host = /

# How frequently to retry connecting with RabbitMQ. (integer value)
#rabbit_retry_interval = 1

# How long to backoff for between retries when connecting to RabbitMQ. (integer
# value)
# Deprecated group/name - [DEFAULT]/rabbit_retry_backoff
#rabbit_retry_backoff = 2

# Maximum number of RabbitMQ connection retries. Default is 0 (infinite retry
# count). (integer value)
# Deprecated group/name - [DEFAULT]/rabbit_max_retries
#rabbit_max_retries = 0

# Use HA queues in RabbitMQ (x-ha-policy: all). If you change this option, you
# must wipe the RabbitMQ database. (boolean value)
# Deprecated group/name - [DEFAULT]/rabbit_ha_queues
#rabbit_ha_queues = false

# Number of seconds after which the Rabbit broker is considered down if
# heartbeat's keep-alive fails (0 disable the heartbeat). EXPERIMENTAL (integer
# value)
#heartbeat_timeout_threshold = 60

# How often times during the heartbeat_timeout_threshold we check the
# heartbeat. (integer value)
#heartbeat_rate = 2

# Deprecated, use rpc_backend=kombu+memory or rpc_backend=fake (boolean value)
# Deprecated group/name - [DEFAULT]/fake_rabbit
#fake_rabbit = false


[oslo_middleware]

#
# From oslo.middleware
#

# The maximum body size for each  request, in bytes. (integer value)
# Deprecated group/name - [DEFAULT]/osapi_max_request_body_size
# Deprecated group/name - [DEFAULT]/max_request_body_size
#max_request_body_size = 114688

#
# From oslo.middleware
#

# The HTTP Header that will be used to determine what the original request
# protocol scheme was, even if it was hidden by an SSL termination proxy.
# (string value)
#secure_proxy_ssl_header = X-Forwarded-Proto


[oslo_policy]

#
# From oslo.policy
#

# The JSON file that defines policies. (string value)
# Deprecated group/name - [DEFAULT]/policy_file
#policy_file = policy.json

# Default rule. Enforced when a requested rule is not found. (string value)
# Deprecated group/name - [DEFAULT]/policy_default_rule
#policy_default_rule = default

# Directories where policy configuration files are stored. They can be relative
# to any directory in the search path defined by the config_dir option, or
# absolute paths. The file defined by policy_file must exist for these
# directories to be searched.  Missing or empty directories are ignored. (multi
# valued)
# Deprecated group/name - [DEFAULT]/policy_dirs
# This option is deprecated for removal.
# Its value may be silently ignored in the future.
#policy_dirs = policy.d


[paste_deploy]

#
# From keystone
#

# Name of the paste configuration file that defines the available pipelines.
# (string value)
#config_file = keystone-paste.ini


[policy]

#
# From keystone
#

# Entrypoint for the policy backend driver in the keystone.policy namespace.
# Supplied drivers are rules and sql. (string value)
#driver = sql

# Maximum number of entities that will be returned in a policy collection.
# (integer value)
#list_limit = <None>


[resource]

#
# From keystone
#

# Entrypoint for the resource backend driver in the keystone.resource
# namespace. Supplied drivers are ldap and sql. If a resource driver is not
# specified, the assignment driver will choose the resource driver. (string
# value)
#driver = <None>

# Toggle for resource caching. This has no effect unless global caching is
# enabled. (boolean value)
# Deprecated group/name - [assignment]/caching
#caching = true

# TTL (in seconds) to cache resource data. This has no effect unless global
# caching is enabled. (integer value)
# Deprecated group/name - [assignment]/cache_time
#cache_time = <None>

# Maximum number of entities that will be returned in a resource collection.
# (integer value)
# Deprecated group/name - [assignment]/list_limit
#list_limit = <None>


[revoke]

#
# From keystone
#

# Entrypoint for an implementation of the backend for persisting revocation
# events in the keystone.revoke namespace. Supplied drivers are kvs and sql.
# (string value)
driver = sql

# This value (calculated in seconds) is added to token expiration before a
# revocation event may be removed from the backend. (integer value)
#expiration_buffer = 1800

# Toggle for revocation event caching. This has no effect unless global caching
# is enabled. (boolean value)
#caching = true

# Time to cache the revocation list and the revocation events (in seconds).
# This has no effect unless global and token caching are enabled. (integer
# value)
# Deprecated group/name - [token]/revocation_cache_time
#cache_time = 3600


[role]

#
# From keystone
#

# Entrypoint for the role backend driver in the keystone.role namespace.
# Supplied drivers are ldap and sql. (string value)
#driver = <None>

# Toggle for role caching. This has no effect unless global caching is enabled.
# (boolean value)
#caching = true

# TTL (in seconds) to cache role data. This has no effect unless global caching
# is enabled. (integer value)
#cache_time = <None>

# Maximum number of entities that will be returned in a role collection.
# (integer value)
#list_limit = <None>


[saml]

#
# From keystone
#

# Default TTL, in seconds, for any generated SAML assertion created by
# Keystone. (integer value)
#assertion_expiration_time = 3600

# Binary to be called for XML signing. Install the appropriate package, specify
# absolute path or adjust your PATH environment variable if the binary cannot
# be found. (string value)
#xmlsec1_binary = xmlsec1

# Path of the certfile for SAML signing. For non-production environments, you
# may be interested in using `keystone-manage pki_setup` to generate self-
# signed certificates. Note, the path cannot contain a comma. (string value)
#certfile = /etc/keystone/ssl/certs/signing_cert.pem

# Path of the keyfile for SAML signing. Note, the path cannot contain a comma.
# (string value)
#keyfile = /etc/keystone/ssl/private/signing_key.pem

# Entity ID value for unique Identity Provider identification. Usually FQDN is
# set with a suffix. A value is required to generate IDP Metadata. For example:
# https://keystone.example.com/v3/OS-FEDERATION/saml2/idp (string value)
#idp_entity_id = <None>

# Identity Provider Single-Sign-On service value, required in the Identity
# Provider's metadata. A value is required to generate IDP Metadata. For
# example: https://keystone.example.com/v3/OS-FEDERATION/saml2/sso (string
# value)
#idp_sso_endpoint = <None>

# Language used by the organization. (string value)
#idp_lang = en

# Organization name the installation belongs to. (string value)
#idp_organization_name = <None>

# Organization name to be displayed. (string value)
#idp_organization_display_name = <None>

# URL of the organization. (string value)
#idp_organization_url = <None>

# Company of contact person. (string value)
#idp_contact_company = <None>

# Given name of contact person (string value)
#idp_contact_name = <None>

# Surname of contact person. (string value)
#idp_contact_surname = <None>

# Email address of contact person. (string value)
#idp_contact_email = <None>

# Telephone number of contact person. (string value)
#idp_contact_telephone = <None>

# The contact type describing the main point of contact for the identity
# provider. (string value)
# Allowed values: technical, support, administrative, billing, other
#idp_contact_type = other

# Path to the Identity Provider Metadata file. This file should be generated
# with the keystone-manage saml_idp_metadata command. (string value)
#idp_metadata_path = /etc/keystone/saml2_idp_metadata.xml

# The prefix to use for the RelayState SAML attribute, used when generating ECP
# wrapped assertions. (string value)
#relay_state_prefix = ss:mem:


[signing]

#
# From keystone
#

# Path of the certfile for token signing. For non-production environments, you
# may be interested in using `keystone-manage pki_setup` to generate self-
# signed certificates. (string value)
#certfile = /etc/keystone/ssl/certs/signing_cert.pem

# Path of the keyfile for token signing. (string value)
#keyfile = /etc/keystone/ssl/private/signing_key.pem

# Path of the CA for token signing. (string value)
#ca_certs = /etc/keystone/ssl/certs/ca.pem

# Path of the CA key for token signing. (string value)
#ca_key = /etc/keystone/ssl/private/cakey.pem

# Key size (in bits) for token signing cert (auto generated certificate).
# (integer value)
# Minimum value: 1024
#key_size = 2048

# Days the token signing cert is valid for (auto generated certificate).
# (integer value)
#valid_days = 3650

# Certificate subject (auto generated certificate) for token signing. (string
# value)
#cert_subject = /C=US/ST=Unset/L=Unset/O=Unset/CN=www.example.com


[ssl]

#
# From keystone
#

# Path of the CA key file for SSL. (string value)
#ca_key = /etc/keystone/ssl/private/cakey.pem

# SSL key length (in bits) (auto generated certificate). (integer value)
# Minimum value: 1024
#key_size = 1024

# Days the certificate is valid for once signed (auto generated certificate).
# (integer value)
#valid_days = 3650

# SSL certificate subject (auto generated certificate). (string value)
#cert_subject = /C=US/ST=Unset/L=Unset/O=Unset/CN=localhost


[token]

#
# From keystone
#

# External auth mechanisms that should add bind information to token, e.g.,
# kerberos,x509. (list value)
#bind =

# Enforcement policy on tokens presented to Keystone with bind information. One
# of disabled, permissive, strict, required or a specifically required bind
# mode, e.g., kerberos or x509 to require binding to that authentication.
# (string value)
#enforce_token_bind = permissive

# Amount of time a token should remain valid (in seconds). (integer value)
#expiration = 3600

# Controls the token construction, validation, and revocation operations.
# Entrypoint in the keystone.token.provider namespace. Core providers are
# [fernet|pkiz|pki|uuid]. (string value)
provider = uuid

# Entrypoint for the token persistence backend driver in the
# keystone.token.persistence namespace. Supplied drivers are kvs, memcache,
# memcache_pool, and sql. (string value)
driver = memcache

# Toggle for token system caching. This has no effect unless global caching is
# enabled. (boolean value)
#caching = true

# Time to cache tokens (in seconds). This has no effect unless global and token
# caching are enabled. (integer value)
#cache_time = <None>

# Revoke token by token identifier. Setting revoke_by_id to true enables
# various forms of enumerating tokens, e.g. `list tokens for user`. These
# enumerations are processed to determine the list of tokens to revoke. Only
# disable if you are switching to using the Revoke extension with a backend
# other than KVS, which stores events in memory. (boolean value)
#revoke_by_id = true

# Allow rescoping of scoped token. Setting allow_rescoped_scoped_token to false
# prevents a user from exchanging a scoped token for any other token. (boolean
# value)
#allow_rescope_scoped_token = true

# The hash algorithm to use for PKI tokens. This can be set to any algorithm
# that hashlib supports. WARNING: Before changing this value, the auth_token
# middleware must be configured with the hash_algorithms, otherwise token
# revocation will not be processed correctly. (string value)
#hash_algorithm = md5


[tokenless_auth]

#
# From keystone
#

# The list of trusted issuers to further filter the certificates that are
# allowed to participate in the X.509 tokenless authorization. If the option is
# absent then no certificates will be allowed. The naming format for the
# attributes of a Distinguished Name(DN) must be separated by a comma and
# contain no spaces. This configuration option may be repeated for multiple
# values. For example: trusted_issuer=CN=john,OU=keystone,O=openstack
# trusted_issuer=CN=mary,OU=eng,O=abc (multi valued)
#trusted_issuer =

# The protocol name for the X.509 tokenless authorization along with the option
# issuer_attribute below can look up its corresponding mapping. (string value)
#protocol = x509

# The issuer attribute that is served as an IdP ID for the X.509 tokenless
# authorization along with the protocol to look up its corresponding mapping.
# It is the environment variable in the WSGI environment that references to the
# issuer of the client certificate. (string value)
#issuer_attribute = SSL_CLIENT_I_DN


[trust]

#
# From keystone
#

# Delegation and impersonation features can be optionally disabled. (boolean
# value)
#enabled = true

# Enable redelegation feature. (boolean value)
#allow_redelegation = false

# Maximum depth of trust redelegation. (integer value)
#max_redelegation_count = 3

# Entrypoint for the trust backend driver in the keystone.trust namespace.
# (string value)
#driver = sql

[extra_headers]
Distribution = Ubuntu

"""


conf_wsgi_keystone_conf = """Listen 5000
Listen 35357

<VirtualHost *:5000>
    WSGIDaemonProcess keystone-public processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-public
    WSGIScriptAlias / /usr/bin/keystone-wsgi-public
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>
    ErrorLog /var/log/apache2/keystone.log
    CustomLog /var/log/apache2/keystone_access.log combined

    <Directory /usr/bin>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
    </Directory>
</VirtualHost>

<VirtualHost *:35357>
    WSGIDaemonProcess keystone-admin processes=5 threads=1 user=keystone group=keystone display-name=%{GROUP}
    WSGIProcessGroup keystone-admin
    WSGIScriptAlias / /usr/bin/keystone-wsgi-admin
    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    <IfVersion >= 2.4>
      ErrorLogFormat "%{cu}t %M"
    </IfVersion>
    ErrorLog /var/log/apache2/keystone.log
    CustomLog /var/log/apache2/keystone_access.log combined

    <Directory /usr/bin>
        <IfVersion >= 2.4>
            Require all granted
        </IfVersion>
        <IfVersion < 2.4>
            Order allow,deny
            Allow from all
        </IfVersion>
    </Directory>
</VirtualHost>
"""

conf_keystone_paste_ini = """
# Keystone PasteDeploy configuration file.

[filter:debug]
use = egg:keystone#debug

[filter:request_id]
use = egg:keystone#request_id

[filter:build_auth_context]
use = egg:keystone#build_auth_context

[filter:token_auth]
use = egg:keystone#token_auth

[filter:admin_token_auth]
use = egg:keystone#admin_token_auth

[filter:json_body]
use = egg:keystone#json_body

[filter:user_crud_extension]
use = egg:keystone#user_crud_extension

[filter:crud_extension]
use = egg:keystone#crud_extension

[filter:ec2_extension]
use = egg:keystone#ec2_extension

[filter:ec2_extension_v3]
use = egg:keystone#ec2_extension_v3

[filter:federation_extension]
use = egg:keystone#federation_extension

[filter:oauth1_extension]
use = egg:keystone#oauth1_extension

[filter:s3_extension]
use = egg:keystone#s3_extension

[filter:endpoint_filter_extension]
use = egg:keystone#endpoint_filter_extension

[filter:simple_cert_extension]
use = egg:keystone#simple_cert_extension

[filter:revoke_extension]
use = egg:keystone#revoke_extension

[filter:url_normalize]
use = egg:keystone#url_normalize

[filter:sizelimit]
use = egg:keystone#sizelimit

[app:public_service]
use = egg:keystone#public_service

[app:service_v3]
use = egg:keystone#service_v3

[app:admin_service]
use = egg:keystone#admin_service

[pipeline:public_api]
# The last item in this pipeline must be public_service or an equivalent
# application. It cannot be a filter.
pipeline = sizelimit url_normalize request_id build_auth_context token_auth json_body ec2_extension user_crud_extension public_service

[pipeline:admin_api]
# The last item in this pipeline must be admin_service or an equivalent
# application. It cannot be a filter.
pipeline = sizelimit url_normalize request_id build_auth_context token_auth json_body ec2_extension s3_extension crud_extension admin_service

[pipeline:api_v3]
# The last item in this pipeline must be service_v3 or an equivalent
# application. It cannot be a filter.
pipeline = sizelimit url_normalize request_id build_auth_context token_auth json_body ec2_extension_v3 s3_extension simple_cert_extension revoke_extension federation_extension oauth1_extension endpoint_filter_extension service_v3

[app:public_version_service]
use = egg:keystone#public_version_service

[app:admin_version_service]
use = egg:keystone#admin_version_service

[pipeline:public_version_api]
pipeline = sizelimit url_normalize public_version_service

[pipeline:admin_version_api]
pipeline = sizelimit url_normalize admin_version_service

[composite:main]
use = egg:Paste#urlmap
/v2.0 = public_api
/v3 = api_v3
/ = public_version_api

[composite:admin]
use = egg:Paste#urlmap
/v2.0 = admin_api
/v3 = api_v3
/ = admin_version_api
"""

class Keystone(object):
    def __init__(self, user, hosts=None, parallel=True):
        self.user = user
        self.hosts = hosts
        self.parallel = parallel
        env.user = self.user
        env.hosts = self.hosts
        env.parallel = self.parallel

    @serial
    def _create_keystone_db(self, root_db_pass, keystone_db_pass):
        sudo("mysql -uroot -p{root_db_pass} -e \"CREATE DATABASE keystone;\"".format(root_db_pass=root_db_pass), shell=False)
        sudo("mysql -uroot -p{root_db_pass} -e \"GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY '{keystone_db_pass}';\"".format(root_db_pass=root_db_pass, 
                                                                                                                                                            keystone_db_pass=keystone_db_pass), shell=False)
        sudo("mysql -uroot -p{root_db_pass} -e \"GRANT ALL PRIVILEGES ON keystone.* TO 'keystone\'@\'%\' IDENTIFIED BY \'{keystone_db_pass}';\"".format(root_db_pass=root_db_pass, 
                                                                                                                                                        keystone_db_pass=keystone_db_pass), shell=False)
    def _install_keystone(self, admin_token, connection, memcache_servers):
        # Disable the keystone service from starting automatically after installation
        sudo('echo "manual" > /etc/init/keystone.override')
        
        sudo("apt-get update")
        sudo("apt-get install keystone apache2 libapache2-mod-wsgi memcached python-memcache -y")

        # Configure /etc/keysone/keystone.conf
        with open('tmp_keystone_conf','w') as f:
            f.write(conf_keystone_conf)
        files.upload_template(filename='tmp_keystone_conf',
                              destination='/etc/keystone/keystone.conf',
                              context={'admin_token': admin_token,
                              'connection': connection,
                              'memcache_servers': memcache_servers,},
                              use_jinja=True,
                              use_sudo=True)
        os.remove('tmp_keystone_conf')

        # Populate the Identity service database
        if args.populate:
            sudo('su -s /bin/sh -c "keystone-manage db_sync" keystone', shell=False)

        # Configure /etc/apache2/sites-available/wsgi-keystone.conf
        with open('tmp_wsgi_keystone_conf', 'w') as f:
            f.write(conf_wsgi_keystone_conf)
        files.upload_template(filename='tmp_wsgi_keystone_conf',
                              destination='/etc/apache2/sites-available/wsgi-keystone.conf',
                              use_sudo=True)
        os.remove('tmp_wsgi_keystone_conf')

        # Enable the Identity service virtual hosts
        sudo('ln -s /etc/apache2/sites-available/wsgi-keystone.conf /etc/apache2/sites-enabled')

        # Add ServerName to apache configuration
        files.append('/etc/apache2/apache2.conf', 'ServerName localhost', use_sudo=True)
        # Restart the Apache HTTP server
        sudo('service apache2 restart')
        
        # Remove the SQLite database file
        sudo('rm -f /var/lib/keystone/keystone.db')

    # Create the service entity and API endpoints
    def _create_entity_and_endpoint(self, os_token, os_url, public_endpoint, internal_endpoint, admin_endpoint):
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} service create --name keystone --description "OpenStack Identity" identity'.format(os_token=os_token, 
                                                                                                                                                   os_url=os_url))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} endpoint create --region RegionOne identity public {public_endpoint}'.format(os_token=os_token, 
                                                                                                                             os_url=os_url, 
                                                                                                                             public_endpoint=public_endpoint))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} endpoint create --region RegionOne identity internal {internal_endpoint}'.format(os_token=os_token, 
                                                                                                                                 os_url=os_url, 
                                                                                                                                 internal_endpoint=internal_endpoint))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} endpoint create --region RegionOne identity admin {admin_endpoint}'.format(os_token=os_token, 
                                                                                                                           os_url=os_url, 
        
                                                                                                                       admin_endpoint=admin_endpoint))

    # Create projects, users, and roles
    def _create_projects_users_roles(self, os_token, os_url, admin_pass, demo_pass):
        # For admin
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} project create --domain default --description "Admin Project" admin'.format(os_token=os_token,
                                                                                                    os_url=os_url))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} user create --domain default --password {admin_pass} admin'.format(os_token=os_token,
                                                                                                    os_url=os_url,
                                                                                                    admin_pass=admin_pass))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} role create admin'.format(os_token=os_token,
                                                                                                                      os_url=os_url))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} role add --project admin --user admin admin'.format(os_token=os_token,
                                                                                                                                                os_url=os_url))

        # For service
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} project create --domain default --description "Service Project" service'.format(os_token=os_token,
                                                                                                                                                                            os_url=os_url))
        # For demo
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} project create --domain default --description "Demo Project" demo'.format(os_token=os_token,
                                                                                                                                                                      os_url=os_url))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} user create --domain default --password {demo_pass} demo'.format(os_token=os_token,
                                                                                                                                                             os_url=os_url,
                                                                                                                                                             demo_pass=demo_pass))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} role create user'.format(os_token=os_token,
                                                                                                                     os_url=os_url))
        sudo('openstack --os-identity-api-version 3 --os-token {os_token} --os-url {os_url} role add --project demo --user demo user'.format(os_token=os_token,
                                                                                                                                             os_url=os_url))

    def _update_keystone_paste_ini(self):
        """remove admin_token_auth from the [pipeline:public_api], 
        [pipeline:admin_api], and [pipeline:api_v3] sections"""
        with open('tmp_keystone_paste_ini', 'w') as f:
            f.write(conf_keystone_paste_ini)
        files.upload_template(filename='tmp_keystone_paste_ini',
                              destination='/etc/keystone/keystone-paste.ini',
                              use_sudo=True)
        os.remove('tmp_keystone_paste_ini')


def main():
    target = Keystone(user=args.user, hosts=args.hosts.split(','))
    if args.subparser_name == 'create-keystone-db':
        execute(target._create_keystone_db, 
                args.root_db_pass, 
                args.keystone_db_pass)
    if args.subparser_name == 'install':
        execute(target._install_keystone, 
                args.admin_token, 
                args.connection, 
                args.memcache_servers)
    if args.subparser_name == 'create-entity-and-endpoint':
        execute(target._create_entity_and_endpoint, 
                args.os_token,
                args.os_url,
                args.public_endpoint,
                args.internal_endpoint,
                args.admin_endpoint)
    if args.subparser_name == 'create-projects-users-roles':
        execute(target._create_projects_users_roles,
                args.os_token,
                args.os_url,
                args.admin_pass,
                args.demo_pass)
        execute(target._update_keystone_paste_ini)

if __name__ == '__main__':
    main()