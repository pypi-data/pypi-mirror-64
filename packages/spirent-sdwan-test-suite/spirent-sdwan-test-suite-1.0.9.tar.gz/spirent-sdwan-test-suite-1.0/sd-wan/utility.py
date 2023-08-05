"""
Define some variables and common functions for mef sd-wan test scripts
"""
import time
from test_framework.testbase.configutility import BaseConfig
from test_framework.testbase.testbase import TestBase


SD_WAN_CONFIG = {
    'Port':{
        #Port configuraton
        'LocalHeadSeconds1M': {'Name': 'LocalHead', 'GeneratorConfig':{'LoadUnit':'BITS_PER_SECOND', 'FixedLoad':'1000000', 'DurationMode':'SECONDS', 'Duration':'60'}},
        'LocalHeadSeconds4M': {'Name': 'LocalHead', 'GeneratorConfig':{'LoadUnit':'BITS_PER_SECOND', 'FixedLoad':'8000000', 'DurationMode':'SECONDS', 'Duration':'60'}},
        'LocalHeadContinuous2M': {'Name': 'LocalHead', 'GeneratorConfig':{'LoadUnit':'BITS_PER_SECOND', 'FixedLoad':'2000000', 'DurationMode':'CONTINUOUS'}},
        'LocalHeadContinuous4M': {'Name': 'LocalHead', 'GeneratorConfig':{'LoadUnit':'BITS_PER_SECOND', 'FixedLoad':'4000000', 'DurationMode':'CONTINUOUS'}},
        'LocalHeadRateBasedSeconds': {'Name': 'LocalHead', 'GeneratorConfig':{'SchedulingMode':'RATE_BASED', 'DurationMode':'SECONDS', 'Duration':'60'}},
        'LocalHeadBurst400': {'Name': 'LocalHead', 'GeneratorConfig':{'LoadUnit':'FRAMES_PER_SECOND', 'FixedLoad':'2000', 'DurationMode':'BURSTS', 'Duration':'400'}},
        'LocalHead': {'Name': 'LocalHead'},
        'RemoteHead': {'Name': 'RemoteHead'},
        'Internet': {'Name': 'Internet'},
        'Mirror1': {'Name': 'MIRROR1'},
        'Mirror2': {'Name': 'MIRROR2'}
    },
    'Device':{
        #Device configuration
        'LocalHead': {},
        'LocalDevice1': {'DeviceCount':'100'},
	'LocalDevice1Count1': {'DeviceCount':'1'},
        'LocalDevice2': {'DeviceCount':'100'},
	'LocalDevice2Count9': {'DeviceCount':'9'},
        'RemoteHead': {},
        'RemoteDevice1': {'DeviceCount':'200'},
	'RemoteDevice1Count1': {'DeviceCount':'1'},
    },
    'StreamBlock':{
        #Streamblock configuration
        'TCP01': {'Name': 'TCP01', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        'TCP02': {'Name': 'TCP02', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        'UDP01': {'Name': 'UDP01', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        'UDP02': {'Name': 'UDP02', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        'UDP03': {'Name': 'UDP03', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        'UDP04': {'Name': 'UDP04', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        'UDP05': {'Name': 'UDP05', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        'UDP06': {'Name': 'UDP06', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        'Ipv4Default1500': {'Name': 'Ipv4-Default', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1500'},
        '4-1': {'Name': 'QoS1', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
        '4-2': {'Name': 'QoS2', 'EnableStreamOnlyGeneration':'FALSE', 'FixedFrameLength':'1024'},
    },
    'StreamProfile':{
        #Stream profile configuration
        'PerStream100K': {'Load': '100000', 'LoadUnit': 'BITS_PER_SECOND'},
        'PerStream900K': {'Load': '900000', 'LoadUnit': 'BITS_PER_SECOND'},
        'PerStream1M': {'Load': '1000000', 'LoadUnit': 'BITS_PER_SECOND'},
        'PerStream3M': {'Load': '3000000', 'LoadUnit': 'BITS_PER_SECOND'},
        'PerStream10M': {'Load': '10000000', 'LoadUnit': 'BITS_PER_SECOND'},
    },
    'ResultParameter':{
        #Stream profile configuration
        'Analyzer': {'JumboFrameThreshold': '1023'},
    }
}

class SdWanTest(TestBase):
    """
    Base class for sd-wan test scripts.
    It may not apply to all the sd-wan test scripts, if not, let test script class
    base on TestBase or create another new class like SdWanTest
    """
    def __init__(self, test_input):
        super().__init__(test_input)
        self.local_head = self.stc.port("local_head")
        self.remote_head = self.stc.port("remote_head")
        self.internet = self.stc.port("internet")
        self.monitor = self.stc.port("monitor")
        self.monitor_1 = self.stc.port("monitor_1")
        self.monitor_2 = self.stc.port("monitor_2")
        self.result = 'pass'
        self.error_info = ''

    def subscribe_result(self, *args):
        '''Subscribe STC results'''
        if args:
            project = self.stc.get('system1', 'children-project')
            for arg in args:
                if arg['result_type'] == 'GeneratorPortResults':
                    self.stc.perform('ResultsSubscribeCommand', Parent=project, resultParent=arg['port'], ConfigType='Generator', ResultType=arg['result_type'])
                elif arg['result_type'] == 'AnalyzerPortResults':
                    self.stc.perform('ResultsSubscribeCommand', Parent=project, resultParent=arg['port'], ConfigType='Analyzer', ResultType=arg['result_type'])
                elif arg['result_type'] == 'txstreamresults':
                    self.stc.perform('ResultsSubscribeCommand', Parent=project, resultParent=project, ConfigType='streamblock', ResultType=arg['result_type'])
                elif arg['result_type'] == 'rxstreamsummaryresults':
                    if self.stc.get(project, 'children-RxPortResultFilter'):
                        result_filter = self.stc.get(project, 'children-RxPortResultFilter')
                    else:
                        result_filter = self.stc.create('RxPortResultFilter', under=project)
                        self.stc.perform('ResultsSubscribeCommand', Parent=project, resultParent=project, ConfigType='streamblock', ResultType=arg['result_type'])
                    self.stc.config(result_filter, RxPortList=arg['port'])
                else:
                    raise RuntimeError('Result type of {0} is not supported yet.'.format(arg['result_type']))

    def verify_same_sig_count_port(self, tx_port, rx_port):
        '''Verify the tx and rx sig count same'''
        tx_sig_count = self.stc.get(self.stc.get(self.stc.get(tx_port, 'children-generator'), 'children-generatorportresults'))['GeneratorSigFrameCount']
        rx_sig_count = self.stc.get(self.stc.get(self.stc.get(rx_port, 'children-analyzer'), 'children-analyzerportresults'))['SigFrameCount']
        self.stc.config(tx_port, {'AppendLocationToPortName':'FALSE'})
        self.stc.config(rx_port, {'AppendLocationToPortName':'FALSE'})
        if tx_sig_count == '0':
            self.result = 'fail'
            self.error_info = self.error_info + 'Send 0 packets from port named {0}.\n'.format(self.stc.get(tx_port, 'name'))
        if tx_sig_count != rx_sig_count:
            self.result = 'fail'
            self.error_info = self.error_info + 'Actually send {0} packets from port named {1} and get {2} packets from port named {3}.\n'.format(tx_sig_count, self.stc.get(tx_port, 'name'), rx_sig_count, self.stc.get(rx_port, 'name'))
            
    def verify_0_sig_count_port(self, rx_port):
        '''Verify no packets received for specific port'''
        rx_sig_count = self.stc.get(self.stc.get(self.stc.get(rx_port, 'children-analyzer'), 'children-analyzerportresults'))['SigFrameCount']
        self.stc.config(rx_port, {'AppendLocationToPortName':'FALSE'})
        if rx_sig_count != '0':
            self.result = 'fail'
            self.error_info = self.error_info + 'Rx Sig counter for port named {1} is not 0, actually receive {0} Sig packets.\n'.format(rx_sig_count, self.stc.get(rx_port, 'name'))

    def verify_no_packet_loss(self, stream):
        '''Verify no packets loss for stream'''
        dropped_frame = self.stc.get(self.stc.get(stream, 'children-rxstreamsummaryresults'))['DroppedFrameCount']
        if dropped_frame != '0':
            self.result = 'fail'
            self.error_info = self.error_info + 'Drop count for stream named {0} is {1}.\n'.format(self.stc.get(stream, 'name'), dropped_frame)

    def verify_no_packet_duplication(self, stream):
        '''Verify no packets duplication for stream'''
        duplicate_frame = self.stc.get(self.stc.get(stream, 'children-rxstreamsummaryresults'))['DuplicateFrameCount']
        if duplicate_frame != '0':
            self.result = 'fail'
            self.error_info = self.error_info + 'Duplicate count for stream named {0} is {1}.\n'.format(self.stc.get(stream, 'name'), duplicate_frame)

    def verify_jumbo_count(self, tx_port, rx_port):
        '''Verify the jumbo counter from rx port is greater or equeal to sig counter from tx port'''
        tx_sig_count = self.stc.get(self.stc.get(self.stc.get(tx_port, 'children-generator'), 'children-generatorportresults'))['GeneratorSigFrameCount']
        rx_jumbo_count = self.stc.get(self.stc.get(self.stc.get(rx_port, 'children-analyzer'), 'children-analyzerportresults'))['JumboFrameCount']
        self.stc.config(tx_port, {'AppendLocationToPortName':'FALSE'})
        self.stc.config(rx_port, {'AppendLocationToPortName':'FALSE'})
        if tx_sig_count == '0':
            self.result = 'fail'
            self.error_info = self.error_info + 'Send 0 packets from port named {0}.\n'.format(self.stc.get(tx_port, 'name'))
        if rx_jumbo_count < tx_sig_count:
            self.result = 'fail'
            self.error_info = self.error_info + 'Actually send {0} packets from port named {1} and get {2} packets from port named {3}.\n'.format(tx_sig_count, self.stc.get(tx_port, 'name'), rx_jumbo_count, self.stc.get(rx_port, 'name'))

    def verify_no_jumbo_count(self, tx_port, rx_port):
        '''Verify the jumbo counter from rx port is less than sig counter from tx port'''
        tx_sig_count = self.stc.get(self.stc.get(self.stc.get(tx_port, 'children-generator'), 'children-generatorportresults'))['GeneratorSigFrameCount']
        rx_jumbo_count = self.stc.get(self.stc.get(self.stc.get(rx_port, 'children-analyzer'), 'children-analyzerportresults'))['JumboFrameCount']
        self.stc.config(tx_port, {'AppendLocationToPortName':'FALSE'})
        self.stc.config(rx_port, {'AppendLocationToPortName':'FALSE'})
        if rx_jumbo_count >= tx_sig_count:
            self.result = 'fail'
            self.error_info = self.error_info + 'Actually send {0} packets from port named {1} and get {2} packets from port named {3}.\n'.format(tx_sig_count, self.stc.get(tx_port, 'name'), rx_jumbo_count, self.stc.get(rx_port, 'name'))

    def verify_stable_jumbo_fps(self, port, expected_fps, tolerance, timeout=5):
        logger = self.logger
        self.stc.config(port, {'AppendLocationToPortName':'FALSE'})
        times = int(timeout / 5)
        for i in range(times):
            time.sleep(5)
            fps = self.stc.get(self.stc.get(self.stc.get(port, 'children-analyzer'), 'children-analyzerportresults'))['JumboFrameRate']
            logger.info("Checking traffic rate of loop %d" % i)
            logger.info(traffic_rate=fps)
            if int(fps) > int(expected_fps * (1-tolerance)):
                break
            if i == (times - 1):
                self.result = 'fail'
                self.stc.perform('SaveResults', SaveDetailedResults=True, ResultFileName=self.test_input.testcase_id + '.db')
                self.error_info = self.error_info + 'Jumbo fps is not as expected {0}, actuall jumbo fps is {1} for port named {2}'.format(expected_fps, fps, self.stc.get(port, 'name'))

    def verify_sig_fps(self, port, expected_fps, tolerance, timeout=5):
        logger = self.logger
        self.stc.config(port, {'AppendLocationToPortName':'FALSE'})
        times = int(timeout / 5)
        for i in range(times):
            time.sleep(5)
            fps = self.stc.get(self.stc.get(self.stc.get(port, 'children-analyzer'), 'children-analyzerportresults'))['SigFrameRate']
            logger.info("Checking traffic rate of loop %d" % i)
            logger.info(traffic_rate=fps)
            if int(fps) > int(expected_fps * (1-tolerance)):
                break
            if i == (times - 1):
                self.result = 'fail'
                self.stc.perform('SaveResults', SaveDetailedResults=True, ResultFileName=self.test_input.testcase_id + '.db')
                self.error_info = self.error_info + 'Sig fps is not as expected {0}, actuall Sig fps is {1} for port named {2}'.format(expected_fps, fps, self.stc.get(port, 'name'))

    def verify_stream_max_bandwidth(self, streams, bps, tolerance):
        '''Verify stream total bps'''
        expected_bps = int(bps)
        stream_total_frame = 0
        stream_total_bps = 0
        for stream in streams:
            frame_length = int(self.stc.get(stream, 'FixedFrameLength')) + 18
            stream_frame = self.stc.get(self.stc.get(stream, 'children-rxstreamsummaryresults'))['SigFrameCount']
            stream_total_frame += int(stream_frame)
        stream_total_bps = int((stream_total_frame * frame_length * 8) / 60)
        if (stream_total_bps < expected_bps * (1 - tolerance)) or (stream_total_bps > expected_bps * (1 + tolerance)):
            self.result = 'fail'
            if len(streams) == 1:
                self.error_info = self.error_info + 'Failed to verify bps of stream named {0}, actual bps is {1}, not same as expected bps {2}.\n'.format(self.stc.get(streams[0], 'name'), stream_total_bps, expected_bps)
            else:   
                self.error_info = self.error_info + 'Failed to verify total bps of stream, actual bps is {0}, not same as expected bps {1}.\n'.format(stream_total_bps, expected_bps)

class StcParamSdwan(BaseConfig):
    """
    Parse the parameters of stc_config in testbed
    "address", "gateway", "phy", "speed" and "auto_negotiation"  come from lab yaml file
    """
    def __init__(self, cfg):
        super().__init__(cfg)
        device_number = 10
        #Use exec to create multiple objects.
        for i in range(1, device_number):
            exec("self.device{0} = self.get_value(['emulated_device','emulated_device{1}'])".format(i, i))

class ParseDevice():
    """Parse parameters for devices"""
    def __init__(self, device):
        for key, value in device.items():
            #Parse parameters for devices
            if key == 'ipv4_if':
                if 'address' in value:
                    self.ipv4_address = value['address']
                if 'gateway' in value:
                    self.ipv4_gateway = value['gateway']
            if key == 'ipv6_if':
                if 'address' in value:
                    self.ipv6_address = value['address']
                if 'gateway' in value:
                    self.ipv6_gateway = value['gateway']
            if key == 'vlan_if':
                if 'vlan_id1' in value:
                    self.vlan_id1 = value['vlan_id1']
                if 'vlan_id2' in value:
                    self.vlan_id2 = value['vlan_id2']
            if key == 'name':
                self.name = value

class StcConfigSdwan():
    """
    Config STC.
    """
    def __init__(self, stc):
        self.stc = stc

    def device_create(self, port, device, device_testbed):
        '''create STC device'''
        devicedic = {}
        portdic = {'Port':port}
        devicedic.update(portdic)
        devicedic.update(device)
        device_para = ParseDevice(device_testbed)
        for key, value in device_testbed.items():
            #TO DO: only support Ipv4If/Ipv6If/VlanIf, not support other stacks
            if key == 'ipv4_if':
                if 'Ipv4If' not in devicedic.keys():
                    devicedic['Ipv4If'] = {}
                    if 'address' in value:
                        devicedic['Ipv4If']['Address'] = device_para.ipv4_address
                    if 'gateway' in value:
                        devicedic['Ipv4If']['Gateway'] = device_para.ipv4_gateway
            if key == 'ipv6_if':
                if 'Ipv6If' not in devicedic.keys():
                    devicedic['Ipv6If'] = {}
                    if 'address' in value:
                        devicedic['Ipv6If']['Address'] = device_para.ipv6_address
                    if 'gateway' in value:
                        devicedic['Ipv6If']['Gateway'] = device_para.ipv6_gateway
            if key == 'vlan_if':
                if 'VlanIf' not in devicedic.keys():
                    devicedic['VlanIf'] = [{}, {}]
                    if 'vlan_id1' in value:
                        devicedic['VlanIf'][0]['VlanId'] = device_para.vlan_id1
                    if 'vlan_id2' in value:
                        devicedic['VlanIf'][1]['VlanId'] = device_para.vlan_id2
            if key == 'name':
                if 'Name' not in devicedic.keys():
                    devicedic['Name'] = device_para.name
        if 'IfStack' not in devicedic:
            devicedic['IfStack'] = 'EthIIIf'
            if 'VlanIf' in devicedic:
                devicedic['IfStack'] = "VlanIf " + devicedic['IfStack']
                if devicedic['VlanIf'][1] != {}:
                    devicedic['IfStack'] = "VlanIf " + devicedic['IfStack']
            if 'Ipv4If' in devicedic:
                devicedic['IfStack'] = "Ipv4If " + devicedic['IfStack']
            if 'Ipv6If' in devicedic:
                devicedic['IfStack'] = "Ipv6If " + devicedic['IfStack']

        if 'IfCount' not in devicedic:
            devicedic['IfCount'] = '1'
            if 'VlanIf' in devicedic:
                devicedic['IfCount'] = '1 ' + devicedic['IfCount']
                if devicedic['VlanIf'][1] != {}:
                    devicedic['IfCount'] = '1 ' + devicedic['IfCount']
            if 'Ipv4If' in devicedic:
                devicedic['IfCount'] = '1 ' + devicedic['IfCount']
            if 'Ipv6If' in devicedic:
                devicedic['IfCount'] = '1 ' + devicedic['IfCount']
        return self.stc.device_config(**devicedic)
