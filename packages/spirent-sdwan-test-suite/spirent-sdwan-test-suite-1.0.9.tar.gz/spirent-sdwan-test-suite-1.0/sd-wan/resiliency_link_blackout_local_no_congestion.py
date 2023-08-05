"""
SD-WAN_Resiliency_Link_Blackout_Local_no_Congestion
"""
import time
import sys
import os
from test_framework.testbase.settings import *
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from .utility import *

class ResiliencyLinkBlackoutLocalNoCongestion(SdWanTest):
    """
    Class to verify DUT/SUT is able to steer traffic correctly when local link failure is detected.
    """
    def __init__(self, test_input):
        super().__init__(test_input)
        if self.local_head is None or self.remote_head is None or self.monitor_1 is None or self.monitor_2 is None:
            raise RuntimeError("Testbed config missing STC port(s)")
    def run(self):
        """
        Main def for case resiliency_link.001
        """
        msg_robot = ''
        logger = self.logger
        stc = self.stc
        sne = self.sne.devices['sne']
        project = stc.project()
        ######################################
        # Define parameters related to cases #
        ######################################
        config_local_head = StcParamSdwan(self.local_head.stc_config)
        config_remote_head = StcParamSdwan(self.remote_head.stc_config)
        config_monitor_1 = StcParamSdwan(self.monitor_1.stc_config)
        config_monitor_2 = StcParamSdwan(self.monitor_2.stc_config)
        config_global = StcParamSdwan(self.testbed.custom.global_config)
        sne_config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), self.test_input.sne_config_file)
        sne_devices = self.testbed.find_devices(os=SPIRENT_OS, type=SNE_TYPE)
        sne_port_to_edeg1 = str(int(list(sne_devices[0].interfaces.keys())[0][2:]) + 1)
        #########################################
        # Config port objects and reserve ports #
        #########################################
        logger.console_info("Configuring stc ports...")
        port_handle_local_head = self.local_head.handle
        stc.config(port_handle_local_head, {'Name':SD_WAN_CONFIG['Port']['LocalHeadContinuous4M']['Name']})
        stc.config_port(port_handle_local_head, phy=config_local_head.port_phy, speed=config_local_head.port_speed)
        generator_local_head = stc.get(port_handle_local_head, 'children-Generator')
        generator_config = SD_WAN_CONFIG['Port']['LocalHeadContinuous4M']['GeneratorConfig']
        generator_config_local_head = stc.get(generator_local_head, 'children-GeneratorConfig')
        stc.config(generator_config_local_head, {'LoadUnit': generator_config['LoadUnit'], 'FixedLoad': generator_config['FixedLoad'], 'DurationMode': generator_config['DurationMode']})
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
        previous_frame_config_stream_tcp01 = stc.get(stream_tcp01, 'frameconfig')
        previous_frame_config_stream_tcp02 = stc.get(stream_tcp02, 'frameconfig')
        previous_frame_config_stream_udp01 = stc.get(stream_udp01, 'frameconfig')
        previous_frame_config_stream_udp02 = stc.get(stream_udp02, 'frameconfig')
        frame_config_stream_tcp01 = previous_frame_config_stream_tcp01.replace('</pdus>', '<pdu name="proto1" pdu="tcp:Tcp"><destPort>80</destPort></pdu></pdus>')
        frame_config_stream_tcp02 = previous_frame_config_stream_tcp02.replace('</pdus>', '<pdu name="proto1" pdu="tcp:Tcp"><destPort>80</destPort></pdu></pdus>')
        frame_config_stream_udp01 = previous_frame_config_stream_udp01.replace('</pdus>', '<pdu name="proto1" pdu="udp:Udp"><destPort>50050</destPort></pdu></pdus>')
        frame_config_stream_udp02 = previous_frame_config_stream_udp02.replace('</pdus>', '<pdu name="proto1" pdu="udp:Udp"><destPort>50050</destPort></pdu></pdus>')
        stc.config(stream_tcp01, {'FrameConfig': frame_config_stream_tcp01})
        stc.config(stream_tcp02, {'FrameConfig': frame_config_stream_tcp02})
        stc.config(stream_udp01, {'FrameConfig': frame_config_stream_udp01})
        stc.config(stream_udp02, {'FrameConfig': frame_config_stream_udp02})
        ranger_modifer_udp01 = stc.create('RangeModifier', under=stream_udp01)
        ranger_modifer_udp02 = stc.create('RangeModifier', under=stream_udp02)
        stc.config(ranger_modifer_udp01, {'RepeatCount': '0', 'RecycleCount': '25', 'StepValue': '2', 'Data': '50050', 'OffsetReference': 'proto1.destPort', 'Mask': '65535'})
        stc.config(ranger_modifer_udp02, {'RepeatCount': '0', 'RecycleCount': '25', 'StepValue': '2', 'Data': '50050', 'OffsetReference': 'proto1.destPort', 'Mask': '65535'})
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
        ###################################
        # Clear results and start traffic #
        ###################################
        logger.console_info("Clear all results for all ports...")
        stc.perform('ResultsClearAllCommand', PortList=project)
        time.sleep(2)
        logger.console_info("done")
        logger.console_info("Start traffic...")
        stc.perform('GeneratorStartCommand', GeneratorList=[generator_local_head])
        logger.console_info("started\n")
        time.sleep(10)
        # get the speed for local port
        traffic_rate = int(stc.get(stc.get(generator_local_head, 'children-GeneratorConfig'), 'FpsLoad'))
        half_traffic_rate = int(traffic_rate / 2)
        self.save_stc_results(result_file_name=self.test_input.testcase_id + '_all_streams_fps_.db')
        ############################################################################
        # Verify stream 1, 3 go via internet link and stream 2, 4 go via mpls link #
        ############################################################################
        self.error_info = ''
        logger.console_info('Start to verify stream 1, 3 go via internet link and stream 2, 4 go via mpls link...')
        self.verify_stable_jumbo_fps(port_handle_monitor_1, half_traffic_rate, config_global.tolerance_traffic_rate)
        self.verify_stable_jumbo_fps(port_handle_monitor_2, half_traffic_rate, config_global.tolerance_traffic_rate)
        if self.error_info:
            logger.info('Failed to verify stream 1, 3 go via internet link and stream 2, 4 go via mpls link, failure info in detail as below.')
            logger.info(self.error_info)
            stc.perform('GeneratorStopCommand', GeneratorList=[generator_local_head])
            raise RuntimeError('Failed to verify stream 1, 3 go via internet link and stream 2, 4 go via mpls link.')
        else:
            logger.console_info("done")
        ######################################################################
        # Break Internet local link, then traffic should switch to Mpls link #
        ######################################################################
        logger.console_info('Break SNE link connect to Edge1 and verify traffic switch to Mpls link...')
        sne.configure()
        sne.upload(config_file=sne_config_file)
        sne.linkdown(sne_port_to_edeg1)
        self.verify_stable_jumbo_fps(port_handle_monitor_1, traffic_rate, config_global.tolerance_traffic_rate, config_global.max_wait_time_after_break_link)
        self.save_stc_results(result_file_name=self.test_input.testcase_id + '_fps_break_internet_link.db')
        if self.error_info:
            logger.info('Traffic can not switch to Mpls link in {0}s after break Internet local link, failure info in detail as below.'.format(config_global.max_wait_time_after_break_link))
            logger.info(self.error_info)
            stc.perform('GeneratorStopCommand', GeneratorList=[generator_local_head])
            raise RuntimeError('Traffic can not switch to Mpls link in {0}s after break Internet local link.'.format(config_global.max_wait_time_after_break_link))
        else:
            stc.perform('GeneratorStopCommand', GeneratorList=[generator_local_head])
            time.sleep(2)
            tx_frame_local_head = stc.get(stc.get(stc.get(port_handle_local_head, 'children-generator'), 'children-generatorportresults'))['GeneratorSigFrameCount']
            rx_frame_remote_head = self.stc.get(self.stc.get(self.stc.get(port_handle_remote_head, 'children-analyzer'), 'children-analyzerportresults'))['SigFrameCount']
            time_switch = int((int(tx_frame_local_head) - int(rx_frame_remote_head))* 1000 / traffic_rate)
            msg_robot = 'Traffic switch to mpls link successfully after blackout internet link and Out of service time is {0} ms\n'.format(time_switch)
            logger.console_info("done")
        #################################################################################
        # Recover Internet local link, then traffic should switch back to Internet link #
        #################################################################################
        logger.console_info("Clear all results for all ports...")
        stc.perform('ResultsClearAllCommand', PortList=project)
        time.sleep(2)
        logger.console_info("done")
        logger.console_info("Start traffic...")
        stc.perform('GeneratorStartCommand', GeneratorList=[generator_local_head])
        logger.console_info("started\n")
        time.sleep(10)
        logger.console_info('Recover SNE link connect to Edge1 and verify traffic switch back to Internet link...')
        sne.linkup(sne_port_to_edeg1)
        self.verify_stable_jumbo_fps(port_handle_monitor_1, half_traffic_rate, config_global.tolerance_traffic_rate, config_global.max_wait_time_after_recover_link)
        self.verify_stable_jumbo_fps(port_handle_monitor_2, half_traffic_rate, config_global.tolerance_traffic_rate, config_global.max_wait_time_after_recover_link)
        self.save_stc_results(result_file_name=self.test_input.testcase_id + '_fps_switch_back_internet_link.db')
        if self.error_info:
            logger.info('Traffic can not switch back to Internet link in {0}s after Recover Internet local link, failure info in detail as below.'.format(config_global.max_wait_time_after_recover_link))
            logger.info(self.error_info)
            stc.perform('GeneratorStopCommand', GeneratorList=[generator_local_head])
            raise RuntimeError('Traffic can not switch back to Internet link in {0}s after Recover Internet local link.'.format(config_global.max_wait_time_after_recover_link))
        else:
            stc.perform('GeneratorStopCommand', GeneratorList=[generator_local_head])
            time.sleep(2)
            tx_frame_local_head = stc.get(stc.get(stc.get(port_handle_local_head, 'children-generator'), 'children-generatorportresults'))['GeneratorSigFrameCount']
            rx_frame_remote_head = self.stc.get(self.stc.get(self.stc.get(port_handle_remote_head, 'children-analyzer'), 'children-analyzerportresults'))['SigFrameCount']
            time_switch = int((int(tx_frame_local_head) - int(rx_frame_remote_head))* 1000 / traffic_rate)
            msg_robot = msg_robot + 'Traffic switch back to Internet link successfully after recover internet link and recovery time is {0} ms\n'.format(time_switch)
            logger.console_info("done")
        return msg_robot
