from __future__ import print_function
# This lets us use the python3-style print() function even in python2. It should have no effect if you're already running python3.

import os
import dwl
import numpy as np

# Configure the printing
np.set_printoptions(suppress=True)

# Construct an instance of the FloatingBaseSystem class, which wraps the C++ class.
fbs = dwl.FloatingBaseSystem()
ws = dwl.WholeBodyState()

# Initializing the URDF model and whole-body state
fpath = str(os.path.dirname(os.path.abspath(__file__)))
fbs.resetFromURDFFile(fpath + '/../../models/hyq.urdf', fpath + '/../../models/hyq.yarf')
ws.setJointDoF(fbs.getJointDoF())


# The robot state
ws.setBaseSE3(dwl.SE3_RPY(np.zeros(3),
                          np.array([0., 0., 0.])))
ws.setBaseVelocity_W(dwl.Motion(np.array([0., 0., 0.]),
                                np.array([0., 0., 0.])))
ws.setBaseAcceleration_W(dwl.Motion(np.array([0., 0., 0.]),
                                    np.array([0., 0., 0.])))
ws.setJointPosition(0.75, fbs.getJointId('lf_hfe_joint'))
ws.setJointPosition(-1.5, fbs.getJointId('lf_kfe_joint'))
ws.setJointPosition(-0.75, fbs.getJointId('lh_hfe_joint'))
ws.setJointPosition(1.5, fbs.getJointId('lh_kfe_joint'))
ws.setJointPosition(0.75, fbs.getJointId('rf_hfe_joint'))
ws.setJointPosition(-1.5, fbs.getJointId('rf_kfe_joint'))
ws.setJointPosition(-0.75, fbs.getJointId('rh_hfe_joint'))
ws.setJointPosition(1.5, fbs.getJointId('rh_kfe_joint'))


# Getting the total mass of the system. Note that you could also get the mass of a specific
# body (e.g. sys.getBodyMass(body_name))
print()
print('total mass:', fbs.getTotalMass())
print('lf_upperleg mass:', fbs.getBodyMass('lf_upperleg'))
print('gravity acceleration is', fbs.getGravityAcceleration())




# Getting the CoM of the floating-base body. Note that you could also get the CoM of a
# specific body (e.g. sys.getBodyCoM(body_name))
print()
print('floating-base CoM:', fbs.getFloatingBaseCoM().transpose())
print('lf_upperleg CoM:', fbs.getBodyCoM('lf_upperleg').transpose())




# Getting the number of system DoF, floating-base Dof, joints and end-effectors
print()
print('NQ:', fbs.getConfigurationDim())
print('NV:', fbs.getTangentDim())
print('number of joints:', fbs.getJointDoF())
print('number of end-effectors:', fbs.getNumberOfEndEffectors())
print('floating-base body name:', fbs.getFloatingBaseName())




# Getting the joint names and ids
print()
joints = fbs.getJoints()
for name in joints:
	print('joint[', joints[name], '] =', name)
print()
print('joint names are', fbs.getJointList())
print('joint name of 3 is', fbs.getJointName(3))




# Getting the body names and ids
print()
bodies = fbs.getBodies()
for name in bodies:
    print('body[', bodies[name], '] =', name)
print()
print('body names are', fbs.getBodyList())
print('body name of 3 is', fbs.getBodyName(3))




# Getting the frame names and ids
print()
frames = fbs.getFrames()
for name in frames:
    print('frame[', frames[name], '] =', name)
print()
print('frame names are', fbs.getFrameList())
print('frame name of 3 is', fbs.getFrameName(3))




# Getting the end-effector names and ids
print()
contacts = fbs.getEndEffectors()
print('number of feet are', fbs.getNumberOfEndEffectors(dwl.FOOT))
for name in contacts:
	print('end-effector[', contacts[name], '] =', name)




# Getting the joint limits
print()
print('lower limits =', fbs.getLowerLimits().transpose())
print('upper limits =', fbs.getUpperLimits().transpose())
print('velocity limits =', fbs.getVelocityLimits().transpose())
print('effort limits =', fbs.getEffortLimits().transpose())




# Getting the default posture
print()
joint_pos0 = fbs.getDefaultPosture()
print('nominal joint positions =', joint_pos0.transpose())




# Getting the body iner
print()
print('floating-base inertia')
print(' ', fbs.getFloatingBaseInertia())
print('lf_hipassembly inertia')
print(' ', fbs.getBodyInertia("lf_hipassembly"))




# Conversion between whole-body state to generalized state, and viceverse
print()
base_state = np.zeros(6)
joint_state = joint_pos0
generalized_state = fbs.toConfigurationState(ws.getBaseSE3(), ws.getJointPosition())
print('Converting the whole-body pose to a configuration vector')
print('base position =', ws.getBaseSE3())
print('joint position =', ws.getJointPosition().transpose())
print('configuration vector =', generalized_state.transpose())




# Setting up the branch states
print()
joint_pos = ws.getJointPosition()
lf_branch_pos = np.array([0.5, 0.75, 1.5]);
fbs.setBranchState(joint_pos, lf_branch_pos, 'lf_foot')
ws.setJointPosition(joint_pos)
print('Setting up the lf_foot branch position =', lf_branch_pos.transpose())
print('joint position =', ws.getJointPosition().transpose())
print('Getting the lf_foot branch position =', fbs.getBranchState(ws.getJointPosition(), 'lf_foot').transpose())