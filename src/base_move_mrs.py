import rospy

from tf.transformations import euler_from_quaternion

from nav_msgs.msg import Odometry

from mrs_msgs.srv import ReferenceStampedSrv, ReferenceStampedSrvRequest

class baseMoveMRS:
    def __init__(self):
        self.curr_pos_x, self.curr_pos_y, self.curr_pos_z, self.curr_pos_yaw = [], [], [], []

        rospy.Subscriber("/uav1/odometry/odom_main", Odometry, self.odomCallback)

        rospy.sleep(1)

        rospy.loginfo("Moving 2 meters in the axis X")
        self.move_local(2, 0, 0, 0)
        rospy.sleep(3)

        rospy.loginfo("Moving 2 meters in the axis Y")
        self.move_local(0, 2, 0, 0)
        rospy.sleep(3)

        rospy.loginfo("Mission Finished")


    def odomCallback(self, odom):
        _, _, yaw = euler_from_quaternion(
            [
                odom.pose.pose.orientation.x, 
                odom.pose.pose.orientation.y, 
                odom.pose.pose.orientation.z, 
                odom.pose.pose.orientation.w
            ]
        )        
        
        self.curr_pos_x = odom.pose.pose.position.x
        self.curr_pos_y = odom.pose.pose.position.y 
        self.curr_pos_z = odom.pose.pose.position.z 
        self.curr_pos_yaw = yaw


    def move_local(self, to_go_x, to_go_y, to_go_z, to_go_yaw):
        rospy.wait_for_service("/uav1/control_manager/reference")
        try:
            request_service = rospy.ServiceProxy("/uav1/control_manager/reference", ReferenceStampedSrv)
            req = ReferenceStampedSrvRequest()
            req.reference.position.x = self.curr_pos_x + to_go_x
            req.reference.position.y = self.curr_pos_y + to_go_y 
            req.reference.position.z = self.curr_pos_z + to_go_z
            req.reference.heading = self.curr_pos_yaw + to_go_yaw 
            resp = request_service(req)
        except rospy.ServiceException as e:
            print("Failing calling service: %s"%e)
        

def main():
    rospy.init_node("base_move_mrs")
    baseMoveMRS()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()
    