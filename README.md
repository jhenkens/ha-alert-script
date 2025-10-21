# ha-alert-script
Copied from Home Assistant's Alert integration, but added data-templating and script calling. Using this as an interim until blueprints are updated to better re-create alert, and alert is deprecated. See https://github.com/home-assistant/home-assistant.io/pull/28930

## Features
- All features from the original Home Assistant Alert integration
- Data templating support for notifications
- Script calling on alert events
- **NEW**: `unique_id` support for better entity management

## Configuration

```yaml
alert_script:
  my_alert:
    name: "My Alert"
    entity_id: sensor.my_sensor
    state: "on"
    repeat: [5, 10, 30]  # minutes
    unique_id: "my_unique_alert_id"  # Optional: Set a unique ID for this alert
    notifiers:
      - mobile_app_my_phone
    message: "Alert: {{ states('sensor.my_sensor') }}"
    data:
      priority: high
    script: my_alert_script
    variables:
      sensor_name: "{{ state_attr('sensor.my_sensor', 'friendly_name') }}"
```

The `unique_id` parameter is optional and allows you to:
- Better manage entities in the Home Assistant UI
- Ensure entity persistence across configuration changes
- Enable proper entity registry management