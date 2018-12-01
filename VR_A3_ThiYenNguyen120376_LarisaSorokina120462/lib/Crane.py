#!/usr/bin/python

# import guacamole libraries
import avango
import avango.gua


### import application libraries
from lib.KeyboardInput import KeyboardInput
from lib.Hinge import Hinge
from lib.Arm import Arm
from lib.Hook import Hook
from lib.Scene import Scene


class Crane:
  
    ## constructor
    def __init__(self,
        PARENT_NODE = None,
        TARGET_LIST = [], # required for bounding box intersection in Hook class 
        ):
        

        ## init base node for whole crane
        self.base_node = avango.gua.nodes.TransformNode(Name = "base_node")
        self.base_node.Transform.value = avango.gua.make_rot_mat(-90.0, 0, 1, 0)
        self.base_node.Transform.value = avango.gua.make_trans_mat(0.0,-0.1,0.0)
        PARENT_NODE.Children.value.append(self.base_node)



        ## init internal sub-classes
        self.input = KeyboardInput()
                     
        ## first hinge
        self.hinge0 = Hinge(
            PARENT_NODE = self.base_node,
            DIAMETER = 0.1,
            HEIGHT = 0.01,
            ROT_OFFSET_MAT = avango.gua.make_identity_mat(),
            SF_ROT_INPUT = self.input.sf_rot_input0,
            MIN = -180,
            MAX = 180,
            )
        
        ## first arm segment
        self.arm0 = Arm(
            PARENT_NODE = self.hinge0.hinge_node,
            LENGTH = 0.13,
            DIAMETER = 0.01,
            ROT_OFFSET_MAT = avango.gua.make_identity_mat(),
            )

        ## second hinge
        self.hinge1 = Hinge(
            PARENT_NODE = self.arm0.arm_end_node,
            DIAMETER = 0.04,
            HEIGHT = 0.01,
            ROT_OFFSET_MAT = avango.gua.make_rot_mat(270.0,1,0,0),
            SF_ROT_INPUT = self.input.sf_rot_input1,
            MIN = 0,
            MAX = 90,
            )

        ## 2nd arm segment
        self.arm1 = Arm(
            PARENT_NODE= self.hinge1.hinge_node,
            LENGTH=0.08,
            DIAMETER=0.008,
            ROT_OFFSET_MAT=avango.gua.make_rot_mat(90.0, 1, 0, 0),
        )

        ## 3rd hinge
        self.hinge2 = Hinge(
            PARENT_NODE= self.arm1.arm_end_node,
            DIAMETER=0.035,
            HEIGHT=0.01,
            ROT_OFFSET_MAT=avango.gua.make_rot_mat(90.0, 1, 0, 0),
            SF_ROT_INPUT=self.input.sf_rot_input2,
            MIN = -90,
            MAX = 90,
        )

        ## 3rd arm segment
        self.arm2 = Arm(
            PARENT_NODE= self.hinge2.hinge_node,
            DIAMETER=0.008,
            LENGTH=0.07,
            ROT_OFFSET_MAT=avango.gua.make_rot_mat(-90.0, 1, 0, 0),
        )

        # ## the Hook segment
        self.hook = Hook()
        self.hook.my_constructor(self.arm2.arm_end_node, 0.02, TARGET_LIST)