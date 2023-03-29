import xml.etree.ElementTree as ET
import numpy as np

def str2arr(string):
    return np.array(string.split(" ")).astype(float)

def get_link_joint_dict(urdf_file):
    tree = ET.parse(urdf_file)
    root = tree.getroot()
    
    # Extract the robot name from the URDF file
    robot_name = root.attrib["name"]
    print("Robot name:", robot_name)

    # Extract the joint information from the URDF file
    link_dict = {}
    for link in root.iter("link"):
        link_name = link.attrib["name"]
        link_dict[link_name] = {}

    joint_dict = {}
    for joint in root.iter("joint"):
        joint_name = joint.attrib["name"]
        joint_origin_xyz = str2arr(joint.find("origin").attrib["xyz"])
        joint_origin_rpy = str2arr(joint.find("origin").attrib["rpy"])
        joint_type = joint.attrib["type"]
        joint_parent = joint.find("parent").attrib["link"]
        joint_child = joint.find("child").attrib["link"]
        joint_dict[joint_name] = {
            "joint_type": joint_type,
            "parent": joint_parent,
            "child": joint_child,
            "origin_xyz": joint_origin_xyz,
            "origin_rpy": joint_origin_rpy
        }
        link_dict[joint_parent]["joint"] = joint_name
        link_dict[joint_child]["parent_joint"] = joint_name
        if joint_type != "fixed":
            joint_axis = [np.array(i.split(" ")).astype(float) for i in joint.find("axis").attrib.values()]
            joint_dict[joint_name]["axis"] = joint_axis
    return link_dict, joint_dict


