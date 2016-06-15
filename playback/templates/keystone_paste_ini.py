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