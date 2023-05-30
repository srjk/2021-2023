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
        "operation": executionRequest.properties.operation5,
        "valueObject": {
            "ntype": executionRequest.properties.ntype,
            "mobileSubscriberType": executionRequest.properties.mobileSubscriberType,
            "umtsSubscriber": {
                "accTypeGSM": executionRequest.properties.umtsSubscriber_accTypeGSM,
                "accTypeGERAN": executionRequest.properties.umtsSubscriber_accTypeGERAN,
                "accTypeUTRAN": executionRequest.properties.umtsSubscriber_accTypeUTRAN
            },
            "ts11": [
                {
                    "msisdn": executionRequest.properties.GPSI
                }
            ],
            "gprs": [
                {
                    "msisdn": ""
                }
            ],
            "pdpContext": [
                {
                    "id": executionRequest.properties.pdpContext_1_id,
                    "qosProfile": executionRequest.properties.pdpContext_1_qosProfile,
                    "refPdpContextName": executionRequest.properties.pdpContext_1_refPdpContextName
                },
                {
                    "id": executionRequest.properties.pdpContext_2_id,
                    "qosProfile": executionRequest.properties.pdpContext_2_qosProfile,
                    "refPdpContextName": executionRequest.properties.pdpContext_2_refPdpContextName
                }
            ],
            "roamSubscription": {
                "roamSubscriptionInfo": executionRequest.properties.roamSubscriptionInfo
            },
            "eps": {
                "defaultPdnContextId": executionRequest.properties.eps_defaultPdnContextId,
                "maxBandwidthUp": executionRequest.properties.dnn4_sessionAmbr.split('|')[0].split(' ')[0],
                "maxBandwidthDown": executionRequest.properties.dnn4_sessionAmbr.split('|')[1].split(' ')[0],
                "accessAPNEnabled": executionRequest.properties.eps_accessAPNEnabled,
                "msisdn": executionRequest.properties.GPSI,
                "subscribedForSMSInMME": executionRequest.properties.eps_subscribedForSMSInMME,
                "eps5GSmsDeliveryMode": executionRequest.properties.eps_eps5GSmsDeliveryMode
            },
            "epsPdnContext": [
                {
                    "apn": executionRequest.properties.dnn4,
                    "contextId": executionRequest.properties.dnn4_contextId,
                    "type": executionRequest.properties.dnn4_type,
                    "pdnGwDynamicAllocation": executionRequest.properties.dnn4_pdnGwDynamicAllocation,
                    "vplmnAddressAllowed": executionRequest.properties.dnn4_vplmnAddressAllowed,
                    "maxBandwidthUp": executionRequest.properties.dnn4_sessionAmbr.split('|')[0].split(' ')[0],
                    "maxBandwidthDown": executionRequest.properties.dnn4_sessionAmbr.split('|')[1].split(' ')[0],
                    "qos": executionRequest.properties.dnn4_qos,
                    "pdnChargingCharacteristics": {
                        "chargingCharacteristicsProfile": executionRequest.properties.dnn4_chargingCharacteristicsProfile,
                        "chargingCharacteristicsBehavior": executionRequest.properties.dnn4_chargingCharacteristicsBehavior
                    },
                    "eps5gInterworkIndicator": executionRequest.properties.dnn4_eps5gInterworkIndicator
                },
                {
                    "apn": executionRequest.properties.dnn5,
                    "contextId": executionRequest.properties.dnn5_contextId,
                    "type": executionRequest.properties.dnn5_type,
                    "pdnGwDynamicAllocation": executionRequest.properties.dnn5_pdnGwDynamicAllocation,
                    "vplmnAddressAllowed": executionRequest.properties.dnn5_vplmnAddressAllowed,
                    "maxBandwidthUp": executionRequest.properties.dnn5_sessionAmbr.split('|')[0].split(' ')[0],
                    "maxBandwidthDown": executionRequest.properties.dnn5_sessionAmbr.split('|')[1].split(' ')[0],
                    "qos": executionRequest.properties.dnn5_qos,
                    "pdnChargingCharacteristics": {
                        "chargingCharacteristicsProfile": executionRequest.properties.dnn5_chargingCharacteristicsProfile,
                        "chargingCharacteristicsBehavior": executionRequest.properties.dnn5_chargingCharacteristicsBehavior
                    },
                    "eps5gInterworkIndicator": executionRequest.properties.dnn5_eps5gInterworkIndicator
                }
            ],
            "epsRoamAreaName": executionRequest.properties.hlr_epsRoamAreaName
        }
    },
    {
        "path": "udm",
        "operation": executionRequest.properties.operation1,
        "valueObject": {
            "udmImsi": [
                executionRequest.properties.SUPI
            ],
            "udmMsisdn": [
                executionRequest.properties.GPSI 
            ],
            "authenticationData": {
                "authenticationMethod": executionRequest.properties.authenticationmethod
            },
            "servingPlmnId": [
                {
                    "plmnId": executionRequest.properties.plmnId,
                    "homePlmnIdIndication": executionRequest.properties.homePlmnIdIndication,
                    "provisionedData": {
                        "accessAndMobilitySubscriptionData": {
                            "genPublicSubscriptionIds": [
                               "msisdn-"+executionRequest.properties.GPSI
                            ],
                            "rfspIndex": executionRequest.properties.udm_rfspIndex,
                            "subsRegTimer": executionRequest.properties.udm_subsRegTimer,
                            "ueUsageType": executionRequest.properties.udm_ueUsageType,
                            "localAreaDataNtwInfo": [
                                executionRequest.properties.localAreaDataNtwInfo
                            ],
                            "mpsPriority": executionRequest.properties.udm_mpsPriority,
                            "activeTime": executionRequest.properties.udm_activeTime,
                            "downLinkPktCount": executionRequest.properties.udm_downLinkPktCount,
                            "nssai": {
                                "defaultSingleNssais": [
                                    "1-ABCDEF"
                                ]
                            },
                            "ueAmbr": {
                                "ueAmbrUpLink": executionRequest.properties.UEAMBRUplink+" bps",
                                "ueAmbrDownLink": executionRequest.properties.UEAMBRDownlink+" bps"
                            }
                        },
                        "smfSelectionSubscriptionData": {
                            "sNssaiInfo": [
                                {
                                    "nssaiId": executionRequest.properties.slice_nssai,
                                    "dnnInfo": [
                                        {
                                            "dnnId": executionRequest.properties.dnn4,
                                            "defaultIndication": executionRequest.properties.dnn4_defaultIndication,
                                            "interworkingEPSIndication": executionRequest.properties.dnn4_interworkingEPSIndication,
                                            "localBrkOutRoamingAllowed": executionRequest.properties.dnn4_localBrkOutRoamingAllowed
                                        },
                                        {
                                            "dnnId": executionRequest.properties.dnn5,
                                            "defaultIndication": executionRequest.properties.dnn5_defaultIndication,
                                            "interworkingEPSIndication": executionRequest.properties.dnn5_interworkingEPSIndication,
                                            "localBrkOutRoamingAllowed": executionRequest.properties.dnn5_localBrkOutRoamingAllowed
                                        }
                                    ]
                                }
                            ]
                        },
                        "sessionManagementSubscriptionData": [
                            {
                                "singleNssai":executionRequest.properties.slice_nssai,
                                "dnnConfiguration": [
                                    {
                                        "dnnId": executionRequest.properties.dnn4,
                                        "pduSessionTypes": {
                                            "defaultSessionType": executionRequest.properties.dnn4_defaultSessionType,
                                            "allowedSessionType": [
                                                executionRequest.properties.dnn4_allowedSessionType
                                            ]
                                        },
                                        "sscModes": {
                                            "defaultSscMode": executionRequest.properties.dnn4_defaultSscMode,
                                            "allowedSscMode": [
                                                executionRequest.properties.dnn4_allowedSscMode
                                            ]
                                        },
                                        "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication4,
                                        "sessionAmbr": executionRequest.properties.dnn4_sessionAmbr,
                                        "udm5gQosProfile": {
                                            "udm5Qi": executionRequest.properties.dnn4_udm5Qi,
                                            "arp": executionRequest.properties.dnn4_arp,
                                            "priorityLevel": executionRequest.properties.dnn4_priorityLevel
                                        }
                                    },
                                    {
                                        "dnnId": executionRequest.properties.dnn5,
                                        "pduSessionTypes": {
                                            "defaultSessionType": executionRequest.properties.dnn5_defaultSessionType,
                                            "allowedSessionType": [
                                                executionRequest.properties.dnn5_allowedSessionType
                                            ]
                                        },
                                        "sscModes": {
                                            "defaultSscMode": executionRequest.properties.dnn5_defaultSscMode,
                                            "allowedSscMode": [
                                                executionRequest.properties.dnn5_allowedSscMode
                                            ]
                                        },
                                        "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication5,
                                        "sessionAmbr": executionRequest.properties.dnn5_sessionAmbr,
                                        "udm5gQosProfile": {
                                            "udm5Qi": executionRequest.properties.dnn5_udm5Qi,
                                            "arp": executionRequest.properties.dnn5_arp,
                                            "priorityLevel": executionRequest.properties.dnn5_priorityLevel
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                }
            ]
        }
    },
    {
        "path": "pcf",
        "operation": executionRequest.properties.operation1,
        "valueObject": {
            "policySubscriptionId": executionRequest.properties.pcf_policySubscriptionId,
            "imsi": [
                executionRequest.properties.SUPI
            ],
            "smPolicyData": {
                "smPolicySnssaiData": [
                    {
                        "snssai": {
                            "sst": executionRequest.properties.slice_sst,
                            "sd": executionRequest.properties.slice_sd
                        },
                        "smPolicyDnnData": [
                            {
                                "dnn": executionRequest.properties.dnn4,
                                "subscCats": [
                                    executionRequest.properties.subscCats1,
                                    executionRequest.properties.subscCats2
                                ],
                                "subscSpendingLimits": executionRequest.properties.pcf_dnn4_subscSpendingLimits,
                                "online": executionRequest.properties.pcf_dnn4_online
                            },
                            {
                                "dnn": executionRequest.properties.dnn5,
                                "subscCats": [
                                    executionRequest.properties.subscCats1,
                                    executionRequest.properties.subscCats2
                                ],
                                "subscSpendingLimits": executionRequest.properties.pcf_dnn5_subscSpendingLimits,
                                "online": executionRequest.properties.pcf_dnn5_online
                            }
                        ]
                    }
                ]
            },
            "amPolicyData": {
                "subscCats": [
                    "Platinum",
                    "Plan1"
                ]
            }
        }
    })
      
      };
   // appending DATA_ROAM XML  in modification array    
  if(item.match(/^DATA_ROAM$/)){
      logger.info("item for DATA ROAM----------"+item);
      message.modifications.push({
		"path": executionRequest.properties.hlr_path1,
		"operation": executionRequest.properties.operation2,
		"valueObject": {
			"epsRoamAreaName": executionRequest.properties.epsRoamAreaName
		}
	})
      
  };
   // appending HOTSPOT XML  in modification array
  if(item.match(/^HOTSPOT$/)){
      logger.info("item for hotspot----------"+item);
      message.modifications.push(  {
        "operation": executionRequest.properties.operation5,
        "path": executionRequest.properties.hlr_dnn6_path,
        "valueObject": {
            "apn": executionRequest.properties.dnn6,
            "contextId": executionRequest.properties.dnn6_contextId,
            "type": executionRequest.properties.dnn6_type,
            "pdnGwDynamicAllocation": executionRequest.properties.dnn6_pdnGwDynamicAllocation,
            "vplmnAddressAllowed": executionRequest.properties.dnn6_vplmnAddressAllowed,
            "maxBandwidthUp": executionRequest.properties.dnn6_sessionAmbr.split('|')[0].split(' ')[0],
            "maxBandwidthDown": executionRequest.properties.dnn6_sessionAmbr.split('|')[1].split(' ')[0],
            "qos": executionRequest.properties.dnn6_qos,
            "pdnChargingCharacteristics": {
                "chargingCharacteristicsProfile": executionRequest.properties.dnn6_chargingCharacteristicsProfile,
                "chargingCharacteristicsBehavior": executionRequest.properties.dnn6_chargingCharacteristicsBehavior
            },
            "eps5gInterworkIndicator": executionRequest.properties.dnn6_eps5gInterworkIndicator
        }
    },
    {
        "operation": executionRequest.properties.operation5,
        "path": executionRequest.properties.udm_path,
        "valueObject": {
            "dnnId": "hotspot",
            "defaultIndication": executionRequest.properties.udm_dnn6_defaultIndication,
            "interworkingEPSIndication": executionRequest.properties.udm_dnn6_interworkingEPSIndication,
            "localBrkOutRoamingAllowed": executionRequest.properties.udm_dnn6_localBrkOutRoamingAllowed
        }
    },
    {
        "operation": executionRequest.properties.operation5,
        "path": executionRequest.properties.udm_dnn6_path,
        "valueObject": {
            "dnnId": executionRequest.properties.dnn6,
            "interworkingEPSIndication": executionRequest.properties.udm_dnn6_interworkingEPSIndication1,
            "sessionAmbr": executionRequest.properties.dnn6_sessionAmbr,
            "udm5gQosProfile": {
                "udm5Qi": executionRequest.properties.udm_dnn6_udm5Qi,
                "arp": executionRequest.properties.udm_dnn6_arp,
                "priorityLevel": executionRequest.properties.udm_dnn6_priorityLevel
            },
            "pduSessionTypes": {
                "defaultSessionType": executionRequest.properties.dnn6_defaultSessionType,
                "allowedSessionType": [
                    executionRequest.properties.dnn6_allowedSessionType
                ]
            },
            "sscModes": {
                "defaultSscMode": executionRequest.properties.dnn6_defaultSscMode,
                "allowedSscMode": [
                    executionRequest.properties.dnn6_allowedSscMode
                ]
            }
        }
    },
    {
        "operation": executionRequest.properties.operation5,
        "path": executionRequest.properties.pcf_path,
        "valueObject": {
            "dnn": executionRequest.properties.dnn6,
            "subscCats": [
                executionRequest.properties.subscCats1,
                executionRequest.properties.subscCats2
            ],
            "subscSpendingLimits": executionRequest.properties.dnn6_subscSpendingLimits,
            "online": executionRequest.properties.dnn6_online
        }
    })
  };
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
