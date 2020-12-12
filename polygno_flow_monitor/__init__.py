# coding=utf-8
from __future__ import absolute_import,unicode_literals

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin, requests, time,threading


class polygno_ProgressTracker(threading.Thread):

    def __init__(self,plugin):
        self.plugin=plugin # parent plugin - allows access to it's state
        threading.Thread.__init__(self)
        self.isDaemon()
        self.running=False
    
    def shutdown(self):
        self.plugin._logger.info("Shut down of polygno thread requested")
        self.running=False

    def run(self):
        """
            Main execution loop
        """
        self.running=True
        while self.running:
            url=self.plugin._settings.get(["url"])

            if url=="...":
                self.plugin._logger.info("URL not set for FlowMonitor")
            else:
                if not url[-1]=="/":
                    url+="/"
                try:
                    res=requests.get(url+"status")
                except Exception as e:
                    self.plugin._logger.error("Failed to fetch status")
                    self.plugin._logger.error(str(e))
                else:
                    if not res.status_code==200:
                        self.plugin._logger.error("Unexpected return status code : %s" % res.status_code)
                    else:
                        self.plugin._logger.info("Succeeded getting status")
                        status=res.json()
                        self.plugin._logger.info(str(status))
                        self.plugin._plugin_manager.send_plugin_message("polygnoflowmonitor",status)
                        """ Example (units are 1/256th mm):

                        actual: 331692
                        alarm_state: 1
                        controller_id: "ec4b661c5210"
                        intended: 333657
                        print_name: "2020-12-12 10:26 [honest_desire]"
                        status: "waiting"
                        """

            time.sleep(5)

        self.plugin._logger.info("polygno thread loop ended")



class polygnoflowmonitorPlugin(octoprint.plugin.StartupPlugin,
                       octoprint.plugin.TemplatePlugin,
                       octoprint.plugin.SettingsPlugin,
                       octoprint.plugin.AssetPlugin,
                       octoprint.plugin.ShutdownPlugin):
    def __init__(self,*args,**kwargs):
        super(polygnoflowmonitorPlugin,self).__init__(*args,**kwargs)
        # Create the threadable monitor
        self.tracker=polygno_ProgressTracker(self)
        
        

   
    def on_after_startup(self):
        self._logger.info("Polygno Flow Monitor now starting with URL currently set to: %s" % self._settings.get(["url"]))
        self.tracker.start()


    def get_settings_defaults(self):
        return dict(url="...")

    def get_template_configs(self):
        return [
            dict(type="sidebar",custom_bindings=False),
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ] # 
    def get_assets(self):
        return dict(
            js=["js/polygnoflowmonitor.js"]
            )

    def on_settings_save(self,data):
        # Settings saved so try and update the graph
        # TBD
        return

    def on_shutdown(self):
        self._logger.debug("Shutdown has been received by the plugin")
        self.tracker.shutdown()
        self._logger.debug("Shutdown has been passed to the thread, now waiting on join...")
        self.tracker.join()
        self._logger.debug("Polygno Flow Monitor Plugin shutdown done")

__plugin_name__ = "Polygno Flow Monitor"
__plugin_pythoncompat__ = ">=2.7,<4"
__plugin_implementation__ = polygnoflowmonitorPlugin()