#!/usr/bin/env python

import rospy
import smach
import smach_ros
from std_msgs.msg import String
from std_srvs.srv import Trigger, TriggerRequest

# define state VoiceCommand
class VoiceCommand(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['what_happened','others','find_material','delivery_product','all_task_clear'])
        self.intent = 0

    def callback(self, data):
        print "callback",data.data
        if data.data == "Others": self.intent = 0
        elif data.data == "IntentFind": self.intent = 1
        elif data.data == "IntentDelivery": self.intent = 2
        elif data.data == "IntentWhat": self.intent = 3
        elif data.data == "Clear": self.intent = 4

    def execute(self, userdata):
        rospy.loginfo('Executing state VoiceCommand')
        rospy.Subscriber('/Intent', String, self.callback)

        if self.intent == 0:
            return 'others'
        elif self.intent == 1:
            self.intent = 0
            rospy.sleep(2.)
            return 'find_material'
        elif self.intent == 2:
            self.intent = 0
            rospy.sleep(2.)
            return 'delivery_product'
        elif self.intent == 3:
            self.intent = 0
            rospy.sleep(2.)
            return 'what_happened'
        elif self.intent == 4:
            self.intent = 0
            rospy.sleep(2.)
            return 'all_task_clear'
        else:
            rospy.sleep(2.)
            return 'others'


# define state ImageCaption
class ImageCaption(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['telling_done','retry','aborted'])
        rospy.wait_for_service('/triggerCaption')
        self.triggerCaption_service = rospy.ServiceProxy('/triggerCaption', Trigger)
        self.error_counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state ImageCaption')
        result = self.triggerCaption_service(TriggerRequest())
        rospy.loginfo(result.message)

        if result.success:
            rospy.sleep(2.)
            return 'telling_done'
        elif error_counter<3:
            error_counter+=1
            rospy.sleep(2.)
            return 'retry'
        else:
            rospy.sleep(2.)
            return 'aborted'


# define state GraspingObject
class GraspingObject(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['grasping_done','retry','aborted'])
        rospy.wait_for_service('/triggerGrasping')
        self.triggerGrasping_service = rospy.ServiceProxy('/triggerGrasping', Trigger)
        self.error_counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state GraspingObject')
        result = self.triggerGrasping_service(TriggerRequest())
        rospy.loginfo(result.message)

        if result.success:
            rospy.sleep(2.)
            return 'grasping_done'
        elif error_counter<3:
            error_counter+=1
            rospy.sleep(2.)
            return 'retry'
        else:
            rospy.sleep(2.)
            return 'aborted'


class PlacingBasket(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['placing_done','retry','aborted'])
        rospy.wait_for_service('/triggerPlacing')
        self.triggerPlacing_service = rospy.ServiceProxy('/triggerPlacing', Trigger)
        self.error_counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state PlacingBasket')
        result = self.triggerPlacing_service(TriggerRequest())
        rospy.loginfo(result.message)

        if result.success:
            rospy.sleep(2.)
            return 'placing_done'
        elif error_counter<3:
            error_counter+=1
            rospy.sleep(2.)
            return 'retry'
        else:
            rospy.sleep(2.)
            return 'aborted'


# define state FetchingBox
class FetchingBox(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['fetching_done','retry','aborted'])
        rospy.wait_for_service('/triggerFetching')
        self.triggerFetching_service = rospy.ServiceProxy('/triggerFetching', Trigger)
        self.error_counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state FetchingBox')
        result = self.triggerFetching_service(TriggerRequest())
        rospy.loginfo(result.message)

        if result.success:
            rospy.sleep(2.)
            return 'fetching_done'
        elif error_counter<3:
            error_counter+=1
            rospy.sleep(2.)
            return 'retry'
        else:
            rospy.sleep(2.)
            return 'aborted'


# define state StackingBox
class StackingBox(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['stacking_done','retry','aborted'])
        rospy.wait_for_service('/triggerStacking')
        self.triggerStacking_service = rospy.ServiceProxy('/triggerStacking', Trigger)
        self.error_counter = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state StackingBox')
        result = self.triggerStacking_service(TriggerRequest())
        rospy.loginfo(result.message)

        if result.success:
            rospy.sleep(2.)
            return 'stacking_done'
        elif error_counter<3:
            error_counter+=1
            rospy.sleep(2.)
            return 'retry'
        else:
            rospy.sleep(2.)
            return 'aborted'


# define state NaviFind
class NaviFind(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['start','reachGoal','restart','home','done'])
        self.state = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state NaviFind')
        if self.state == 0:
            self.state += 1
            rospy.sleep(2.)
            return 'start'
        elif self.state == 1:
            self.state += 1
            rospy.sleep(2.)
            return 'reachGoal'
        elif self.state == 2:
            self.state += 1
            rospy.sleep(2.)
            return 'restart'
        elif self.state == 3:
            self.state += 1
            rospy.sleep(2.)
            return 'home'
        elif self.state == 4:
            self.state = 0
            rospy.sleep(2.)
            return 'done'

# define state NaviDelivery
class NaviDelivery(smach.State):
    def __init__(self):
        smach.State.__init__(self, outcomes=['start','reachGoal','restart','home','done'])
        self.state = 0

    def execute(self, userdata):
        rospy.loginfo('Executing state NaviDelivery')
        if self.state == 0:
            self.state += 1
            rospy.sleep(2.)
            return 'start'
        elif self.state == 1:
            rospy.sleep(2.)
            self.state += 1
            return 'reachGoal'
        elif self.state == 2:
            self.state += 1
            rospy.sleep(2.)
            return 'restart'
        elif self.state == 3:
            self.state += 1
            rospy.sleep(2.)
            return 'home'
        elif self.state == 4:
            self.state = 0
            rospy.sleep(2.)
            return 'done'


def main():
    rospy.init_node('smach_example_state_machine')


    # ************************************************
    # *********** SM_ROOT ****************************
    # ************************************************
    sm_top = smach.StateMachine(outcomes=['demo_done'])
    sis_root = smach_ros.IntrospectionServer('server_pmc', sm_top, '/SM_ROOT')
    sis_root.start()
    with sm_top:

        smach.StateMachine.add('VoiceCommand', VoiceCommand(),
                               transitions={'others':'VoiceCommand',
                                            'find_material':'NAVI_F',
                                            'delivery_product':'NAVI_D',
                                            'what_happened':'ImageCaption',
                                            'all_task_clear':'demo_done'})

        smach.StateMachine.add('ImageCaption', ImageCaption(),
                                transitions={'telling_done':'VoiceCommand',
                                             'retry':'ImageCaption',
                                             'aborted':'VoiceCommand',
                                            })


        # ************************************************
        # *********** SM_ROOT/NAVI_F *********************
        # ************************************************
        sm_naviF = smach.StateMachine(outcomes=['finding_done'])
        sis_naviF = smach_ros.IntrospectionServer('server_pmc', sm_naviF, '/SM_ROOT/NAVI_F')
        sis_naviF.start()
        with sm_naviF:
            smach.StateMachine.add('NaviFind', NaviFind(),
                                   transitions={'start':'NaviFind',
                                                'reachGoal':'GraspingObject',
                                                'restart':'NaviFind',
                                                'home':'PlacingBasket',
                                                'done':'finding_done'})
            smach.StateMachine.add('GraspingObject', GraspingObject(),
                                    transitions={'grasping_done':'NaviFind',
                                                 'retry':'GraspingObject',
                                                 'aborted':'NaviFind',
                                                })
            smach.StateMachine.add('PlacingBasket', PlacingBasket(),
                                    transitions={'placing_done':'NaviFind',
                                                 'retry':'PlacingBasket',
                                                 'aborted':'NaviFind',
                                                })
        smach.StateMachine.add('NAVI_F', sm_naviF, transitions={'finding_done':'VoiceCommand'})

        # ************************************************
        # *********** SM_ROOT/NAVI_D *********************
        # ************************************************
        sm_naviD = smach.StateMachine(outcomes=['delivering_done'])
        sis_naviD = smach_ros.IntrospectionServer('server_pmc', sm_naviD, '/SM_ROOT/NAVI_D')
        sis_naviD.start()
        with sm_naviD:
            smach.StateMachine.add('NaviDelivery', NaviDelivery(),
                                   transitions={'start':'FetchingBox',
                                                'reachGoal':'StackingBox',
                                                'restart':'NaviDelivery',
                                                'home':'NaviDelivery',
                                                'done':'delivering_done'})
            smach.StateMachine.add('FetchingBox', FetchingBox(),
                                    transitions={'fetching_done':'NaviDelivery',
                                                 'retry':'FetchingBox',
                                                 'aborted':'NaviDelivery',
                                                })
            smach.StateMachine.add('StackingBox', StackingBox(),
                                    transitions={'stacking_done':'NaviDelivery',
                                                 'retry':'StackingBox',
                                                 'aborted':'NaviDelivery',
                                                })
        smach.StateMachine.add('NAVI_D', sm_naviD, transitions={'delivering_done':'VoiceCommand'})

    # Execute SMACH plan
    outcome = sm_top.execute()
    sis_root.stop()
    sis_NaviD.stop()
    sis_NaviF.stop()

if __name__ == '__main__':
    main()
