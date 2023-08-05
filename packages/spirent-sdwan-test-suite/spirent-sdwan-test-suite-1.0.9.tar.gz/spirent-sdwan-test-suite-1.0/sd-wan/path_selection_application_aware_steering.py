"""
SD-WAN_Path_Selection_Application_Aware_Steering
"""
import os
import sys
from test_framework.testbase.settings import *
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .utility import *

class PathSelectionApplicationAwareSteering(SdWanTest):
    """
    Class to test application aware steering functionality of DUT/SUT
    """
    def __init__(self, test_input):
        super().__init__(test_input)
        if self.local_head is None or self.remote_head is None or self.monitor_1 is None or self.monitor_2 is None:
            raise RuntimeError("Testbed config missing STC port(s)")
    def run(self):
        """
        Main def
        """

        logger = self.logger
        stc = self.stc
        project = stc.project()
        msg_robot = ''
        #######################
        # Configuration phase #
        #######################
        config_local_head = StcParamSdwan(self.local_head.stc_config)
        config_remote_head = StcParamSdwan(self.remote_head.stc_config)
        config_monitor_1 = StcParamSdwan(self.monitor_1.stc_config)
        config_monitor_2 = StcParamSdwan(self.monitor_2.stc_config)
        ### Configure ports ###
        logger.console_info("Configuring stc ports...")
        port_handle_local_head = self.local_head.handle
        stc.config(port_handle_local_head, {'Name': SD_WAN_CONFIG['Port']['LocalHead']['Name']})
        stc.config_port(port_handle_local_head, phy=config_local_head.port_phy, speed=config_local_head.port_speed)
        port_handle_remote_head = self.remote_head.handle
        stc.config(port_handle_remote_head, {'Name': SD_WAN_CONFIG['Port']['RemoteHead']['Name']})
        stc.config_port(port_handle_remote_head, phy=config_remote_head.port_phy, speed=config_remote_head.port_speed)
        logger.console_info("done\n")
        ### Creating devices ###
        stc_config = StcConfigSdwan(stc)
        logger.console_info("Creating devices...")
        SD_WAN_CONFIG['Device']['LocalDevice1']['DeviceCount'] = '10'
        SD_WAN_CONFIG['Device']['RemoteDevice1']['DeviceCount'] = '20'
        device_local_head = stc_config.device_create(port_handle_local_head, SD_WAN_CONFIG['Device']['LocalHead'], config_local_head.device1)
        device_local_device1 = stc_config.device_create(port_handle_local_head, SD_WAN_CONFIG['Device']['LocalDevice1'], config_local_head.device2)
        device_remote_head = stc_config.device_create(port_handle_remote_head, SD_WAN_CONFIG['Device']['RemoteHead'], config_remote_head.device1)
        device_remote_device1 = stc_config.device_create(port_handle_remote_head, SD_WAN_CONFIG['Device']['RemoteDevice1'], config_remote_head.device2)
        ### Create links ###
        logger.info("Creating links")
        stc.perform('LinkCreate', SrcDev=device_local_device1['ReturnList'], DstDev=device_local_head['ReturnList'], LinkType='L3 Forwarding Link')
        stc.perform('LinkCreate', SrcDev=device_remote_device1['ReturnList'], DstDev=device_remote_head['ReturnList'], LinkType='L3 Forwarding Link')
        logger.console_info("done\n")
        ### Configure device-level HTTP ###
        logger.console_info("Configuring HTTP protocol...")
        http_client_load_type = 'CONNECTIONS_PER_TIME_UNIT'
        http_client_max_conn_attempt = 1500
        http_client_max_tran_attempt = 10 * http_client_max_conn_attempt
        http_client_max_open_conn = 20
        http_server = stc.create('HttpServerProtocolConfig', under=device_remote_device1['ReturnList'], Name='HTTP Server MPLS', ServerName='HTTP Server MPLS')
        http_client = stc.create("HttpClientProtocolConfig", under=device_local_device1['ReturnList'], Name='HTTP Client')
        stc.config(http_client, {"ConnectionDestination-targets" :http_server})
        ### Configure HTTP profiles ###
        logger.console_info("Configuring HTTP profiles")
        http_client_load = stc.create('ClientLoadProfile', under=project, MaxConnectionsAttempted=http_client_max_conn_attempt, \
        LoadType=http_client_load_type, MaxOpenConnections=http_client_max_open_conn, ProfileName="HTTP client load profile")
        ## phase1 ##
        http_load_phase_1 = stc.create("ClientLoadPhase", under=http_client_load, PhaseName="Delay", PhaseNum="1", LoadPattern="FLAT", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("FlatPatternDescriptor", under=http_load_phase_1, Height="0", RampTime="0", SteadyTime="5", Active="TRUE", LocalActive="TRUE")
        ## phase2 ##
        http_load_phase_2 = stc.create("ClientLoadPhase", under=http_client_load, PhaseName="Ramp Up", PhaseNum="2", LoadPattern="STAIR", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("StairPatternDescriptor", under=http_load_phase_2, Height="10", Repetitions="1", RampTime="10", SteadyTime="0", Active="TRUE", LocalActive="TRUE")
        ## phase3 ##
        http_load_phase_3 = stc.create("ClientLoadPhase", under=http_client_load, PhaseName="Stair Step", PhaseNum="3", LoadPattern="STAIR", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("StairPatternDescriptor", under=http_load_phase_3, Height="4", Repetitions="5", RampTime="5", SteadyTime="5", Active="TRUE", LocalActive="TRUE")
        ## phase4 ##
        http_load_phase_4 = stc.create("ClientLoadPhase", under=http_client_load, PhaseName="Steady State", PhaseNum="4", LoadPattern="STAIR", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("StairPatternDescriptor", under=http_load_phase_4, Height="0", Repetitions="1", RampTime="0", SteadyTime="30", Active="TRUE", LocalActive="TRUE")
        ## phase5 ##
        http_load_phase_5 = stc.create("ClientLoadPhase", under=http_client_load, PhaseName="Ramp Down", PhaseNum="5", LoadPattern="FLAT", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("FlatPatternDescriptor", under=http_load_phase_5, Height="0", RampTime="0", SteadyTime="20", Active="TRUE", LocalActive="TRUE")
        stc.config(http_client, {"AffiliatedClientLoadProfile-targets" : [http_client_load]})
        logger.console_info("done\n")
        ### Configure device-level SIP ###
        logger.console_info("Configuring SIP protocol...")
        sip_caller_uanumberformat = 'Caller_%08u'
        sip_callee_uanumberformat = 'Callee_%06u'
        sip_load_loadtype = 'CONNECTIONS_PER_TIME_UNIT'
        sip_load_max_openconnections = 10
        sip_load_max_connectionsattempted = 200
        sip_callee = stc.create('SipUaProtocolconfig', under=device_remote_device1['ReturnList'], \
                    UaNumFormat=sip_callee_uanumberformat, Name='SIP Callee')
        sip_caller = stc.create('SipUaProtocolconfig', under=device_local_device1['ReturnList'], \
                    UaNumFormat=sip_caller_uanumberformat, Name='SIP Caller')

        ### Configure SIP call profile and load profile ###
        logger.console_info("Configuring SIP profiles")
        local_device1_ipv4if = stc.get(device_local_device1['ReturnList'], 'children-Ipv4If')
        sip_load_profile = stc.create('ClientLoadProfile', under=project, ProfileName="SIP_LoadProfile_1", \
                         LoadType=sip_load_loadtype, MaxConnectionsAttempted=sip_load_max_connectionsattempted, \
                         MaxOpenConnections=sip_load_max_openconnections)
        sip_load_phase_1 = stc.create("ClientLoadPhase", under=sip_load_profile, PhaseName="Label 1", PhaseNum="1", \
                         LoadPattern="FLAT", LoadPhaseDurationUnits="SECONDS", Active="TRUE", LocalActive="TRUE")
        stc.create("FlatPatternDescriptor", under=sip_load_phase_1, Height="4", RampTime="180", \
                  SteadyTime="0", Active="TRUE", LocalActive="TRUE")
        sip_caller_profile = stc.create('ClientProfile', under=project, ProfileName="SIP_ClientProfile_1")
        stc.create("SipUaProtocolProfile", under=sip_caller_profile, CallTime="3")
        stc.config(sip_caller, {"ConnectionDestination-targets" : [sip_callee], "UsesIf-targets" :[local_device1_ipv4if]})
        stc.config(sip_caller, {"AffiliatedClientLoadProfile-targets" : [sip_load_profile]})
        stc.config(sip_caller, {"AffiliatedClientProfile-targets" : [sip_caller_profile]})
        stc.config(sip_callee, {"AffiliatedClientProfile-targets" : [sip_caller_profile]})
        logger.console_info("done\n")
        ### Configure sequencer commands ###
        logger.console_info("Configuring command sequencer...")
        sequencer = stc.create("Sequencer", under='system1', ErrorHandler='STOP_ON_ERROR')
        clear_all_result_atbeginning = stc.create("ResultsClearAllCommand", under=sequencer, Name='Clear all results before start testing')
        arpat_beginning = stc.create('ArpNdStartOnAllDevicesCommand', under=sequencer, Name='Start ARP on all devices')
        verify_arp_status = stc.create('ArpNdVerifyResolvedCommand', under=sequencer, ErrorOnFailure='TRUE', HandleList=[device_local_head['ReturnList'], device_remote_head['ReturnList']])
        start_http_server = stc.create('ProtocolStartCommand', under=sequencer, Name='Start HTTP server', ProtocolList=[http_server])
        wait_http_server = stc.create('WaitCommand', under=sequencer, Name='Wait for HTTP server to be brought up', WaitTime='10')
        start_http_client = stc.create('ProtocolStartCommand', under=sequencer, Name='Start HTTP client', ProtocolList=[http_client])
        wait_http_client = stc.create('WaitCommand', under=sequencer, Name='Wait for HTTP client to be brought up', WaitTime='20')
        ## Verify HTTP results ##
        verify_http_result = stc.create('VerifyResultsValueCommand', under=sequencer, WaitTimeout="180", ErrorOnFailure='TRUE', Name='Verify HTTP results')
        # Condition 1 #
        http_result_dataset_1 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpClientProtocolConfig")
        http_result_query_1 = stc.create('ResultQuery', under=http_result_dataset_1, ConfigClassId="httpclientprotocolconfig", ResultClassId="httpclientresults", PropertyIdArray="httpclientresults.attemptedconnections")
        stc.config(http_result_query_1, ResultRootList=http_client, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_http_result, PropertyOperand="AttemptedConnections", ValueOperand=http_client_max_conn_attempt, ComparisonOperator="EQUAL", MinValueOperand=http_client_max_conn_attempt, MaxValueOperand=http_client_max_conn_attempt, ResultQuery=http_result_query_1)
        # Condition 2 #
        http_result_dataset_2 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpClientProtocolConfig")
        http_result_query_2 = stc.create('ResultQuery', under=http_result_dataset_2, ConfigClassId="httpclientprotocolconfig", ResultClassId="httpclientresults", PropertyIdArray="httpclientresults.attemptedtransactions")
        stc.config(http_result_query_2, ResultRootList=http_client, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_http_result, PropertyOperand="AttemptedTransactions", ValueOperand=http_client_max_tran_attempt, ComparisonOperator="EQUAL", MinValueOperand=http_client_max_tran_attempt, MaxValueOperand=http_client_max_tran_attempt, ResultQuery=http_result_query_2)
        # Condition 3 #
        http_result_dataset_3 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpClientProtocolConfig")
        http_result_query_3 = stc.create('ResultQuery', under=http_result_dataset_3, ConfigClassId="httpclientprotocolconfig", ResultClassId="httpclientresults", PropertyIdArray="httpclientresults.successfultransactions")
        stc.config(http_result_query_3, ResultRootList=http_client, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_http_result, PropertyOperand="SuccessfulTransactions", ValueOperand=http_client_max_tran_attempt, ComparisonOperator="EQUAL", MinValueOperand=http_client_max_tran_attempt, MaxValueOperand=http_client_max_tran_attempt, ResultQuery=http_result_query_3)
        # Condition 4 #
        http_result_dataset_4 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpClientProtocolConfig")
        http_result_query_4 = stc.create('ResultQuery', under=http_result_dataset_4, ConfigClassId="httpclientprotocolconfig", ResultClassId="httpclientresults", PropertyIdArray="httpclientresults.successfulconnections")
        stc.config(http_result_query_4, ResultRootList=http_client, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_http_result, PropertyOperand="Successfulconnections", ValueOperand=http_client_max_conn_attempt, ComparisonOperator="EQUAL", MinValueOperand=http_client_max_conn_attempt, MaxValueOperand=http_client_max_conn_attempt, ResultQuery=http_result_query_4)
        # Condition 5 #
        http_result_dataset_5 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpServerProtocolConfig")
        http_result_query_5 = stc.create('ResultQuery', under=http_result_dataset_5, ConfigClassId="httpserverprotocolconfig", ResultClassId="httpserverresults", PropertyIdArray="httpserverresults.successfultransactions")
        stc.config(http_result_query_5, ResultRootList=http_server, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_http_result, PropertyOperand="SuccessfulTransactions", ValueOperand=http_client_max_tran_attempt, ComparisonOperator="EQUAL", MinValueOperand=http_client_max_tran_attempt, MaxValueOperand=http_client_max_tran_attempt, ResultQuery=http_result_query_5)
        # Condition 6 #
        http_result_dataset_6 = stc.create('ResultDataSet', under=project, PrimaryClass="HttpServerProtocolConfig")
        http_result_query_6 = stc.create('ResultQuery', under=http_result_dataset_6, ConfigClassId="httpserverprotocolconfig", ResultClassId="httpserverresults", PropertyIdArray="httpserverresults.Totalconnections")
        stc.config(http_result_query_6, ResultRootList=http_server, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_http_result, PropertyOperand="Totalconnections", ValueOperand=http_client_max_conn_attempt, ComparisonOperator="EQUAL", MinValueOperand=http_client_max_conn_attempt, MaxValueOperand=http_client_max_conn_attempt, ResultQuery=http_result_query_6)
        ## Stop HTTP client and server ##
        stop_http_server = stc.create('ProtocolStopCommand', under=sequencer, Name='Stop HTTP server', ProtocolList=[http_server])
        stop_http_client = stc.create('ProtocolStopCommand', under=sequencer, Name='Stop HTTP client', ProtocolList=[http_client])
        ## Start SIP caller ##
        start_sip_caller = stc.create('ProtocolStartCommand', under=sequencer, Name='Start SIP caller', ProtocolList=[sip_caller])
        wait_sip_caller = stc.create('WaitCommand', under=sequencer, Name='Wait for SIP caller to be brought up', WaitTime='10')
        ## Verify SIP results ##
        verify_sip_result = stc.create('VerifyResultsValueCommand', under=sequencer, WaitTimeout="300", ErrorOnFailure='TRUE', Name='Verify SIP results')
        # Condition 1 #
        sip_result_dataset_1 = stc.create('ResultDataSet', under=project, PrimaryClass="SipUaProtocolConfig")
        sip_result_query_1 = stc.create('ResultQuery', under=sip_result_dataset_1, ConfigClassId="sipuaprotocolconfig", ResultClassId="sipuaresults", PropertyIdArray="sipuaresults.callattemptcount")
        stc.config(sip_result_query_1, ResultRootList=sip_caller, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_sip_result, PropertyOperand="CallAttemptCount", ValueOperand=sip_load_max_connectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=sip_load_max_connectionsattempted, MaxValueOperand=sip_load_max_connectionsattempted, ResultQuery=sip_result_query_1)
        # Condition 2 #
        sip_result_dataset_2 = stc.create('ResultDataSet', under=project, PrimaryClass="SipUaProtocolConfig")
        sip_result_query_2 = stc.create('ResultQuery', under=sip_result_dataset_2, ConfigClassId="sipuaprotocolconfig", ResultClassId="sipuaresults", PropertyIdArray="sipuaresults.callsuccesscount")
        stc.config(sip_result_query_2, ResultRootList=sip_caller, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_sip_result, PropertyOperand="CallSuccessCount", ValueOperand=sip_load_max_connectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=sip_load_max_connectionsattempted, MaxValueOperand=sip_load_max_connectionsattempted, ResultQuery=sip_result_query_2)
        # Condition 3 #
        sip_result_dataset_3 = stc.create('ResultDataSet', under=project, PrimaryClass="SipUaProtocolConfig")
        sip_result_query_3 = stc.create('ResultQuery', under=sip_result_dataset_3, ConfigClassId="sipuaprotocolconfig", ResultClassId="sipuaresults", PropertyIdArray="sipuaresults.callsansweredcount")
        stc.config(sip_result_query_3, ResultRootList=sip_callee, PropertyHandleArray="")
        stc.create('VerifyResultsValueCondition', under=verify_sip_result, PropertyOperand="CallsAnsweredCount", ValueOperand=sip_load_max_connectionsattempted, ComparisonOperator="EQUAL", MinValueOperand=sip_load_max_connectionsattempted, MaxValueOperand=sip_load_max_connectionsattempted, ResultQuery=sip_result_query_3)
        ## Stop SIP caller ##
        stop_sip_caller = stc.create('ProtocolStopCommand', under=sequencer, Name='Stop SIP caller', ProtocolList=[sip_caller])
        stc.config(sequencer, CommandList=[clear_all_result_atbeginning, arpat_beginning, verify_arp_status, start_http_server, wait_http_server, start_http_client, wait_http_client, verify_http_result, stop_http_server, stop_http_client, start_sip_caller, wait_sip_caller, verify_sip_result, stop_sip_caller])
        ######################
        # Subcscribe results #
        ######################
        logger.console_info("Subscribing results")
        stc.perform('ResultsSubscribeCommand', parent=project, resultParent=project, configType='httpclientprotocolconfig', resultType='httpclientresults', filenamePrefix=self.test_input.testcase_id+'-httpclientresults')
        stc.perform('ResultsSubscribeCommand', parent=project, resultParent=project, configType='httpserverprotocolconfig', resultType='httpserverresults', filenamePrefix=self.test_input.testcase_id+'-httpserverresults')
        stc.perform('ResultsSubscribeCommand', parent=project, resultParent=project, configType='sipuaprotocolconfig', resultType='sipuaresults', filenamePrefix=self.test_input.testcase_id+'-sipuaresults')
        logger.console_info("done\n")
        #########################
        # Apply and save config #
        #########################
        logger.console_info("Applying STC configuration ...")
        stc.apply()
        logger.console_info("done")
        logger.console_info("Save config file...")
        self.save_stc_config()
        logger.console_info("done")
        #############################
        # Run commands in sequencer #
        #############################
        ### Start the sequencer ###
        test_state = 'PASSED'
        logger.console_info("Starting command sequencer...\n")
        stc.perform('sequencerStart')
        logger.console_info("Sequencer started, it will take several minutes to finish.\n")
        ### Wait for sequencer to finish ###
        logger.console_info("Wait command sequencer to stop...\n")
        test_state = stc.wait_until_complete()
        logger.console_info("Sequencer stopped\n")
        sequencer_status = stc.get(sequencer, 'Status')
        self.save_stc_results()
        stc.perform('SaveAsXml', filename=self.test_input.testcase_id + '_eot.xml')
        http_client_results = stc.get(http_client, 'children-HttpClientResults')
        http_server_results = stc.get(http_server, 'children-HttpServerResults')
        sip_caller_result = stc.get(sip_caller, 'children-SipUaResults')
        sip_callee_result = stc.get(sip_callee, 'children-SipUaResults')
        http_client_attempted_connections = stc.get(http_client_results, 'AttemptedConnections')
        http_client_attempted_transactions = stc.get(http_client_results, 'AttemptedTransactions')
        http_client_successful_connections = stc.get(http_client_results, 'SuccessfulConnections')
        http_client_succ_tran = stc.get(http_client_results, 'SuccessfulTransactions')
        http_server_succ_tran = stc.get(http_server_results, 'SuccessfulTransactions')
        http_server_total_connections = stc.get(http_server_results, 'TotalConnections')
        sip_caller_attempted_calls = stc.get(sip_caller_result, 'CallAttemptCount')
        sip_caller_successful_calls = stc.get(sip_caller_result, 'CallSuccessCount')
        sip_callee_answered_calls = stc.get(sip_callee_result, 'CallsAnsweredCount')
        log_msg = ''
        log_msg = log_msg +'Actual HTTP client attempted connection count='+ str(http_client_attempted_connections) + ', expected value=' + str(http_client_max_conn_attempt) + '.\n'
        log_msg = log_msg +'Actual HTTP client attempted transaction count='+ str(http_client_attempted_transactions) + ', expected value=' + str(http_client_max_tran_attempt) + '.\n'
        log_msg = log_msg +'Actual HTTP client successful connection count='+ str(http_client_successful_connections) + ', expected value=' + str(http_client_max_conn_attempt) + '.\n'
        log_msg = log_msg +'Actual HTTP client successful transaction count='+ str(http_client_succ_tran) + ', expected value=' + str(http_client_max_tran_attempt) + '.\n'
        log_msg = log_msg +'Actual HTTP server successful transaction count='+ str(http_server_succ_tran) + ', expected value=' + str(http_client_max_tran_attempt) + '.\n'
        log_msg = log_msg +'Actual HTTP server total connection count='+ str(http_server_total_connections) + ', expected value=' + str(http_client_max_conn_attempt) + '.\n'
        log_msg = log_msg +'Actual SIP caller attempted call count='+ str(sip_caller_attempted_calls) + ', expected value=' + str(sip_load_max_connectionsattempted) + '.\n'
        log_msg = log_msg +'Actual SIP caller successful call count='+ str(sip_caller_successful_calls) + ', expected value=' + str(sip_load_max_connectionsattempted) + '.\n'
        log_msg = log_msg +'Actual SIP callee answered call count='+ str(sip_callee_answered_calls) + ', expected value=' + str(sip_load_max_connectionsattempted) + '.\n'
        msg_robot = msg_robot + log_msg
        ##############################
        # Get test result and return #
        ##############################
        if test_state != 'PASSED':
            errorinfo = 'Test failed, ' + sequencer_status + '.\n'
            msg_robot = msg_robot + errorinfo
            raise RuntimeError(msg_robot)
        msg_robot = msg_robot + 'All HTTP traffic is steered towards Internet link.\n' + \
                    'All SIP/RTP traffic is steered towards MPLS link.\n' + 'Test Passed.\n'
        logger.console_info("Final test state is " + test_state + '\n')
        return msg_robot
