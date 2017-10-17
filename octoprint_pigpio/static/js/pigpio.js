$(function() {
  /** @const */
  var PLUGIN_ID = 'pigpio';

  function PiGpioViewModel(parameters) {
    var self = this;

    self.uiData = {};
    //
    self.isRpi = ko.observable();
    self.navbarWidgetTitle = ko.observable();
    self.navbarWidgetText = ko.observable();

    self.onBeforeBinding = function() {
      self.settings = parameters[0].settings.plugins[PLUGIN_ID];
    };

    self.onAfterBinding = function() {
      $.ajax('/api/plugin/' + PLUGIN_ID, {
        'type': 'POST',
        'contentType': 'application/json',
        'data': JSON.stringify({'command': 'init_ui'})
      });
    };

    self.onDataUpdaterPluginMessage = function(plugin, message) {
      if (plugin !== PLUGIN_ID) {
        return;
      }

      switch (message['type']) {
        case 'ui_data':
          self.uiData = message;
          self.isRpi(message['is_rpi']);
          self.navbarWidgetTitle(message['navbar_widget_title']);
          self.navbarWidgetText(message['navbar_widget'] !== '' ? '…' : '');
          break;
        case 'sensor_data':
          var navbarWidget = self.uiData['navbar_widget'];
          self.navbarWidgetText(navbarWidget !== '' ?
              message['sensor_data'][navbarWidget] || '…' :
              '');
          break;
      }
    };
  }

  OCTOPRINT_VIEWMODELS.push({
    'construct': PiGpioViewModel,
    'dependencies': ['settingsViewModel'],
    'elements': ['#navbar_plugin_' + PLUGIN_ID, '#settings_plugin_' + PLUGIN_ID]
  });
});
