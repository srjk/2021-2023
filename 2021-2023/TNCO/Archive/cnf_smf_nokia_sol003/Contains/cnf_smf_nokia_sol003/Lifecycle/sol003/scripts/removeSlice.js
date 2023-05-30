/*
 This is the generic message creation logic for InstantiateVnfRequest messages based on the 2.4.1 version of the ETSI SOL003 specification
 */
logger.debug('Generating addSliceConfig message for ETSI SOL003 v2.4.1');
load('classpath:scripts/lib.js');

// Create the message object to be returned
var message = {vnfConfigurableProperties: {}, metadata: {}, extensions: {}, vimConnectionInfo: []};

// Set the standard message properties
// The flavourId is required, the other fields are optional
setPropertyIfNotNull(executionRequest.properties, message, 'vnfInstanceName');
setPropertyIfNotNull(executionRequest.properties, message, 'vnfInstanceDescription');
setPropertyIfNotNull(executionRequest.properties, message, 'vnfPkgId');
setPropertyIfNotNull(executionRequest.properties, message.vnfConfigurableProperties, 'slice_config_param1');
setPropertyIfNotNull(executionRequest.properties, message.vnfConfigurableProperties, 'slice_config_param2');
setPropertyIfNotNull(executionRequest.properties, message.vnfConfigurableProperties, 'slice_config_param3');

for (var key in executionRequest.getProperties()) {
    if (key.startsWith('vnfConfigurableProperties.') || key.startsWith('metadata.') || key.startsWith('extensions.') || key.startsWith('vimConnectionInfo.')) {
        // print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}

//vnfConfigurableProperties
// message.vnfConfigurableProperties = {};
// message.vnfConfigurableProperties['slice_config_param1'] = executionRequest.properties.slice_config_param1';
// message.vnfConfigurableProperties['slice_config_param2'] = executionRequest.properties.slice_config_param2';
// message.vnfConfigurableProperties['slice_config_param3'] = executionRequest.properties.slice_config_param3';

logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);