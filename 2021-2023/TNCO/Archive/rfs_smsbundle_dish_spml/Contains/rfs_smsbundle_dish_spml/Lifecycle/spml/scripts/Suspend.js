logger.debug('Generating Modification requst message for prov gateway');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = { modifications: []};
// spliting request service variable based on comma and assigned to a array
var array = executionRequest.properties.requestedServices.split(',');
// iteration on every value of array to perform task 
array.forEach(function (item, index) {
    logger.info("item----------"+item);
     // appending SMS XML  in modification array
    if(item.match(/^SMS$/)){
      logger.info("item for SMS----------"+item);
      message.modifications.push(
        {
            "path": executionRequest.properties.path11,
            "operation": executionRequest.properties.operation5,
            "valueObject": {
                "basicServiceGroup": executionRequest.properties.basicServiceGroup,
                "status": executionRequest.properties.status
            }
        },
        {
            "path": executionRequest.properties.path16,
            "operation": executionRequest.properties.operation1,
            "valueObject": {
                "smsSubscribed": executionRequest.properties.smsSubscribed1
            }
        }

      )
    };
     // appending MMS XML  in modification array
    if(item.match(/^MMS$/)){
        logger.info("item for MMS----------"+item);
        message.modifications.push(
            {
                "path": executionRequest.properties.path12,
                "operation": executionRequest.properties.operation1,
                "valueObject": {
                    "flagAPNBlockedOverS6A": executionRequest.properties.flagAPNBlockedOverS6A,
                    "flagAPNBlockedOverSWx": executionRequest.properties.flagAPNBlockedOverSWx
                }
            },
			{
                "path": "udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId='"+executionRequest.properties.dnn7+"']/dnnBarred='true'",
                "operation": executionRequest.properties.operation3,
                 "valueObject": {
                   "dnnBarred":executionRequest.properties.dnnBarred
                }
			}
          
        )
      };
});
// message.modifications = 
// [
//         {
//                 "path": executionRequest.properties.path11,
//                 "operation": executionRequest.properties.operation5,
//                 "valueObject": {
//                     "basicServiceGroup": executionRequest.properties.basicServiceGroup,
//                     "status": executionRequest.properties.status1
//                 }
//             },
// 			{
//                 "path": executionRequest.properties.path16,
//                 "operation": executionRequest.properties.operation1,
//                 "valueObject": {
//                     "smsSubscribed": executionRequest.properties.smsSubscribed1
//                 }
//             }, /*#sms*/
// 			{
//                 "path": executionRequest.properties.path12,
//                 "operation": executionRequest.properties.operation1,
//                 "valueObject": {
//                     "flagAPNBlockedOverS6A": executionRequest.properties.flagAPNBlockedOverS6A,
//                     "flagAPNBlockedOverSWx": executionRequest.properties.flagAPNBlockedOverSWx
//                 }
//             },
// 			{
//                 "path": "udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId='"+executionRequest.properties.dnn7+"']/dnnBarred='true'",
//                 "operation": executionRequest.properties.operation3,
//                  "valueObject": {
//                    "dnnBarred":executionRequest.properties.dnnBarred
//                 }
// 			}/*#mms*/
// ];
message["requestId"] = executionRequest.properties.extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = executionRequest.properties.ObjectClass;
message["targetVersion"] = "SDL_MULTIAPPSUBSCRIBER_v10";
message["loopbackMode"] = "false";
for (var key in executionRequest.getProperties()) {
    if (key.startsWith('additionalParams.') || key.startsWith('extVirtualLinks.') || key.startsWith('extManagedVirtualLinks.') || key.startsWith('modifications.') ) {
         print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}
logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);
