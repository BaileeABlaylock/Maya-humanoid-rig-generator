import maya.cmds as mc
from functools import partial

''' This script will create our controllers, cleanup our hierarchy, and connect the joints to the controllers. '''

# Global variables storing name lists for use in ctrl rig creation.

names = ['root', 'spine', 'chest', 'neck', 'head', 'l_Clavicle', 'l_Shoulder', 'l_Elbow']
jnt_Names = ['root_Jnt', 'spine_Jnt', 'chest_Jnt', 'neck_Jnt', 'head_Jnt', 'head_End_Jnt', 'l_Clavicle_Jnt', 'l_Shoulder_Jnt', 'l_Shoulder_Helper_Jnt', 'l_Bicep_Twist_Jnt', 'l_Elbow_Jnt', 'l_Wrist_Twist_Jnt', 'l_Wrist_Jnt', 'flood_Jnt']

class ig_Rig(object):
    # Creating our constructor.
    def __init__(self):        
        # Create the controllers.
        ctrls = self.create_Ctrls()

        # Create the parent and scale constraints.
        constraints = self.ps_Constraints()

        # Modify the control shapes to fit appropriately.
        shapes = self.modify_Ctrl_Shapes()

        # Lock and hide the joints.
        cleanup = self.lock_and_Hide()

        # Create the top group.
        grp = self.main_Grp()
        
    # Function that creates our joints. 
    def create_Skel(self):

        # Creating a group for all the joints to be parented under.
        self.jnt_Grp = mc.group(name = 'Jnt_Grp', empty = True)

        # Creating a joint for each joint name.
        root = mc.joint(name = jnt_Names[0], position = (0, 100.339, 1.018))       
        spine = mc.joint(name = jnt_Names[1], position = (0, 119.490, -1.796)) 
        chest = mc.joint(name = jnt_Names[2], position = (0, 139.735, -1.182))        
        neck = mc.joint(name = jnt_Names[3], position = (0, 153.464, 1.149))     
        head = mc.joint(name = jnt_Names[4], position = (0, 164.179, 4.362))       
        head_End = mc.joint(name = jnt_Names[5], position = (0, 183.385, 4.362))       
        clavicle = mc.joint(name = jnt_Names[6], position = (-8.560, 146.376, 2.317))

        mc.parent(clavicle, chest, absolute = True)

        shoulder = mc.joint(name = jnt_Names[7], position = (-19.670, 145.324, -2.584))
        shoulder_Helper = mc.joint(name = jnt_Names[8], position = (-19.670, 150.727, -2.584))  
        bicep_Twist = mc.joint(name = jnt_Names[9], position = (-30.818, 133.213, -3.468))

        mc.parent(bicep_Twist, shoulder)

        elbow = mc.joint(name = jnt_Names[10], position = (-40.112, 122.949, -4.009))       
        wrist_Twist = mc.joint(name = jnt_Names[11], position = (-50.024, 111.087, 5.323), absolute = False)       
        wrist = mc.joint(name = jnt_Names[12], position = (-55.539, 104.156, 10.924))       
        flood = mc.joint(name = jnt_Names[13], position = (38, 124, -4))

        mc.parent(flood, world = True)

        mc.parent(flood, 'Jnt_Grp')

        mc.select('root_Jnt')

        # Modifying the chains joint orientation.
        mc.joint(edit = True, orientJoint = 'xyz', secondaryAxisOrient = 'yup', children = True, zeroScaleOrient = True)
        
    # Function that creates our animator friendly controllers.
    def create_Ctrls(self):
        # Creating our main controllers group
        self.ctrl_Grp = mc.group(name='Ctrl_Grp', empty=True)

        # For loop that creates all the controllers we need and their offset groups.
        for i in names:
            ctrls = mc.circle(name=str(i) + '_ctrl', radius=5)

            self.ctrl_Offset_Grp = mc.group(name=str(i) + '_ctrl_Offset_Grp', empty=True)

        # Parenting the controllers under their offset group.

        mc.parent('root_ctrl', 'root_ctrl_Offset_Grp')

        mc.parent('spine_ctrl', 'spine_ctrl_Offset_Grp')

        mc.parent('chest_ctrl', 'chest_ctrl_Offset_Grp')

        mc.parent('neck_ctrl', 'neck_ctrl_Offset_Grp')

        mc.parent('head_ctrl', 'head_ctrl_Offset_Grp')

        mc.parent('l_Clavicle_ctrl', 'l_Clavicle_ctrl_Offset_Grp')

        mc.parent('l_Shoulder_ctrl', 'l_Shoulder_ctrl_Offset_Grp')

        mc.parent('l_Elbow_ctrl', 'l_Elbow_ctrl_Offset_Grp')

        # Parenting the curves into their hierarchy.

        mc.parent('root_ctrl_Offset_Grp', self.ctrl_Grp)

        mc.parent('spine_ctrl_Offset_Grp', 'root_ctrl')

        mc.parent('chest_ctrl_Offset_Grp', 'spine_ctrl')

        mc.parent('neck_ctrl_Offset_Grp', 'chest_ctrl')

        mc.parent('head_ctrl_Offset_Grp', 'neck_ctrl')

        mc.parent('l_Clavicle_ctrl_Offset_Grp', 'chest_ctrl')

        mc.parent('l_Shoulder_ctrl_Offset_Grp', 'l_Clavicle_ctrl')

        mc.parent('l_Elbow_ctrl_Offset_Grp', 'l_Shoulder_ctrl')

    # Function that parent/scale constrains the joints to the controllers.

    def ps_Constraints(self):
        # Constraining root ctrl offset grp

        mc.matchTransform('root_ctrl_Offset_Grp', 'root_Jnt', position=True, pivots=True, rotation=True)

        mc.parentConstraint('root_ctrl', 'root_Jnt', name='root_Jnt_PC', maintainOffset=True, weight=True)

        mc.scaleConstraint('root_ctrl', 'root_Jnt', name='root_Jnt_SC', offset=(1, 1, 1), weight=True)

        # Constraining spine ctrl offset grp

        mc.matchTransform('spine_ctrl_Offset_Grp', 'spine_Jnt', position=True, pivots=True, rotation=True)

        mc.parentConstraint('spine_ctrl', 'spine_Jnt', name='spine_Jnt_PC', maintainOffset=True, weight=True)

        mc.scaleConstraint('spine_ctrl', 'spine_Jnt', name='spine_Jnt_SC', offset=(1, 1, 1), weight=True)

        mc.matchTransform('chest_ctrl_Offset_Grp', 'chest_Jnt', position=True, pivots=True, rotation=True)

        mc.parentConstraint('chest_ctrl', 'chest_Jnt', name='chest_Jnt_PC', maintainOffset=True, weight=True)

        mc.scaleConstraint('chest_ctrl', 'chest_Jnt', name='chest_Jnt_SC', offset=(1, 1, 1), weight=True)

        mc.matchTransform('neck_ctrl_Offset_Grp', 'neck_Jnt', position=True, pivots=True, rotation=True)

        mc.parentConstraint('neck_ctrl', 'neck_Jnt', name='neck_Jnt_PC', maintainOffset=True, weight=True)

        mc.scaleConstraint('neck_ctrl', 'neck_Jnt', name='neck_Jnt_SC', offset=(1, 1, 1), weight=True)

        mc.matchTransform('head_ctrl_Offset_Grp', 'head_Jnt', position=True, pivots=True, rotation=True)

        mc.parentConstraint('head_ctrl', 'head_Jnt', name='head_Jnt_PC', maintainOffset=True, weight=True)

        mc.scaleConstraint('head_ctrl', 'head_Jnt', name='head_Jnt_SC', offset=(1, 1, 1), weight=True)

        mc.matchTransform('l_Clavicle_ctrl_Offset_Grp', 'l_Clavicle_Jnt', position=True, pivots=True, rotation=True)

        mc.parentConstraint('l_Clavicle_ctrl', 'l_Clavicle_Jnt', name='l_Clavicle_Jnt_PC', maintainOffset=True,
                            weight=True)

        mc.scaleConstraint('l_Clavicle_ctrl', 'l_Clavicle_Jnt', name='l_Clavicle_Jnt_SC', offset=(1, 1, 1), weight=True)

        mc.matchTransform('l_Shoulder_ctrl_Offset_Grp', 'l_Shoulder_Jnt', position=True, pivots=True, rotation=True)

        mc.parentConstraint('l_Shoulder_ctrl', 'l_Shoulder_Jnt', name='l_Shoulder_Jnt_PC', maintainOffset=True,
                            weight=True)

        mc.scaleConstraint('l_Shoulder_ctrl', 'l_Shoulder_Jnt', name='l_Shoulder_Jnt_SC', offset=(1, 1, 1), weight=True)

        mc.matchTransform('l_Elbow_ctrl_Offset_Grp', 'l_Elbow_Jnt', position=True, pivots=True, rotation=True)
    
        mc.parentConstraint('l_Elbow_ctrl', 'l_Elbow_Jnt', name='l_Elbow_Jnt_PC', maintainOffset=True, weight=True)
    
        mc.scaleConstraint('l_Elbow_ctrl', 'l_Elbow_Jnt', name='l_Elbow_Jnt_SC', offset=(1, 1, 1), weight=True)

    # Function that modifies the CV's of the controllers to give us a better shape.


    def modify_Ctrl_Shapes(self):
        mc.select('root_ctrlShape.cv[0:7]')
    
        mc.scale(6, 6, 6, relative=True, pivot=('0cm', '100.339cm', '1.018cm'))
    
        mc.rotate('90deg', '90deg', '90deg', relative=True, pivot=('0cm', '100.339cm', '1.018cm'), objectSpace=True,
                  forceOrderXYZ=True)
    
        mc.setAttr('root_ctrlShape' + ".overrideEnabled", 1)
    
        mc.setAttr('root_ctrlShape' + ".overrideColor", 17)
    
        mc.select('spine_ctrlShape.cv[0:7]')
    
        mc.scale(5, 5, 5, relative=True, pivot=('0cm', '119.49cm', '-1.796cm'))
    
        mc.rotate('90deg', '90deg', '90deg', relative=True, pivot=('0cm', '119.49cm', '-1.796cm'), objectSpace=True,
                  forceOrderXYZ=True)
    
        mc.setAttr('spine_ctrlShape' + ".overrideEnabled", 1)
    
        mc.setAttr('spine_ctrlShape' + ".overrideColor", 17)
    
        mc.select('chest_ctrlShape.cv[0:7]')
    
        mc.scale(4, 4, 4, relative=True, pivot=('0cm', '139.735cm', '-1.182cm'))
    
        mc.rotate('90deg', '90deg', '90deg', relative=True, pivot=('0cm', '139.735cm', '-1.182cm'), objectSpace=True,
                  forceOrderXYZ=True)
    
        mc.setAttr('chest_ctrlShape' + ".overrideEnabled", 1)
    
        mc.setAttr('chest_ctrlShape' + ".overrideColor", 17)
    
        mc.select('neck_ctrlShape.cv[0:7]')
    
        mc.scale(3, 3, 3, relative=True, pivot=('0cm', '153.464cm', '1.149cm'))
    
        mc.rotate('90deg', '90deg', '90deg', relative=True, pivot=('0cm', '153.464cm', '1.149cm'), objectSpace=True,
                  forceOrderXYZ=True)
    
        mc.setAttr('neck_ctrlShape' + ".overrideEnabled", 1)
    
        mc.setAttr('neck_ctrlShape' + ".overrideColor", 17)
    
        mc.select('head_ctrlShape.cv[0:7]')
    
        mc.scale(3, 3, 3, relative=True, pivot=('0cm', '164.179cm', '4.362cm'))
    
        mc.rotate('90deg', '90deg', '90deg', relative=True, pivot=('0cm', '164.179cm', '4.362cm'), objectSpace=True,
                  forceOrderXYZ=True)
    
        mc.setAttr('head_ctrlShape' + ".overrideEnabled", 1)
    
        mc.setAttr('head_ctrlShape' + ".overrideColor", 17)
    
        mc.select('l_Clavicle_ctrlShape.cv[0:7]')
    
        mc.rotate(0, -4, 0, relative=True, pivot=('-8.56cm', '146.376cm', '-18.174742cm'), objectSpace=True,
                  forceOrderXYZ=True)
    
        mc.setAttr('l_Clavicle_ctrlShape' + ".overrideEnabled", 1)
    
        mc.setAttr('l_Clavicle_ctrlShape' + ".overrideColor", 13)
    
        mc.move(12, 0, 40, relative=True, os=True, wd=True)
    
        mc.rotate(-1.687708, 20.3989, -0.51094, relative=True, pivot=('-4.777863', '145.225653cm', '-39.15536cm'), ws=True,
                  forceOrderXYZ=True)
    
        mc.select('l_Shoulder_ctrlShape.cv[0:7]')
    
        mc.rotate('0deg', '90deg', '90deg', relative=True, pivot=('-19.67cm', '145.324cm', '-2.584cm'), objectSpace=True,
                  forceOrderXYZ=True)
    
        mc.scale(2, 2, 2, relative=True, pivot=('-19.67cm', '145.324cm', '-2.584cm'))
    
        mc.setAttr('l_Shoulder_ctrlShape' + ".overrideEnabled", 1)
    
        mc.setAttr('l_Shoulder_ctrlShape' + ".overrideColor", 13)
    
        mc.select('l_Elbow_ctrlShape.cv[0:7]')
    
        mc.rotate('0deg', '90deg', '0deg', relative=True, pivot=('-40.112cm', '122.949cm', '-4.009cm'), objectSpace=True,
                  forceOrderXYZ=True)
    
        mc.scale(1.5, 1.5, 1.5, relative=True, pivot=('-40.112cm', '122.949cm', '-4.009cm'))
    
        mc.setAttr('l_Elbow_ctrlShape' + ".overrideEnabled", 1)
    
        mc.setAttr('l_Elbow_ctrlShape' + ".overrideColor", 13)
    
    
    def main_Grp(self):
        rig_All_Grp = mc.group(name='rig_All_Grp', empty=True)
    
        self.geo_Grp = mc.group(name='geo_Grp', empty=True)
    
        mc.parent('male_base_torso', self.geo_Grp)
    
        mc.parent(self.ctrl_Grp, 'Jnt_Grp', self.geo_Grp, rig_All_Grp)
    
        # Function that locks and hides our joints from the animators.


    def lock_and_Hide(self):
        # Hiding all of the joints.
    
        mc.hide('Jnt_Grp')
    
        for i in jnt_Names:
            # Locking visibilty.
    
            mc.setAttr(i + '.visibility', lock=True, keyable=False, channelBox=False)
    
            # Locking radius.
    
            mc.setAttr(i + '.radius', lock=True, keyable=False, channelBox=False)
    
            # Locking the translate values.
    
            mc.setAttr(i + '.translateX', lock=True, keyable=False, channelBox=False)
    
            mc.setAttr(i + '.translateY', lock=True, keyable=False, channelBox=False)
    
            mc.setAttr(i + '.translateZ', lock=True, keyable=False, channelBox=False)
    
            # Locking the rotate values.
    
            mc.setAttr(i + '.rotateX', lock=True, keyable=False, channelBox=False)
    
            mc.setAttr(i + '.rotateY', lock=True, keyable=False, channelBox=False)
    
            mc.setAttr(i + '.rotateZ', lock=True, keyable=False, channelBox=False)
    
            # Locking the scale values.
    
            mc.setAttr(i + '.scaleX', lock=True, keyable=False, channelBox=False)
    
            mc.setAttr(i + '.scaleY', lock=True, keyable=False, channelBox=False)
    
            mc.setAttr(i + '.scaleZ', lock=True, keyable=False, channelBox=False)


# Function to create the rig with only the skeleton.
def create_rig_Preskin():
    ig_Rig.create_Skel(ig_Rig)
    
# The create_rig function that calls the functions that come after joints and bindskin.    
def create_Rig():
    return ig_Rig()

create_rig_Preskin()
create_Rig()
