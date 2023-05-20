//
// Created by Paras Sharma on 6/7/2020.
//
#include <math.h>
#include <iostream>
#include "Utils.h"

Node Utils::extend(Node start, Node end, float step_size) {
    float distance = eul_dist(start, end);
    float ratio = step_size/distance;
    return std::make_tuple((1 - ratio) * std::get<0>(start) + ratio * std::get<0>(end),
            ((1 - ratio) * std::get<1>(start) + ratio * std::get<1>(end)),
            ((1 - ratio) * std::get<2>(start) + ratio * std::get<2>(end)));
}

Node Utils::rotate(Node root, Node node, float angle, float axis, float step_size){
    // roll, yaw, pitch
    angle *= M_PI / 180;

    
    //TODO: Test code, remove afterwards
    float ox = std::get<0>(root);
    float oy = std::get<1>(root);
    float px = std::get<0>(node);
    float py = std::get<1>(node);
    float qx = ox + cos(angle) * (px - ox) - sin(angle) * (py - oy);
    float qy = oy + sin(angle) * (px - ox) + cos(angle) * (py - oy);
    //return std::make_tuple(qx, qy, 0);

    
    Eigen::Vector3d parent;
    Eigen::Vector3d child;
    Eigen::Vector3d base;
    Eigen::Vector3d world_coordinate_ref;

    world_coordinate_ref << 1, 0, 0;
     
    /*
    base << 1.,0.,0.;
    parent << 0.,0.,0.;
    child << 1.,1.,0.;
    
    
    axis = 90 * M_PI / 180;
    angle = 30 * M_PI / 180;*/

     
    base << step_size, 0, 0;
    parent << std::get<0>(root), std::get<1>(root), std::get<2>(root);
    child << std::get<0>(node), std::get<1>(node), std::get<2>(node);
    
    //AG: setFromTwoVectors(a, b) gives a rotation matrix to represent a rotation
    //sending the line of direction a to the line of direction b
    Eigen::Matrix3d Rot1;
    Rot1 = Eigen::Quaterniond().setFromTwoVectors(child - parent, world_coordinate_ref);

    Eigen::Matrix3d node_rotation_mat;
    /*
    node_rotation_mat = Eigen::AngleAxisd(axis, Eigen::Vector3d::UnitX())
            * Eigen::AngleAxisd(0, Eigen::Vector3d::UnitY())
            * Eigen::AngleAxisd(angle, Eigen::Vector3d::UnitZ());
    
    node_rotation_mat = Eigen::AngleAxisd(angle, Eigen::Vector3d::UnitZ())
            * Eigen::AngleAxisd(axis, Eigen::Vector3d::UnitX());
    
    std::cout<<"Node Rotation Matix :\n"<<node_rotation_mat<<std::endl;*/

    //AG: Rotation is performed in the follwoing order: Roll (Axis), Yaw (Angle) about x and z axis respectively
    Eigen::Quaterniond q_angle(Eigen::AngleAxisd(angle, Eigen::Vector3d::UnitZ())); 
    Eigen::Quaterniond q_axis(Eigen::AngleAxisd(axis , Eigen::Vector3d::UnitX())); 

    Eigen::Quaterniond q_resultant = q_angle * q_axis;
    
    std::cout<<"Roatation Matrix :"<<Rot1<<std::endl;
    //std::cout<<"Node Rotation Matix from Q:\n"<<q_resultant.normalized().toRotationMatrix()<<std::endl;

    Eigen::Vector3d output;
    //output = Rot1.transpose()*node_rotation_mat*base;
    output = Rot1.transpose()*q_resultant.normalized().toRotationMatrix()*base;
    output += parent;
    
    std::cout<<"2D Rotation result :"<<qx<<" "<<qy<<std::endl;
    std::cout<<"Output vector :\n"<<output<<std::endl;

    return std::make_tuple(output(0), output(1), output(2));
}

float Utils::eul_dist(Node node1, Node node2) {
    return sqrt(pow(std::get<0>(node1) - std::get<0>(node2), 2) +  pow(std::get<1>(node1) - std::get<1>(node2), 2));
}

float Utils::shift_toward(float mean, float centre, float shift) {
    if(abs(dist_mean(mean-shift, centre)) <= abs(dist_mean(mean+shift, centre))){
        mean-=shift;
    } else{
        mean+=shift;
    }
    return remainder(mean, 360);
}

float Utils::shift_away(float mean, float centre, float shift) {
    if(abs(dist_mean(mean-shift, centre)) <= abs(dist_mean(mean+shift, centre))){
        mean+=shift;
    } else{
        mean-=shift;
    }
    return remainder(mean, 360);
}

float Utils::dist_mean(float node1_mean, float node2_mean) {
//    std::cout << fmin(fmod(fabs(node1_mean - node2_mean), 360), fmod(360 - fabs(node1_mean - node2_mean), 360)) << "Node mean " << node1_mean<< std::endl;
    return fmin(fmod(fabs(node1_mean - node2_mean), 360), fmod(360 - fabs(node1_mean - node2_mean), 360));
}

float Utils::get_angle(Node a, Node b, Node c) {
    float ang = (180 / M_PI) * (atan2(std::get<1>(c) - std::get<1>(b), std::get<0>(c) - std::get<0>(b)) -
                                atan2(std::get<1>(a) - std::get<1>(b), std::get<0>(a) - std::get<0>(b)));
    if (ang < 0){
        return ang + 360;
    }
    else {
        return ang;
    }
}

bool Utils::feasible(Node parent, float yaw, Node node, float angle, float max_turn) {
    return dist_mean(yaw, angle) <= max_turn;
//    return true;
}

bool Utils::feasible_3D(Node parent, Node end, Node node, float axis, float angle, float max_turn, float step_size) {
    
    //Call extend function and get the next possible node
    Node new_unitl_potential_node = extend(node, end, 1.);
    new_unitl_potential_node = rotate(node, new_unitl_potential_node, angle, axis, 1.);
    
    //Length of Parent_Current_Node vector = step_size
    float a1b1 =  (std::get<0>(node) - std::get<0>(parent))*(std::get<0>(new_unitl_potential_node) - std::get<0>(node));
    float a2b2 =  (std::get<1>(node) - std::get<1>(parent))*(std::get<1>(new_unitl_potential_node) - std::get<1>(node));
    float a3b3 =  (std::get<2>(node) - std::get<2>(parent))*(std::get<2>(new_unitl_potential_node) - std::get<2>(node));

    //Get the angle between the two 3D vectors, new_unitl_potential_node is unit length 
    //Another vector has length step_size
    float cos_angle_between_vectors =  (a1b1+a2b2+a3b3)/(step_size);
    
    if (cos_angle_between_vectors > 1)
       cos_angle_between_vectors = 1;
    else if(cos_angle_between_vectors < -1)
       cos_angle_between_vectors = -1;   
    
    float angle_between_vectors =  acos(cos_angle_between_vectors) * 180/M_PI;

    bool feasibility = angle_between_vectors <= max_turn; 
    
    if(!feasibility)
       std::cout<<"Feasibility Error"<<std::endl;

    return feasibility;
    //return true;
}



