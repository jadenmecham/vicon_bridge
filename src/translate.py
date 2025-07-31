#!/usr/bin/env python
import rospy

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TransformStamped 

class Trans:
	def __init__(self):
		
		self.vicon_sub = rospy.Subscriber("/vicon/Botfly2/Botfly2", TransformStamped, self.viconCallback)
		self.trans_pub = rospy.Publisher("/mavros/vision_pose/pose",PoseStamped,queue_size = 10)

	def viconCallback(self,data):
		msg = PoseStamped()
		msg.header = data.header
		msg.pose.position.x = data.transform.translation.x
		msg.pose.position.y = data.transform.translation.y
		msg.pose.position.z = data.transform.translation.z


		msg.pose.orientation.x = data.transform.rotation.x
		msg.pose.orientation.y = data.transform.rotation.y
		msg.pose.orientation.z = data.transform.rotation.z
		msg.pose.orientation.w = data.transform.rotation.w
		self.trans_pub.publish(msg)

	def main(self):
		try:
			rospy.spin()
		except KeyboardInterrupt:
			print ("Dying")

if __name__ == '__main__':
	rospy.init_node('trans')
	trans = Trans()
	Trans.main(trans)

