
logger.debug('Generating InstantiateVnfRequest message for ETSI SOL003 v2.4.1');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = {vnfConfigurableProperties: {}, vimConnectionInfo: [], additionalParams: {}};
message.vimConnectionInfo = [ // info of the target cluster where CNF is to be deployed
      {
         vimType: executionRequest.properties.vimType,
         vimId: executionRequest.properties.vimId
      }
   ];   
message.additionalParams = {
     envType: executionRequest.properties.envType,
     nfType: executionRequest.properties.nfType,
     "custom_values":"nrfv1_customfile.yaml"
   };
message.vnfConfigurableProperties = {
        "config_param1": "value1",
        "config_param2": "value2"
}
// Set the standard message properties
// The flavourId is required, the other fields are optional
setPropertyIfNotNull(executionRequest.properties, message, 'vnfdId');
for (var key in executionRequest.getProperties()) {
    if (key.startsWith('additionalParams.') || key.startsWith('vimConnectionInfo.') ) {
         print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}
logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);