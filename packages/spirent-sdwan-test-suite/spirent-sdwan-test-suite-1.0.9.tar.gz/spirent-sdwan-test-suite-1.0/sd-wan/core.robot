*** Settings ***
Resource        ${EXECDIR}/test_framework/script/resources.robot

Test Setup      TestInit    TESTCASE_FILE=${CURDIR}${/}${TESTCASE_FILES}[${TEST NAME}]
Test Teardown   TestFinish

*** Variables ***
&{TESTCASE_FILES}   sd-wan.path_selection.001=path_selection_l2_to_l4_steering.yaml
...                 sd-wan.path_selection.002=path_selection_application_aware_steering.yaml
...                 sd-wan.resiliency_link.001=resiliency_link_blackout_local_no_congestion.yaml
...                 sd-wan.resiliency_link.002=resiliency_link_blackout_remote_no_congestion.yaml
...                 sd-wan.resiliency_link.003=resiliency_link_brownout_packet_loss.yaml
...                 sd-wan.resiliency_link.004=resiliency_link_brownout_packet_delay.yaml
...                 sd-wan.resiliency_link.005=resiliency_link_brownout_jitter.yaml
...                 sd-wan.resiliency_link.006=resiliency_link_brownout_packet_out_of_order.yaml
...                 sd-wan.resiliency_link.007=resiliency_link_brownout_packet_duplication.yaml

*** Test Cases ***
sd-wan.path_selection.001
    [Tags]      priority=0
    TestRun

sd-wan.path_selection.002
    [Tags]      priority=0
    TestRun

sd-wan.resiliency_link.001
    [Tags]          priority=1
    TestRun

sd-wan.resiliency_link.002
    [Tags]          priority=1
    TestRun

sd-wan.resiliency_link.003
    [Tags]          priority=1
    TestRun

sd-wan.resiliency_link.004
    [Tags]          priority=1
    TestRun

sd-wan.resiliency_link.005
    [Tags]          priority=2
    TestRun

sd-wan.resiliency_link.006
    [Tags]          priority=2
    TestRun

sd-wan.resiliency_link.007
    [Tags]          priority=2
    TestRun
