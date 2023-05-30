
logger.debug('Generating ChangeCurrentVnfPkgRequest message for ETSI SOL003 v2.4.1');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = {};
message.vimConnectionInfo = [ // info of the target cluster where CNF is to be deployed
      {
         vimType: executionRequest.properties.vimType,
         vimId: executionRequest.properties.vim_id
      }
   ];
message.additionalParams = {};   
message.additionalParams['nfType'] = executionRequest.properties.nfType;
message.additionalParams['envType'] = executionRequest.properties.envType;
message.additionalParams.customValues= {
         "cnfPackageVersionFile": executionRequest.properties.cnfPackageVersionFile,
         "cnfName": executionRequest.properties.cucp_cnfname,
         "profiles.mav_cucp_dev.charts[0].chart_key": executionRequest.properties.cucp_chartkey,
      }
message["flavourId"] = executionRequest.properties.flavourId;
message["vnfdId"] = executionRequest.properties.vnfdId;
// Set the standard message properties
// The flavourId is required, the other fields are optional
for (var key in executionRequest.getProperties()) {
    if (key.startsWith('additionalParams.') || key.startsWith('vimConnectionInfo.') ) {
         print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}
logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);