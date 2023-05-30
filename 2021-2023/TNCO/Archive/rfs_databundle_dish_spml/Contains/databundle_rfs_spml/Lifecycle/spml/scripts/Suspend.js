logger.debug('Generating Modification requst message for prov gateway');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = { modifications: []};
// spliting request service variable based on comma and assigned to a array
var array = executionRequest.properties.requestedServices.split(',');
// iteration on every value of array to perform task
array.forEach(function (item, index) {
    logger.info("item----------"+item);
     // appending DATA XML  in modification array
    if(item.match(/^DATA$/)){
      logger.info("item for DATA----------"+item);
      message.modifications.push({
         "path": executionRequest.properties.hlr_path1,
         "operation": executionRequest.properties.operation2,
         "valueObject":{
            "odbgprs": executionRequest.properties.hlr_odbgprs
         }
      },
      {
         "path": executionRequest.properties.hlr_path2,
         "operation": executionRequest.properties.operation2,
         "valueObject":{
            "defaultPdnContextId": executionRequest.properties.hlr_defaultPdnContextId
         }
      },
      {
         "path": executionRequest.properties.hlr_path3,
         "operation": executionRequest.properties.operation1,
         "valueObject":{
            "flagAPNBlockedOverS6A": executionRequest.properties.hlr_flagAPNBlockedOverS6A,
            "flagAPNBlockedOverSWx": executionRequest.properties.hlr_flagAPNBlockedOverSWx
         }
      },
	  {
         "path": "udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId='"+executionRequest.properties.dnn5+"']",
         "operation": executionRequest.properties.operation2,
         "valueObject":{
            "defaultIndication": executionRequest.properties.dnn5_defaultIndication1
         }
      },
      {
         "path":"udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId='"+executionRequest.properties.dnn4+"']",
         "operation": executionRequest.properties.operation2,
         "valueObject":{
            "defaultIndication": executionRequest.properties.dnn4_defaultIndication1
         }
      },
      {
         "path":"udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId='"+executionRequest.properties.dnn4+"']/dnnBarred='true'",
         "operation": executionRequest.properties.operation3,
         "valueObject":{
            "dnnBarred": executionRequest.properties.dnn4_dnnBarred
         }
      }
      
      )};
       // appending HOTSPOT XML  in modification array
      if(item.match(/^HOTSPOT$/)){
         logger.info("item for HOTSPOT----------"+item);
         message.modifications.push({
            "path": executionRequest.properties.hlr_path4,
            "operation": executionRequest.properties.operation1,
            "valueObject":{
               "flagAPNBlockedOverS6A": executionRequest.properties.hlr_flagAPNBlockedOverS6A,
               "flagAPNBlockedOverSWx": executionRequest.properties.hlr_flagAPNBlockedOverSWx
            }
         },
        {
            "path":"udm5gData/servingPlmnId/provisionedData/smfSelectionSubscriptionData/sNssaiInfo/dnnInfo[@dnnId='"+executionRequest.properties.dnn6+"']/dnnBarred='true'",
            "operation": executionRequest.properties.operation3,
            "valueObject":{
               "dnnBarred": executionRequest.properties.dnn6_dnnBarred
            }
         }
         
         )};

   });
message["requestId"] = executionRequest.properties.extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = executionRequest.properties.objectClass;
message["targetVersion"] = executionRequest.properties.targetVersion;
message["loopbackMode"] = "false";
// Whilst not specifically present in the 2.4.1 version of the specification, we will add an
// additionalParams block here since all other request messages feature this.
for (var key in executionRequest.getProperties()) {
    if (key.startsWith('additionalParams.') || key.startsWith('extVirtualLinks.') || key.startsWith('extManagedVirtualLinks.') || key.startsWith('modifications.') ) {
         print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}
logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);
