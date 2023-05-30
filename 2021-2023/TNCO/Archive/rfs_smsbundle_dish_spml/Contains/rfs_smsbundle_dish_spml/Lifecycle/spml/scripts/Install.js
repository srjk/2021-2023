logger.debug('Generating Modification requst message for prov gateway');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = { modifications: []};
// spliting request service variable based on comma and assigned to a array 
var array = executionRequest.properties.requestedServices.split(',');


// iteration on every value of array to perform task
array.forEach(function (item, index) {
    logger.info("item----------"+item);
    //  append xml part of SMS in modification
    if(item.match(/^SMS$/)){
      logger.info("item for DATA----------"+item);
      message.modifications.push(

        {
            "path": executionRequest.properties.path1,
            "operation": executionRequest.properties.operation5,
            "valueObject": {
                "msisdn": executionRequest.properties.GPSI
            }
        },
        {
            "path": executionRequest.properties.path2,
            "operation": executionRequest.properties.operation5,
            "valueObject": {
                "msisdn": executionRequest.properties.GPSI
            }
        },
        {
            "path": executionRequest.properties.path3,
            "operation": executionRequest.properties.operation5,
            "valueObject": {
                "basicServiceGroup": executionRequest.properties.basicServiceGroup,
                "status": executionRequest.properties.status
            }
        },
        {
            "path": executionRequest.properties.path15,
            "operation": executionRequest.properties.operation3,
            "valueObject": {
                "osb1": executionRequest.properties.osb1
            }
        },
        {
            "path": executionRequest.properties.path4,
            "operation": executionRequest.properties.operation3,
            "valueObject": {
                "refPriorityListName": executionRequest.properties.refPriorityListName
            }
        },
        {
            "path": executionRequest.properties.path5,
            "operation": executionRequest.properties.operation5,
            "valueObject": {
                "globalFilterId": executionRequest.properties.globalFilterId
            }
        },
        {
            "path": executionRequest.properties.path5,
            "operation": executionRequest.properties.operation5,
            "valueObject": {
                "globalFilterId": executionRequest.properties.globalFilterId1
            }
        },
         {
            "path": executionRequest.properties.path16,
            "operation": executionRequest.properties.operation5,
            "valueObject": {
                "smsSubscribed": executionRequest.properties.smsSubscribed
            }
        },
        {
            "path": executionRequest.properties.path6,
            "operation": executionRequest.properties.operation5,
            "valueObject": {
                "mtSmsSubscribed": executionRequest.properties.smsSubscribed,
                "mtSmsBarringAll": executionRequest.properties.mtSmsBarringAll,
                "mtSmsBarringRoaming": executionRequest.properties.mtSmsBarringRoaming,
                "moSmsSubscribed": executionRequest.properties.moSmsSubscribed,
                "moSmsBarringAll": executionRequest.properties.moSmsBarringAll,
                "moSmsbarringRoaming": executionRequest.properties.moSmsbarringRoaming
            }
        }


      )
    };
    // appending SMS_ROAM XML part to modification array 
    if(item.match(/^SMS_ROAM$/)){
        logger.info("item for DATA----------"+item);
        message.modifications.push(
  
            {
                "path": executionRequest.properties.path3,
                "operation": executionRequest.properties.operation1,
                "valueObject": {
                    "basicServiceGroup": executionRequest.properties.basicServiceGroup,
                    "status": executionRequest.properties.status1
                }
            },
            {
                "path": executionRequest.properties.hlr_path,
                "operation": executionRequest.properties.operation1,
                "valueObject": {
                    "osb1": executionRequest.properties.osb12
                }
            },
            {
                "path": executionRequest.properties.udm_path1,
                "operation": executionRequest.properties.operation2,
                "valueObject": {
                    "mtSmsBarringRoaming": "false"
                }
            },
            {
                "path": executionRequest.properties.udm_path2,
                "operation": executionRequest.properties.operation2,
                "valueObject": {
                    "moSmsbarringRoaming": "false"
                }
            }
        )
      };
     // appending MMS xml to modification array 
      if(item.match(/^MMS$/)){
        logger.info("item for DATA----------"+item);
        message.modifications.push(
  
            {
                "operation": executionRequest.properties.operation5,
                "path": executionRequest.properties.path7,
                "valueObject": {
                    "apn": executionRequest.properties.dnn7,
                    "contextId": executionRequest.properties.contextId,
                    "type": executionRequest.properties.ntype,
                    "pdnGwDynamicAllocation": executionRequest.properties.pdnGwDynamicAllocation,
                    "vplmnAddressAllowed": executionRequest.properties.vplmnAddressAllowed,
                    "maxBandwidthUp": executionRequest.properties.dnn7_sessionAmbr.split('|')[0].split(' ')[0],
                    "maxBandwidthDown": executionRequest.properties.dnn7_sessionAmbr.split('|')[1].split(' ')[0],
                    "qos": executionRequest.properties.qos,
                    "pdnChargingCharacteristics": {
                        "chargingCharacteristicsProfile": executionRequest.properties.chargingCharacteristicsProfile,
                        "chargingCharacteristicsBehavior": executionRequest.properties.chargingCharacteristicsBehavior
                    },
                    "eps5gInterworkIndicator": executionRequest.properties.eps5gInterworkIndicator
                }
            },
             {
                "operation": executionRequest.properties.operation5,
                "path": executionRequest.properties.path8,
                "valueObject": {
                    "dnnId": executionRequest.properties.dnn7,
                    "defaultIndication": executionRequest.properties.defaultIndication,
                    "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
                    "localBrkOutRoamingAllowed": executionRequest.properties.localBrkOutRoamingAllowed
                }
            },
            {
                "operation": executionRequest.properties.operation5,
                "path": executionRequest.properties.path9,
                "valueObject": {
                    "dnnId": executionRequest.properties.dnn7,
                    "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
                    "sessionAmbr": executionRequest.properties.dnn7_sessionAmbr,
                    "udm5gQosProfile": {
                        "udm5Qi": executionRequest.properties.udm5Qi,
                        "arp": executionRequest.properties.arp,
                        "priorityLevel": executionRequest.properties.priorityLevel
                    },
                    "pduSessionTypes": {
                        "defaultSessionType": executionRequest.properties.defaultSessionType,
                        "allowedSessionType": [
                            executionRequest.properties.allowedSessionType
                        ]
                    },
                    "sscModes": {
                        "defaultSscMode": executionRequest.properties.defaultSscMode,
                        "allowedSscMode": [
                            executionRequest.properties.allowedSscMode
                        ]
                    }
                }
            },
            {
            "operation": executionRequest.properties.operation5,
            "path": executionRequest.properties.path10,
            "valueObject": {
                "dnn": executionRequest.properties.dnn7,
                "subscCats": [
                    executionRequest.properties.subscCats1,
                    executionRequest.properties.subscCats2
                ],
                "subscSpendingLimits": executionRequest.properties.subscSpendingLimits,
                "online": executionRequest.properties.online
            }
       }
        )
      };
    
    });
// message.modifications = 
// [
// 				{
//                     "path": executionRequest.properties.path1,
//                     "operation": executionRequest.properties.operation5,
//                     "valueObject": {
//                         "msisdn": executionRequest.properties.GPSI
//                     }
//                 },
//                 {
//                     "path": executionRequest.properties.path2,
//                     "operation": executionRequest.properties.operation5,
//                     "valueObject": {
//                         "msisdn": executionRequest.properties.GPSI
//                     }
//                 },
//                 {
//                     "path": executionRequest.properties.path3,
//                     "operation": executionRequest.properties.operation5,
//                     "valueObject": {
//                         "basicServiceGroup": executionRequest.properties.basicServiceGroup,
//                         "status": executionRequest.properties.status
//                     }
//                 },
//                 {
//                     "path": executionRequest.properties.path15,
//                     "operation": executionRequest.properties.operation3,
//                     "valueObject": {
//                         "osb1": executionRequest.properties.osb1
//                     }
//                 },
//                 {
//                     "path": executionRequest.properties.path4,
//                     "operation": executionRequest.properties.operation3,
//                     "valueObject": {
//                         "refPriorityListName": executionRequest.properties.refPriorityListName
//                     }
//                 },
// 				{
//                     "path": executionRequest.properties.path5,
//                     "operation": executionRequest.properties.operation5,
//                     "valueObject": {
//                         "globalFilterId": executionRequest.properties.globalFilterId
//                     }
//                 },
//                 {
//                     "path": executionRequest.properties.path5,
//                     "operation": executionRequest.properties.operation5,
//                     "valueObject": {
//                         "globalFilterId": executionRequest.properties.globalFilterId1
//                     }
//                 },
// 				 {
//                     "path": executionRequest.properties.path16,
//                     "operation": executionRequest.properties.operation5,
//                     "valueObject": {
//                         "smsSubscribed": executionRequest.properties.smsSubscribed
//                     }
//                 },
//                 {
//                     "path": executionRequest.properties.path6,
//                     "operation": executionRequest.properties.operation5,
//                     "valueObject": {
//                         "mtSmsSubscribed": executionRequest.properties.smsSubscribed,
//                         "mtSmsBarringAll": executionRequest.properties.mtSmsBarringAll,
//                         "mtSmsBarringRoaming": executionRequest.properties.mtSmsBarringRoaming,
//                         "moSmsSubscribed": executionRequest.properties.moSmsSubscribed,
//                         "moSmsBarringAll": executionRequest.properties.moSmsBarringAll,
//                         "moSmsbarringRoaming": executionRequest.properties.moSmsbarringRoaming
//                     }
//                 },#sms
// 				{
//                     "path": executionRequest.properties.path3,
//                     "operation": executionRequest.properties.operation1,
//                     "valueObject": {
//                         "basicServiceGroup": executionRequest.properties.basicServiceGroup,
//                         "status": executionRequest.properties.status1
//                     }
//                 },
//                 {
//                     "path": executionRequest.properties.hlr_path,
//                     "operation": executionRequest.properties.operation1,
//                     "valueObject": {
//                         "osb1": executionRequest.properties.osb12
//                     }
//                 },
// 				{
//                     "path": executionRequest.properties.udm_path1,
//                     "operation": executionRequest.properties.operation2,
//                     "valueObject": {
//                         "mtSmsBarringRoaming": "false"
//                     }
//                 },
//                 {
//                     "path": executionRequest.properties.udm_path2,
//                     "operation": executionRequest.properties.operation2,
//                     "valueObject": {
//                         "moSmsbarringRoaming": "false"
//                     }
//                 },#sms_roam
// 				{
//                     "operation": executionRequest.properties.operation5,
//                     "path": executionRequest.properties.path7,
//                     "valueObject": {
//                         "apn": executionRequest.properties.dnn7,
//                         "contextId": executionRequest.properties.contextId,
//                         "type": executionRequest.properties.ntype,
//                         "pdnGwDynamicAllocation": executionRequest.properties.pdnGwDynamicAllocation,
//                         "vplmnAddressAllowed": executionRequest.properties.vplmnAddressAllowed,
//                         "maxBandwidthUp": executionRequest.properties.maxBandwidthUp,
//                         "maxBandwidthDown": executionRequest.properties.maxBandwidthDown,
//                         "qos": executionRequest.properties.qos,
//                         "pdnChargingCharacteristics": {
//                             "chargingCharacteristicsProfile": executionRequest.properties.chargingCharacteristicsProfile,
//                             "chargingCharacteristicsBehavior": executionRequest.properties.chargingCharacteristicsBehavior
//                         },
//                         "eps5gInterworkIndicator": executionRequest.properties.eps5gInterworkIndicator
//                     }
//                 },
// 				 {
//                     "operation": executionRequest.properties.operation5,
//                     "path": executionRequest.properties.path8,
//                     "valueObject": {
//                         "dnnId": executionRequest.properties.dnn7,
//                         "defaultIndication": executionRequest.properties.defaultIndication,
//                         "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
//                         "localBrkOutRoamingAllowed": executionRequest.properties.localBrkOutRoamingAllowed
//                     }
//                 },
//                 {
//                     "operation": executionRequest.properties.operation5,
//                     "path": executionRequest.properties.path9,
//                     "valueObject": {
//                         "dnnId": executionRequest.properties.dnn7,
//                         "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
//                         "sessionAmbr": executionRequest.properties.dnn7_sessionAmbr,
//                         "udm5gQosProfile": {
//                             "udm5Qi": executionRequest.properties.udm5Qi,
//                             "arp": executionRequest.properties.arp,
//                             "priorityLevel": executionRequest.properties.priorityLevel
//                         },
//                         "pduSessionTypes": {
//                             "defaultSessionType": executionRequest.properties.defaultSessionType,
//                             "allowedSessionType": [
//                                 executionRequest.properties.allowedSessionType
//                             ]
//                         },
//                         "sscModes": {
//                             "defaultSscMode": executionRequest.properties.defaultSscMode,
//                             "allowedSscMode": [
//                                 executionRequest.properties.allowedSscMode
//                             ]
//                         }
//                     }
//                 },
// 				{
//                 "operation": executionRequest.properties.operation5,
//                 "path": executionRequest.properties.path10,
//                 "valueObject": {
//                     "dnn": executionRequest.properties.dnn7,
//                     "subscCats": [
//                         executionRequest.properties.subscCats1,
//                         executionRequest.properties.subscCats2
//                     ],
//                     "subscSpendingLimits": executionRequest.properties.subscSpendingLimits,
//                     "online": executionRequest.properties.online
//                 }
// }#mms
// ];
message["loopbackMode"] = "false";
message["requestId"] = executionRequest.properties.extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = executionRequest.properties.ObjectClass;
message["targetVersion"] = "SDL_MULTIAPPSUBSCRIBER_v10";
for (var key in executionRequest.getProperties()) {
    if (key.startsWith('additionalParams.') || key.startsWith('extVirtualLinks.') || key.startsWith('extManagedVirtualLinks.') || key.startsWith('modifications.') ) {
         print('Got property [' + key + '], value = [' + executionRequest.properties[key] + ']');
        addProperty(message, key, executionRequest.properties[key]);
    }
}
logger.debug('Message generated successfully');
// Turn the message object into a JSON string to be returned back to the Java driver
JSON.stringify(message);