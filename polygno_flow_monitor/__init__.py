# coding=utf-8
from __future__ import absolute_import,unicode_literals

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
class polygnoflowmonitorPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin):#
    def on_after_startup(self):
        self._logger.info("Hello fongleblasters! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(url="...")

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ] # 
    def get_assets(self):
        return dict(
            js=["js/polygnoflowmonitor.js"]
            )

__plugin_name__ = "Polygno Flow Monitor"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = polygnoflowmonitorPlugin()