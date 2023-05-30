logger.debug('Generating Modification requst message for prov gateway');
load('classpath:scripts/lib.js');
// Create the message object to be returned
var message = { modifications: []};
message.modifications = 
[
        {
            "path": executionRequest.properties.hlr_path,
            "operation": executionRequest.properties.operation1,
            "valueObject": {
                "apn": executionRequest.properties.dnn1,
                "contextId": executionRequest.properties.dnn1_contextId,
                "type": executionRequest.properties.dnn1_type,
                "pdnGwDynamicAllocation": executionRequest.properties.dnn1_pdnGwDynamicAllocation,
                "vplmnAddressAllowed": executionRequest.properties.dnn1_vplmnAddressAllowed,
                "maxBandwidthUp": executionRequest.properties.dnn1_sessionAmbr.split('|')[0].split(' ')[0],
                "maxBandwidthDown": executionRequest.properties.dnn1_sessionAmbr.split('|')[1].split(' ')[0],
                "qos": executionRequest.properties.dnn1_qos,
                "pdnChargingCharacteristics": {
                    "chargingCharacteristicsProfile": executionRequest.properties.dnn1_pdnChargingCharacteristics_chargingCharacteristicsProfile,
                    "chargingCharacteristicsBehavior": executionRequest.properties.dnn1_pdnChargingCharacteristics_chargingCharacteristicsBehavior
                },
                "eps5gInterworkIndicator": executionRequest.properties.eps5gInterworkIndicator
            }
        },
        {
            "path": executionRequest.properties.hlr_path,
            "operation": executionRequest.properties.operation1,
            "valueObject": {
                "apn": executionRequest.properties.dnn2_apn,
                "contextId": executionRequest.properties.dnn2_contextId,
                "type": executionRequest.properties.dnn2_type,
                "pdnGwDynamicAllocation": executionRequest.properties.dnn2_pdnGwDynamicAllocation,
                "vplmnAddressAllowed": executionRequest.properties.dnn2_vplmnAddressAllowed,
                "maxBandwidthUp": executionRequest.properties.dnn2_sessionAmbr.split('|')[0].split(' ')[0],
                "maxBandwidthDown": executionRequest.properties.dnn2_sessionAmbr.split('|')[1].split(' ')[0],
                "qos": executionRequest.properties.dnn2_qos,
                "pdnChargingCharacteristics": {
                    "chargingCharacteristicsProfile": executionRequest.properties.dnn2_pdnChargingCharacteristics_chargingCharacteristicsProfile,
                    "chargingCharacteristicsBehavior": executionRequest.properties.dnn2_pdnChargingCharacteristics_chargingCharacteristicsProfile_chargingCharacteristicsBehavior
                },
                "eps5gInterworkIndicator": executionRequest.properties.eps5gInterworkIndicator
            }
        },
        {
            "path": executionRequest.properties.hlr_path,
            "operation": executionRequest.properties.operation1,
            "valueObject": {
                "apn": executionRequest.properties.dnn3_apn,
                "contextId": executionRequest.properties.dnn3_contextId,
                "type": executionRequest.properties.dnn3_type,
                "pdnGwDynamicAllocation": executionRequest.properties.dnn3_pdnGwDynamicAllocation,
                "vplmnAddressAllowed": executionRequest.properties.dnn3_vplmnAddressAllowed,
                "maxBandwidthUp": executionRequest.properties.dnn3_sessionAmbr.split('|')[0].split(' ')[0],
                "maxBandwidthDown": executionRequest.properties.dnn3_sessionAmbr.split('|')[1].split(' ')[0],
                "qos": executionRequest.properties.dnn3_qos,
                "pdnChargingCharacteristics": {
                    "chargingCharacteristicsProfile": executionRequest.properties.dnn3_pdnChargingCharacteristics_chargingCharacteristicsProfile,
                    "chargingCharacteristicsBehavior": executionRequest.properties.dnn3_pdnChargingCharacteristics_chargingCharacteristicsBehavio
                },
                "eps5gInterworkIndicator": executionRequest.properties.eps5gInterworkIndicator
            }
        },
        {
            "operation": executionRequest.properties.operation1,
			"path": executionRequest.properties.hss_path1,
            "valueObject": {
                "subscriptionId": executionRequest.properties.hss_subscriptionId,
                "profileType": executionRequest.properties.hss_profileType,
                "adminBlocked": executionRequest.properties.hss_adminBlocked,
                "defaultScscfRequired": executionRequest.properties.hss_defaultScscfRequired,
                "maximumPublicIds": executionRequest.properties.hss_maximumPublicIds,
                "privateUserId": [
                    {
                        "privateUserId": executionRequest.properties.SUPI+"@ims.mnc340.mcc313.3gppnetwork.org",
                        "provisionedImsi": [
                            {
                                "provisionedImsi": executionRequest.properties.SUPI
                            }
                        ],
                        "msisdn": executionRequest.properties.GPSI,
                        "preferredAuthenticationScheme": executionRequest.properties.preferredAuthenticationScheme,
                        "preferredDomain": executionRequest.properties.dnn1,
                        "refGussDataId": executionRequest.properties.refGussDataId,
                        "looseRoutingIndicationRequired": executionRequest.properties.looseRoutingIndicationRequired,
                        "digestRealm": executionRequest.properties.digestRealm
                    },
                    {
                        "privateUserId": executionRequest.properties.GPSI+"@ims.mnc340.mcc313.3gppnetwork.org",
                        "provisionedImsi": [
                            {
                                "provisionedImsi": executionRequest.properties.SUPI
                            }
                        ],
                        "msisdn": executionRequest.properties.GPSI,
                        "preferredAuthenticationScheme": executionRequest.properties.preferredAuthenticationScheme,
                        "preferredDomain": executionRequest.properties.dnn1,
                        "refGussDataId": executionRequest.properties.refGussDataId,
                        "looseRoutingIndicationRequired": executionRequest.properties.looseRoutingIndicationRequired,
                        "digestRealm": executionRequest.properties.digestRealm
                    }
                ],
                "implicitRegisteredSet": [
                    {
                        "irsId": executionRequest.properties.irsld
                    }
                ],
                "publicUserId": [
                    {
                        "originalPublicUserId": "sip:+"+executionRequest.properties.GPSI+"@ims.mnc340.mcc313.3gppnetwork.org",
                        "barringIndication": executionRequest.properties.barringIndication,
                        "defaultIndication": executionRequest.properties.defaultIndication,
                        "serviceProfileName": executionRequest.properties.serviceProfileName,
                        "irsId": executionRequest.properties.irsId
                    },
                    {
                        "originalPublicUserId": "sip:+"+executionRequest.properties.SUPI+"@ims.mnc340.mcc313.3gppnetwork.org",
                        "barringIndication": executionRequest.properties.barringIndication1,
                        "defaultIndication": executionRequest.properties.defaultIndication1,
                        "serviceProfileName": executionRequest.properties.serviceProfileName,
                        "irsId": executionRequest.properties.irsId
                    },
                    {
                        "originalPublicUserId": "tel:+"+executionRequest.properties.GPSI,
                        "barringIndication": executionRequest.properties.barringIndication,
                        "defaultIndication": executionRequest.properties.defaultIndication1,
                        "serviceProfileName": executionRequest.properties.serviceProfileName,
                        "irsId": executionRequest.properties.irsld
                    }
                ],
                "serviceProfile": [
                    {
                        "profileName": executionRequest.properties.profileName,
                        "mandatoryCapability": [
                            {
                                "mandatoryCapability": executionRequest.properties.mandatoryCapability
                            }
                        ],
                        "globalFilterId": [
                            {
                                "globalFilterId": executionRequest.properties.globalFilterId
                            },
                            {
                                "globalFilterId": executionRequest.properties.globalFilterId1
                            },
                            {
                                "globalFilterId": executionRequest.properties.globalFilterId2
                            },
                            {
                                "globalFilterId": executionRequest.properties.globalFilterId3
                            },
                            {
                                "globalFilterId": executionRequest.properties.globalFilterId4
                            },
                            {
                                "globalFilterId": executionRequest.properties.globalFilterId5
                            }
                        ],
                        "subscribedMediaProfileID": {
                            "sessionReleasePolicy": executionRequest.properties.sessionReleasePolicy,
                            "forkingPolicy": executionRequest.properties.forkingPolicy
                        }
                    }
                ],
                "gussData": [
                    {
                        "gussDataId": executionRequest.properties.gussDataId,
                        "uiccSecurityType": executionRequest.properties.uiccSecurityType,
                        "keyLifetime": executionRequest.properties.keyLifetime,
                        "ussData": [
                            {
                                "ussDataId": executionRequest.properties.ussDataId,
                                "gsId": executionRequest.properties.gsld,
                                "activeIndication": executionRequest.properties.activeIndication,
                                "ussType": executionRequest.properties.ussType,
                                "refNafGroupId": executionRequest.properties.refNafGroupId,
                                "keySelectionId": executionRequest.properties.keySelectionId,
                                "upiListItem": [
                                    {
                                        "upi": "sip:+"+executionRequest.properties.GPSI+"@ims.mnc340.mcc313.3gppnetwork.org"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.udm_path,
            "valueObject": {
                "dnnId": executionRequest.properties.dnn1,
                "defaultIndication": executionRequest.properties.defaultIndication1,
                "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
                "localBrkOutRoamingAllowed": executionRequest.properties.localBrkOutRoamingAllowed
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.udm_path,
            "valueObject": {
                "dnnId": executionRequest.properties.dnn2,
                "defaultIndication": executionRequest.properties.defaultIndication1,
                "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
                "localBrkOutRoamingAllowed": executionRequest.properties.localBrkOutRoamingAllowed
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.udm_path,
            "valueObject": {
                "dnnId": executionRequest.properties.dnn3,
                "defaultIndication": executionRequest.properties.defaultIndication1,
                "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
                "localBrkOutRoamingAllowed": executionRequest.properties.localBrkOutRoamingAllowed
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.udm_path1,
            "valueObject": {
                "dnnId": executionRequest.properties.dnn1,
                "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
                "sessionAmbr": executionRequest.properties.dnn1_sessionAmbr,
                "udm5gQosProfile": {
                    "udm5Qi": executionRequest.properties.udm5Qi,
                    "arp": executionRequest.properties.dnn1_arp,
                    "priorityLevel": executionRequest.properties.dnn1_priorityLevel
                },
                "pduSessionTypes": {
                    "defaultSessionType": executionRequest.properties.defaultSessionType,
                    "allowedSessionType": [
                        executionRequest.properties.allowedSessionType
                    ]
                },
                "sscModes": {
                    "defaultSscMode": executionRequest.properties.sscModes_defaultSscMode,
                    "allowedSscMode": [
                        executionRequest.properties.allowedSscMode
                    ]
                }
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.udm_path1,
            "valueObject": {
                "dnnId": executionRequest.properties.dnn2,
                "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
                "sessionAmbr": executionRequest.properties.dnn2_sessionAmbr,
                "udm5gQosProfile": {
                    "udm5Qi": executionRequest.properties.udm5Qi,
                    "arp": executionRequest.properties.dnn2_arp,
                    "priorityLevel": executionRequest.properties.dnn2_priorityLevel
                },
                "pduSessionTypes": {
                    "defaultSessionType": executionRequest.properties.defaultSessionType,
                    "allowedSessionType": [
                        executionRequest.properties.allowedSessionType
                    ]
                },
                "sscModes": {
                    "defaultSscMode": executionRequest.properties.sscModes_defaultSscMode,
                    "allowedSscMode": [
                        executionRequest.properties.allowedSscMode
                    ]
                }
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.udm_path1,
            "valueObject": {
                "dnnId": executionRequest.properties.dnn3,
                "interworkingEPSIndication": executionRequest.properties.interworkingEPSIndication,
                "sessionAmbr": executionRequest.properties.dnn3_sessionAmbr,
                "udm5gQosProfile": {
                    "udm5Qi": executionRequest.properties.udm5gQosProfile_udm5Qi,
                    "arp": executionRequest.properties.dnn3_arp,
                    "priorityLevel": executionRequest.properties.dnn3_priorityLevel
                },
                "pduSessionTypes": {
                    "defaultSessionType": executionRequest.properties.defaultSessionType,
                    "allowedSessionType": [
                        executionRequest.properties.allowedSessionType
                    ]
                },
                "sscModes": {
                    "defaultSscMode": executionRequest.properties.sscModes_defaultSscMode,
                    "allowedSscMode": [
                        executionRequest.properties.allowedSscMode
                    ]
                }
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.pcf_path,
            "valueObject": {
                "dnn": executionRequest.properties.dnn1,
                "allowedServices": [
                    executionRequest.properties.allowedServices
                ],
                "subscCats": [
                    executionRequest.properties.subscCats1,
                    executionRequest.properties.subscCats2
                ],
                "subscSpendingLimits": executionRequest.properties.subscSpendingLimits,
                "online": executionRequest.properties.online
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.pcf_path,
            "valueObject": {
                "dnn": executionRequest.properties.dnn2,
                "subscCats": [
                    executionRequest.properties.subscCats1,
                    executionRequest.properties.subscCats2
                ],
                "subscSpendingLimits": executionRequest.properties.subscSpendingLimits,
                "online": executionRequest.properties.online
            }
        },
        {
            "operation": executionRequest.properties.operation1,
            "path": executionRequest.properties.pcf_path,
            "valueObject": {
                "dnn": executionRequest.properties.dnn3,
                "subscCats": [
                    executionRequest.properties.subscCats1,
                    executionRequest.properties.subscCats2
                ],
                "subscSpendingLimits": executionRequest.properties.subscSpendingLimits,
                "online": executionRequest.properties.online
            }
        }
];
message["loopbackMode"] = "false";
message["requestId"] = executionRequest.properties.extOrderId;
message["supi"] = executionRequest.properties.SUPI;
message["objectClass"] = executionRequest.properties.objectClass;
message["targetVersion"] = executionRequest.properties.targetVersion;
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
