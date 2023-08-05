"""
SD-WAN_Path_Selection_L2_to_L4_Steering
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .utility import *

class PathSelectionL2ToL4Steering(SdWanTest):
    """
    Class to test L2 to L4 steering functionality of DUT/SUT.
    """
    def __init__(self, test_input):
        super().__init__(test_input)
        if self.local_head is None or self.remote_head is None or self.monitor_1 is None or self.monitor_2 is None:
            raise RuntimeError("Testbed config missing STC port(s)")
    def run(self):
        """
        Main def for case path_selection.001
        """
        msg_robot = ''
        logger = self.logger
        stc = self.stc
        project = stc.project()
        ######################################
        # Define parameters related to cases #
        ######################################
        config_local_head = StcParamSdwan(self.local_head.stc_config)
        config_remote_head = StcParamSdwan(self.remote_head.stc_config)
        config_monitor_1 = StcParamSdwan(self.monitor_1.stc_config)
        config_monitor_2 = StcParamSdwan(self.monitor_2.stc_config)
        #########################################
        # Config port objects and reserve ports #
        #########################################
        logger.console_info("Configuring stc ports...")
        port_handle_local_head = self.local_head.handle
        stc.config(port_handle_local_head, {'Name':SD_WAN_CONFIG['Port']['LocalHeadSeconds4M']['Name']})
        stc.config_port(port_handle_local_head, phy=config_local_head.port_phy, speed=config_local_head.port_speed)
        generator_local_head = stc.get(port_handle_local_head, 'children-Generator')
        generator_config = SD_WAN_CONFIG['Port']['LocalHeadSeconds4M']['GeneratorConfig']
        generator_config_local_head = stc.get(generator_local_head, 'children-GeneratorConfig')
        stc.config(generator_config_local_head, {'LoadUnit': generator_config['LoadUnit'], 'FixedLoad': generator_config['FixedLoad'], 'DurationMode': generator_config['DurationMode'], 'Duration': generator_config['Duration']})
        port_handle_remote_head = self.remote_head.handle
        stc.config(port_handle_remote_head, {'Name':SD_WAN_CONFIG['Port']['RemoteHead']['Name']})
        stc.config_port(port_handle_remote_head, phy=config_remote_head.port_phy, speed=config_remote_head.port_speed)
        port_handle_monitor_1 = self.monitor_1.handle
        stc.config(port_handle_monitor_1, {'Name':SD_WAN_CONFIG['Port']['Mirror1']['Name']})
        stc.config_port(port_handle_monitor_1, phy=config_monitor_1.port_phy, speed=config_monitor_1.port_speed)
        port_handle_monitor_2 = self.monitor_2.handle
        stc.config(port_handle_monitor_2, {'Name':SD_WAN_CONFIG['Port']['Mirror2']['Name']})
        stc.config_port(port_handle_monitor_2, phy=config_monitor_2.port_phy, speed=config_monitor_2.port_speed)
        logger.console_info("done")
        #########################
        # Config device objects #
        #########################
        logger.console_info("Config STC objects ...")
        stc_config = StcConfigSdwan(stc)
        device_local_head = stc_config.device_create(port_handle_local_head, SD_WAN_CONFIG['Device']['LocalHead'], config_local_head.device1)
        device_local_device1 = stc_config.device_create(port_handle_local_head, SD_WAN_CONFIG['Device']['LocalDevice1'], config_local_head.device2)
        device_local_device2 = stc_config.device_create(port_handle_local_head, SD_WAN_CONFIG['Device']['LocalDevice2'], config_local_head.device3)
        device_remote_head = stc_config.device_create(port_handle_remote_head, SD_WAN_CONFIG['Device']['RemoteHead'], config_remote_head.device1)
        device_remote_device1 = stc_config.device_create(port_handle_remote_head, SD_WAN_CONFIG['Device']['RemoteDevice1'], config_remote_head.device2)
        ########################
        # Config links objects #
        ########################
        stc.perform('LinkCreate', SrcDev=device_local_device1['ReturnList'], DstDev=device_local_head['ReturnList'], LinkType='L3 Forwarding Link')
        stc.perform('LinkCreate', SrcDev=device_local_device2['ReturnList'], DstDev=device_local_head['ReturnList'], LinkType='L3 Forwarding Link')
        stc.perform('LinkCreate', SrcDev=device_remote_device1['ReturnList'], DstDev=device_remote_head['ReturnList'], LinkType='L3 Forwarding Link')
        #########################
        # Config stream objects #
        #########################
        ipv4if_local_device1 = stc.get(device_local_device1['ReturnList'], 'children-Ipv4If')
        ipv4if_local_device2 = stc.get(device_local_device2['ReturnList'], 'children-Ipv4If')
        ipv4if_remote_device1 = stc.get(device_remote_device1['ReturnList'], 'children-Ipv4If')
        stream_tcp01 = stc.create('streamBlock', under=port_handle_local_head, attributes={'SrcBinding-targets':[ipv4if_local_device1], 'DstBinding-targets':[ipv4if_remote_device1], **SD_WAN_CONFIG['StreamBlock']['TCP01']})
        stream_tcp02 = stc.create('streamBlock', under=port_handle_local_head, attributes={'SrcBinding-targets':[ipv4if_local_device2], 'DstBinding-targets':[ipv4if_remote_device1], **SD_WAN_CONFIG['StreamBlock']['TCP02']})
        stream_udp01 = stc.create('streamBlock', under=port_handle_local_head, attributes={'SrcBinding-targets':[ipv4if_local_device1], 'DstBinding-targets':[ipv4if_remote_device1], **SD_WAN_CONFIG['StreamBlock']['UDP01']})
        stream_udp02 = stc.create('streamBlock', under=port_handle_local_head, attributes={'SrcBinding-targets':[ipv4if_local_device2], 'DstBinding-targets':[ipv4if_remote_device1], **SD_WAN_CONFIG['StreamBlock']['UDP02']})
        stream_udp03 = stc.create('streamBlock', under=port_handle_local_head, attributes={'SrcBinding-targets':[ipv4if_local_device1], 'DstBinding-targets':[ipv4if_remote_device1], **SD_WAN_CONFIG['StreamBlock']['UDP03']})
        stream_udp04 = stc.create('streamBlock', under=port_handle_local_head, attributes={'SrcBinding-targets':[ipv4if_local_device2], 'DstBinding-targets':[ipv4if_remote_device1], **SD_WAN_CONFIG['StreamBlock']['UDP04']})
        stream_udp05 = stc.create('streamBlock', under=port_handle_local_head, attributes={'SrcBinding-targets':[ipv4if_local_device1], 'DstBinding-targets':[ipv4if_remote_device1], **SD_WAN_CONFIG['StreamBlock']['UDP05']})
        stream_udp06 = stc.create('streamBlock', under=port_handle_local_head, attributes={'SrcBinding-targets':[ipv4if_local_device2], 'DstBinding-targets':[ipv4if_remote_device1], **SD_WAN_CONFIG['StreamBlock']['UDP06']})
        previous_frame_config_stream_tcp01 = stc.get(stream_tcp01, 'frameconfig')
        previous_frame_config_stream_tcp02 = stc.get(stream_tcp02, 'frameconfig')
        previous_frame_config_stream_udp01 = stc.get(stream_udp01, 'frameconfig')
        previous_frame_config_stream_udp02 = stc.get(stream_udp02, 'frameconfig')
        previous_frame_config_stream_udp03 = stc.get(stream_udp03, 'frameconfig')
        previous_frame_config_stream_udp04 = stc.get(stream_udp04, 'frameconfig')
        previous_frame_config_stream_udp05 = stc.get(stream_udp05, 'frameconfig')
        previous_frame_config_stream_udp06 = stc.get(stream_udp06, 'frameconfig')
        frame_config_stream_tcp01 = previous_frame_config_stream_tcp01.replace('</pdus>', '<pdu name="proto1" pdu="tcp:Tcp"><destPort>80</destPort></pdu></pdus>')
        frame_config_stream_tcp02 = previous_frame_config_stream_tcp02.replace('</pdus>', '<pdu name="proto1" pdu="tcp:Tcp"><destPort>80</destPort></pdu></pdus>')
        frame_config_stream_udp01 = previous_frame_config_stream_udp01.replace('</pdus>', '<pdu name="proto1" pdu="udp:Udp"><destPort>5060</destPort></pdu></pdus>')
        frame_config_stream_udp02 = previous_frame_config_stream_udp02.replace('</pdus>', '<pdu name="proto1" pdu="udp:Udp"><destPort>5060</destPort></pdu></pdus>')
        frame_config_stream_udp03 = previous_frame_config_stream_udp03.replace('</pdus>', '<pdu name="proto1" pdu="udp:Udp"><destPort>50050</destPort></pdu></pdus>')
        frame_config_stream_udp04 = previous_frame_config_stream_udp04.replace('</pdus>', '<pdu name="proto1" pdu="udp:Udp"><destPort>50050</destPort></pdu></pdus>')
        frame_config_stream_udp05 = previous_frame_config_stream_udp05.replace('</pdus>', '<pdu name="proto1" pdu="udp:Udp"><destPort>50050</destPort></pdu></pdus>')
        frame_config_stream_udp06 = previous_frame_config_stream_udp06.replace('</pdus>', '<pdu name="proto1" pdu="udp:Udp"><destPort>50050</destPort></pdu></pdus>')
        stc.config(stream_tcp01, {'FrameConfig': frame_config_stream_tcp01})
        stc.config(stream_tcp02, {'FrameConfig': frame_config_stream_tcp02})
        stc.config(stream_udp01, {'FrameConfig': frame_config_stream_udp01})
        stc.config(stream_udp02, {'FrameConfig': frame_config_stream_udp02})
        stc.config(stream_udp03, {'FrameConfig': frame_config_stream_udp03})
        stc.config(stream_udp04, {'FrameConfig': frame_config_stream_udp04})
        stc.config(stream_udp05, {'FrameConfig': frame_config_stream_udp05})
        stc.config(stream_udp06, {'FrameConfig': frame_config_stream_udp06})
        ranger_modifer_udp03 = stc.create('RangeModifier', under=stream_udp03)
        ranger_modifer_udp04 = stc.create('RangeModifier', under=stream_udp04)
        ranger_modifer_udp05 = stc.create('RangeModifier', under=stream_udp05)
        ranger_modifer_udp06 = stc.create('RangeModifier', under=stream_udp06)
        stc.config(ranger_modifer_udp03, {'RepeatCount': '0', 'RecycleCount': '25', 'StepValue': '2', 'Data': '50050', 'OffsetReference': 'proto1.destPort', 'Mask': '65535'})
        stc.config(ranger_modifer_udp04, {'RepeatCount': '0', 'RecycleCount': '25', 'StepValue': '2', 'Data': '50050', 'OffsetReference': 'proto1.destPort', 'Mask': '65535'})
        stc.config(ranger_modifer_udp05, {'RepeatCount': '0', 'RecycleCount': '25', 'StepValue': '2', 'Data': '50051', 'OffsetReference': 'proto1.destPort', 'Mask': '65535'})
        stc.config(ranger_modifer_udp06, {'RepeatCount': '0', 'RecycleCount': '25', 'StepValue': '2', 'Data': '50051', 'OffsetReference': 'proto1.destPort', 'Mask': '65535'})
        logger.console_info("done")
        ######################################################################
        # Set the Jumbo frame length, used to get counters from monitor port #
        ######################################################################
        analyzer_monitor_1 = stc.get(stc.get(port_handle_monitor_1, 'children-analyzer'), 'children-analyzerconfig')
        analyzer_monitor_2 = stc.get(stc.get(port_handle_monitor_2, 'children-analyzer'), 'children-analyzerconfig')
        stc.config(analyzer_monitor_1, {'JumboFrameThreshold':SD_WAN_CONFIG['ResultParameter']['Analyzer']['JumboFrameThreshold']})
        stc.config(analyzer_monitor_2, {'JumboFrameThreshold':SD_WAN_CONFIG['ResultParameter']['Analyzer']['JumboFrameThreshold']})
        #####################
        # Subscribe results #
        #####################
        self.subscribe_result({'port': port_handle_local_head, 'result_type': 'GeneratorPortResults'}, {'port': port_handle_local_head, 'result_type': 'AnalyzerPortResults'}, {'port': port_handle_remote_head, 'result_type': 'AnalyzerPortResults'}, \
        {'port': port_handle_monitor_1, 'result_type': 'AnalyzerPortResults'}, {'port': port_handle_monitor_2, 'result_type': 'AnalyzerPortResults'}, {'result_type': 'txstreamresults'}, {'port': port_handle_remote_head, 'result_type': 'rxstreamsummaryresults'})
        #########################
        # Apply and save config #
        #########################
        logger.console_info("Applying STC configuration ...")
        stc.apply()
        logger.console_info("done")
        logger.console_info("Save config file...")
        self.save_stc_config()
        logger.console_info("done")
        ###################################
        # Start Arp and verify Arp status #
        ###################################
        logger.console_info("Performing ARP...")
        arp_status = stc.perform('ArpNdStartCommand', WaitForArpToFinish="TRUE", HandleList=project)
        if arp_status['ArpNdState'] != 'SUCCESSFUL':
            raise RuntimeError('Arp failed, please check all configuration for both STC and DUT.')
        logger.console_info("done")
        #######################################################################################################################################
        # Start stream 1, 4, 5, 7 and verify stream are received on remote STC port and Traffic Analyzer 2 without packet loss or duplication #
        #######################################################################################################################################
        self.error_info = ''
        logger.console_info("Start stream 1, 4, 5, 7 and verify stream...")
        stc.perform('ResultsClearAllCommand', PortList=project)
        stc.config(stream_tcp02, {'Active': 'false'})
        stc.config(stream_udp01, {'Active': 'false'})
        stc.config(stream_udp04, {'Active': 'false'})
        stc.config(stream_udp06, {'Active': 'false'})
        time.sleep(2)
        stc.perform('GeneratorStartCommand', GeneratorList=generator_local_head)
        stc.perform('GeneratorWaitForStopCommand', GeneratorList=generator_local_head, WaitTimeout=70)
        time.sleep(2)
        #<===Verify stream 1, 4, 5, 7 are only received at remote STC port=====>
        self.verify_same_sig_count_port(tx_port=port_handle_local_head, rx_port=port_handle_remote_head)
        #<===Verify stream 1, 4, 5, 7 are only received at Traffic Analyzer 2=====>
        self.verify_jumbo_count(tx_port=port_handle_local_head, rx_port=port_handle_monitor_2)
        self.verify_no_jumbo_count(tx_port=port_handle_local_head, rx_port=port_handle_monitor_1)
        #<===Verify no packets loss or duplication for stream 1, 4, 5, 7=====>
        self.verify_no_packet_loss(stream=stream_tcp01)
        self.verify_no_packet_duplication(stream=stream_tcp01)
        self.verify_no_packet_loss(stream=stream_udp02)
        self.verify_no_packet_duplication(stream=stream_udp02)
        self.verify_no_packet_loss(stream=stream_udp03)
        self.verify_no_packet_duplication(stream=stream_udp03)
        self.verify_no_packet_loss(stream=stream_udp05)
        self.verify_no_packet_duplication(stream=stream_udp05)
        if self.error_info:
            logger.console_error('Failed to verify result for stream 1, 4, 5, 7, failure info in detail as below.')
            logger.console_error(self.error_info)
        else:
            logger.console_info("done")
        #######################################################################################################################################
        # Start stream 2, 3, 6, 8 and verify stream are received on remote STC port and Traffic Analyzer 1 without packet loss or duplication #
        #######################################################################################################################################
        self.error_info = ''
        logger.console_info("Start stream 2, 3, 6, 8 and verify stream...")
        stc.perform('ResultsClearAllCommand', PortList=project)
        stc.config(stream_tcp02, {'Active': 'true'})
        stc.config(stream_udp01, {'Active': 'true'})
        stc.config(stream_udp04, {'Active': 'true'})
        stc.config(stream_udp06, {'Active': 'true'})
        stc.config(stream_tcp01, {'Active': 'false'})
        stc.config(stream_udp02, {'Active': 'false'})
        stc.config(stream_udp03, {'Active': 'false'})
        stc.config(stream_udp05, {'Active': 'false'})
        time.sleep(2)
        stc.perform('GeneratorStartCommand', GeneratorList=generator_local_head)
        stc.perform('GeneratorWaitForStopCommand', GeneratorList=generator_local_head, WaitTimeout=70)
        time.sleep(2)
        #<===Verify stream 2, 3, 6, 8 are only received at remote STC port=====>
        self.verify_same_sig_count_port(tx_port=port_handle_local_head, rx_port=port_handle_remote_head)
        #<===Verify stream 2, 3, 6, 8 are only received at Traffic Analyzer 1=====>
        self.verify_jumbo_count(tx_port=port_handle_local_head, rx_port=port_handle_monitor_1)
        self.verify_no_jumbo_count(tx_port=port_handle_local_head, rx_port=port_handle_monitor_2)
        #<===Verify no packets loss or duplication for stream 2, 3, 6, 8=====>
        self.verify_no_packet_loss(stream=stream_tcp02)
        self.verify_no_packet_duplication(stream=stream_tcp02)
        self.verify_no_packet_loss(stream=stream_udp01)
        self.verify_no_packet_duplication(stream=stream_udp01)
        self.verify_no_packet_loss(stream=stream_udp04)
        self.verify_no_packet_duplication(stream=stream_udp04)
        self.verify_no_packet_loss(stream=stream_udp06)
        self.verify_no_packet_duplication(stream=stream_udp06)
        if self.error_info:
            logger.console_error('Failed to verify result for stream 2, 3, 6, 8, failure info in detail as below.')
            logger.console_error(self.error_info)
        else:
            logger.console_info("done")
        self.save_stc_results()
        ################################
        # Raise failure info when fail #
        ################################
        if self.result != 'pass':
            self.raise_failure()
        return msg_robot
