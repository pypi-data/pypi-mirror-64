default_framework_conf = """
{
    "properties": {
        "pelix.log.level": "INFO"
    },
    "bundles": [
        "pelix.ipopo.core",
        "pelix.services.configadmin",
        "pelix.shell.core",
        "pelix.shell.ipopo",
        "pelix.shell.configadmin",
        "pelix.shell.remote",
        "pelix.http.basic"
    ],
    "components": [
    {
      "factory": "pelix.http.service.basic.factory",
      "name": "httpd",
      "properties": {
        "pelix.http.address": "127.0.0.1"
        "pelix.http.port": "9000"
      }
    },
    {
      "factory": "ipopo-remote-shell-factory",
      "name": "remote-shell",
      "properties": {
         "pelix.shell.port": "9999"
         "pelix.shell.address": "127.0.0.1"
      }
    }
  ]
}
"""

empty_extra_bundles_conf = """
{
    "bundles": [

    ]
}
"""
