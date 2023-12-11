import maya.cmds as mc
from functools import partial

''' This script will create our Skeleton and Control Rig for the left side of the body. '''

# Global variables storing name lists for use in ctrl rig creation. 
names = ['Head', 'Neck', 'l_Clavicle', 'l_Shoulder', 'l_Elbow', 'l_Wrist'] 
     
jnt_Names = ['Neck_Jnt', 'Head_Jnt', 'l_Clavicle_Jnt', 'l_Shoulder_Jnt', 'l_Shoulder_Helper_Jnt', 'l_Bicep_Twist_Jnt', 'l_Elbow_Jnt', 'l_Wrist_Jnt']

class ig_Rig(object):
    # Creating our constructor.
    def __init__(self):
        # Global variables storing name lists for use in ctrl rig creation. 
        
        # Create the skeleton.
        skeleton = self.create_Skel()
        
        # Create the controllers.
        ctrls = self.create_Ctrls()
        
        constraints = self.parent_Constraints()
        
        # Lock and hide the joints.
        cleanup = self.lock_and_Hide()
        
        grp = self.main_Grp()
        
        skin = self.bind_Skin()
    
    # Function that creates our joints.   
    def create_Skel(self):
        self.jnt_Grp = mc.group(name = 'Jnt_Grp', empty = True)  
        
        neck = mc.joint(name = jnt_Names[0], position = (0, 153.464, 1.149))
        
        head = mc.joint(name = jnt_Names[1], position = (0, 182.841, 3.958))
        
        clavicle = mc.joint(name = jnt_Names[2], position = (-8.560, 146.376, 2.317))
        
        mc.parent(clavicle, neck)
        
        shoulder = mc.joint(name = jnt_Names[3], position = (-19.670, 145.324, -2.584))
        
        shoulder_Helper = mc.joint(name = jnt_Names[4], position = (-19.670, 150.727, -2.584))
        
        bicep_Twist = mc.joint(name = jnt_Names[5], position = (-30.818, 133.213, -3.468))
        
        mc.parent(bicep_Twist, shoulder)
        
        elbow = mc.joint(name = jnt_Names[6], position = (-40.112, 122.949, -4.009))
        
        mc.parent(elbow, shoulder)
        
        wrist = mc.joint(name = jnt_Names[7], position = (-54.890, 105.006, 10.736))
        
    # Function that creates our animator friendly controllers.
    def create_Ctrls(self):
        self.ctrl_Grp = mc.group(name = 'Ctrl_Grp', empty = True)
        
        for i in names:
            ctrls = mc.circle(name = str(i) + '_ctrl')
            
        mc.parent(mc.ls(type = 'nurbsCurve'), self.ctrl_Grp)
        
        mc.parent('Neck_ctrl', 'Head_ctrl')
        mc.parent('l_Clavicle_ctrl', 'Neck_ctrl')
        mc.parent('l_Shoulder_ctrl', 'l_Clavicle_ctrl')
        mc.parent('l_Elbow_ctrl', 'l_Shoulder_ctrl')
        mc.parent('l_Wrist_ctrl', 'l_Elbow_ctrl')
    
    # Function that parent constrains the joints to the controllers.    
    def parent_Constraints(self):
        pass
    
    def main_Grp(self):
        rig_All_Grp = mc.group(name = 'rig_All_Grp', empty = True) 
        mc.parent(self.ctrl_Grp, self.jnt_Grp, rig_All_Grp)
                                 
    # Function that locks and hides our joints from the animators.   
    def lock_and_Hide(self):        
        for i in jnt_Names:
            # Hiding all of the joints.
            #mc.hide(i)
            
            # Locking visibilty.
            mc.setAttr(i + '.visibility', lock = True, keyable = False, channelBox = False)
            
            # Locking radius.
            mc.setAttr(i + '.radius', lock = True, keyable = False, channelBox = False)
            
            # Locking the translate values.
            mc.setAttr(i + '.translateX', lock = True, keyable = False, channelBox = False)
            mc.setAttr(i + '.translateY', lock = True, keyable = False, channelBox = False)
            mc.setAttr(i + '.translateZ', lock = True, keyable = False, channelBox = False)
            
            # Locking the rotate values.
            mc.setAttr(i + '.rotateX', lock = True, keyable = False, channelBox = False)
            mc.setAttr(i + '.rotateY', lock = True, keyable = False, channelBox = False)
            mc.setAttr(i + '.rotateZ', lock = True, keyable = False, channelBox = False)
            
            # Locking the scale values.
            mc.setAttr(i + '.scaleX', lock = True, keyable = False, channelBox = False)
            mc.setAttr(i + '.scaleY', lock = True, keyable = False, channelBox = False)
            mc.setAttr(i + '.scaleZ', lock = True, keyable = False, channelBox = False)
            
    def bind_Skin(self):
        geo_Grp = mc.group(name = 'Geo_Grp', empty = True)
        mc.bindSkin('male_base_geo', jnt_Names)
        
        mc.parent('male_base_geo', geo_Grp)
        mc.parent(geo_Grp, 'rig_All_Grp')
        
# The create_rig function that calls the class and makes the entire control rig.        
def create_Rig():            
    ig_Rig()
    
create_Rig()