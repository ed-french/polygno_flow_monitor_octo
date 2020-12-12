$(function() {
    function polygnoflowmonitorViewModel(parameters) {
        var self = this;
        self.pfm_actual=ko.observable();
        self.pfm_intended=ko.observable();
        self.pfm_extrusion_ratio=ko.observable();
        self.pfm_status=ko.observable();
        
        self.settings = parameters[0];

        // this will hold the URL currently displayed by the iframe
        self.currentUrl = ko.observable();

        // this will hold the URL entered in the text field
        self.newUrl = ko.observable();

        // this will be called when the user clicks the "Go" button and set the iframe's URL to
        // the entered URL
        self.goToUrl = function() {
            self.currentUrl(self.newUrl());
        };

        // This will get called before the HelloWorldViewModel gets bound to the DOM, but after its
        // dependencies have already been initialized. It is especially guaranteed that this method
        // gets called _after_ the settings have been retrieved from the OctoPrint backend and thus
        // the SettingsViewModel been properly populated.
        self.onBeforeBinding = function() {
            self.newUrl(self.settings.settings.plugins.polygnoflowmonitor.url());
            self.goToUrl();
        }



        self.onDataUpdaterPluginMessage = function(plugin, data) {
            if (plugin != "polygnoflowmonitor") {
                return;
            }
            console.log("UI has received update message from plugin");
            console.log(data);
            /* Example: actual: 331692
                        alarm_state: 1
                        controller_id: "ec4b661c5210"
                        intended: 333657
                        print_name: "2020-12-12 10:26 [honest_desire]"
                        status: "waiting"*/
            var ALARM_LEVELS=["ERROR","OK","WARN","HALT"];

            var alarm_words=ALARM_LEVELS[data.alarm_state];
            var status=data.status+" "+alarm_words;
            self.pfm_status(status);
            self.pfm_intended((data.intended/256.0).toFixed(2));
            self.pfm_actual((data.actual/256.0).toFixed(2));
            self.pfm_extrusion_ratio((100*data.actual/data.intended).toFixed(1));
            console.log("Finished updating ko observabes...");

        };
    }

    // This is how our plugin registers itself with the application, by adding some configuration
    // information to the global variable OCTOPRINT_VIEWMODELS
    OCTOPRINT_VIEWMODELS.push([
        // This is the constructor to call for instantiating the plugin
        polygnoflowmonitorViewModel,

        // This is a list of dependencies to inject into the plugin, the order which you request
        // here is the order in which the dependencies will be injected into your view model upon
        // instantiation via the parameters argument
        ["settingsViewModel"],

        // Finally, this is the list of selectors for all elements we want this view model to be bound to.
        ["#tab_plugin_polygnoflowmonitor","#sidebar_plugin_polygnoflowmonitor"]
    ]);
});