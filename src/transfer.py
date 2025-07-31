#!/usr/bin/env python
import rospy
from pyquaternion import Quaternion
import math
from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TransformStamped 

class Trans:
	def __init__(self):
		self.vicon_sub = rospy.Subscriber("/vicon/bigbug/bigbug", TransformStamped, self.viconCallback)
		self.enu_pub = rospy.Publisher("/mavros/vision_pose/pose",PoseStamped,queue_size = 50)
		#self.trans_pub = rospy.Publisher("/botfly4/nwu/pose_stamped",PoseStamped,queue_size = 50)
		#self.trans_pub_1=rospy.Publisher("/mavros/mocap/tf", TransformStamped,queue_size=50)

	def viconCallback(self,data):
		msg = PoseStamped()
		msg.header = data.header
		# negative signs are meant to convert the drone from seu to nwu
		msg.pose.position.x = -1 * data.transform.translation.y
		msg.pose.position.y = data.transform.translation.x
		msg.pose.position.z = data.transform.translation.z
		# msg.pose.orientation.x = data.transform.rotation.x
		# msg.pose.orientation.y = data.transform.rotation.y
		# msg.pose.orientation.z = data.transform.rotation.z
		# msg.pose.orientation.w = data.transform.rotation.w
		Q_NWU=Quaternion(data.transform.rotation.w, data.transform.rotation.x, data.transform.rotation.y, data.transform.rotation.z)
		R=Quaternion(axis=[0, 0, 1], angle=1*math.pi / 2)
		Q_ENU=R*Q_NWU
		msg.pose.orientation.x = Q_ENU[1]
		msg.pose.orientation.y =  Q_ENU[2]
		msg.pose.orientation.z =  Q_ENU[3]
		msg.pose.orientation.w =  Q_ENU[0]

		self.enu_pub.publish(msg)

		# Compute yaw angles
		yaw_nwu = math.degrees(math.atan2(2.0 * (Q_NWU.w * Q_NWU.z + Q_NWU.x * Q_NWU.y), 1.0 - 2.0 * (Q_NWU.y * Q_NWU.y + Q_NWU.z * Q_NWU.z)))
		yaw_enu = math.degrees(math.atan2(2.0 * (Q_ENU.w * Q_ENU.z + Q_ENU.x * Q_ENU.y), 1.0 - 2.0 * (Q_ENU.y * Q_ENU.y + Q_ENU.z * Q_ENU.z)))

		print(f"NWU: {Q_NWU} | Yaw degrees from North: {yaw_nwu:.2f}")
		print(f"ENU: {Q_ENU} | Yaw degrees from East: {yaw_enu:.2f}")
		# print("NWU",Q_NWU)
		# print("ENU",Q_ENU)
		#msge = PoseStamped() #message_enu
		#msge.header = data.header
		# negative signs are meant to convert the drone from seu to nwu
		#msge.pose.position.x = -1 * data.transform.translation.y
		#msge.pose.position.y = data.transform.translation.x
		#msge.pose.position.z = data.transform.translation.z
		#msge.pose.orientation.x = data.transform.rotation.x
		#msge.pose.orientation.y = data.transform.rotation.y
		#msge.pose.orientation.z = data.transform.rotation.z
		#msge.pose.orientation.w = data.transform.rotation.w
		#self.enu_pub.publish(msge)
		#msg1=TransformStamped()
		#msg1.header=data.header
		#msg1.child_frame_id=data.child_frame_id
		#msg1.transform=data.transform
		#self.trans_pub_1.publish(msg1)


	def main(self):
		try:
			rospy.spin()
		except KeyboardInterrupt:
			print ("Dying")

if __name__ == '__main__':
	rospy.init_node('trans')
	trans = Trans()
	Trans.main(trans)
